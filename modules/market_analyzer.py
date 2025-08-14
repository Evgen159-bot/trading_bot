import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from config.trading_config import TradingConfig

# Попытка импорта ta (технический анализ)
try:
    import ta
except ImportError:
    logging.error("ta library not installed. Please install: pip install ta")
    raise ImportError("Required 'ta' library not found")


class MarketAnalyzer:
    """Анализатор рынка для технического анализа и генерации торговых сигналов"""

    def __init__(self, data_fetcher):
        self.data_fetcher = data_fetcher
        self.logger = logging.getLogger(__name__)

        # Получаем параметры индикаторов из конфигурации
        self.indicator_params = TradingConfig.INDICATORS

        # Кэш для хранения последних расчетов
        self.cache = {}
        self.cache_timeout = 60  # секунд

        self.logger.info("MarketAnalyzer initialized with config parameters")

    def calculate_indicators(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """Расчет всех технических индикаторов для DataFrame"""
        if df is None or df.empty:
            self.logger.error("Empty or None dataframe provided")
            return None

        if len(df) < 50:
            self.logger.warning(f"Insufficient data for indicators calculation: {len(df)} rows")
            return None

        try:
            # Создаем копию для безопасности
            df_calc = df.copy()

            # Проверяем наличие необходимых колонок
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            if not all(col in df_calc.columns for col in required_cols):
                self.logger.error(f"Missing required columns. Expected: {required_cols}, Got: {list(df_calc.columns)}")
                return None

            # EMA индикаторы
            ema_params = self.indicator_params['ema']
            df_calc['ema_fast'] = ta.trend.EMAIndicator(df_calc['close'], window=ema_params['fast']).ema_indicator()
            df_calc['ema_medium'] = ta.trend.EMAIndicator(df_calc['close'], window=ema_params['medium']).ema_indicator()
            df_calc['ema_slow'] = ta.trend.EMAIndicator(df_calc['close'], window=ema_params['slow']).ema_indicator()
            df_calc['ema_trend'] = ta.trend.EMAIndicator(df_calc['close'], window=ema_params['trend']).ema_indicator()

            # RSI
            rsi_params = self.indicator_params['rsi']
            df_calc['rsi'] = ta.momentum.RSIIndicator(df_calc['close'], window=rsi_params['period']).rsi()

            # MACD
            macd_params = self.indicator_params['macd']
            macd_indicator = ta.trend.MACD(
                df_calc['close'],
                window_fast=macd_params['fast'],
                window_slow=macd_params['slow'],
                window_sign=macd_params['signal']
            )
            df_calc['macd'] = macd_indicator.macd()
            df_calc['macd_signal'] = macd_indicator.macd_signal()
            df_calc['macd_histogram'] = macd_indicator.macd_diff()

            # Bollinger Bands
            bb_params = self.indicator_params['bollinger']
            bollinger = ta.volatility.BollingerBands(
                df_calc['close'],
                window=bb_params['period'],
                window_dev=bb_params['std']
            )
            df_calc['bb_upper'] = bollinger.bollinger_hband()
            df_calc['bb_lower'] = bollinger.bollinger_lband()
            df_calc['bb_middle'] = bollinger.bollinger_mavg()
            df_calc['bb_width'] = (df_calc['bb_upper'] - df_calc['bb_lower']) / df_calc['bb_middle']

            # Volume indicators
            volume_params = self.indicator_params['volume']
            df_calc['volume_sma'] = df_calc['volume'].rolling(window=volume_params['sma_period']).mean()
            df_calc['volume_ratio'] = df_calc['volume'] / df_calc['volume_sma']

            # ATR
            atr_params = self.indicator_params['atr']
            df_calc['atr'] = ta.volatility.AverageTrueRange(
                high=df_calc['high'],
                low=df_calc['low'],
                close=df_calc['close'],
                window=atr_params['period']
            ).average_true_range()

            # Stochastic
            stoch_params = self.indicator_params['stochastic']
            stoch = ta.momentum.StochasticOscillator(
                high=df_calc['high'],
                low=df_calc['low'],
                close=df_calc['close'],
                window=stoch_params['k_period'],
                smooth_window=stoch_params['smooth_k']
            )
            df_calc['stoch_k'] = stoch.stoch()
            df_calc['stoch_d'] = stoch.stoch_signal()

            # Дополнительные индикаторы
            df_calc['price_change'] = df_calc['close'].pct_change()
            df_calc['volatility'] = df_calc['price_change'].rolling(window=20).std()

            # Проверяем на NaN значения
            nan_count = df_calc.isnull().sum().sum()
            if nan_count > 0:
                self.logger.warning(f"Found {nan_count} NaN values after indicator calculation")
                # Заполняем NaN значения методом forward fill
                df_calc = df_calc.fillna(method='ffill').fillna(method='bfill')

            self.logger.debug(f"Successfully calculated indicators for {len(df_calc)} rows")
            return df_calc

        except Exception as e:
            self.logger.error(f"Error calculating indicators: {e}", exc_info=True)
            return None

    def analyze_market_conditions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Комплексный анализ рыночных условий"""
        if df is None or df.empty:
            return {
                'trend': 'UNKNOWN',
                'volatility': 'UNKNOWN',
                'volume': 'UNKNOWN',
                'support_resistance': [],
                'market_phase': 'UNKNOWN',
                'strength': 0.0
            }

        try:
            # Добавляем индикаторы если их нет
            if 'ema_fast' not in df.columns:
                df = self.calculate_indicators(df)
                if df is None:
                    return self._get_default_conditions()

            analysis = {
                'trend': self._analyze_trend(df),
                'volatility': self._analyze_volatility(df),
                'volume': self._analyze_volume(df),
                'support_resistance': self._find_support_resistance(df),
                'market_phase': self._determine_market_phase(df),
                'strength': self._calculate_trend_strength(df),
                'momentum': self._analyze_momentum(df),
                'timestamp': datetime.now()
            }

            self.logger.debug(
                f"Market analysis completed: {analysis['trend']}, {analysis['volatility']}, {analysis['volume']}")
            return analysis

        except Exception as e:
            self.logger.error(f"Error analyzing market conditions: {e}", exc_info=True)
            return self._get_default_conditions()

    def _analyze_trend(self, df: pd.DataFrame) -> str:
        """Анализ тренда на основе EMA"""
        if df.empty or len(df) < 10:
            return 'UNKNOWN'

        try:
            last_row = df.iloc[-1]

            # Проверяем наличие необходимых колонок
            required_cols = ['ema_fast', 'ema_medium', 'ema_slow', 'ema_trend', 'close']
            if not all(col in df.columns and pd.notna(last_row[col]) for col in required_cols):
                return 'UNKNOWN'

            # Анализ расположения EMA
            ema_alignment_up = (
                    last_row['ema_fast'] > last_row['ema_medium'] >
                    last_row['ema_slow'] > last_row['ema_trend']
            )
            ema_alignment_down = (
                    last_row['ema_fast'] < last_row['ema_medium'] <
                    last_row['ema_slow'] < last_row['ema_trend']
            )

            # Позиция цены относительно EMA
            price_above_trend = last_row['close'] > last_row['ema_trend']
            price_below_trend = last_row['close'] < last_row['ema_trend']

            if ema_alignment_up and price_above_trend:
                return 'STRONG_UPTREND'
            elif last_row['ema_fast'] > last_row['ema_medium'] and price_above_trend:
                return 'UPTREND'
            elif ema_alignment_down and price_below_trend:
                return 'STRONG_DOWNTREND'
            elif last_row['ema_fast'] < last_row['ema_medium'] and price_below_trend:
                return 'DOWNTREND'
            else:
                return 'SIDEWAYS'

        except Exception as e:
            self.logger.error(f"Error in trend analysis: {e}")
            return 'UNKNOWN'

    def _analyze_volatility(self, df: pd.DataFrame) -> str:
        """Анализ волатильности на основе ATR и BB"""
        if df.empty:
            return 'UNKNOWN'

        try:
            if 'atr' not in df.columns or 'bb_width' not in df.columns:
                return 'UNKNOWN'

            current_atr = df['atr'].iloc[-1]
            avg_atr = df['atr'].rolling(window=20).mean().iloc[-1]
            current_bb_width = df['bb_width'].iloc[-1]
            avg_bb_width = df['bb_width'].rolling(window=20).mean().iloc[-1]

            if pd.isna(current_atr) or pd.isna(avg_atr) or pd.isna(current_bb_width) or pd.isna(avg_bb_width):
                return 'UNKNOWN'

            # Комбинированный анализ волатильности
            atr_ratio = current_atr / avg_atr if avg_atr > 0 else 1
            bb_ratio = current_bb_width / avg_bb_width if avg_bb_width > 0 else 1

            volatility_score = (atr_ratio + bb_ratio) / 2

            if volatility_score > 1.5:
                return 'HIGH'
            elif volatility_score < 0.7:
                return 'LOW'
            else:
                return 'MEDIUM'

        except Exception as e:
            self.logger.error(f"Error in volatility analysis: {e}")
            return 'UNKNOWN'

    def _analyze_volume(self, df: pd.DataFrame) -> str:
        """Анализ объема торгов"""
        if df.empty or 'volume_ratio' not in df.columns:
            return 'UNKNOWN'

        try:
            current_volume_ratio = df['volume_ratio'].iloc[-1]

            if pd.isna(current_volume_ratio):
                return 'UNKNOWN'

            volume_params = self.indicator_params['volume']

            if current_volume_ratio > volume_params['surge_threshold']:
                return 'SURGE'
            elif current_volume_ratio > volume_params['min_threshold']:
                return 'HIGH'
            elif current_volume_ratio < 0.7:
                return 'LOW'
            else:
                return 'MEDIUM'

        except Exception as e:
            self.logger.error(f"Error in volume analysis: {e}")
            return 'UNKNOWN'

    def _find_support_resistance(self, df: pd.DataFrame, lookback: int = 50) -> List[Dict[str, Any]]:
        """Поиск уровней поддержки и сопротивления"""
        if df.empty or len(df) < lookback:
            return []

        try:
            levels = []
            window = 5

            # Ограничиваем анализ последними данными
            recent_df = df.tail(lookback)

            for i in range(window, len(recent_df) - window):
                current_idx = i

                # Проверка на локальный минимум (поддержка)
                if self._is_local_minimum(recent_df, current_idx, window):
                    levels.append({
                        'type': 'SUPPORT',
                        'price': recent_df['low'].iloc[current_idx],
                        'strength': self._calculate_level_strength(recent_df, recent_df['low'].iloc[current_idx],
                                                                   'SUPPORT'),
                        'timestamp': recent_df.index[current_idx] if hasattr(recent_df.index[current_idx],
                                                                             'timestamp') else datetime.now()
                    })

                # Проверка на локальный максимум (сопротивление)
                if self._is_local_maximum(recent_df, current_idx, window):
                    levels.append({
                        'type': 'RESISTANCE',
                        'price': recent_df['high'].iloc[current_idx],
                        'strength': self._calculate_level_strength(recent_df, recent_df['high'].iloc[current_idx],
                                                                   'RESISTANCE'),
                        'timestamp': recent_df.index[current_idx] if hasattr(recent_df.index[current_idx],
                                                                             'timestamp') else datetime.now()
                    })

            # Сортируем по силе уровня и возвращаем топ-5
            levels.sort(key=lambda x: x['strength'], reverse=True)
            return levels[:5]

        except Exception as e:
            self.logger.error(f"Error finding support/resistance: {e}")
            return []

    def _is_local_minimum(self, df: pd.DataFrame, idx: int, window: int) -> bool:
        """Проверка на локальный минимум"""
        try:
            current_low = df['low'].iloc[idx]
            left_lows = df['low'].iloc[idx - window:idx]
            right_lows = df['low'].iloc[idx + 1:idx + window + 1]

            return (current_low <= left_lows.min()) and (current_low <= right_lows.min())
        except:
            return False

    def _is_local_maximum(self, df: pd.DataFrame, idx: int, window: int) -> bool:
        """Проверка на локальный максимум"""
        try:
            current_high = df['high'].iloc[idx]
            left_highs = df['high'].iloc[idx - window:idx]
            right_highs = df['high'].iloc[idx + 1:idx + window + 1]

            return (current_high >= left_highs.max()) and (current_high >= right_highs.max())
        except:
            return False

    def _calculate_level_strength(self, df: pd.DataFrame, price: float, level_type: str) -> float:
        """Расчет силы уровня поддержки/сопротивления"""
        try:
            touches = 0
            tolerance = 0.001  # 0.1% толерантность

            if level_type == 'SUPPORT':
                touches = len(df[abs(df['low'] - price) / price <= tolerance])
            else:  # RESISTANCE
                touches = len(df[abs(df['high'] - price) / price <= tolerance])

            return min(touches / 10.0, 1.0)  # Нормализуем от 0 до 1
        except:
            return 0.0

    def _determine_market_phase(self, df: pd.DataFrame) -> str:
        """Определение фазы рынка"""
        try:
            if 'rsi' not in df.columns or 'bb_width' not in df.columns:
                return 'UNKNOWN'

            last_rsi = df['rsi'].iloc[-1]
            bb_width = df['bb_width'].iloc[-1]
            volatility = self._analyze_volatility(df)

            if pd.isna(last_rsi) or pd.isna(bb_width):
                return 'UNKNOWN'

            # Определяем фазу на основе RSI и волатильности
            if last_rsi > 70 and volatility == 'HIGH':
                return 'EUPHORIA'
            elif last_rsi < 30 and volatility == 'HIGH':
                return 'PANIC'
            elif 40 <= last_rsi <= 60 and volatility == 'LOW':
                return 'ACCUMULATION'
            elif volatility == 'HIGH':
                return 'TRENDING'
            else:
                return 'CONSOLIDATION'

        except Exception as e:
            self.logger.error(f"Error determining market phase: {e}")
            return 'UNKNOWN'

    def _calculate_trend_strength(self, df: pd.DataFrame) -> float:
        """Расчет силы тренда (0-1)"""
        try:
            if len(df) < 20:
                return 0.0

            # Анализ последних 20 свечей
            recent_df = df.tail(20)

            if 'ema_fast' not in recent_df.columns or 'ema_slow' not in recent_df.columns:
                return 0.0

            # Считаем количество свечей, где быстрая EMA выше медленной
            uptrend_candles = len(recent_df[recent_df['ema_fast'] > recent_df['ema_slow']])
            strength = uptrend_candles / len(recent_df)

            # Корректируем на основе расстояния между EMA
            ema_distance = abs(recent_df['ema_fast'].iloc[-1] - recent_df['ema_slow'].iloc[-1])
            price = recent_df['close'].iloc[-1]

            if price > 0:
                distance_factor = min(ema_distance / price, 0.1) * 10  # Нормализуем
                strength = min(strength + distance_factor, 1.0)

            return round(strength, 3)

        except Exception as e:
            self.logger.error(f"Error calculating trend strength: {e}")
            return 0.0

    def _analyze_momentum(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализ моментума"""
        try:
            if 'rsi' not in df.columns or 'macd' not in df.columns:
                return {'rsi_momentum': 'UNKNOWN', 'macd_momentum': 'UNKNOWN'}

            last_rsi = df['rsi'].iloc[-1]
            last_macd = df['macd'].iloc[-1]
            last_macd_signal = df['macd_signal'].iloc[-1]

            # RSI моментум
            if last_rsi > 60:
                rsi_momentum = 'BULLISH'
            elif last_rsi < 40:
                rsi_momentum = 'BEARISH'
            else:
                rsi_momentum = 'NEUTRAL'

            # MACD моментум
            if last_macd > last_macd_signal:
                macd_momentum = 'BULLISH'
            elif last_macd < last_macd_signal:
                macd_momentum = 'BEARISH'
            else:
                macd_momentum = 'NEUTRAL'

            return {
                'rsi_momentum': rsi_momentum,
                'macd_momentum': macd_momentum,
                'overall': 'BULLISH' if rsi_momentum == 'BULLISH' and macd_momentum == 'BULLISH' else
                'BEARISH' if rsi_momentum == 'BEARISH' and macd_momentum == 'BEARISH' else 'NEUTRAL'
            }

        except Exception as e:
            self.logger.error(f"Error analyzing momentum: {e}")
            return {'rsi_momentum': 'UNKNOWN', 'macd_momentum': 'UNKNOWN', 'overall': 'UNKNOWN'}

    def _get_default_conditions(self) -> Dict[str, Any]:
        """Возвращает условия по умолчанию при ошибках"""
        return {
            'trend': 'UNKNOWN',
            'volatility': 'UNKNOWN',
            'volume': 'UNKNOWN',
            'support_resistance': [],
            'market_phase': 'UNKNOWN',
            'strength': 0.0,
            'momentum': {'rsi_momentum': 'UNKNOWN', 'macd_momentum': 'UNKNOWN', 'overall': 'UNKNOWN'},
            'timestamp': datetime.now()
        }

    def get_market_summary(self, symbol: str) -> Dict[str, Any]:
        """Получение краткой сводки по рынку"""
        try:
            # Получаем данные через data_fetcher
            end_time = datetime.now()
            start_time = end_time - pd.Timedelta(days=1)

            df = self.data_fetcher.get_kline(
                symbol=symbol,
                interval=TradingConfig.TIMEFRAMES['primary'],
                start_time=int(start_time.timestamp()),
                end_time=int(end_time.timestamp())
            )

            if df is None or df.empty:
                return {'error': 'No data available'}

            # Рассчитываем индикаторы
            df_with_indicators = self.calculate_indicators(df)
            if df_with_indicators is None:
                return {'error': 'Failed to calculate indicators'}

            # Анализируем условия
            conditions = self.analyze_market_conditions(df_with_indicators)

            # Текущая цена
            current_price = df['close'].iloc[-1]

            return {
                'symbol': symbol,
                'current_price': current_price,
                'conditions': conditions,
                'last_update': datetime.now()
            }

        except Exception as e:
            self.logger.error(f"Error getting market summary for {symbol}: {e}")
            return {'error': str(e)}