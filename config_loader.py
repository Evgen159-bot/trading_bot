"""
🔧 ЗАГРУЗЧИК ПОЛЬЗОВАТЕЛЬСКОЙ КОНФИГУРАЦИИ
==========================================

Этот модуль загружает пользовательскую конфигурацию и интегрирует её с основным ботом.
"""

import logging
import sys
from typing import Dict, Any
from user_config import UserConfig
from config.trading_config import TradingConfig
from strategies.strategy_factory import StrategyFactory


class ConfigLoader:
    """Загрузчик и валидатор пользовательской конфигурации"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_config = UserConfig()
        self.strategy_factory = StrategyFactory()

    def load_and_validate(self) -> bool:
        """
        Загрузка и валидация пользовательской конфигурации

        Returns:
            bool: True если конфигурация валидна
        """
        try:
            print("\n🔍 Загрузка пользовательской конфигурации...")

            # Валидация конфигурации
            is_valid, errors = self.user_config.validate_config()

            if not is_valid:
                print("❌ ОШИБКИ В КОНФИГУРАЦИИ:")
                for error in errors:
                    print(f"   {error}")
                print("\n🔧 Исправьте ошибки в файле user_config.py и перезапустите бота")
                return False

            # Применение конфигурации
            self._apply_user_config()

            # Валидация выбранной стратегии
            if not self._validate_strategy_selection():
                return False

            print("✅ Пользовательская конфигурация загружена успешно!")
            self.user_config.print_config_summary()

            return True

        except Exception as e:
            print(f"💥 Критическая ошибка загрузки конфигурации: {e}")
            return False

    def _validate_strategy_selection(self) -> bool:
        """Валидация выбранной стратегии"""
        try:
            selected_strategy = self.user_config.SELECTED_STRATEGY

            if not self.strategy_factory.validate_strategy_name(selected_strategy):
                available = ', '.join(self.strategy_factory.get_available_strategies())
                print(f"❌ НЕИЗВЕСТНАЯ СТРАТЕГИЯ: {selected_strategy}")
                print(f"📋 Доступные стратегии: {available}")
                print("🔧 Исправьте SELECTED_STRATEGY в файле user_config.py")
                return False

            strategy_info = self.user_config.get_strategy_info()
            print(f"\n🎯 Выбранная стратегия: {strategy_info.get('name', selected_strategy)}")
            print(f"📝 Тип: {'Настраиваемая' if strategy_info.get('type') == 'configurable' else 'Автоматическая'}")

            return True

        except Exception as e:
            self.logger.error(f"Error validating strategy selection: {e}")
            return False

    def _apply_user_config(self):
        """Применение пользовательской конфигурации к основному боту"""
        try:
            # API настройки
            TradingConfig.API_KEY = self.user_config.BYBIT_API_KEY
            TradingConfig.API_SECRET = self.user_config.BYBIT_API_SECRET
            TradingConfig.TESTNET = self.user_config.USE_TESTNET

            # Торговые пары (только включенные)
            TradingConfig.TRADING_PAIRS = self.user_config.get_enabled_pairs()

            # Риск-менеджмент
            TradingConfig.RISK_MANAGEMENT.update(self.user_config.RISK_SETTINGS)

            # Индикаторы (только включенные)
            enabled_indicators = self.user_config.get_enabled_indicators()
            for indicator_name, config in enabled_indicators.items():
                if indicator_name in TradingConfig.INDICATORS:
                    TradingConfig.INDICATORS[indicator_name].update(config)

            # Настройки стратегии
            TradingConfig.STRATEGY_SETTINGS.update(self.user_config.STRATEGY_SETTINGS)

            # Обновляем название стратегии на основе выбора пользователя
            strategy_info = self.user_config.get_strategy_info()
            TradingConfig.STRATEGY_SETTINGS['strategy_name'] = strategy_info.get('name', self.user_config.SELECTED_STRATEGY)

            # Временные настройки
            TradingConfig.CYCLE_INTERVAL = self.user_config.TIME_SETTINGS['intervals']['cycle_interval']
            TradingConfig.TRADING_HOURS = self.user_config.TIME_SETTINGS['trading_hours']
            TradingConfig.TIMEFRAMES = self.user_config.TIME_SETTINGS['timeframes']

            # Уведомления
            TradingConfig.NOTIFICATIONS = self.user_config.NOTIFICATIONS

            # Дополнительные настройки
            TradingConfig.PERFORMANCE_SETTINGS = self.user_config.DATA_SETTINGS
            TradingConfig.CONNECTION_SETTINGS.update(self.user_config.SECURITY_SETTINGS)

            self.logger.info("User configuration applied successfully")

        except Exception as e:
            self.logger.error(f"Error applying user configuration: {e}")
            raise

    def create_strategy(self, market_analyzer, position_manager):
        """Создание стратегии на основе пользовательского выбора"""
        try:
            strategy = self.strategy_factory.create_strategy_from_config(
                self.user_config, market_analyzer, position_manager
            )

            if strategy is None:
                self.logger.error("Failed to create strategy")
                return None

            self.logger.info(f"Successfully created strategy: {strategy.name}")
            return strategy

        except Exception as e:
            self.logger.error(f"Error creating strategy: {e}")
            return None

    def get_balance_info(self) -> Dict[str, float]:
        """Получение информации о балансе из конфигурации"""
        return {
            'initial_balance': self.user_config.INITIAL_BALANCE,
            'min_balance_threshold': self.user_config.MIN_BALANCE_THRESHOLD
        }

    def is_demo_mode(self) -> bool:
        """Проверка демо режима"""
        return self.user_config.ADVANCED_SETTINGS['modes']['demo_mode']

    def is_paper_trading(self) -> bool:
        """Проверка бумажной торговли"""
        return self.user_config.ADVANCED_SETTINGS['modes']['paper_trading']

    def should_validate_strategy(self) -> bool:
        """Нужно ли валидировать стратегию"""
        return self.user_config.ADVANCED_SETTINGS['modes']['strategy_validation']

    def get_strategy_name(self) -> str:
        """Получить название выбранной стратегии"""
        return self.user_config.SELECTED_STRATEGY

    def get_strategy_description(self) -> str:
        """Получить описание выбранной стратегии"""
        strategy_info = self.user_config.get_strategy_info()
        return strategy_info.get('description', 'No description available')


def load_user_configuration() -> ConfigLoader:
    """
    Главная функция загрузки пользовательской конфигурации

    Returns:
        ConfigLoader: Загрузчик конфигурации
    """
    loader = ConfigLoader()

    if not loader.load_and_validate():
        print("\n🚨 КРИТИЧЕСКАЯ ОШИБКА: Невозможно загрузить конфигурацию!")
        print("Проверьте файл user_config.py и исправьте ошибки")
        sys.exit(1)

    return loader


if __name__ == "__main__":
    # Тестирование загрузки конфигурации
    loader = load_user_configuration()
    print("\n✅ Конфигурация загружена и готова к использованию!")