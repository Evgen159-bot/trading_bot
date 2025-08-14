#!/usr/bin/env python3
"""
Утилита для выбора и настройки торговых стратегий
"""

import sys
from pathlib import Path
from user_config import UserConfig


class StrategySelector:
    """Интерактивный селектор стратегий"""

    def __init__(self):
        self.user_config = UserConfig()

    def show_strategy_menu(self):
        """Показать меню выбора стратегий"""
        print("\n" + "=" * 70)
        print("🎯 ВЫБОР ТОРГОВОЙ СТРАТЕГИИ")
        print("=" * 70)

        strategies = self.user_config.AVAILABLE_STRATEGIES

        print("Доступные стратегии:")
        print()

        for i, (strategy_id, info) in enumerate(strategies.items(), 1):
            risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(info['risk_level'], "⚪")
            type_emoji = "🛠️" if info['type'] == 'configurable' else "🤖"
            selected = "👉 " if strategy_id == self.user_config.SELECTED_STRATEGY else "   "

            print(f"{selected}{i}. {type_emoji} {info['name']} {risk_emoji}")
            print(f"     📝 {info['description']}")
            print(f"     ⏰ Таймфрейм: {info['timeframe']} | 🎯 {info['best_for']}")
            print()

        print("=" * 70)

    def interactive_selection(self):
        """Интерактивный выбор стратегии"""
        while True:
            self.show_strategy_menu()

            print("\nВыберите действие:")
            print("1-8. Выбрать стратегию")
            print("9. Показать текущую конфигурацию")
            print("10. Настроить пользовательскую стратегию")
            print("0. Выход")

            choice = input("\nВаш выбор: ").strip()

            if choice == "0":
                break
            elif choice == "9":
                self.user_config.print_config_summary()
            elif choice == "10":
                self.configure_custom_strategy()
            elif choice.isdigit() and 1 <= int(choice) <= 8:
                self.select_strategy(int(choice))
            else:
                print("❌ Неверный выбор")

    def select_strategy(self, choice: int):
        """Выбрать стратегию по номеру"""
        strategies = list(self.user_config.AVAILABLE_STRATEGIES.keys())

        if 1 <= choice <= len(strategies):
            selected_strategy = strategies[choice - 1]
            strategy_info = self.user_config.AVAILABLE_STRATEGIES[selected_strategy]

            print(f"\n✅ Выбрана стратегия: {strategy_info['name']}")
            print(f"📝 {strategy_info['description']}")

            # Здесь можно добавить код для обновления user_config.py
            print(f"\n🔧 Для применения изменений:")
            print(f"   Измените SELECTED_STRATEGY = '{selected_strategy}' в файле user_config.py")

            if selected_strategy == 'custom':
                print(f"   Также настройте CUSTOM_STRATEGY_CONFIG в том же файле")
        else:
            print("❌ Неверный номер стратегии")

    def configure_custom_strategy(self):
        """Настройка пользовательской стратегии"""
        print("\n" + "=" * 50)
        print("🛠️ НАСТРОЙКА ПОЛЬЗОВАТЕЛЬСКОЙ СТРАТЕГИИ")
        print("=" * 50)

        config = self.user_config.CUSTOM_STRATEGY_CONFIG

        print("Текущие настройки:")
        print(f"📊 RSI период: {config['rsi_settings']['period']}")
        print(
            f"📊 MACD: {config['macd_settings']['fast_period']}/{config['macd_settings']['slow_period']}/{config['macd_settings']['signal_period']}")
        print(
            f"📊 EMA: {config['ema_settings']['fast_period']}/{config['ema_settings']['slow_period']}/{config['ema_settings']['trend_period']}")
        print(f"🎯 Риск на сделку: {config['risk_management']['risk_per_trade'] * 100:.1f}%")
        print(f"🛑 Макс. стоп-лосс: {config['risk_management']['max_stop_loss_pct'] * 100:.1f}%")
        print(f"💰 Мин. тейк-профит: {config['risk_management']['min_take_profit_pct'] * 100:.1f}%")

        print("\n💡 Для изменения параметров отредактируйте CUSTOM_STRATEGY_CONFIG в user_config.py")
        print("📚 Подробное описание параметров см. в комментариях к файлу")


def main():
    """Главная функция"""
    selector = StrategySelector()

    if len(sys.argv) > 1:
        if sys.argv[1] == '--list':
            selector.show_strategy_menu()
        elif sys.argv[1] == '--interactive':
            selector.interactive_selection()
        elif sys.argv[1] == '--custom':
            selector.configure_custom_strategy()
        else:
            print("Использование:")
            print("  python utils/strategy_selector.py --list        # Показать список стратегий")
            print("  python utils/strategy_selector.py --interactive # Интерактивный выбор")
            print("  python utils/strategy_selector.py --custom      # Настройка пользовательской стратегии")
    else:
        selector.interactive_selection()


if __name__ == "__main__":
    main()