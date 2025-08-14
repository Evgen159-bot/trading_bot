import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime
import ta
from strategies.base_strategy import BaseStrategy


class MeanReversionStrategy(BaseStrategy):
    """
    Стратегия возврата к среднему

    Основана на принципах:
    - Цены возвращаются к среднему значению
    - Торговля против краткосрочных экстремумов
    - Использование Bollinger Bands и RSI
    - Работа в боковых трендах
    """

    def __init__(self, market_analyzer, position_manager):
        super().__init__(name="MeanReversionStrategy")
        self.market_analyzer = market_analyzer
        self.position_manager = position_manager

        # Параметры стратегии возврата к среднему
        self.MIN_CONFIDENCE = 0.65
        self.SIGNAL_COOLDOWN = 900  # 15 минут между сигналами

        # Параметры Bollinger Bands
        self.BB_PERIOD = 20
        self.BB_STD = 2.0
        self.BB_EXTREME_STD = 2.5  # Для экстремальных уровней

        # Параметры RSI
        self.RSI_PERIOD = 14
        self.RSI_OVERSOLD = 25
        self.RSI_OVERBOUGHT = 75
        self.RSI_EXTREME_OVERSOLD = 15
        self.RSI_EXTREME_OVERBOUGHT = 85

        # Фильтр тренда (избегаем сильных трендов)
        self.MAX_TREND_STRENGTH = 0.6

        # Управление рисками
        self.STOP_LOSS_PCT = 0.025  # 2.5% стоп-лосс
        self.PROFIT_TARGET_PCT = 0.04  # 4% цель прибыли

        self.logger.info("MeanReversionStrategy initialized for range trading")

    def generate_signal(self, data: pd.DataFrame, symbol: str = None) -> Optional[Dict[str, Any]]:
        """Генерация сигнала возврата к среднему"""
        try:
            if len(data) < 50:
                return None

            # Проверка cooldown
            if self._is_signal_cooldown_active():
                return None

            # Расчет индикаторов
            indicators = self._calculate_mean_reversion_indicators(data)
            if not indicators:
                return None

            # Проверка рыночных условий (избегаем сильных трендов)
            if not self._check_ranging_market(indicators):
                return None

            # Генерация сигнала
            signal = self._generate_mean_reversion_signal(indicators)

            if signal and signal['confidence'] >= self.MIN_CONFIDENCE:
                self.last_signal_time = datetime.now()
                return signal

            return None

        except Exception as e:
            self.logger.error(f"Error generating mean reversion signal: {e}")
            return None

    def _calculate_mean_reversion_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Расчет индикаторов для стратегии возврата к среднему"""
        try:
            df_calc = df.copy()

            # Bollinger Bands
            bb = ta.volatility.BollingerBands(df_calc['close'], window=self.BB_PERIOD, window_dev=self.BB_STD)
            df_calc['bb_upper'] = bb.bollinger_hband()
            df_calc['bb_lower'] = bb.bollinger_lband()
            df_calc['bb_middle'] = bb.bollinger_mavg()

            # Экстремальные Bollinger Bands
            bb_extreme = ta.volatility.BollingerBands(df_calc['close'], window=self.BB_PERIOD,
                                                      window_dev=self.BB_EXTREME_STD)
            df_calc['bb_upper_extreme'] = bb_extreme.bollinger_hband()
            df_calc['bb_lower_extreme'] = bb_extreme.bollinger_lband()

            # RSI
            df_calc['rsi'] = ta.momentum.RSIIndicator(df_calc['close'], window=self.RSI_PERIOD).rsi()

            # EMA для определения тренда
            df_calc['ema_20'] = ta.trend.EMAIndicator(df_calc['close'], window=20).ema_indicator()
            df_calc['ema_50'] = ta.trend.EMAIndicator(df_calc['close'], window=50).ema_indicator()

            # Расстояние от средней
            df_calc['distance_from_mean'] = (df_calc['close'] - df_calc['bb_middle']) / df_calc['bb_middle']

            last_idx = -1
            return {
                'close': df_calc['close'].iloc[last_idx],
                'bb_upper': df_calc['bb_upper'].iloc[last_idx],
                'bb_lower': df_calc['bb_lower'].iloc[last_idx],
                'bb_middle': df_calc['bb_middle'].iloc[last_idx],
                'bb_upper_extreme': df_calc['bb_upper_extreme'].iloc[last_idx],
                'bb_lower_extreme': df_calc['bb_lower_extreme'].iloc[last_idx],
                'rsi': df_calc['rsi'].iloc[last_idx],
                'ema_20': df_calc['ema_20'].iloc[last_idx],
                'ema_50': df_calc['ema_50'].iloc[last_idx],
                'distance_from_mean': df_calc['distance_from_mean'].iloc[last_idx]
            }

        except Exception as e:
            self.logger.error(f"Error calculating mean reversion indicators: {e}")
            return {}

    def _check_ranging_market(self, indicators: Dict[str, Any]) -> bool:
        """Проверка бокового рынка (подходящего для mean reversion)"""
        try:
            ema_20 = indicators.get('ema_20', 0)
            ema_50 = indicators.get('ema_50', 0)

            # Проверяем, что EMA близки друг к другу (боковой тренд)
            if ema_20 > 0 and ema_50 > 0:
                ema_difference = abs(ema_20 - ema_50) / ema_50
                if ema_difference > self.MAX_TREND_STRENGTH:
                    return False  # Слишком сильный тренд

            return True

        except Exception as e:
            self.logger.error(f"Error checking ranging market: {e}")
            return False

    def _generate_mean_reversion_signal(self, indicators: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Генерация сигнала возврата к среднему"""
        try:
            current_price = indicators.get('close', 0)
            bb_upper = indicators.get('bb_upper', 0)
            bb_lower = indicators.get('bb_lower', 0)
            bb_middle = indicators.get('bb_middle', 0)
            bb_upper_extreme = indicators.get('bb_upper_extreme', 0)
            bb_lower_extreme = indicators.get('bb_lower_extreme', 0)
            rsi = indicators.get('rsi', 50)
            distance_from_mean = indicators.get('distance_from_mean', 0)

            confidence = 0.0
            reasons = []

            # Сигнал на покупку (цена у нижней границы)
            if current_price <= bb_lower and rsi <= self.RSI_OVERBOUGHT:
                confidence += 0.4
                reasons.append("BB_OVERSOLD")

                # Экстремальная перепроданность
                if current_price <= bb_lower_extreme and rsi <= self.RSI_EXTREME_OVERSOLD:
                    confidence += 0.3
                    reasons.append("EXTREME_OVERSOLD")

                # Расстояние от средней
                if distance_from_mean < -0.02:  # Более 2% ниже средней
                    confidence += 0.2
                    reasons.append("FAR_FROM_MEAN")

                if confidence >= self.MIN_CONFIDENCE:
                    return {
                        'action': 'BUY',
                        'entry_price': current_price,
                        'confidence': min(confidence, 1.0),
                        'reasons': ', '.join(reasons),
                        'mean_distance': distance_from_mean,
                        'timestamp': datetime.now()
                    }

            # Сигнал на продажу (цена у верхней границы)
            elif current_price >= bb_upper and rsi >= self.RSI_OVERSOLD:
                confidence += 0.4
                reasons.append("BB_OVERBOUGHT")

                # Экстремальная перекупленность
                if current_price >= bb_upper_extreme and rsi >= self.RSI_EXTREME_OVERBOUGHT:
                    confidence += 0.3
                    reasons.append("EXTREME_OVERBOUGHT")

                # Расстояние от средней
                if distance_from_mean > 0.02:  # Более 2% выше средней
                    confidence += 0.2
                    reasons.append("FAR_FROM_MEAN")

                if confidence >= self.MIN_CONFIDENCE:
                    return {
                        'action': 'SELL',
                        'entry_price': current_price,
                        'confidence': min(confidence, 1.0),
                        'reasons': ', '.join(reasons),
                        'mean_distance': distance_from_mean,
                        'timestamp': datetime.now()
                    }

            return None

        except Exception as e:
            self.logger.error(f"Error generating mean reversion signal: {e}")
            return None

    def _check_breakout_exit(self, symbol: str, df: pd.DataFrame, position: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Проверка условий выхода"""
        try:
            current_price = df['close'].iloc[-1]

            # Расчет BB для проверки возврата к средней
            bb_middle = ta.volatility.BollingerBands(df['close'], window=self.BB_PERIOD).bollinger_mavg().iloc[-1]

            direction = position.get('direction', '')
            entry_price = position.get('entry_price', 0)

            # Проверка возврата к средней (цель стратегии)
            if direction == 'BUY':
                # Для лонга - проверяем приближение к средней сверху
                if current_price >= bb_middle * 0.998:  # Близко к средней
                    return {
                        'action': 'CLOSE',
                        'reason': 'mean_reversion_target',
                        'exit_price': current_price
                    }
            elif direction == 'SELL':
                # Для шорта - проверяем приближение к средней снизу
                if current_price <= bb_middle * 1.002:  # Близко к средней
                    return {
                        'action': 'CLOSE',
                        'reason': 'mean_reversion_target',
                        'exit_price': current_price
                    }

            return None

        except Exception as e:
            self.logger.error(f"Error checking mean reversion exit: {e}")
            return None

    def _is_signal_cooldown_active(self) -> bool:
        """Проверка cooldown"""
        if not self.last_signal_time:
            return False

        time_since_last = (datetime.now() - self.last_signal_time).total_seconds()
        return time_since_last < self.SIGNAL_COOLDOWN