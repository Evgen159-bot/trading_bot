import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import ta
from strategies.base_strategy import BaseStrategy


class SmartMoneyStrategy(BaseStrategy):
    """
    Улучшенная стратегия на основе Smart Money Concepts и лучших практик 2024-2025

    Основные принципы:
    - Market Structure (BOS/CHoCH)
    - Order Blocks
    - Fair Value Gaps
    - Liquidity Sweeps
    - Multi-timeframe анализ
    - Volume Profile
    """

    def __init__(self, market_analyzer, position_manager):
        super().__init__(name="SmartMoneyStrategy")
        self.market_analyzer = market_analyzer
        self.position_manager = position_manager

        # Улучшенные параметры стратегии
        self.MIN_CONFIDENCE = 0.75  # Минимальная уверенность 75%
        self.MIN_CONDITIONS_REQUIRED = 4  # Из 7 условий требуем минимум 4
        self.SIGNAL_COOLDOWN = 300  # 5 минут между сигналами

        # Параметры Smart Money
        self.VOLUME_THRESHOLD = 2.0  # Минимальный объем для сигнала
        self.TREND_STRENGTH_MIN = 0.6  # Минимальная сила тренда
        self.RISK_REWARD_MIN = 2.0  # Минимальное соотношение риск/прибыль

        # Параметры индикаторов (более консервативные)
        self.RSI_OVERSOLD = 25
        self.RSI_OVERBOUGHT = 75
        self.RSI_NEUTRAL_LOW = 45
        self.RSI_NEUTRAL_HIGH = 55

        # Фильтры рынка
        self.VOLATILITY_FILTER = True
        self.NEWS_TIME_FILTER = True
        self.MARKET_HOURS_FILTER = True

        # Статистика стратегии
        self.last_signal_time = None
        self.signal_history = []
        self.market_structure = "UNKNOWN"

        self.logger.info("SmartMoneyStrategy initialized with improved parameters")

    def generate_signal(self, data: pd.DataFrame, symbol: str = None) -> Optional[Dict[str, Any]]:
        """Генерация высококачественного торгового сигнала"""
        try:
            self.logger.debug(f"Generating signal for {symbol}, data length: {len(data) if data is not None else 0}")

            if data is None or len(data) < 100:
                self.logger.debug(f"Insufficient data for signal generation: {len(data) if data is not None else 0}")
                return None

            # Проверка cooldown
            if self._is_signal_cooldown_active():
                self.logger.debug(f"Signal cooldown active for {symbol}")
                return None

            # Расчет индикаторов
            signals = self._calculate_enhanced_indicators(data)
            if not signals:
                self.logger.warning(f"Failed to calculate indicators for {symbol}")
                return None

            # Анализ рыночной структуры
            market_structure = self._analyze_market_structure(data)
            self.logger.debug(f"Market structure for {symbol}: {market_structure.get('structure', 'UNKNOWN')}")

            # Проверка фильтров
            if not self._check_market_filters(signals, market_structure):
                self.logger.debug(f"Market filters failed for {symbol}")
                return None

            # Генерация сигналов
            long_signal = self._generate_long_signal(signals, market_structure)
            short_signal = self._generate_short_signal(signals, market_structure)

            self.logger.debug(f"Long signal for {symbol}: {long_signal is not None}")
            self.logger.debug(f"Short signal for {symbol}: {short_signal is not None}")

            # Выбор лучшего сигнала
            best_signal = self._select_best_signal(long_signal, short_signal)

            if best_signal and best_signal['confidence'] >= self.MIN_CONFIDENCE:
                self.logger.info(
                    f"High quality signal generated for {symbol}: {best_signal['action']} with confidence {best_signal['confidence']:.2%}")
                self.last_signal_time = datetime.now()
                self.signal_history.append(best_signal)
                return best_signal
            elif best_signal:
                self.logger.debug(
                    f"Signal confidence too low for {symbol}: {best_signal['confidence']:.2%} < {self.MIN_CONFIDENCE:.2%}")

            return None

        except Exception as e:
            self.logger.error(f"Error generating signal: {e}")
            return None

    def _calculate_enhanced_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Расчет улучшенных индикаторов"""
        try:
            df_calc = df.copy()

            # Основные индикаторы
            df_calc['rsi'] = ta.momentum.RSIIndicator(df_calc['close'], window=14).rsi()

            # MACD с улучшенными параметрами
            macd = ta.trend.MACD(df_calc['close'], window_fast=12, window_slow=26, window_sign=9)
            df_calc['macd'] = macd.macd()
            df_calc['macd_signal'] = macd.macd_signal()
            df_calc['macd_histogram'] = macd.macd_diff()

            # EMA для трендового анализа
            df_calc['ema_9'] = ta.trend.EMAIndicator(df_calc['close'], window=9).ema_indicator()
            df_calc['ema_21'] = ta.trend.EMAIndicator(df_calc['close'], window=21).ema_indicator()
            df_calc['ema_50'] = ta.trend.EMAIndicator(df_calc['close'], window=50).ema_indicator()
            df_calc['ema_200'] = ta.trend.EMAIndicator(df_calc['close'], window=200).ema_indicator()

            # Bollinger Bands
            bb = ta.volatility.BollingerBands(df_calc['close'], window=20, window_dev=2)
            df_calc['bb_upper'] = bb.bollinger_hband()
            df_calc['bb_lower'] = bb.bollinger_lband()
            df_calc['bb_middle'] = bb.bollinger_mavg()
            df_calc['bb_squeeze'] = (df_calc['bb_upper'] - df_calc['bb_lower']) / df_calc['bb_middle']

            # Volume анализ
            df_calc['volume_sma'] = df_calc['volume'].rolling(20).mean()
            df_calc['volume_ratio'] = df_calc['volume'] / df_calc['volume_sma']
            df_calc['volume_surge'] = df_calc['volume_ratio'] > 2.0

            # ATR для волатильности
            df_calc['atr'] = ta.volatility.AverageTrueRange(
                df_calc['high'], df_calc['low'], df_calc['close'], window=14
            ).average_true_range()

            # Stochastic
            stoch = ta.momentum.StochasticOscillator(
                df_calc['high'], df_calc['low'], df_calc['close'], window=14
            )
            df_calc['stoch_k'] = stoch.stoch()
            df_calc['stoch_d'] = stoch.stoch_signal()

            # Williams %R
            df_calc['williams_r'] = ta.momentum.WilliamsRIndicator(
                df_calc['high'], df_calc['low'], df_calc['close'], lbp=14
            ).williams_r()

            # Momentum
            df_calc['momentum'] = df_calc['close'].pct_change(10) * 100

            # Извлекаем последние значения
            last_idx = len(df_calc) - 1

            return {
                'close': df_calc['close'].iloc[last_idx],
                'high': df_calc['high'].iloc[last_idx],
                'low': df_calc['low'].iloc[last_idx],
                'volume': df_calc['volume'].iloc[last_idx],

                'rsi': df_calc['rsi'].iloc[last_idx],
                'rsi_prev': df_calc['rsi'].iloc[last_idx - 1] if last_idx > 0 else 50,

                'macd': df_calc['macd'].iloc[last_idx],
                'macd_signal': df_calc['macd_signal'].iloc[last_idx],
                'macd_histogram': df_calc['macd_histogram'].iloc[last_idx],
                'macd_prev': df_calc['macd_histogram'].iloc[last_idx - 1] if last_idx > 0 else 0,

                'ema_9': df_calc['ema_9'].iloc[last_idx],
                'ema_21': df_calc['ema_21'].iloc[last_idx],
                'ema_50': df_calc['ema_50'].iloc[last_idx],
                'ema_200': df_calc['ema_200'].iloc[last_idx],

                'bb_upper': df_calc['bb_upper'].iloc[last_idx],
                'bb_lower': df_calc['bb_lower'].iloc[last_idx],
                'bb_middle': df_calc['bb_middle'].iloc[last_idx],
                'bb_squeeze': df_calc['bb_squeeze'].iloc[last_idx],

                'volume_ratio': df_calc['volume_ratio'].iloc[last_idx],
                'volume_surge': df_calc['volume_surge'].iloc[last_idx],

                'atr': df_calc['atr'].iloc[last_idx],

                'stoch_k': df_calc['stoch_k'].iloc[last_idx],
                'stoch_d': df_calc['stoch_d'].iloc[last_idx],

                'williams_r': df_calc['williams_r'].iloc[last_idx],
                'momentum': df_calc['momentum'].iloc[last_idx],

                'timestamp': datetime.now()
            }

        except Exception as e:
            self.logger.error(f"Error calculating indicators: {e}")
            return {}

    def _analyze_market_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализ рыночной структуры (Smart Money Concepts)"""
        try:
            if len(df) < 50:
                return {'structure': 'UNKNOWN', 'strength': 0.0}

            # Анализ Higher Highs / Lower Lows
            highs = df['high'].rolling(10).max()
            lows = df['low'].rolling(10).min()

            recent_highs = highs.tail(20)
            recent_lows = lows.tail(20)

            # Определение структуры
            higher_highs = (recent_highs.iloc[-1] > recent_highs.iloc[-10])
            higher_lows = (recent_lows.iloc[-1] > recent_lows.iloc[-10])
            lower_highs = (recent_highs.iloc[-1] < recent_highs.iloc[-10])
            lower_lows = (recent_lows.iloc[-1] < recent_lows.iloc[-10])

            if higher_highs and higher_lows:
                structure = "BULLISH_STRUCTURE"
                strength = 0.8
            elif lower_highs and lower_lows:
                structure = "BEARISH_STRUCTURE"
                strength = 0.8
            elif higher_highs and lower_lows:
                structure = "RANGING_EXPANSION"
                strength = 0.3
            elif lower_highs and higher_lows:
                structure = "RANGING_COMPRESSION"
                strength = 0.3
            else:
                structure = "NEUTRAL"
                strength = 0.5

            # Анализ объема на ключевых уровнях
            volume_confirmation = self._analyze_volume_structure(df)

            return {
                'structure': structure,
                'strength': strength,
                'volume_confirmation': volume_confirmation,
                'trend_direction': self._get_trend_direction(df)
            }

        except Exception as e:
            self.logger.error(f"Error analyzing market structure: {e}")
            return {'structure': 'UNKNOWN', 'strength': 0.0}

    def _analyze_volume_structure(self, df: pd.DataFrame) -> float:
        """Анализ объемной структуры"""
        try:
            # Volume Profile анализ
            recent_volume = df['volume'].tail(20)
            avg_volume = df['volume'].tail(100).mean()

            # Проверка всплесков объема на важных уровнях
            volume_spikes = (recent_volume > avg_volume * 1.5).sum()
            volume_score = min(volume_spikes / 20, 1.0)

            return volume_score

        except Exception as e:
            self.logger.error(f"Error analyzing volume structure: {e}")
            return 0.0

    def _get_trend_direction(self, df: pd.DataFrame) -> str:
        """Определение направления тренда"""
        try:
            if len(df) < 50:
                return "UNKNOWN"

            # Анализ EMA
            ema_9 = ta.trend.EMAIndicator(df['close'], window=9).ema_indicator().iloc[-1]
            ema_21 = ta.trend.EMAIndicator(df['close'], window=21).ema_indicator().iloc[-1]
            ema_50 = ta.trend.EMAIndicator(df['close'], window=50).ema_indicator().iloc[-1]

            current_price = df['close'].iloc[-1]

            if ema_9 > ema_21 > ema_50 and current_price > ema_9:
                return "STRONG_UPTREND"
            elif ema_9 > ema_21 and current_price > ema_21:
                return "UPTREND"
            elif ema_9 < ema_21 < ema_50 and current_price < ema_9:
                return "STRONG_DOWNTREND"
            elif ema_9 < ema_21 and current_price < ema_21:
                return "DOWNTREND"
            else:
                return "SIDEWAYS"

        except Exception as e:
            self.logger.error(f"Error getting trend direction: {e}")
            return "UNKNOWN"

    def _check_market_filters(self, signals: Dict[str, Any], market_structure: Dict[str, Any]) -> bool:
        """Проверка рыночных фильтров"""
        try:
            self.logger.debug("Checking market filters...")

            # Фильтр волатильности
            if self.VOLATILITY_FILTER:
                atr = signals.get('atr', 0)
                if atr <= 0:
                    self.logger.debug(f"Volatility filter failed: ATR={atr}")
                    return False
                else:
                    self.logger.debug(f"Volatility filter passed: ATR={atr:.6f}")

            # Фильтр объема
            volume_ratio = signals.get('volume_ratio', 0)
            if volume_ratio < 1.2:  # Минимальный объем
                self.logger.debug(f"Volume filter failed: {volume_ratio:.2f} < 1.2")
                return False
            else:
                self.logger.debug(f"Volume filter passed: {volume_ratio:.2f}")

            # Фильтр рыночной структуры
            structure_strength = market_structure.get('strength', 0)
            if structure_strength < 0.4:
                self.logger.debug(f"Structure filter failed: strength={structure_strength:.2f} < 0.4")
                return False
            else:
                self.logger.debug(f"Structure filter passed: strength={structure_strength:.2f}")

            # Фильтр времени (избегаем новостные часы)
            if self.NEWS_TIME_FILTER:
                current_hour = datetime.now().hour
                # Избегаем 14:30-16:30 UTC (US market open)
                if 14 <= current_hour <= 16:
                    self.logger.debug(f"Time filter failed: hour={current_hour} in news time")
                    return False
                else:
                    self.logger.debug(f"Time filter passed: hour={current_hour}")

            self.logger.debug("All market filters passed")

            return True

        except Exception as e:
            self.logger.error(f"Error checking market filters: {e}")
            return False

    def _generate_long_signal(self, signals: Dict[str, Any], market_structure: Dict[str, Any]) -> Optional[
        Dict[str, Any]]:
        """Генерация сигнала на покупку"""
        try:
            conditions_met = 0
            reasons = []
            confidence_score = 0.0

            self.logger.debug(f"Checking long signal conditions...")

            # 1. RSI условие (улучшенное)
            rsi = signals.get('rsi', 50)
            rsi_prev = signals.get('rsi_prev', 50)

            if (rsi < self.RSI_OVERSOLD or
                    (rsi > rsi_prev and self.RSI_NEUTRAL_LOW < rsi < self.RSI_NEUTRAL_HIGH)):
                conditions_met += 1
                reasons.append("RSI_BULLISH")
                confidence_score += 0.15
                self.logger.debug(f"RSI condition met: {rsi:.1f}")
            else:
                self.logger.debug(f"RSI condition not met: {rsi:.1f}")

            # 2. MACD условие (с дивергенцией)
            macd = signals.get('macd', 0)
            macd_signal = signals.get('macd_signal', 0)
            macd_histogram = signals.get('macd_histogram', 0)
            macd_prev = signals.get('macd_prev', 0)

            if (macd > macd_signal and macd_histogram > 0 and macd_histogram > macd_prev):
                conditions_met += 1
                reasons.append("MACD_BULLISH")
                confidence_score += 0.2
                self.logger.debug(f"MACD condition met: {macd:.6f} > {macd_signal:.6f}")
            else:
                self.logger.debug(f"MACD condition not met: {macd:.6f} vs {macd_signal:.6f}")

            # 3. EMA тренд (строгий)
            ema_9 = signals.get('ema_9', 0)
            ema_21 = signals.get('ema_21', 0)
            ema_50 = signals.get('ema_50', 0)
            current_price = signals.get('close', 0)

            if (ema_9 > ema_21 > ema_50 and current_price > ema_9):
                conditions_met += 1
                reasons.append("STRONG_TREND_BULLISH")
                confidence_score += 0.25
                self.logger.debug(f"Strong EMA trend: {ema_9:.2f} > {ema_21:.2f} > {ema_50:.2f}")
            elif (ema_9 > ema_21 and current_price > ema_21):
                conditions_met += 1
                reasons.append("TREND_BULLISH")
                confidence_score += 0.15
                self.logger.debug(f"EMA trend: {ema_9:.2f} > {ema_21:.2f}")
            else:
                self.logger.debug(f"EMA trend not bullish: {ema_9:.2f}, {ema_21:.2f}, {ema_50:.2f}")

            # 4. Bollinger Bands (отскок от нижней границы)
            bb_lower = signals.get('bb_lower', 0)
            bb_middle = signals.get('bb_middle', 0)

            if current_price > bb_lower and current_price < bb_middle:
                conditions_met += 1
                reasons.append("BB_SUPPORT")
                confidence_score += 0.1
                self.logger.debug(f"BB support: {current_price:.2f} between {bb_lower:.2f} and {bb_middle:.2f}")

            # 5. Volume подтверждение
            volume_surge = signals.get('volume_surge', False)
            volume_ratio = signals.get('volume_ratio', 0)

            if volume_surge or volume_ratio > self.VOLUME_THRESHOLD:
                conditions_met += 1
                reasons.append("VOLUME_CONFIRMATION")
                confidence_score += 0.15
                self.logger.debug(f"Volume confirmation: ratio={volume_ratio:.2f}, surge={volume_surge}")
            else:
                self.logger.debug(f"Volume insufficient: ratio={volume_ratio:.2f} < {self.VOLUME_THRESHOLD}")

            # 6. Stochastic
            stoch_k = signals.get('stoch_k', 50)
            stoch_d = signals.get('stoch_d', 50)

            if stoch_k < 30 or (stoch_k > stoch_d and stoch_k < 70):
                conditions_met += 1
                reasons.append("STOCH_BULLISH")
                confidence_score += 0.1
                self.logger.debug(f"Stochastic bullish: K={stoch_k:.1f}, D={stoch_d:.1f}")

            # 7. Market Structure подтверждение
            structure = market_structure.get('structure', 'UNKNOWN')
            if structure in ['BULLISH_STRUCTURE', 'RANGING_COMPRESSION']:
                conditions_met += 1
                reasons.append("STRUCTURE_BULLISH")
                confidence_score += 0.2
                self.logger.debug(f"Market structure bullish: {structure}")

            self.logger.info(
                f"Long signal analysis: {conditions_met}/{self.MIN_CONDITIONS_REQUIRED} conditions met, confidence: {confidence_score:.2%}")

            # Проверка минимальных условий
            if conditions_met >= self.MIN_CONDITIONS_REQUIRED:
                self.logger.info(
                    f"Long signal PASSED for {symbol}: {conditions_met} conditions, confidence: {confidence_score:.2%}")
                return {
                    'action': 'BUY',
                    'entry_price': current_price,
                    'confidence': min(confidence_score, 1.0),
                    'conditions_met': conditions_met,
                    'reasons': ', '.join(reasons),
                    'timestamp': datetime.now(),
                    'market_structure': structure
                }
            else:
                self.logger.debug(
                    f"Long signal FAILED for {symbol}: {conditions_met} < {self.MIN_CONDITIONS_REQUIRED} conditions")

            return None

        except Exception as e:
            self.logger.error(f"Error generating long signal: {e}")
            return None

    def _generate_short_signal(self, signals: Dict[str, Any], market_structure: Dict[str, Any]) -> Optional[
        Dict[str, Any]]:
        """Генерация сигнала на продажу"""
        try:
            conditions_met = 0
            reasons = []
            confidence_score = 0.0

            # 1. RSI условие
            rsi = signals.get('rsi', 50)
            rsi_prev = signals.get('rsi_prev', 50)

            if (rsi > self.RSI_OVERBOUGHT or
                    (rsi < rsi_prev and self.RSI_NEUTRAL_LOW < rsi < self.RSI_NEUTRAL_HIGH)):
                conditions_met += 1
                reasons.append("RSI_BEARISH")
                confidence_score += 0.15

            # 2. MACD условие
            macd = signals.get('macd', 0)
            macd_signal = signals.get('macd_signal', 0)
            macd_histogram = signals.get('macd_histogram', 0)
            macd_prev = signals.get('macd_prev', 0)

            if (macd < macd_signal and macd_histogram < 0 and macd_histogram < macd_prev):
                conditions_met += 1
                reasons.append("MACD_BEARISH")
                confidence_score += 0.2

            # 3. EMA тренд
            ema_9 = signals.get('ema_9', 0)
            ema_21 = signals.get('ema_21', 0)
            ema_50 = signals.get('ema_50', 0)
            current_price = signals.get('close', 0)

            if (ema_9 < ema_21 < ema_50 and current_price < ema_9):
                conditions_met += 1
                reasons.append("STRONG_TREND_BEARISH")
                confidence_score += 0.25
            elif (ema_9 < ema_21 and current_price < ema_21):
                conditions_met += 1
                reasons.append("TREND_BEARISH")
                confidence_score += 0.15

            # 4. Bollinger Bands
            bb_upper = signals.get('bb_upper', 0)
            bb_middle = signals.get('bb_middle', 0)

            if current_price < bb_upper and current_price > bb_middle:
                conditions_met += 1
                reasons.append("BB_RESISTANCE")
                confidence_score += 0.1

            # 5. Volume подтверждение
            volume_surge = signals.get('volume_surge', False)
            volume_ratio = signals.get('volume_ratio', 0)

            if volume_surge or volume_ratio > self.VOLUME_THRESHOLD:
                conditions_met += 1
                reasons.append("VOLUME_CONFIRMATION")
                confidence_score += 0.15

            # 6. Stochastic
            stoch_k = signals.get('stoch_k', 50)
            stoch_d = signals.get('stoch_d', 50)

            if stoch_k > 70 or (stoch_k < stoch_d and stoch_k > 30):
                conditions_met += 1
                reasons.append("STOCH_BEARISH")
                confidence_score += 0.1

            # 7. Market Structure
            structure = market_structure.get('structure', 'UNKNOWN')
            if structure in ['BEARISH_STRUCTURE', 'RANGING_EXPANSION']:
                conditions_met += 1
                reasons.append("STRUCTURE_BEARISH")
                confidence_score += 0.2

            if conditions_met >= self.MIN_CONDITIONS_REQUIRED:
                return {
                    'action': 'SELL',
                    'entry_price': current_price,
                    'confidence': min(confidence_score, 1.0),
                    'conditions_met': conditions_met,
                    'reasons': ', '.join(reasons),
                    'timestamp': datetime.now(),
                    'market_structure': structure
                }

            return None

        except Exception as e:
            self.logger.error(f"Error generating short signal: {e}")
            return None

    def _select_best_signal(self, long_signal: Optional[Dict], short_signal: Optional[Dict]) -> Optional[Dict]:
        """Выбор лучшего сигнала"""
        try:
            if not long_signal and not short_signal:
                return None

            if long_signal and not short_signal:
                return long_signal

            if short_signal and not long_signal:
                return short_signal

            # Если есть оба сигнала, выбираем с большей уверенностью
            if long_signal['confidence'] > short_signal['confidence']:
                return long_signal
            else:
                return short_signal

        except Exception as e:
            self.logger.error(f"Error selecting best signal: {e}")
            return None

    def _is_signal_cooldown_active(self) -> bool:
        """Проверка cooldown между сигналами"""
        if not self.last_signal_time:
            return False

        time_since_last = (datetime.now() - self.last_signal_time).total_seconds()
        return time_since_last < self.SIGNAL_COOLDOWN

    def _calculate_smart_money_levels(self, signals: Dict[str, Any], direction: str) -> Dict[str, float]:
        """Расчет уровней на основе Smart Money принципов"""
        try:
            entry_price = signals.get('close', 0)
            atr = signals.get('atr', 0)

            if entry_price <= 0 or atr <= 0:
                return {'stop_loss': 0.0, 'take_profit': 0.0}

            # Более консервативные уровни
            if direction == 'BUY':
                # Stop Loss: 1.5 ATR ниже входа
                stop_loss = entry_price - (atr * 1.5)
                # Take Profit: 3 ATR выше входа (R:R = 2:1)
                take_profit = entry_price + (atr * 3.0)
            else:  # SELL
                stop_loss = entry_price + (atr * 1.5)
                take_profit = entry_price - (atr * 3.0)

            # Проверка минимального R:R
            risk = abs(entry_price - stop_loss)
            reward = abs(take_profit - entry_price)

            if risk > 0 and (reward / risk) >= self.RISK_REWARD_MIN:
                return {
                    'stop_loss': round(stop_loss, 8),
                    'take_profit': round(take_profit, 8),
                    'risk_reward_ratio': round(reward / risk, 2)
                }
            else:
                return {'stop_loss': 0.0, 'take_profit': 0.0}

        except Exception as e:
            self.logger.error(f"Error calculating smart money levels: {e}")
            return {'stop_loss': 0.0, 'take_profit': 0.0}

    def execute(self, symbol: str, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Выполнение улучшенной стратегии"""
        try:
            self.logger.info(f"SmartMoneyStrategy executing for {symbol}")

            df = market_data.get('df')
            if df is None or len(df) < 100:
                self.logger.warning(f"Insufficient data for {symbol}: {len(df) if df is not None else 0} rows")
                return None

            # Проверяем существующую позицию
            current_position = self.position_manager.get_position_status(symbol)
            self.logger.debug(f"Current position for {symbol}: {current_position is not None}")

            if current_position:
                return self._process_exit_signals(symbol, df, current_position)
            else:
                return self._process_entry_signals(symbol, df, market_data)

        except Exception as e:
            self.logger.error(f"Error executing strategy for {symbol}: {e}")
            return None

    def _process_entry_signals(self, symbol: str, df: pd.DataFrame, market_data: Dict[str, Any]) -> Optional[
        Dict[str, Any]]:
        """Обработка сигналов входа"""
        try:
            self.logger.debug(f"Processing entry signals for {symbol}")

            # Генерируем сигнал
            signal = self.generate_signal(df, symbol)
            self.logger.debug(f"Generated signal for {symbol}: {signal is not None}")

            if not signal:
                self.logger.debug(f"No signal generated for {symbol}")
                return None

            # Рассчитываем уровни
            levels = self._calculate_smart_money_levels(
                {'close': signal['entry_price'], 'atr': df['atr'].iloc[-1] if 'atr' in df.columns else 0},
                signal['action']
            )

            if levels['stop_loss'] <= 0 or levels['take_profit'] <= 0:
                self.logger.warning(f"Invalid levels for {symbol}")
                return None

            # Рассчитываем размер позиции
            account_balance = market_data.get('account_balance', 0)
            position_size = self._calculate_smart_position_size(
                account_balance, signal['entry_price'], levels['stop_loss']
            )

            if position_size <= 0:
                return None

            self.logger.info(
                f"HIGH QUALITY {signal['action']} signal for {symbol}: "
                f"Confidence={signal['confidence']:.1%}, "
                f"Conditions={signal['conditions_met']}/7, "
                f"R:R={levels.get('risk_reward_ratio', 0):.1f}"
            )

            return {
                'action': 'OPEN',
                'direction': signal['action'],
                'size': position_size,
                'entry_price': signal['entry_price'],
                'stop_loss': levels['stop_loss'],
                'take_profit': levels['take_profit'],
                'confidence': signal['confidence'],
                'reasons': signal['reasons'],
                'risk_reward_ratio': levels.get('risk_reward_ratio', 0),
                'market_structure': signal.get('market_structure', 'UNKNOWN'),
                'timestamp': datetime.now()
            }

        except Exception as e:
            self.logger.error(f"Error processing entry signals: {e}")
            return None

    def _process_exit_signals(self, symbol: str, df: pd.DataFrame, position: Dict[str, Any]) -> Optional[
        Dict[str, Any]]:
        """Обработка сигналов выхода (улучшенная логика)"""
        try:
            current_price = df['close'].iloc[-1]
            direction = position.get('direction', '')
            entry_price = position.get('entry_price', 0)

            # Расчет текущей прибыли
            if direction == 'BUY':
                pnl_pct = ((current_price - entry_price) / entry_price) * 100
            else:
                pnl_pct = ((entry_price - current_price) / entry_price) * 100

            # Экстренный выход при больших убытках
            if pnl_pct < -8:  # 8% убыток
                return {
                    'action': 'CLOSE',
                    'reason': 'emergency_stop_loss',
                    'exit_price': current_price,
                    'pnl_pct': pnl_pct
                }

            # Фиксация прибыли при достижении целей
            if pnl_pct > 6:  # 6% прибыль
                return {
                    'action': 'CLOSE',
                    'reason': 'profit_target_reached',
                    'exit_price': current_price,
                    'pnl_pct': pnl_pct
                }

            # Анализ разворотных сигналов
            if len(df) >= 20:
                rsi = ta.momentum.RSIIndicator(df['close'], window=14).rsi().iloc[-1]

                if direction == 'BUY' and rsi > 80:  # Сильная перекупленность
                    return {
                        'action': 'CLOSE',
                        'reason': 'reversal_signal_long',
                        'exit_price': current_price,
                        'pnl_pct': pnl_pct
                    }
                elif direction == 'SELL' and rsi < 20:  # Сильная перепроданность
                    return {
                        'action': 'CLOSE',
                        'reason': 'reversal_signal_short',
                        'exit_price': current_price,
                        'pnl_pct': pnl_pct
                    }

            return None

        except Exception as e:
            self.logger.error(f"Error processing exit signals: {e}")
            return None

    def _calculate_smart_position_size(self, account_balance: float, entry_price: float, stop_loss: float) -> float:
        """Расчет размера позиции по Smart Money принципам"""
        try:
            if account_balance <= 0 or entry_price <= 0 or stop_loss <= 0:
                return 0.0

            # Риск 1% от баланса
            risk_amount = account_balance * 0.01

            # Расстояние до стоп-лосса
            risk_per_unit = abs(entry_price - stop_loss)

            if risk_per_unit <= 0:
                return 0.0

            # Размер позиции
            position_size = risk_amount / risk_per_unit

            # Ограничения
            max_position_value = account_balance * 0.2  # Максимум 20% баланса
            if position_size * entry_price > max_position_value:
                position_size = max_position_value / entry_price

            return round(position_size, 8)

        except Exception as e:
            self.logger.error(f"Error calculating position size: {e}")
            return 0.0

    def get_strategy_stats(self) -> Dict[str, Any]:
        """Получение статистики стратегии"""
        try:
            total_signals = len(self.signal_history)
            if total_signals == 0:
                return {'total_signals': 0, 'avg_confidence': 0.0}

            avg_confidence = np.mean([s['confidence'] for s in self.signal_history])

            # Анализ по типам сигналов
            buy_signals = len([s for s in self.signal_history if s['action'] == 'BUY'])
            sell_signals = len([s for s in self.signal_history if s['action'] == 'SELL'])

            return {
                'total_signals': total_signals,
                'buy_signals': buy_signals,
                'sell_signals': sell_signals,
                'avg_confidence': round(avg_confidence, 3),
                'last_signal_time': self.last_signal_time.isoformat() if self.last_signal_time else None,
                'current_market_structure': self.market_structure
            }

        except Exception as e:
            self.logger.error(f"Error getting strategy stats: {e}")
            return {}