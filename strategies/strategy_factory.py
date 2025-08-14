"""
Фабрика стратегий для создания экземпляров стратегий на основе пользовательского выбора
"""

import logging
from typing import Dict, Any, Optional

# Импорт всех доступных стратегий
from strategies.custom_strategy import CustomStrategy
from strategies.smart_money_strategy import SmartMoneyStrategy
from strategies.trend_following_strategy import TrendFollowingStrategy
from strategies.scalping_strategy import ScalpingStrategy
from strategies.swing_strategy import SwingStrategy
from strategies.breakout_strategy import BreakoutStrategy
from strategies.mean_reversion_strategy import MeanReversionStrategy
from strategies.momentum_strategy import MomentumStrategy


class StrategyFactory:
    """Фабрика для создания торговых стратегий"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Маппинг названий стратегий к классам
        self.strategy_classes = {
            'custom': CustomStrategy,
            'smart_money': SmartMoneyStrategy,
            'trend_following': TrendFollowingStrategy,
            'scalping': ScalpingStrategy,
            'swing': SwingStrategy,
            'breakout': BreakoutStrategy,
            'mean_reversion': MeanReversionStrategy,
            'momentum': MomentumStrategy
        }

        self.logger.info("StrategyFactory initialized with 8 available strategies")

    def create_strategy(self, strategy_name: str, market_analyzer, position_manager,
                        user_config: Dict[str, Any] = None):
        """
        Создание экземпляра стратегии

        Args:
            strategy_name: Название стратегии
            market_analyzer: Анализатор рынка
            position_manager: Менеджер позиций
            user_config: Пользовательская конфигурация (для custom стратегии)

        Returns:
            Экземпляр стратегии или None при ошибке
        """
        try:
            if strategy_name not in self.strategy_classes:
                self.logger.error(f"Unknown strategy: {strategy_name}")
                available = ', '.join(self.strategy_classes.keys())
                self.logger.error(f"Available strategies: {available}")
                return None

            strategy_class = self.strategy_classes[strategy_name]

            # Для пользовательской стратегии передаем конфигурацию
            if strategy_name == 'custom':
                if user_config is None:
                    self.logger.error("User config required for custom strategy")
                    return None
                strategy = strategy_class(market_analyzer, position_manager, user_config)
            else:
                # Для автоматических стратегий
                strategy = strategy_class(market_analyzer, position_manager)

            self.logger.info(f"Successfully created strategy: {strategy_name}")
            return strategy

        except Exception as e:
            self.logger.error(f"Error creating strategy {strategy_name}: {e}", exc_info=True)
            return None

    def get_available_strategies(self) -> Dict[str, str]:
        """Получить список доступных стратегий"""
        return list(self.strategy_classes.keys())

    def validate_strategy_name(self, strategy_name: str) -> bool:
        """Проверить корректность названия стратегии"""
        return strategy_name in self.strategy_classes

    def get_strategy_info(self, strategy_name: str) -> Optional[Dict[str, Any]]:
        """Получить информацию о стратегии"""
        if strategy_name not in self.strategy_classes:
            return None

        strategy_class = self.strategy_classes[strategy_name]

        # Базовая информация
        info = {
            'name': strategy_name,
            'class_name': strategy_class.__name__,
            'description': strategy_class.__doc__ or "No description available"
        }

        return info

    def create_strategy_from_config(self, user_config_class, market_analyzer, position_manager):
        """
        Создание стратегии на основе пользовательской конфигурации

        Args:
            user_config_class: Класс пользовательской конфигурации
            market_analyzer: Анализатор рынка
            position_manager: Менеджер позиций

        Returns:
            Экземпляр выбранной стратегии
        """
        try:
            selected_strategy = getattr(user_config_class, 'SELECTED_STRATEGY', 'smart_money')

            self.logger.info(f"Creating strategy from config: {selected_strategy}")

            # Для пользовательской стратегии передаем всю конфигурацию
            if selected_strategy == 'custom':
                user_config_dict = {
                    'CUSTOM_STRATEGY_CONFIG': getattr(user_config_class, 'CUSTOM_STRATEGY_CONFIG', {})
                }
                return self.create_strategy(selected_strategy, market_analyzer, position_manager, user_config_dict)
            else:
                return self.create_strategy(selected_strategy, market_analyzer, position_manager)

        except Exception as e:
            self.logger.error(f"Error creating strategy from config: {e}")
            # Fallback к Smart Money стратегии
            self.logger.info("Falling back to SmartMoneyStrategy")
            return self.create_strategy('smart_money', market_analyzer, position_manager)