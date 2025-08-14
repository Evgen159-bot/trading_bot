import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime
import ta
from strategies.base_strategy import BaseStrategy


class SwingStrategy(BaseStrategy):
    """
    Стратегия свинг-трейдинга для среднесрочных позиций

    Основана на принципах:
    - Удержание позиций от нескольких часов до дней
    - Торговля на больших движениях
    - Меньшая частота сделок
    - Более широкие стоп-лоссы и тейк-профиты
    """

    def __init__(self, market_analyzer, position_manager):
        super().__init__(name="SwingStrategy")
        self.market_analyzer = market_analyzer
        self.position_manager = position_manager

        # Параметры свинг-трейдинга
        self.MIN_CONFIDENCE = 0.8  # Высокий порог для качественных сигналов
        self.SIGNAL_COOLDOWN = 3600  # 1 час между сигналами
        self.MAX_POSITION_TIME = 7 * 24 * 3600  # 7 дней максимум

        # Цели прибыли и убытков
        self.PROFIT_TARGET_PCT = 0.08  # 8% цель прибыли
        self.STOP_LOSS_PCT = 0.04  # 4% стоп-лосс (R:R = 2:1)
        self.TRAILING_STOP_PCT = 0.03  # 3% трейлинг-стоп

        # Параметры индикаторов (медленные)
        self.EMA_FAST = 21
        self.EMA_SLOW = 50
        self.EMA_TREND = 200
        self.RSI_PERIOD = 21
        self.MACD_FAST = 12
        self.MACD_SLOW = 26
        self.MACD_SIGNAL = 9

        # Фильтры тренда
        self.MIN_TREND_STRENGTH = 0.7
        self.ADX_THRESHOLD = 25

        self.logger.info("SwingStrategy initialized for medium-term trading")

    def generate_signal(self, data: pd.DataFrame, symbol: str = None) -> Optional[Dict[str, Any]]:
        """Генерация свинг-сигнала"""
        try:
            if len(data) < 200:  # Больше данных для свинг-анализа
                return None

            # Проверка cooldown
            if self._is_signal_cooldown_active():
                return None

            # Расчет индикаторов
            indicators = self._calculate_swing_indicators(data)
            if not indicators:
                return None

            # Анализ тренда
            trend_analysis = self._analyze_swing_trend(indicators)

            # Проверка силы тренда
            if trend_analysis['strength'] < self.MIN_TREND_STRENGTH:
                return None

            # Генерация сигнала
            signal = self._generate_swing_signal(indicators, trend_analysis)

            if signal and signal['confidence'] >= self.MIN_CONFIDENCE:
                self.last_signal_time = datetime.now()
                return signal

            return None

        except Exception as e:
            self.logger.error(f"Error generating swing signal: {e}")
            return None

    def _calculate_swing_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Расчет индикаторов для свинг-трейдинга"""
        try:
            df_calc = df.copy()

            # EMA для трендового анализа
            df_calc['ema_fast'] = ta.trend.EMAIndicator(df_calc['close'], window=self.EMA_FAST).ema_indicator()
            df_calc['ema_slow'] = ta.trend.EMAIndicator(df_calc['close'], window=self.EMA_SLOW).ema_indicator()
            df_calc['ema_trend'] = ta.trend.EMAIndicator(df_calc['close'], window=self.EMA_TREND).ema_indicator()

            # RSI для перекупленности/перепроданности
            df_calc['rsi'] = ta.momentum.RSIIndicator(df_calc['close'], window=self.RSI_PERIOD).rsi()

            # MACD для подтверждения тренда
            macd = ta.trend.MACD(df_calc['close'],
                                 window_fast=self.MACD_FAST,
                                 window_slow=self.MACD_SLOW,
                                 window_sign=self.MACD_SIGNAL)
            df_calc['macd'] = macd.macd()
            df_calc['macd_signal'] = macd.macd_signal()

            # ADX для силы тренда
            df_calc['adx'] = ta.trend.ADXIndicator(
                df_calc['high'], df_calc['low'], df_calc['close'], window=14
            ).adx()

            # Поддержка и сопротивление
            df_calc['resistance'] = df_calc['high'].rolling(20).max()
            df_calc['support'] = df_calc['low'].rolling(20).min()

            last_idx = -1
            return {
                'close': df_calc['close'].iloc[last_idx],
                'ema_fast': df_calc['ema_fast'].iloc[last_idx],
                'ema_slow': df_calc['ema_slow'].iloc[last_idx],
                'ema_trend': df_calc['ema_trend'].iloc[last_idx],
                'rsi': df_calc['rsi'].iloc[last_idx],
                'macd': df_calc['macd'].iloc[last_idx],
                'macd_signal': df_calc['macd_signal'].iloc[last_idx],
                'adx': df_calc['adx'].iloc[last_idx],
                'resistance': df_calc['resistance'].iloc[last_idx],
                'support': df_calc['support'].iloc[last_idx]
            }

        except Exception as e:
            self.logger.error(f"Error calculating swing indicators: {e}")
            return {}

    def _analyze_swing_trend(self, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ тренда для свинг-трейдинга"""
        try:
            ema_fast = indicators.get('ema_fast', 0)
            ema_slow = indicators.get('ema_slow', 0)
            ema_trend = indicators.get('ema_trend', 0)
            current_price = indicators.get('close', 0)
            adx = indicators.get('adx', 0)

            # Определение направления тренда
            if ema_fast > ema_slow > ema_trend and current_price > ema_trend:
                direction = 'BULLISH'
                base_strength = 0.8
            elif ema_fast < ema_slow < ema_trend and current_price < ema_trend:
                direction = 'BEARISH'
                base_strength = 0.8
            else:
                direction = 'SIDEWAYS'
                base_strength = 0.3

            # Корректировка силы на основе ADX
            if adx > self.ADX_THRESHOLD:
                strength = min(base_strength + 0.2, 1.0)
            else:
                strength = base_strength * 0.7

            return {
                'direction': direction,
                'strength': strength,
                'adx': adx
            }

        except Exception as e:
            self.logger.error(f"Error analyzing swing trend: {e}")
            return {'direction': 'UNKNOWN', 'strength': 0.0}

    def _generate_swing_signal(self, indicators: Dict[str, Any], trend: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Генерация свинг-сигнала"""
        try:
            current_price = indicators.get('close', 0)
            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            support = indicators.get('support', 0)
            resistance = indicators.get('resistance', 0)

            confidence = trend['strength']
            reasons = [f"TREND_{trend['direction']}"]

            if trend['direction'] == 'BULLISH':
                # Проверка отскока от поддержки
                if current_price > support and (current_price - support) / support < 0.02:
                    confidence += 0.1
                    reasons.append("SUPPORT_BOUNCE")

                # RSI не перекуплен
                if rsi < 70:
                    confidence += 0.1
                    reasons.append("RSI_OK")

                # MACD подтверждение
                if macd > macd_signal:
                    confidence += 0.1
                    reasons.append("MACD_BULLISH")

                if confidence >= self.MIN_CONFIDENCE:
                    return {
                        'action': 'BUY',
                        'entry_price': current_price,
                        'confidence': min(confidence, 1.0),
                        'reasons': ', '.join(reasons),
                        'timestamp': datetime.now()
                    }

            elif trend['direction'] == 'BEARISH':
                # Проверка отскока от сопротивления
                if current_price < resistance and (resistance - current_price) / resistance < 0.02:
                    confidence += 0.1
                    reasons.append("RESISTANCE_REJECTION")

                # RSI не перепродан
                if rsi > 30:
                    confidence += 0.1
                    reasons.append("RSI_OK")

                # MACD подтверждение
                if macd < macd_signal:
                    confidence += 0.1
                    reasons.append("MACD_BEARISH")

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
            self.logger.error(f"Error generating swing signal: {e}")
            return None

    def _is_signal_cooldown_active(self) -> bool:
        """Проверка cooldown для свинг-трейдинга"""
        if not self.last_signal_time:
            return False

        time_since_last = (datetime.now() - self.last_signal_time).total_seconds()
        return time_since_last < self.SIGNAL_COOLDOWN