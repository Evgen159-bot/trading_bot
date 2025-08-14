import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime
import ta
from strategies.base_strategy import BaseStrategy


class ScalpingStrategy(BaseStrategy):
    """
    Скальпинговая стратегия для быстрой торговли

    Основана на принципах:
    - Быстрые входы и выходы (1-15 минут)
    - Высокая частота сделок
    - Малые цели прибыли (0.5-2%)
    - Строгий риск-менеджмент
    - Объемный анализ
    """

    def __init__(self, market_analyzer, position_manager):
        super().__init__(name="ScalpingStrategy")
        self.market_analyzer = market_analyzer
        self.position_manager = position_manager

        # Параметры скальпинга
        self.MIN_CONFIDENCE = 0.6  # Более низкий порог для частых сделок
        self.SIGNAL_COOLDOWN = 60  # 1 минута между сигналами
        self.MAX_POSITION_TIME = 900  # 15 минут максимум

        # Цели прибыли и убытков
        self.PROFIT_TARGET_PCT = 0.008  # 0.8% цель прибыли
        self.STOP_LOSS_PCT = 0.004  # 0.4% стоп-лосс (R:R = 2:1)
        self.EMERGENCY_STOP_PCT = 0.006  # 0.6% экстренный стоп

        # Параметры индикаторов (быстрые)
        self.EMA_FAST = 5
        self.EMA_SLOW = 13
        self.RSI_PERIOD = 7
        self.STOCH_PERIOD = 5

        # Объемные фильтры
        self.MIN_VOLUME_RATIO = 1.3
        self.VOLUME_SURGE_THRESHOLD = 2.0

        self.logger.info("ScalpingStrategy initialized for high-frequency trading")

    def generate_signal(self, data: pd.DataFrame, symbol: str = None) -> Optional[Dict[str, Any]]:
        """Генерация скальпингового сигнала"""
        try:
            if len(data) < 50:
                return None

            # Проверка cooldown
            if self._is_signal_cooldown_active():
                return None

            # Расчет быстрых индикаторов
            indicators = self._calculate_scalping_indicators(data)
            if not indicators:
                return None

            # Проверка рыночных условий для скальпинга
            if not self._check_scalping_conditions(indicators):
                return None

            # Генерация сигналов
            signal = self._generate_scalping_signal(indicators)

            if signal and signal['confidence'] >= self.MIN_CONFIDENCE:
                self.last_signal_time = datetime.now()
                return signal

            return None

        except Exception as e:
            self.logger.error(f"Error generating scalping signal: {e}")
            return None

    def _calculate_scalping_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Расчет быстрых индикаторов для скальпинга"""
        try:
            df_calc = df.copy()

            # Быстрые EMA
            df_calc['ema_fast'] = ta.trend.EMAIndicator(df_calc['close'], window=self.EMA_FAST).ema_indicator()
            df_calc['ema_slow'] = ta.trend.EMAIndicator(df_calc['close'], window=self.EMA_SLOW).ema_indicator()

            # Быстрый RSI
            df_calc['rsi'] = ta.momentum.RSIIndicator(df_calc['close'], window=self.RSI_PERIOD).rsi()

            # Быстрый Stochastic
            stoch = ta.momentum.StochasticOscillator(
                df_calc['high'], df_calc['low'], df_calc['close'], window=self.STOCH_PERIOD
            )
            df_calc['stoch_k'] = stoch.stoch()

            # Объем
            df_calc['volume_sma'] = df_calc['volume'].rolling(10).mean()
            df_calc['volume_ratio'] = df_calc['volume'] / df_calc['volume_sma']

            # Волатильность
            df_calc['price_change'] = df_calc['close'].pct_change()
            df_calc['volatility'] = df_calc['price_change'].rolling(10).std()

            last_idx = -1
            return {
                'close': df_calc['close'].iloc[last_idx],
                'close_prev': df_calc['close'].iloc[last_idx - 1] if len(df_calc) > 1 else df_calc['close'].iloc[
                    last_idx],
                'ema_fast': df_calc['ema_fast'].iloc[last_idx],
                'ema_slow': df_calc['ema_slow'].iloc[last_idx],
                'rsi': df_calc['rsi'].iloc[last_idx],
                'stoch_k': df_calc['stoch_k'].iloc[last_idx],
                'volume_ratio': df_calc['volume_ratio'].iloc[last_idx],
                'volatility': df_calc['volatility'].iloc[last_idx],
                'price_change': df_calc['price_change'].iloc[last_idx]
            }

        except Exception as e:
            self.logger.error(f"Error calculating scalping indicators: {e}")
            return {}

    def _check_scalping_conditions(self, indicators: Dict[str, Any]) -> bool:
        """Проверка условий для скальпинга"""
        try:
            # Проверка объема
            volume_ratio = indicators.get('volume_ratio', 0)
            if volume_ratio < self.MIN_VOLUME_RATIO:
                return False

            # Проверка волатильности (не слишком высокая)
            volatility = indicators.get('volatility', 0)
            if volatility > 0.02:  # Более 2% волатильность слишком рискованна для скальпинга
                return False

            return True

        except Exception as e:
            self.logger.error(f"Error checking scalping conditions: {e}")
            return False

    def _generate_scalping_signal(self, indicators: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Генерация скальпингового сигнала"""
        try:
            current_price = indicators.get('close', 0)
            ema_fast = indicators.get('ema_fast', 0)
            ema_slow = indicators.get('ema_slow', 0)
            rsi = indicators.get('rsi', 50)
            stoch_k = indicators.get('stoch_k', 50)
            volume_ratio = indicators.get('volume_ratio', 0)

            confidence = 0.0
            reasons = []

            # Определение направления
            if ema_fast > ema_slow and current_price > ema_fast:
                # Бычий сигнал
                if rsi < 70 and stoch_k < 80:  # Не перекуплено
                    confidence += 0.3
                    reasons.append("EMA_BULLISH")

                    if volume_ratio > self.VOLUME_SURGE_THRESHOLD:
                        confidence += 0.3
                        reasons.append("VOLUME_SURGE")

                    if 30 < rsi < 60:  # RSI в нейтральной зоне
                        confidence += 0.2
                        reasons.append("RSI_NEUTRAL")

                    if confidence >= self.MIN_CONFIDENCE:
                        return {
                            'action': 'BUY',
                            'entry_price': current_price,
                            'confidence': min(confidence, 1.0),
                            'reasons': ', '.join(reasons),
                            'timestamp': datetime.now()
                        }

            elif ema_fast < ema_slow and current_price < ema_fast:
                # Медвежий сигнал
                if rsi > 30 and stoch_k > 20:  # Не перепродано
                    confidence += 0.3
                    reasons.append("EMA_BEARISH")

                    if volume_ratio > self.VOLUME_SURGE_THRESHOLD:
                        confidence += 0.3
                        reasons.append("VOLUME_SURGE")

                    if 40 < rsi < 70:  # RSI в нейтральной зоне
                        confidence += 0.2
                        reasons.append("RSI_NEUTRAL")

                    if confidence >= self.MIN_CONFIDENCE:
                        return {
                            'action': 'SELL',
                            'entry_price': current_price,
                            'confidence': min(confidence, 1.0),
                            'reasons': ', '.join(reasons),
                            'timestamp': datetime.now()
                        }

            return None

        except Exception as e:
            self.logger.error(f"Error generating scalping signal: {e}")
            return None

    def execute(self, symbol: str, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Выполнение скальпинговой стратегии"""
        try:
            df = market_data.get('df')
            if df is None or len(df) < 50:
                return None

            current_position = self.position_manager.get_position_status(symbol)

            if current_position:
                return self._check_scalping_exit(symbol, df, current_position)
            else:
                return self._check_scalping_entry(symbol, df, market_data)

        except Exception as e:
            self.logger.error(f"Error executing scalping strategy: {e}")
            return None

    def _check_scalping_entry(self, symbol: str, df: pd.DataFrame, market_data: Dict[str, Any]) -> Optional[
        Dict[str, Any]]:
        """Проверка условий входа для скальпинга"""
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

            # Размер позиции (меньше для скальпинга)
            position_size = self._calculate_scalping_position_size(account_balance, entry_price, stop_loss)

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
                'timestamp': datetime.now()
            }

        except Exception as e:
            self.logger.error(f"Error checking scalping entry: {e}")
            return None

    def _check_scalping_exit(self, symbol: str, df: pd.DataFrame, position: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Проверка условий выхода для скальпинга"""
        try:
            current_price = df['close'].iloc[-1]
            entry_price = position.get('entry_price', 0)
            entry_time = position.get('entry_time')
            direction = position.get('direction', '')

            # Проверка времени в позиции
            if entry_time:
                if isinstance(entry_time, str):
                    entry_time = datetime.fromisoformat(entry_time)

                time_in_position = (datetime.now() - entry_time).total_seconds()
                if time_in_position > self.MAX_POSITION_TIME:
                    return {
                        'action': 'CLOSE',
                        'reason': 'max_time_scalping',
                        'exit_price': current_price
                    }

            # Быстрый выход при достижении целей
            if entry_price > 0:
                if direction == 'BUY':
                    pnl_pct = ((current_price - entry_price) / entry_price) * 100
                else:
                    pnl_pct = ((entry_price - current_price) / entry_price) * 100

                # Быстрая фиксация прибыли
                if pnl_pct >= self.PROFIT_TARGET_PCT * 100:
                    return {
                        'action': 'CLOSE',
                        'reason': 'scalping_profit_target',
                        'exit_price': current_price,
                        'pnl_pct': pnl_pct
                    }

                # Быстрый стоп-лосс
                if pnl_pct <= -self.EMERGENCY_STOP_PCT * 100:
                    return {
                        'action': 'CLOSE',
                        'reason': 'scalping_stop_loss',
                        'exit_price': current_price,
                        'pnl_pct': pnl_pct
                    }

            return None

        except Exception as e:
            self.logger.error(f"Error checking scalping exit: {e}")
            return None

    def _calculate_scalping_position_size(self, balance: float, entry: float, stop: float) -> float:
        """Расчет размера позиции для скальпинга (более консервативный)"""
        try:
            risk_amount = balance * 0.005  # 0.5% риск для скальпинга
            risk_per_unit = abs(entry - stop)

            if risk_per_unit <= 0:
                return 0.0

            position_size = risk_amount / risk_per_unit

            # Ограничение для скальпинга
            max_value = balance * 0.1  # Максимум 10% баланса
            if position_size * entry > max_value:
                position_size = max_value / entry

            return round(position_size, 8)

        except Exception as e:
            self.logger.error(f"Error calculating scalping position size: {e}")
            return 0.0

    def _is_signal_cooldown_active(self) -> bool:
        """Проверка cooldown для скальпинга"""
        if not self.last_signal_time:
            return False

        time_since_last = (datetime.now() - self.last_signal_time).total_seconds()
        return time_since_last < self.SIGNAL_COOLDOWN