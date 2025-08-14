import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime
import ta
from strategies.base_strategy import BaseStrategy


class BreakoutStrategy(BaseStrategy):
    """
    Стратегия пробоя уровней поддержки и сопротивления

    Основана на принципах:
    - Пробой ключевых уровней с объемным подтверждением
    - Торговля на волатильности
    - Быстрые движения после пробоя
    - Строгие стоп-лоссы
    """

    def __init__(self, market_analyzer, position_manager):
        super().__init__(name="BreakoutStrategy")
        self.market_analyzer = market_analyzer
        self.position_manager = position_manager

        # Параметры пробойной стратегии
        self.MIN_CONFIDENCE = 0.7
        self.SIGNAL_COOLDOWN = 1800  # 30 минут между сигналами
        self.LOOKBACK_PERIOD = 50  # Период для поиска уровней

        # Параметры пробоя
        self.MIN_BREAKOUT_STRENGTH = 0.005  # 0.5% минимальный пробой
        self.MAX_BREAKOUT_STRENGTH = 0.03  # 3% максимальный пробой
        self.VOLUME_CONFIRMATION_RATIO = 2.0  # Объем должен быть в 2 раза больше среднего

        # Управление рисками
        self.STOP_LOSS_PCT = 0.02  # 2% стоп-лосс
        self.PROFIT_TARGET_PCT = 0.06  # 6% цель прибыли
        self.BREAKOUT_TIMEOUT = 3600  # 1 час на развитие пробоя

        self.logger.info("BreakoutStrategy initialized for breakout trading")

    def generate_signal(self, data: pd.DataFrame, symbol: str = None) -> Optional[Dict[str, Any]]:
        """Генерация сигнала пробоя"""
        try:
            if len(data) < self.LOOKBACK_PERIOD + 20:
                return None

            # Проверка cooldown
            if self._is_signal_cooldown_active():
                return None

            # Поиск уровней поддержки и сопротивления
            levels = self._find_support_resistance_levels(data)
            if not levels:
                return None

            # Проверка пробоя
            breakout_signal = self._check_breakout(data, levels)

            if breakout_signal and breakout_signal['confidence'] >= self.MIN_CONFIDENCE:
                self.last_signal_time = datetime.now()
                return breakout_signal

            return None

        except Exception as e:
            self.logger.error(f"Error generating breakout signal: {e}")
            return None

    def _find_support_resistance_levels(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Поиск уровней поддержки и сопротивления"""
        try:
            # Анализируем последние данные
            recent_data = df.tail(self.LOOKBACK_PERIOD)

            # Находим локальные максимумы и минимумы
            highs = recent_data['high']
            lows = recent_data['low']

            # Сопротивление - максимум за период
            resistance = highs.max()
            resistance_touches = len(highs[highs >= resistance * 0.998])  # Касания в пределах 0.2%

            # Поддержка - минимум за период
            support = lows.min()
            support_touches = len(lows[lows <= support * 1.002])  # Касания в пределах 0.2%

            # Текущая цена
            current_price = df['close'].iloc[-1]

            return {
                'resistance': resistance,
                'support': support,
                'resistance_strength': min(resistance_touches / 5, 1.0),
                'support_strength': min(support_touches / 5, 1.0),
                'current_price': current_price,
                'distance_to_resistance': (resistance - current_price) / current_price,
                'distance_to_support': (current_price - support) / current_price
            }

        except Exception as e:
            self.logger.error(f"Error finding support/resistance levels: {e}")
            return {}

    def _check_breakout(self, df: pd.DataFrame, levels: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Проверка пробоя уровней"""
        try:
            current_price = levels['current_price']
            resistance = levels['resistance']
            support = levels['support']

            # Проверка объема
            volume_ratio = self._get_volume_confirmation(df)
            if volume_ratio < self.VOLUME_CONFIRMATION_RATIO:
                return None

            # Проверка пробоя сопротивления (бычий сигнал)
            resistance_breakout = current_price > resistance
            breakout_strength_up = (current_price - resistance) / resistance

            if (resistance_breakout and
                    self.MIN_BREAKOUT_STRENGTH < breakout_strength_up < self.MAX_BREAKOUT_STRENGTH and
                    levels['resistance_strength'] > 0.3):
                confidence = 0.5 + (levels['resistance_strength'] * 0.3) + min(volume_ratio / 3, 0.2)

                return {
                    'action': 'BUY',
                    'entry_price': current_price,
                    'confidence': min(confidence, 1.0),
                    'breakout_type': 'resistance_breakout',
                    'breakout_strength': breakout_strength_up,
                    'volume_confirmation': volume_ratio,
                    'level_strength': levels['resistance_strength'],
                    'timestamp': datetime.now()
                }

            # Проверка пробоя поддержки (медвежий сигнал)
            support_breakout = current_price < support
            breakout_strength_down = (support - current_price) / support

            if (support_breakout and
                    self.MIN_BREAKOUT_STRENGTH < breakout_strength_down < self.MAX_BREAKOUT_STRENGTH and
                    levels['support_strength'] > 0.3):
                confidence = 0.5 + (levels['support_strength'] * 0.3) + min(volume_ratio / 3, 0.2)

                return {
                    'action': 'SELL',
                    'entry_price': current_price,
                    'confidence': min(confidence, 1.0),
                    'breakout_type': 'support_breakout',
                    'breakout_strength': breakout_strength_down,
                    'volume_confirmation': volume_ratio,
                    'level_strength': levels['support_strength'],
                    'timestamp': datetime.now()
                }

            return None

        except Exception as e:
            self.logger.error(f"Error checking breakout: {e}")
            return None

    def _get_volume_confirmation(self, df: pd.DataFrame) -> float:
        """Получение подтверждения объемом"""
        try:
            current_volume = df['volume'].iloc[-1]
            avg_volume = df['volume'].rolling(20).mean().iloc[-1]

            if avg_volume > 0:
                return current_volume / avg_volume
            return 0.0

        except Exception as e:
            self.logger.error(f"Error getting volume confirmation: {e}")
            return 0.0

    def execute(self, symbol: str, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Выполнение пробойной стратегии"""
        try:
            df = market_data.get('df')
            if df is None or len(df) < self.LOOKBACK_PERIOD + 20:
                return None

            current_position = self.position_manager.get_position_status(symbol)

            if current_position:
                return self._check_breakout_exit(symbol, df, current_position)
            else:
                return self._check_breakout_entry(symbol, df, market_data)

        except Exception as e:
            self.logger.error(f"Error executing breakout strategy: {e}")
            return None

    def _check_breakout_entry(self, symbol: str, df: pd.DataFrame, market_data: Dict[str, Any]) -> Optional[
        Dict[str, Any]]:
        """Проверка условий входа для пробоя"""
        try:
            signal = self.generate_signal(df, symbol)
            if not signal:
                return None

            entry_price = signal['entry_price']
            account_balance = market_data.get('account_balance', 0)

            # Расчет уровней на основе типа пробоя
            if signal['action'] == 'BUY':
                stop_loss = entry_price * (1 - self.STOP_LOSS_PCT)
                take_profit = entry_price * (1 + self.PROFIT_TARGET_PCT)
            else:
                stop_loss = entry_price * (1 + self.STOP_LOSS_PCT)
                take_profit = entry_price * (1 - self.PROFIT_TARGET_PCT)

            # Размер позиции
            position_size = self._calculate_breakout_position_size(account_balance, entry_price, stop_loss)

            if position_size <= 0:
                return None

            return {
                'action': 'OPEN',
                'direction': signal['action'],
                'size': position_size,
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'confidence': signal['confidence'],
                'breakout_type': signal.get('breakout_type'),
                'timestamp': datetime.now()
            }

        except Exception as e:
            self.logger.error(f"Error checking breakout entry: {e}")
            return None

    def _check_breakout_exit(self, symbol: str, df: pd.DataFrame, position: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Проверка условий выхода для пробоя"""
        try:
            current_price = df['close'].iloc[-1]
            entry_time = position.get('entry_time')

            # Проверка таймаута пробоя
            if entry_time:
                if isinstance(entry_time, str):
                    entry_time = datetime.fromisoformat(entry_time)

                time_in_position = (datetime.now() - entry_time).total_seconds()
                if time_in_position > self.BREAKOUT_TIMEOUT:
                    return {
                        'action': 'CLOSE',
                        'reason': 'breakout_timeout',
                        'exit_price': current_price
                    }

            # Проверка ложного пробоя (возврат к уровню)
            entry_price = position.get('entry_price', 0)
            direction = position.get('direction', '')

            if entry_price > 0:
                if direction == 'BUY':
                    # Проверка возврата ниже уровня пробоя
                    if current_price < entry_price * 0.995:  # 0.5% ниже входа
                        return {
                            'action': 'CLOSE',
                            'reason': 'false_breakout',
                            'exit_price': current_price
                        }
                elif direction == 'SELL':
                    # Проверка возврата выше уровня пробоя
                    if current_price > entry_price * 1.005:  # 0.5% выше входа
                        return {
                            'action': 'CLOSE',
                            'reason': 'false_breakout',
                            'exit_price': current_price
                        }

            return None

        except Exception as e:
            self.logger.error(f"Error checking breakout exit: {e}")
            return None

    def _calculate_breakout_position_size(self, balance: float, entry: float, stop: float) -> float:
        """Расчет размера позиции для пробоя"""
        try:
            risk_amount = balance * 0.02  # 2% риск для пробоев
            risk_per_unit = abs(entry - stop)

            if risk_per_unit <= 0:
                return 0.0

            return round(risk_amount / risk_per_unit, 8)

        except Exception as e:
            self.logger.error(f"Error calculating breakout position size: {e}")
            return 0.0

    def _is_signal_cooldown_active(self) -> bool:
        """Проверка cooldown для пробойной стратегии"""
        if not self.last_signal_time:
            return False

        time_since_last = (datetime.now() - self.last_signal_time).total_seconds()
        return time_since_last < self.SIGNAL_COOLDOWN