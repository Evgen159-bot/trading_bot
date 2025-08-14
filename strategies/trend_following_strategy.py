import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime
import ta
from strategies.base_strategy import BaseStrategy


class TrendFollowingStrategy(BaseStrategy):
    """
    Стратегия следования тренду с улучшенными фильтрами

    Основана на принципах:
    - Trend is your friend
    - Multiple timeframe confirmation
    - Volume confirmation
    - Risk management
    """

    def __init__(self, market_analyzer, position_manager):
        super().__init__(name="TrendFollowingStrategy")
        self.market_analyzer = market_analyzer
        self.position_manager = position_manager

        # Параметры стратегии
        self.MIN_TREND_STRENGTH = 0.7
        self.MIN_VOLUME_CONFIRMATION = 1.5
        self.MAX_DRAWDOWN_PERCENT = 3.0
        self.PROFIT_TARGET_PERCENT = 5.0

        # Параметры индикаторов
        self.EMA_FAST = 12
        self.EMA_SLOW = 26
        self.EMA_TREND = 50
        self.ADX_PERIOD = 14
        self.ADX_THRESHOLD = 25

        self.logger.info("TrendFollowingStrategy initialized")

    def generate_signal(self, data: pd.DataFrame, symbol: str = None) -> Optional[Dict[str, Any]]:
        """Генерация сигнала следования тренду"""
        try:
            if len(data) < 100:
                return None

            # Расчет индикаторов
            indicators = self._calculate_trend_indicators(data)
            if not indicators:
                return None

            # Определение тренда
            trend_analysis = self._analyze_trend_strength(indicators)

            # Проверка условий входа
            if trend_analysis['strength'] < self.MIN_TREND_STRENGTH:
                return None

            # Генерация сигнала
            if trend_analysis['direction'] == 'BULLISH':
                return self._generate_bullish_signal(indicators, trend_analysis)
            elif trend_analysis['direction'] == 'BEARISH':
                return self._generate_bearish_signal(indicators, trend_analysis)

            return None

        except Exception as e:
            self.logger.error(f"Error generating trend signal: {e}")
            return None

    def _calculate_trend_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Расчет индикаторов тренда"""
        try:
            df_calc = df.copy()

            # EMA
            df_calc['ema_fast'] = ta.trend.EMAIndicator(df_calc['close'], window=self.EMA_FAST).ema_indicator()
            df_calc['ema_slow'] = ta.trend.EMAIndicator(df_calc['close'], window=self.EMA_SLOW).ema_indicator()
            df_calc['ema_trend'] = ta.trend.EMAIndicator(df_calc['close'], window=self.EMA_TREND).ema_indicator()

            # ADX для силы тренда
            df_calc['adx'] = ta.trend.ADXIndicator(
                df_calc['high'], df_calc['low'], df_calc['close'], window=self.ADX_PERIOD
            ).adx()

            # MACD
            macd = ta.trend.MACD(df_calc['close'])
            df_calc['macd'] = macd.macd()
            df_calc['macd_signal'] = macd.macd_signal()

            # Volume
            df_calc['volume_sma'] = df_calc['volume'].rolling(20).mean()
            df_calc['volume_ratio'] = df_calc['volume'] / df_calc['volume_sma']

            # ATR
            df_calc['atr'] = ta.volatility.AverageTrueRange(
                df_calc['high'], df_calc['low'], df_calc['close'], window=14
            ).average_true_range()

            last_idx = -1
            return {
                'close': df_calc['close'].iloc[last_idx],
                'ema_fast': df_calc['ema_fast'].iloc[last_idx],
                'ema_slow': df_calc['ema_slow'].iloc[last_idx],
                'ema_trend': df_calc['ema_trend'].iloc[last_idx],
                'adx': df_calc['adx'].iloc[last_idx],
                'macd': df_calc['macd'].iloc[last_idx],
                'macd_signal': df_calc['macd_signal'].iloc[last_idx],
                'volume_ratio': df_calc['volume_ratio'].iloc[last_idx],
                'atr': df_calc['atr'].iloc[last_idx]
            }

        except Exception as e:
            self.logger.error(f"Error calculating trend indicators: {e}")
            return {}

    def _analyze_trend_strength(self, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ силы и направления тренда"""
        try:
            ema_fast = indicators.get('ema_fast', 0)
            ema_slow = indicators.get('ema_slow', 0)
            ema_trend = indicators.get('ema_trend', 0)
            current_price = indicators.get('close', 0)
            adx = indicators.get('adx', 0)

            # Определение направления
            if ema_fast > ema_slow > ema_trend and current_price > ema_fast:
                direction = 'BULLISH'
                base_strength = 0.8
            elif ema_fast < ema_slow < ema_trend and current_price < ema_fast:
                direction = 'BEARISH'
                base_strength = 0.8
            elif ema_fast > ema_slow and current_price > ema_slow:
                direction = 'BULLISH'
                base_strength = 0.6
            elif ema_fast < ema_slow and current_price < ema_slow:
                direction = 'BEARISH'
                base_strength = 0.6
            else:
                direction = 'SIDEWAYS'
                base_strength = 0.3

            # Корректировка на основе ADX
            if adx > self.ADX_THRESHOLD:
                strength = min(base_strength + 0.2, 1.0)
            else:
                strength = base_strength * 0.8

            return {
                'direction': direction,
                'strength': strength,
                'adx': adx
            }

        except Exception as e:
            self.logger.error(f"Error analyzing trend strength: {e}")
            return {'direction': 'UNKNOWN', 'strength': 0.0}

    def _generate_bullish_signal(self, indicators: Dict[str, Any], trend: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Генерация бычьего сигнала"""
        try:
            # Проверка объема
            volume_ratio = indicators.get('volume_ratio', 0)
            if volume_ratio < self.MIN_VOLUME_CONFIRMATION:
                return None

            # Проверка MACD
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            if macd <= macd_signal:
                return None

            confidence = trend['strength']

            # Бонус за объем
            if volume_ratio > 2.0:
                confidence += 0.1

            return {
                'action': 'BUY',
                'entry_price': indicators['close'],
                'confidence': min(confidence, 1.0),
                'trend_strength': trend['strength'],
                'volume_confirmation': volume_ratio,
                'timestamp': datetime.now()
            }

        except Exception as e:
            self.logger.error(f"Error generating bullish signal: {e}")
            return None

    def _generate_bearish_signal(self, indicators: Dict[str, Any], trend: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Генерация медвежьего сигнала"""
        try:
            # Проверка объема
            volume_ratio = indicators.get('volume_ratio', 0)
            if volume_ratio < self.MIN_VOLUME_CONFIRMATION:
                return None

            # Проверка MACD
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            if macd >= macd_signal:
                return None

            confidence = trend['strength']

            # Бонус за объем
            if volume_ratio > 2.0:
                confidence += 0.1

            return {
                'action': 'SELL',
                'entry_price': indicators['close'],
                'confidence': min(confidence, 1.0),
                'trend_strength': trend['strength'],
                'volume_confirmation': volume_ratio,
                'timestamp': datetime.now()
            }

        except Exception as e:
            self.logger.error(f"Error generating bearish signal: {e}")
            return None

    def execute(self, symbol: str, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Выполнение стратегии следования тренду"""
        try:
            df = market_data.get('df')
            if df is None or len(df) < 100:
                return None

            current_position = self.position_manager.get_position_status(symbol)

            if current_position:
                return self._check_exit_conditions(symbol, df, current_position)
            else:
                return self._check_entry_conditions(symbol, df, market_data)

        except Exception as e:
            self.logger.error(f"Error executing trend strategy: {e}")
            return None

    def _check_entry_conditions(self, symbol: str, df: pd.DataFrame, market_data: Dict[str, Any]) -> Optional[
        Dict[str, Any]]:
        """Проверка условий входа"""
        try:
            signal = self.generate_signal(df, symbol)
            if not signal:
                return None

            # Расчет уровней
            atr = ta.volatility.AverageTrueRange(
                df['high'], df['low'], df['close'], window=14
            ).average_true_range().iloc[-1]

            entry_price = signal['entry_price']

            if signal['action'] == 'BUY':
                stop_loss = entry_price - (atr * 2.0)
                take_profit = entry_price + (atr * 4.0)
            else:
                stop_loss = entry_price + (atr * 2.0)
                take_profit = entry_price - (atr * 4.0)

            # Размер позиции
            account_balance = market_data.get('account_balance', 0)
            position_size = self._calculate_position_size(account_balance, entry_price, stop_loss)

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
                'atr': atr,
                'timestamp': datetime.now()
            }

        except Exception as e:
            self.logger.error(f"Error checking entry conditions: {e}")
            return None

    def _check_exit_conditions(self, symbol: str, df: pd.DataFrame, position: Dict[str, Any]) -> Optional[
        Dict[str, Any]]:
        """Проверка условий выхода"""
        try:
            current_price = df['close'].iloc[-1]
            direction = position.get('direction', '')
            entry_price = position.get('entry_price', 0)

            # Расчет PnL
            if direction == 'BUY':
                pnl_pct = ((current_price - entry_price) / entry_price) * 100
            else:
                pnl_pct = ((entry_price - current_price) / entry_price) * 100

            # Проверка максимального убытка
            if pnl_pct < -self.MAX_DRAWDOWN_PERCENT:
                return {
                    'action': 'CLOSE',
                    'reason': 'max_drawdown',
                    'exit_price': current_price,
                    'pnl_pct': pnl_pct
                }

            # Проверка цели прибыли
            if pnl_pct > self.PROFIT_TARGET_PERCENT:
                return {
                    'action': 'CLOSE',
                    'reason': 'profit_target',
                    'exit_price': current_price,
                    'pnl_pct': pnl_pct
                }

            # Проверка разворота тренда
            trend_analysis = self._analyze_trend_strength(self._calculate_trend_indicators(df))

            if direction == 'BUY' and trend_analysis['direction'] == 'BEARISH':
                return {
                    'action': 'CLOSE',
                    'reason': 'trend_reversal',
                    'exit_price': current_price,
                    'pnl_pct': pnl_pct
                }
            elif direction == 'SELL' and trend_analysis['direction'] == 'BULLISH':
                return {
                    'action': 'CLOSE',
                    'reason': 'trend_reversal',
                    'exit_price': current_price,
                    'pnl_pct': pnl_pct
                }

            return None

        except Exception as e:
            self.logger.error(f"Error checking exit conditions: {e}")
            return None

    def _calculate_position_size(self, balance: float, entry: float, stop: float) -> float:
        """Расчет размера позиции"""
        try:
            risk_amount = balance * 0.015  # 1.5% риск
            risk_per_unit = abs(entry - stop)

            if risk_per_unit <= 0:
                return 0.0

            return round(risk_amount / risk_per_unit, 8)

        except Exception as e:
            self.logger.error(f"Error calculating position size: {e}")
            return 0.0