import logging
import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime
import ta
from strategies.base_strategy import BaseStrategy


class CustomStrategy(BaseStrategy):
    """
    Настраиваемая пользователем торговая стратегия

    Эта стратегия полностью настраивается через user_config.py
    Пользователь может изменять все параметры индикаторов,
    стоп-лоссы, тейк-профиты и условия входа/выхода
    """

    def __init__(self, market_analyzer, position_manager, user_config):
        """Инициализация пользовательской стратегии"""
        super().__init__(name="CustomStrategy")
        self.market_analyzer = market_analyzer
        self.position_manager = position_manager
        self.user_config = user_config

        # Загружаем настройки из пользовательской конфигурации
        self.config = user_config.get('CUSTOM_STRATEGY_CONFIG', {})

        # Параметры RSI
        rsi_settings = self.config.get('rsi_settings', {})
        self.RSI_PERIOD = rsi_settings.get('period', 14)
        self.RSI_OVERSOLD_LOWER = rsi_settings.get('oversold_lower', 25)
        self.RSI_OVERSOLD_UPPER = rsi_settings.get('oversold_upper', 45)
        self.RSI_OVERBOUGHT_LOWER = rsi_settings.get('overbought_lower', 55)
        self.RSI_OVERBOUGHT_UPPER = rsi_settings.get('overbought_upper', 75)
        self.RSI_ENABLED = rsi_settings.get('enabled', True)
        self.RSI_WEIGHT = rsi_settings.get('weight', 1.0)

        # Параметры MACD
        macd_settings = self.config.get('macd_settings', {})
        self.MACD_FAST = macd_settings.get('fast_period', 12)
        self.MACD_SLOW = macd_settings.get('slow_period', 26)
        self.MACD_SIGNAL = macd_settings.get('signal_period', 9)
        self.MACD_THRESHOLD = macd_settings.get('histogram_threshold', 0.0002)
        self.MACD_ENABLED = macd_settings.get('enabled', True)
        self.MACD_WEIGHT = macd_settings.get('weight', 1.0)

        # Параметры EMA
        ema_settings = self.config.get('ema_settings', {})
        self.EMA_FAST = ema_settings.get('fast_period', 9)
        self.EMA_SLOW = ema_settings.get('slow_period', 21)
        self.EMA_TREND = ema_settings.get('trend_period', 50)
        self.EMA_ENABLED = ema_settings.get('enabled', True)
        self.EMA_WEIGHT = ema_settings.get('weight', 1.0)

        # Параметры Bollinger Bands
        bb_settings = self.config.get('bollinger_settings', {})
        self.BB_PERIOD = bb_settings.get('period', 20)
        self.BB_STD = bb_settings.get('std_deviation', 2.0)
        self.BB_ENABLED = bb_settings.get('enabled', True)
        self.BB_WEIGHT = bb_settings.get('weight', 0.8)

        # Параметры объема
        volume_settings = self.config.get('volume_settings', {})
        self.VOLUME_SMA_PERIOD = volume_settings.get('sma_period', 20)
        self.MIN_VOLUME_RATIO = volume_settings.get('min_ratio', 0.8)
        self.VOLUME_SURGE_THRESHOLD = volume_settings.get('surge_threshold', 2.5)
        self.VOLUME_ENABLED = volume_settings.get('enabled', True)
        self.VOLUME_WEIGHT = volume_settings.get('weight', 0.7)

        # Параметры Stochastic
        stoch_settings = self.config.get('stochastic_settings', {})
        self.STOCH_K_PERIOD = stoch_settings.get('k_period', 14)
        self.STOCH_D_PERIOD = stoch_settings.get('d_period', 3)
        self.STOCH_SMOOTH_K = stoch_settings.get('smooth_k', 3)
        self.STOCH_OVERSOLD = stoch_settings.get('oversold', 25)
        self.STOCH_OVERBOUGHT = stoch_settings.get('overbought', 75)
        self.STOCH_ENABLED = stoch_settings.get('enabled', True)
        self.STOCH_WEIGHT = stoch_settings.get('weight', 0.8)

        # Параметры ATR
        atr_settings = self.config.get('atr_settings', {})
        self.ATR_PERIOD = atr_settings.get('period', 14)
        self.ATR_SL_MULTIPLIER = atr_settings.get('stop_loss_multiplier', 2.0)
        self.ATR_TP_MULTIPLIER = atr_settings.get('take_profit_multiplier', 2.5)
        self.ATR_TRAILING_MULTIPLIER = atr_settings.get('trailing_multiplier', 1.5)
        self.ATR_ENABLED = atr_settings.get('enabled', True)

        # Условия входа
        entry_conditions = self.config.get('entry_conditions', {})
        self.MIN_CONDITIONS_REQUIRED = entry_conditions.get('min_conditions_required', 2)
        self.TREND_STRENGTH_THRESHOLD = entry_conditions.get('trend_strength_threshold', 0.3)
        self.VOLUME_CONFIRMATION = entry_conditions.get('volume_confirmation', True)
        self.SIGNAL_COOLDOWN = entry_conditions.get('signal_cooldown', 1800)

        # Условия выхода
        exit_conditions = self.config.get('exit_conditions', {})
        self.USE_TRAILING_STOP = exit_conditions.get('use_trailing_stop', True)
        self.EMERGENCY_RSI_LONG = exit_conditions.get('emergency_rsi_long', 80)
        self.EMERGENCY_RSI_SHORT = exit_conditions.get('emergency_rsi_short', 20)
        self.PROFIT_EXIT_RSI_LONG = exit_conditions.get('profit_exit_rsi_long', 65)
        self.PROFIT_EXIT_RSI_SHORT = exit_conditions.get('profit_exit_rsi_short', 35)

        # Управление рисками
        risk_mgmt = self.config.get('risk_management', {})
        self.RISK_PER_TRADE = risk_mgmt.get('risk_per_trade', 0.005)
        self.MAX_STOP_LOSS_PERCENT = risk_mgmt.get('max_stop_loss_pct', 0.03)
        self.MIN_TAKE_PROFIT_PERCENT = risk_mgmt.get('min_take_profit_pct', 0.06)
        self.MAX_TAKE_PROFIT_PERCENT = risk_mgmt.get('max_take_profit_pct', 0.10)
        self.LEVERAGE = risk_mgmt.get('leverage', 5)
        self.MAX_POSITION_VALUE_PCT = risk_mgmt.get('max_position_value_pct', 0.05)

        # Статистика
        self.last_signal_time = None

        self.logger.info(f"CustomStrategy initialized with user configuration")
        self.logger.info(f"Enabled indicators: RSI={self.RSI_ENABLED}, MACD={self.MACD_ENABLED}, "
                         f"EMA={self.EMA_ENABLED}, BB={self.BB_ENABLED}, Volume={self.VOLUME_ENABLED}, "
                         f"Stoch={self.STOCH_ENABLED}, ATR={self.ATR_ENABLED}")

    def generate_signal(self, data: pd.DataFrame, symbol: str = None) -> Optional[Dict[str, Any]]:
        """Генерация торгового сигнала на основе пользовательских настроек"""
        try:
            signals = self.generate_signals(data)
            if not signals:
                return None

            # Проверяем cooldown
            if self._is_signal_cooldown_active():
                return None

            # Проверяем условия для лонга
            long_valid, long_score, long_reasons = self._check_long_entry_conditions(signals)
            if long_valid:
                return {
                    'action': 'BUY',
                    'entry_price': signals.get('close'),
                    'timestamp': datetime.now(),
                    'confidence': long_score / self._get_max_conditions(),
                    'reasons': long_reasons
                }

            # Проверяем условия для шорта
            short_valid, short_score, short_reasons = self._check_short_entry_conditions(signals)
            if short_valid:
                return {
                    'action': 'SELL',
                    'entry_price': signals.get('close'),
                    'timestamp': datetime.now(),
                    'confidence': short_score / self._get_max_conditions(),
                    'reasons': short_reasons
                }

            return None

        except Exception as e:
            self.logger.error(f"Error generating signal: {e}")
            return None

    def execute(self, symbol: str, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Выполнение пользовательской стратегии"""
        try:
            self.logger.info(f"Executing custom strategy for {symbol}")

            df = market_data.get('df')
            if df is None or len(df) < 50:
                self.logger.warning(f"Insufficient data for {symbol}. Length: {len(df) if df is not None else 0}")
                return None

            # Проверяем наличие position_manager
            if self.position_manager is None:
                self.logger.warning(f"Position manager is None for {symbol}, treating as no position")
                current_position = None
            else:
                current_position = self.position_manager.get_position_status(symbol)

            self.logger.debug(f"Current position for {symbol}: {current_position is not None}")

            signals = self.generate_signals(df)
            if not signals:
                self.logger.warning(f"No signals generated for {symbol} - failed to calculate indicators")
                return None

            # Детальное логирование сигналов
            self.logger.info(f"Generated signals for {symbol}:")
            self.logger.info(f"  RSI: {signals.get('rsi', 0):.1f}")
            self.logger.info(f"  Volume Ratio: {signals.get('volume_ratio', 0):.2f}")
            self.logger.info(f"  MACD: {signals.get('macd', 0):.6f}")
            self.logger.info(f"  MACD Signal: {signals.get('macd_signal', 0):.6f}")
            self.logger.info(f"  EMA Fast: {signals.get('ema_fast', 0):.2f}")
            self.logger.info(f"  EMA Slow: {signals.get('ema_slow', 0):.2f}")
            self.logger.info(f"  Current Price: ${signals.get('close', 0):.4f}")

            if current_position:
                self.logger.info(f"Existing position found for {symbol}, checking exit conditions")
                return self.process_exit_signals(symbol, signals, current_position, df)
            else:
                self.logger.info(f"No existing position for {symbol}, checking entry conditions")
                return self.process_entry_signals(symbol, signals, market_data)

        except Exception as e:
            self.logger.error(f"Error executing custom strategy for {symbol}: {e}", exc_info=True)
            return None

    def generate_signals(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Генерация сигналов на основе пользовательских настроек"""
        try:
            self.logger.debug(f"Generating signals for DataFrame with {len(df)} rows")

            required_cols = ['open', 'high', 'low', 'close', 'volume']
            if not all(col in df.columns for col in required_cols):
                self.logger.error(f"Missing required columns in DataFrame")
                return {}

            df_copy = df.copy()

            self.logger.debug("Calculating technical indicators...")
            signals = {}

            # RSI
            if self.RSI_ENABLED:
                self.logger.debug(f"Calculating RSI with period {self.RSI_PERIOD}")
                df_copy['rsi'] = ta.momentum.RSIIndicator(df_copy['close'], window=self.RSI_PERIOD).rsi()
                signals['rsi'] = df_copy['rsi'].iloc[-1]
                signals['rsi_prev'] = df_copy['rsi'].iloc[-2] if len(df_copy) > 1 else 50

            # MACD
            if self.MACD_ENABLED:
                self.logger.debug(f"Calculating MACD with periods {self.MACD_FAST}/{self.MACD_SLOW}/{self.MACD_SIGNAL}")
                macd_indicator = ta.trend.MACD(df_copy['close'],
                                               window_fast=self.MACD_FAST,
                                               window_slow=self.MACD_SLOW,
                                               window_sign=self.MACD_SIGNAL)
                df_copy['macd'] = macd_indicator.macd()
                df_copy['macd_signal'] = macd_indicator.macd_signal()
                df_copy['macd_histogram'] = macd_indicator.macd_diff()

                signals['macd'] = df_copy['macd'].iloc[-1]
                signals['macd_signal'] = df_copy['macd_signal'].iloc[-1]
                signals['macd_histogram'] = df_copy['macd_histogram'].iloc[-1]

            # EMA
            if self.EMA_ENABLED:
                self.logger.debug(f"Calculating EMA with periods {self.EMA_FAST}/{self.EMA_SLOW}/{self.EMA_TREND}")
                df_copy['ema_fast'] = ta.trend.EMAIndicator(df_copy['close'], window=self.EMA_FAST).ema_indicator()
                df_copy['ema_slow'] = ta.trend.EMAIndicator(df_copy['close'], window=self.EMA_SLOW).ema_indicator()
                df_copy['ema_trend'] = ta.trend.EMAIndicator(df_copy['close'], window=self.EMA_TREND).ema_indicator()

                signals['ema_fast'] = df_copy['ema_fast'].iloc[-1]
                signals['ema_slow'] = df_copy['ema_slow'].iloc[-1]
                signals['ema_trend'] = df_copy['ema_trend'].iloc[-1]

            # Bollinger Bands
            if self.BB_ENABLED:
                bollinger = ta.volatility.BollingerBands(df_copy['close'],
                                                         window=self.BB_PERIOD,
                                                         window_dev=self.BB_STD)
                df_copy['bb_upper'] = bollinger.bollinger_hband()
                df_copy['bb_lower'] = bollinger.bollinger_lband()
                df_copy['bb_middle'] = bollinger.bollinger_mavg()

                signals['bb_upper'] = df_copy['bb_upper'].iloc[-1]
                signals['bb_lower'] = df_copy['bb_lower'].iloc[-1]
                signals['bb_middle'] = df_copy['bb_middle'].iloc[-1]

            # Volume
            if self.VOLUME_ENABLED:
                self.logger.debug(f"Calculating Volume with SMA period {self.VOLUME_SMA_PERIOD}")
                df_copy['volume_sma'] = df_copy['volume'].rolling(window=self.VOLUME_SMA_PERIOD).mean()
                df_copy['volume_ratio'] = df_copy['volume'] / df_copy['volume_sma']

                signals['volume_ratio'] = df_copy['volume_ratio'].iloc[-1]

            # Stochastic
            if self.STOCH_ENABLED:
                stoch = ta.momentum.StochasticOscillator(df_copy['high'], df_copy['low'], df_copy['close'],
                                                         window=self.STOCH_K_PERIOD,
                                                         smooth_window=self.STOCH_SMOOTH_K)
                df_copy['stoch_k'] = stoch.stoch()
                df_copy['stoch_d'] = stoch.stoch_signal()

                signals['stoch_k'] = df_copy['stoch_k'].iloc[-1]
                signals['stoch_d'] = df_copy['stoch_d'].iloc[-1]

            # ATR
            if self.ATR_ENABLED:
                df_copy['atr'] = ta.volatility.AverageTrueRange(
                    high=df_copy['high'],
                    low=df_copy['low'],
                    close=df_copy['close'],
                    window=self.ATR_PERIOD
                ).average_true_range()

                signals['atr'] = df_copy['atr'].iloc[-1]

            # Базовые данные
            signals['close'] = df_copy['close'].iloc[-1]
            signals['close_prev'] = df_copy['close'].iloc[-2] if len(df_copy) > 1 else signals['close']
            signals['high'] = df_copy['high'].iloc[-1]
            signals['low'] = df_copy['low'].iloc[-1]

            # Фильтруем NaN значения
            signals = {k: v for k, v in signals.items() if pd.notna(v)}

            self.logger.debug(f"Generated {len(signals)} valid signals")
            self.logger.debug(
                f"Key signals: RSI={signals.get('rsi', 0):.1f}, Volume={signals.get('volume_ratio', 0):.2f}")

            return signals

        except Exception as e:
            self.logger.error(f"Error generating custom signals: {e}", exc_info=True)
            return {}

    def _get_max_conditions(self) -> int:
        """Получить максимальное количество условий на основе включенных индикаторов"""
        max_conditions = 0
        if self.RSI_ENABLED: max_conditions += 1
        if self.MACD_ENABLED: max_conditions += 1
        if self.EMA_ENABLED: max_conditions += 1
        if self.BB_ENABLED: max_conditions += 1
        if self.VOLUME_ENABLED: max_conditions += 1
        if self.STOCH_ENABLED: max_conditions += 1
        return max(max_conditions, 1)

    def _check_long_entry_conditions(self, signals: Dict[str, Any]) -> tuple[bool, int, str]:
        """Проверка условий для входа в длинную позицию"""
        try:
            conditions_met = 0
            reasons = []

            self.logger.debug(f"Checking long entry conditions with {len(signals)} signals")

            # 1. RSI условие
            if self.RSI_ENABLED and 'rsi' in signals:
                rsi = signals['rsi']
                rsi_prev = signals.get('rsi_prev', 50)

                rsi_bullish = (
                        rsi < self.RSI_OVERSOLD_UPPER or
                        (rsi > rsi_prev and rsi < 50)
                )
                self.logger.debug(f"RSI check: {rsi:.1f} (prev={rsi_prev:.1f}) -> {'✅' if rsi_bullish else '❌'}")
                if rsi_bullish:
                    conditions_met += self.RSI_WEIGHT
                    reasons.append("RSI_BULLISH")
                else:
                    self.logger.debug(f"RSI condition failed: {rsi:.1f} not < {self.RSI_OVERSOLD_UPPER} and not rising")

            # 2. MACD условие
            if self.MACD_ENABLED and all(k in signals for k in ['macd', 'macd_signal', 'macd_histogram']):
                macd_bullish = (
                        signals['macd'] > signals['macd_signal'] or
                        signals['macd_histogram'] > self.MACD_THRESHOLD
                )
                self.logger.debug(
                    f"MACD check: {signals['macd']:.6f} vs {signals['macd_signal']:.6f} -> {'✅' if macd_bullish else '❌'}")
                if macd_bullish:
                    conditions_met += self.MACD_WEIGHT
                    reasons.append("MACD_BULLISH")
                else:
                    self.logger.debug(
                        f"MACD condition failed: {signals['macd']:.6f} not > {signals['macd_signal']:.6f}")

            # 3. EMA тренд
            if self.EMA_ENABLED and all(k in signals for k in ['ema_fast', 'ema_slow', 'ema_trend', 'close']):
                ema_bullish = (
                        signals['ema_fast'] > signals['ema_slow'] or
                        signals['close'] > signals['ema_trend']
                )
                self.logger.debug(
                    f"EMA check: fast={signals['ema_fast']:.2f} vs slow={signals['ema_slow']:.2f} -> {'✅' if ema_bullish else '❌'}")
                if ema_bullish:
                    conditions_met += self.EMA_WEIGHT
                    reasons.append("EMA_BULLISH")
                else:
                    self.logger.debug(f"EMA condition failed: fast not > slow and price not > trend")

            # 4. Bollinger Bands
            if self.BB_ENABLED and all(k in signals for k in ['bb_lower', 'bb_middle', 'close', 'close_prev']):
                bb_bullish = (
                        signals['close'] > signals['bb_lower'] and signals['close_prev'] <= signals['bb_lower'] or
                        signals['close'] > signals['bb_middle']
                )
                if bb_bullish:
                    conditions_met += self.BB_WEIGHT
                    reasons.append("BB_BULLISH")
                else:
                    self.logger.debug(f"BB condition failed: no bounce or above middle")

            # 5. Объем
            if self.VOLUME_ENABLED and 'volume_ratio' in signals:
                volume_ok = signals['volume_ratio'] > self.MIN_VOLUME_RATIO
                self.logger.debug(
                    f"Volume check: {signals['volume_ratio']:.2f} vs {self.MIN_VOLUME_RATIO} -> {'✅' if volume_ok else '❌'}")
                if volume_ok:
                    conditions_met += self.VOLUME_WEIGHT
                    reasons.append("VOLUME_OK")
                else:
                    self.logger.debug(
                        f"Volume condition failed: {signals['volume_ratio']:.2f} not > {self.MIN_VOLUME_RATIO}")

            # 6. Stochastic
            if self.STOCH_ENABLED and all(k in signals for k in ['stoch_k', 'stoch_d']):
                stoch_bullish = (
                        signals['stoch_k'] < self.STOCH_OVERSOLD or
                        (signals['stoch_k'] > signals['stoch_d'] and signals['stoch_k'] < 70)
                )
                self.logger.debug(
                    f"Stoch check: K={signals['stoch_k']:.1f}, D={signals['stoch_d']:.1f} -> {'✅' if stoch_bullish else '❌'}")
                if stoch_bullish:
                    conditions_met += self.STOCH_WEIGHT
                    reasons.append("STOCH_BULLISH")
                else:
                    self.logger.debug(f"Stoch condition failed: not oversold and no bullish cross")

            is_valid = conditions_met >= self.MIN_CONDITIONS_REQUIRED
            reason_str = ", ".join(reasons) if reasons else "NONE"

            self.logger.info(f"LONG ANALYSIS: {conditions_met:.1f}/{self.MIN_CONDITIONS_REQUIRED} conditions met. "
                             f"Valid: {'✅ YES' if is_valid else '❌ NO'}. Reasons: {reason_str}")

            return is_valid, int(conditions_met), reason_str

        except Exception as e:
            self.logger.error(f"Error checking long conditions: {e}")
            return False, 0, "ERROR"

    def _check_short_entry_conditions(self, signals: Dict[str, Any]) -> tuple[bool, int, str]:
        """Проверка условий для входа в короткую позицию"""
        try:
            conditions_met = 0
            reasons = []

            self.logger.debug(f"Checking short entry conditions with {len(signals)} signals")

            # 1. RSI условие
            if self.RSI_ENABLED and 'rsi' in signals:
                rsi = signals['rsi']
                rsi_prev = signals.get('rsi_prev', 50)

                rsi_bearish = (
                        rsi > self.RSI_OVERBOUGHT_LOWER or
                        (rsi < rsi_prev and rsi > 50)
                )
                self.logger.debug(f"RSI check: {rsi:.1f} (prev={rsi_prev:.1f}) -> {'✅' if rsi_bearish else '❌'}")
                if rsi_bearish:
                    conditions_met += self.RSI_WEIGHT
                    reasons.append("RSI_BEARISH")
                else:
                    self.logger.debug(
                        f"RSI condition failed: {rsi:.1f} not > {self.RSI_OVERBOUGHT_LOWER} and not falling")

            # 2. MACD условие
            if self.MACD_ENABLED and all(k in signals for k in ['macd', 'macd_signal', 'macd_histogram']):
                macd_bearish = (
                        signals['macd'] < signals['macd_signal'] or
                        signals['macd_histogram'] < -self.MACD_THRESHOLD
                )
                self.logger.debug(
                    f"MACD check: {signals['macd']:.6f} vs {signals['macd_signal']:.6f} -> {'✅' if macd_bearish else '❌'}")
                if macd_bearish:
                    conditions_met += self.MACD_WEIGHT
                    reasons.append("MACD_BEARISH")
                else:
                    self.logger.debug(
                        f"MACD condition failed: {signals['macd']:.6f} not < {signals['macd_signal']:.6f}")

            # 3. EMA тренд
            if self.EMA_ENABLED and all(k in signals for k in ['ema_fast', 'ema_slow', 'ema_trend', 'close']):
                ema_bearish = (
                        signals['ema_fast'] < signals['ema_slow'] or
                        signals['close'] < signals['ema_trend']
                )
                self.logger.debug(
                    f"EMA check: fast={signals['ema_fast']:.2f} vs slow={signals['ema_slow']:.2f} -> {'✅' if ema_bearish else '❌'}")
                if ema_bearish:
                    conditions_met += self.EMA_WEIGHT
                    reasons.append("EMA_BEARISH")
                else:
                    self.logger.debug(f"EMA condition failed: fast not < slow and price not < trend")

            # 4. Bollinger Bands
            if self.BB_ENABLED and all(k in signals for k in ['bb_upper', 'bb_middle', 'close', 'close_prev']):
                bb_bearish = (
                        signals['close'] < signals['bb_upper'] and signals['close_prev'] >= signals['bb_upper'] or
                        signals['close'] < signals['bb_middle']
                )
                if bb_bearish:
                    conditions_met += self.BB_WEIGHT
                    reasons.append("BB_BEARISH")
                else:
                    self.logger.debug(f"BB condition failed: no rejection or below middle")

            # 5. Объем
            if self.VOLUME_ENABLED and 'volume_ratio' in signals:
                volume_ok = signals['volume_ratio'] > self.MIN_VOLUME_RATIO
                self.logger.debug(
                    f"Volume check: {signals['volume_ratio']:.2f} vs {self.MIN_VOLUME_RATIO} -> {'✅' if volume_ok else '❌'}")
                if volume_ok:
                    conditions_met += self.VOLUME_WEIGHT
                    reasons.append("VOLUME_OK")
                else:
                    self.logger.debug(
                        f"Volume condition failed: {signals['volume_ratio']:.2f} not > {self.MIN_VOLUME_RATIO}")

            # 6. Stochastic
            if self.STOCH_ENABLED and all(k in signals for k in ['stoch_k', 'stoch_d']):
                stoch_bearish = (
                        signals['stoch_k'] > self.STOCH_OVERBOUGHT or
                        (signals['stoch_k'] < signals['stoch_d'] and signals['stoch_k'] > 30)
                )
                self.logger.debug(
                    f"Stoch check: K={signals['stoch_k']:.1f}, D={signals['stoch_d']:.1f} -> {'✅' if stoch_bearish else '❌'}")
                if stoch_bearish:
                    conditions_met += self.STOCH_WEIGHT
                    reasons.append("STOCH_BEARISH")
                else:
                    self.logger.debug(f"Stoch condition failed: not overbought and no bearish cross")

            is_valid = conditions_met >= self.MIN_CONDITIONS_REQUIRED
            reason_str = ", ".join(reasons) if reasons else "NONE"

            self.logger.info(f"SHORT ANALYSIS: {conditions_met:.1f}/{self.MIN_CONDITIONS_REQUIRED} conditions met. "
                             f"Valid: {'✅ YES' if is_valid else '❌ NO'}. Reasons: {reason_str}")

            return is_valid, int(conditions_met), reason_str

        except Exception as e:
            self.logger.error(f"Error checking short conditions: {e}")
            return False, 0, "ERROR"

    def _calculate_trade_parameters(self, entry_price: float, atr: float, direction: str) -> Dict[str, float]:
        """Расчет параметров сделки на основе пользовательских настроек"""
        try:
            if entry_price <= 0:
                self.logger.error(f"Неверная цена входа: {entry_price}")
                return {'stop_loss': 0.0, 'take_profit': 0.0}

            # Если ATR = 0, используем процентный метод
            if atr <= 0:
                self.logger.warning(f"ATR = 0, используем процентный метод")
                if direction == 'BUY':
                    return {
                        'stop_loss': entry_price * (1 - 0.03),  # 3% стоп-лосс
                        'take_profit': entry_price * (1 + 0.06)  # 6% тейк-профит
                    }
                else:  # SELL
                    return {
                        'stop_loss': entry_price * (1 + 0.03),  # 3% стоп-лосс
                        'take_profit': entry_price * (1 - 0.06)  # 6% тейк-профит
                    }

            # Расстояния на основе ATR
            atr_sl_distance = atr * self.ATR_SL_MULTIPLIER
            atr_tp_distance = atr * self.ATR_TP_MULTIPLIER

            if direction == 'BUY':
                calculated_stop_loss = entry_price - atr_sl_distance
                calculated_take_profit = entry_price + atr_tp_distance
            elif direction == 'SELL':
                calculated_stop_loss = entry_price + atr_sl_distance
                calculated_take_profit = entry_price - atr_tp_distance
            else:
                self.logger.error(f"Unknown direction: {direction}")
                return {'stop_loss': 0.0, 'take_profit': 0.0}

            # Ограничения для безопасности
            max_sl_distance = entry_price * self.MAX_STOP_LOSS_PERCENT
            min_tp_distance = entry_price * self.MIN_TAKE_PROFIT_PERCENT
            max_tp_distance = entry_price * self.MAX_TAKE_PROFIT_PERCENT

            if direction == 'BUY':
                calculated_stop_loss = max(calculated_stop_loss, entry_price - max_sl_distance)
                calculated_take_profit = max(entry_price + min_tp_distance,
                                             min(calculated_take_profit, entry_price + max_tp_distance))
            else:  # SELL
                calculated_stop_loss = min(calculated_stop_loss, entry_price + max_sl_distance)
                calculated_take_profit = min(entry_price - min_tp_distance,
                                             max(calculated_take_profit, entry_price - max_tp_distance))

            # Проверка R:R соотношения
            risk = abs(entry_price - calculated_stop_loss)
            reward = abs(calculated_take_profit - entry_price)

            if risk > 0:
                rr_ratio = reward / risk
                if rr_ratio < 1.5:  # Минимум 1.5:1
                    self.logger.warning(f"Плохое R:R соотношение: {rr_ratio:.2f}")
                    return {'stop_loss': 0.0, 'take_profit': 0.0}

            self.logger.info(f"📊 Параметры сделки {direction}:")
            self.logger.info(f"   💵 Вход: ${entry_price:.4f}")
            self.logger.info(
                f"   🛑 Стоп: ${calculated_stop_loss:.4f} ({abs(entry_price - calculated_stop_loss) / entry_price * 100:.1f}%)")
            self.logger.info(
                f"   🎯 Цель: ${calculated_take_profit:.4f} ({abs(calculated_take_profit - entry_price) / entry_price * 100:.1f}%)")
            self.logger.info(f"   📊 R:R: {reward / risk:.2f}:1")

            return {
                'stop_loss': round(calculated_stop_loss, 8),
                'take_profit': round(calculated_take_profit, 8)
            }

        except Exception as e:
            self.logger.error(f"Error calculating trade parameters: {e}")
            return {'stop_loss': 0.0, 'take_profit': 0.0}

    def process_entry_signals(self, symbol: str, signals: Dict[str, Any], market_data: Dict[str, Any]) -> Optional[
        Dict[str, Any]]:
        """Обработка сигналов для открытия новой позиции"""
        try:
            self.logger.info(f"Processing entry signals for {symbol}")

            current_price = signals.get('close')
            atr = signals.get('atr', 0)
            account_balance = market_data.get('account_balance')

            if not all([current_price, account_balance]):
                self.logger.warning(f"Отсутствуют данные для {symbol}: цена={current_price}, баланс={account_balance}")
                return None

            position_size = self.calculate_position_size(account_balance, current_price)
            if position_size <= 0:
                self.logger.warning(f"Invalid position size {position_size} for {symbol}")
                return None

            self.logger.info(f"🎯 ПОПЫТКА ОТКРЫТЬ ПОЗИЦИЮ для {symbol}:")
            self.logger.info(f"   💰 Баланс: ${account_balance:.2f}")
            self.logger.info(f"   📊 Размер позиции: {position_size}")
            self.logger.info(f"   💵 Цена входа: ${current_price:.4f}")

            # Проверяем условия для лонга
            long_valid, long_score, long_reasons = self._check_long_entry_conditions(signals)
            self.logger.info(f"Long entry check for {symbol}: valid={long_valid}, score={long_score}")

            if long_valid:
                self.logger.info(f"CUSTOM LONG signal for {symbol}: {long_score} conditions. Reasons: {long_reasons}")

                if atr > 0:
                    trade_params = self._calculate_trade_parameters(current_price, atr, 'BUY')
                else:
                    # Fallback если ATR недоступен
                    trade_params = {
                        'stop_loss': current_price * (1 - self.MAX_STOP_LOSS_PERCENT),
                        'take_profit': current_price * (1 + self.MIN_TAKE_PROFIT_PERCENT)
                    }

                if trade_params['stop_loss'] > 0 and trade_params['take_profit'] > 0:
                    return {
                        'action': 'OPEN',
                        'direction': 'BUY',
                        'size': position_size,
                        'entry_price': current_price,
                        'stop_loss': trade_params['stop_loss'],
                        'take_profit': trade_params['take_profit'],
                        'atr': atr,
                        'confidence': long_score / self._get_max_conditions(),
                        'reasons': long_reasons,
                        'timestamp': datetime.now()
                    }
                else:
                    self.logger.warning(f"Long signal for {symbol} failed: invalid trade parameters")

            # Проверяем условия для шорта
            short_valid, short_score, short_reasons = self._check_short_entry_conditions(signals)
            self.logger.info(f"Short entry check for {symbol}: valid={short_valid}, score={short_score}")

            if short_valid:
                self.logger.info(
                    f"CUSTOM SHORT signal for {symbol}: {short_score} conditions. Reasons: {short_reasons}")

                if atr > 0:
                    trade_params = self._calculate_trade_parameters(current_price, atr, 'SELL')
                else:
                    # Fallback если ATR недоступен
                    trade_params = {
                        'stop_loss': current_price * (1 + self.MAX_STOP_LOSS_PERCENT),
                        'take_profit': current_price * (1 - self.MIN_TAKE_PROFIT_PERCENT)
                    }

                if trade_params['stop_loss'] > 0 and trade_params['take_profit'] > 0:
                    return {
                        'action': 'OPEN',
                        'direction': 'SELL',
                        'size': position_size,
                        'entry_price': current_price,
                        'stop_loss': trade_params['stop_loss'],
                        'take_profit': trade_params['take_profit'],
                        'atr': atr,
                        'confidence': short_score / self._get_max_conditions(),
                        'reasons': short_reasons,
                        'timestamp': datetime.now()
                    }
                else:
                    self.logger.warning(f"Short signal for {symbol} failed: invalid trade parameters")

            self.logger.info(
                f"No valid entry signal for {symbol}: Long={long_valid}({long_score}), Short={short_valid}({short_score})")

            return None

        except Exception as e:
            self.logger.error(f"Error processing entry signals for {symbol}: {e}", exc_info=True)
            return None

    def process_exit_signals(self, symbol: str, signals: Dict[str, Any], position: Dict[str, Any], df: pd.DataFrame) -> \
    Optional[Dict[str, Any]]:
        """Обработка сигналов для закрытия позиции"""
        try:
            direction = position.get('direction')
            current_price = signals.get('close')

            if not current_price:
                return None

            # Проверяем RSI для экстренного выхода
            if self.RSI_ENABLED and 'rsi' in signals:
                rsi = signals['rsi']

                if direction == 'BUY':
                    # Экстренный выход из лонга
                    if rsi > self.EMERGENCY_RSI_LONG:
                        return {
                            'action': 'CLOSE',
                            'direction': 'SELL',
                            'size': position.get('size'),
                            'reason': 'emergency_rsi_exit',
                            'exit_price': current_price,
                            'timestamp': datetime.now()
                        }
                    # Обычный выход из прибыльного лонга
                    elif rsi > self.PROFIT_EXIT_RSI_LONG:
                        entry_price = position.get('entry_price', 0)
                        if entry_price > 0 and current_price > entry_price:  # Проверяем прибыльность
                            return {
                                'action': 'CLOSE',
                                'direction': 'SELL',
                                'size': position.get('size'),
                                'reason': 'profit_rsi_exit',
                                'exit_price': current_price,
                                'timestamp': datetime.now()
                            }

                elif direction == 'SELL':
                    # Экстренный выход из шорта
                    if rsi < self.EMERGENCY_RSI_SHORT:
                        return {
                            'action': 'CLOSE',
                            'direction': 'BUY',
                            'size': position.get('size'),
                            'reason': 'emergency_rsi_exit',
                            'exit_price': current_price,
                            'timestamp': datetime.now()
                        }
                    # Обычный выход из прибыльного шорта
                    elif rsi < self.PROFIT_EXIT_RSI_SHORT:
                        entry_price = position.get('entry_price', 0)
                        if entry_price > 0 and current_price < entry_price:  # Проверяем прибыльность
                            return {
                                'action': 'CLOSE',
                                'direction': 'BUY',
                                'size': position.get('size'),
                                'reason': 'profit_rsi_exit',
                                'exit_price': current_price,
                                'timestamp': datetime.now()
                            }

            return None

        except Exception as e:
            self.logger.error(f"Error processing exit signals for {symbol}: {e}", exc_info=True)
            return None

    def calculate_position_size(self, account_balance: float, current_price: float) -> float:
        """Расчет размера позиции на основе пользовательских настроек"""
        try:
            # Используем fallback баланс если API не работает
            if account_balance <= 0:
                account_balance = 1100.0  # Fallback баланс
                self.logger.warning(f"Используем fallback баланс: ${account_balance}")

            if current_price <= 0:
                self.logger.error(f"Неверная цена: {current_price}")
                return 0.0

            # Безопасный расчет размера позиции
            risk_amount = account_balance * self.RISK_PER_TRADE  # 0.5% от баланса

            # Размер позиции БЕЗ плеча (плечо применяется биржей)
            position_size = risk_amount / current_price

            # Ограничение: максимум $50 на позицию
            max_position_value = 50.0  # Максимум $50 на позицию
            if position_size * current_price > max_position_value:
                position_size = max_position_value / current_price
                self.logger.info(f"   ⚠️ Размер ограничен до $50: {position_size:.8f}")

            self.logger.info(f"📊 Расчет позиции:")
            self.logger.info(f"   💰 Баланс: ${account_balance:.2f}")
            self.logger.info(f"   🎯 Риск: {self.RISK_PER_TRADE * 100:.1f}% = ${risk_amount:.2f}")
            self.logger.info(f"   💵 Цена: ${current_price:.4f}")
            self.logger.info(f"   📏 Размер: {position_size:.8f}")

            # Минимальные и максимальные размеры
            position_size = max(0.001, min(position_size, 10.0))  # От 0.001 до 10

            final_value = position_size * current_price
            self.logger.info(f"   💵 Итоговая стоимость: ${final_value:.2f}")

            return round(position_size, 8)

        except Exception as e:
            self.logger.error(f"Error calculating position size: {e}")
            return 0.0

    def _is_signal_cooldown_active(self) -> bool:
        """Проверка cooldown между сигналами"""
        if not self.last_signal_time:
            return False

        time_since_last = (datetime.now() - self.last_signal_time).total_seconds()
        return time_since_last < self.SIGNAL_COOLDOWN

    def update_trailing_stop(self, position: Dict[str, Any], current_price: float) -> float:
        """Обновление трейлинг-стопа на основе пользовательских настроек"""
        try:
            if not self.USE_TRAILING_STOP:
                return position.get('stop_loss', 0.0)

            if not all(k in position for k in ['direction', 'stop_loss']):
                return position.get('stop_loss', 0.0)

            current_stop = position['stop_loss']
            atr = position.get('atr', 0)
            direction = position['direction']

            if atr <= 0:
                return current_stop

            trailing_distance = atr * self.ATR_TRAILING_MULTIPLIER

            if direction == 'BUY':
                new_stop = current_price - trailing_distance
                return max(new_stop, current_stop)  # Стоп может только подниматься
            else:  # SELL
                new_stop = current_price + trailing_distance
                return min(new_stop, current_stop)  # Стоп может только опускаться

        except Exception as e:
            self.logger.error(f"Error updating trailing stop: {e}")
            return position.get('stop_loss', 0.0)