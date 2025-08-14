import logging
import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime
import ta
from strategies.custom_strategy import CustomStrategy


class MultiIndicatorStrategy(CustomStrategy):
    """
    УСТАРЕВШАЯ: Используйте CustomStrategy вместо этого класса

    Этот класс оставлен для обратной совместимости.
    Новая система позволяет настраивать стратегию через user_config.py
    """

    def __init__(self, market_analyzer, position_manager, user_config=None):
        """Инициализация стратегии"""
        # Создаем конфигурацию по умолчанию если не передана
        if user_config is None:
            user_config = {
                'CUSTOM_STRATEGY_CONFIG': {
                    'name': 'MultiIndicatorStrategy',
                    'rsi_settings': {'enabled': True, 'period': 14, 'oversold_lower': 30, 'oversold_upper': 40,
                                     'overbought_lower': 60, 'overbought_upper': 70, 'weight': 1.0},
                    'macd_settings': {'enabled': True, 'fast_period': 12, 'slow_period': 26, 'signal_period': 9,
                                      'histogram_threshold': 0.0002, 'weight': 1.0},
                    'ema_settings': {'enabled': True, 'fast_period': 9, 'slow_period': 21, 'trend_period': 50,
                                     'weight': 1.0},
                    'bollinger_settings': {'enabled': True, 'period': 20, 'std_deviation': 2.0, 'weight': 0.8},
                    'volume_settings': {'enabled': True, 'sma_period': 20, 'min_ratio': 1.1, 'surge_threshold': 2.5,
                                        'weight': 0.7},
                    'stochastic_settings': {'enabled': True, 'k_period': 14, 'd_period': 3, 'smooth_k': 3,
                                            'oversold': 25, 'overbought': 75, 'weight': 0.8},
                    'atr_settings': {'enabled': True, 'period': 14, 'stop_loss_multiplier': 2.0,
                                     'take_profit_multiplier': 2.5, 'trailing_multiplier': 1.5},
                    'entry_conditions': {'min_conditions_required': 3, 'trend_strength_threshold': 0.3,
                                         'volume_confirmation': True, 'signal_cooldown': 300},
                    'exit_conditions': {'use_trailing_stop': True, 'emergency_rsi_long': 80, 'emergency_rsi_short': 20,
                                        'profit_exit_rsi_long': 65, 'profit_exit_rsi_short': 35},
                    'risk_management': {'risk_per_trade': 0.015, 'max_stop_loss_pct': 0.08, 'min_take_profit_pct': 0.12,
                                        'max_take_profit_pct': 0.25, 'leverage': 3, 'max_position_value_pct': 0.3}
                }
            }

        super().__init__(market_analyzer, position_manager, user_config)
        self.logger.warning("MultiIndicatorStrategy is deprecated. Please use CustomStrategy with user_config.py")