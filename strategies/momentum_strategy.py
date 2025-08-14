import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime
import ta
from strategies.base_strategy import BaseStrategy


class MomentumStrategy(BaseStrategy):
    """
    Стратегия импульса для торговли на сильных движениях

    Основана на принципах:
    - Торговля в направлении сильного импульса
    - Использование MACD, RSI и объемных индикаторов
    - Быстрые входы при подтверждении импульса
    - Трейлинг-стопы для максимизации прибыли
    """

    def __init__(self, market_analyzer, position_manager):
        super().__init__(name="MomentumStrategy")
        self.market_analyzer = market_analyzer
        self.position_manager = position_manager

        # Параметры импульсной стратегии
        self.MIN_CONFIDENCE = 0.7
        self.SIGNAL_COOLDOWN = 600  # 10 минут между сигналами

        # Параметры импульса
        self.MIN_MOMENTUM_STRENGTH = 0.02  # 2% минимальное движение
        self.MOMENTUM_PERIOD = 10  # Период для расчета импульса
        self.VOLUME_MULTIPLIER = 2.5  # Объем должен быть в 2.5 раза больше

        # Параметры индикаторов
        self.RSI_PERIOD = 14
        self.RSI_MOMENTUM_THRESHOLD = 60  # RSI выше 60 для бычьего импульса
        self.MACD_FAST = 12
        self.MACD_SLOW = 26
        self.MACD_SIGNAL = 9

        # Управление рисками
        self.STOP_LOSS_PCT = 0.03  # 3% стоп-лосс
        self.PROFIT_TARGET_PCT = 0.09  # 9% цель прибыли
        self.TRAILING_STOP_PCT = 0.02  # 2% трейлинг-стоп

        self.logger.info("MomentumStrategy initialized for momentum trading")

    def generate_signal(self, data: pd.DataFrame, symbol: str = None) -> Optional[Dict[str, Any]]:
        """Генерация импульсного сигнала"""
        try:
            if len(data) < 50:
                return None

            # Проверка cooldown
            if self._is_signal_cooldown_active():
                return None

            # Расчет индикаторов импульса
            indicators = self._calculate_momentum_indicators(data)
            if not indicators:
                return None

            # Проверка импульса
            momentum_signal = self._check_momentum_conditions(indicators)

            if momentum_signal and momentum_signal['confidence'] >= self.MIN_CONFIDENCE:
                self.last_signal_time = datetime.now()
                return momentum_signal

            return None

        except Exception as e:
            self.logger.error(f"Error generating momentum signal: {e}")
            return None

    def _calculate_momentum_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Расчет индикаторов импульса"""
        try:
            df_calc = df.copy()

            # Импульс цены
            df_calc['momentum'] = df_calc['close'].pct_change(self.MOMENTUM_PERIOD) * 100
            df_calc['momentum_sma'] = df_calc['momentum'].rolling(5).mean()

            # RSI
            df_calc['rsi'] = ta.momentum.RSIIndicator(df_calc['close'], window=self.RSI_PERIOD).rsi()

            # MACD
            macd = ta.trend.MACD(df_calc['close'],
                                 window_fast=self.MACD_FAST,
                                 window_slow=self.MACD_SLOW,
                                 window_sign=self.MACD_SIGNAL)
            df_calc['macd'] = macd.macd()
            df_calc['macd_signal'] = macd.macd_signal()
            df_calc['macd_histogram'] = macd.macd_diff()

            # Объем
            df_calc['volume_sma'] = df_calc['volume'].rolling(20).mean()
            df_calc['volume_ratio'] = df_calc['volume'] / df_calc['volume_sma']

            # Rate of Change (ROC)
            df_calc['roc'] = ta.momentum.ROCIndicator(df_calc['close'], window=10).roc()

            # Williams %R
            df_calc['williams_r'] = ta.momentum.WilliamsRIndicator(
                df_calc['high'], df_calc['low'], df_calc['close'], lbp=14
            ).williams_r()

            last_idx = -1
            return {
                'close': df_calc['close'].iloc[last_idx],
                'momentum': df_calc['momentum'].iloc[last_idx],
                'momentum_sma': df_calc['momentum_sma'].iloc[last_idx],
                'rsi': df_calc['rsi'].iloc[last_idx],
                'macd': df_calc['macd'].iloc[last_idx],
                'macd_signal': df_calc['macd_signal'].iloc[last_idx],
                'macd_histogram': df_calc['macd_histogram'].iloc[last_idx],
                'volume_ratio': df_calc['volume_ratio'].iloc[last_idx],
                'roc': df_calc['roc'].iloc[last_idx],
                'williams_r': df_calc['williams_r'].iloc[last_idx]
            }

        except Exception as e:
            self.logger.error(f"Error calculating momentum indicators: {e}")
            return {}

    def _check_momentum_conditions(self, indicators: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Проверка условий импульса"""
        try:
            momentum = indicators.get('momentum', 0)
            momentum_sma = indicators.get('momentum_sma', 0)
            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            macd_histogram = indicators.get('macd_histogram', 0)
            volume_ratio = indicators.get('volume_ratio', 0)
            roc = indicators.get('roc', 0)
            williams_r = indicators.get('williams_r', -50)
            current_price = indicators.get('close', 0)

            # Проверка объемного подтверждения
            if volume_ratio < self.VOLUME_MULTIPLIER:
                return None

            confidence = 0.0
            reasons = []

            # Бычий импульс
            if (momentum > self.MIN_MOMENTUM_STRENGTH and
                    momentum_sma > 0 and
                    rsi > self.RSI_MOMENTUM_THRESHOLD and
                    macd > macd_signal and
                    macd_histogram > 0):

                confidence += 0.4
                reasons.append("BULLISH_MOMENTUM")

                # Дополнительные подтверждения
                if roc > 2:  # Сильный ROC
                    confidence += 0.2
                    reasons.append("STRONG_ROC")

                if williams_r > -20:  # Williams %R показывает силу
                    confidence += 0.1
                    reasons.append("WILLIAMS_BULLISH")

                if volume_ratio > 3:  # Очень высокий объем
                    confidence += 0.2
                    reasons.append("VOLUME_EXPLOSION")

                if confidence >= self.MIN_CONFIDENCE:
                    return {
                        'action': 'BUY',
                        'entry_price': current_price,
                        'confidence': min(confidence, 1.0),
                        'reasons': ', '.join(reasons),
                        'momentum_strength': momentum,
                        'volume_confirmation': volume_ratio,
                        'timestamp': datetime.now()
                    }

            # Медвежий импульс
            elif (momentum < -self.MIN_MOMENTUM_STRENGTH and
                  momentum_sma < 0 and
                  rsi < (100 - self.RSI_MOMENTUM_THRESHOLD) and
                  macd < macd_signal and
                  macd_histogram < 0):

                confidence += 0.4
                reasons.append("BEARISH_MOMENTUM")

                # Дополнительные подтверждения
                if roc < -2:  # Сильный отрицательный ROC
                    confidence += 0.2
                    reasons.append("STRONG_NEGATIVE_ROC")

                if williams_r < -80:  # Williams %R показывает слабость
                    confidence += 0.1
                    reasons.append("WILLIAMS_BEARISH")

                if volume_ratio > 3:  # Очень высокий объем
                    confidence += 0.2
                    reasons.append("VOLUME_EXPLOSION")

                if confidence >= self.MIN_CONFIDENCE:
                    return {
                        'action': 'SELL',
                        'entry_price': current_price,
                        'confidence': min(confidence, 1.0),
                        'reasons': ', '.join(reasons),
                        'momentum_strength': momentum,
                        'volume_confirmation': volume_ratio,
                        'timestamp': datetime.now()
                    }

            return None

        except Exception as e:
            self.logger.error(f"Error checking momentum conditions: {e}")
            return None

    def execute(self, symbol: str, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Выполнение импульсной стратегии"""
        try:
            df = market_data.get('df')
            if df is None or len(df) < 50:
                return None

            current_position = self.position_manager.get_position_status(symbol)

            if current_position:
                return self._check_momentum_exit(symbol, df, current_position)
            else:
                return self._check_momentum_entry(symbol, df, market_data)

        except Exception as e:
            self.logger.error(f"Error executing momentum strategy: {e}")
            return None

    def _check_momentum_entry(self, symbol: str, df: pd.DataFrame, market_data: Dict[str, Any]) -> Optional[
        Dict[str, Any]]:
        """Проверка условий входа для импульсной торговли"""
        try:
            signal = self.generate_signal(df, symbol)
            if not signal:
                return None

            entry_price = signal['entry_price']
            account_balance = market_data.get('account_balance', 0)

            # Расчет уровней
            if signal['action'] == 'BUY':
                stop_loss = entry_price * (1 - self.STOP_LOSS_PCT)
                take_profit = entry_price * (1 + self.PROFIT_TARGET_PCT)
            else:
                stop_loss = entry_price * (1 + self.STOP_LOSS_PCT)
                take_profit = entry_price * (1 - self.PROFIT_TARGET_PCT)

            # Размер позиции
            position_size = self._calculate_momentum_position_size(account_balance, entry_price, stop_loss)

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
                'momentum_strength': signal.get('momentum_strength'),
                'timestamp': datetime.now()
            }

        except Exception as e:
            self.logger.error(f"Error checking momentum entry: {e}")
            return None

    def _check_momentum_exit(self, symbol: str, df: pd.DataFrame, position: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Проверка условий выхода для импульсной торговли"""
        try:
            current_price = df['close'].iloc[-1]

            # Проверка ослабления импульса
            momentum = df['close'].pct_change(self.MOMENTUM_PERIOD).iloc[-1] * 100

            direction = position.get('direction', '')

            # Проверка ослабления импульса
            if direction == 'BUY' and momentum < 0:  # Импульс ослаб
                return {
                    'action': 'CLOSE',
                    'reason': 'momentum_weakening',
                    'exit_price': current_price
                }
            elif direction == 'SELL' and momentum > 0:  # Импульс ослаб
                return {
                    'action': 'CLOSE',
                    'reason': 'momentum_weakening',
                    'exit_price': current_price
                }

            return None

        except Exception as e:
            self.logger.error(f"Error checking momentum exit: {e}")
            return None

    def _calculate_momentum_position_size(self, balance: float, entry: float, stop: float) -> float:
        """Расчет размера позиции для импульсной торговли"""
        try:
            risk_amount = balance * 0.025  # 2.5% риск для импульсной торговли
            risk_per_unit = abs(entry - stop)

            if risk_per_unit <= 0:
                return 0.0

            return round(risk_amount / risk_per_unit, 8)

        except Exception as e:
            self.logger.error(f"Error calculating momentum position size: {e}")
            return 0.0

    def _is_signal_cooldown_active(self) -> bool:
        """Проверка cooldown для импульсной стратегии"""
        if not self.last_signal_time:
            return False

        time_since_last = (datetime.now() - self.last_signal_time).total_seconds()
        return time_since_last < self.SIGNAL_COOLDOWN