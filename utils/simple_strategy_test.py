#!/usr/bin/env python3
"""
Простой тест стратегии без сложных зависимостей
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Добавляем корневую папку в путь
sys.path.append(str(Path(__file__).parent.parent))


def test_strategy_simple():
    """Простое тестирование стратегии"""
    try:
        print("🔍 ПРОСТОЙ ТЕСТ СТРАТЕГИИ")
        print("=" * 40)

        # Импорт модулей
        from modules.data_fetcher import DataFetcher
        from strategies.custom_strategy import CustomStrategy
        from user_config import UserConfig

        print("✅ Модули импортированы")

        # Создание компонентов
        data_fetcher = DataFetcher()
        print("✅ DataFetcher создан")

        # Создание стратегии без position_manager для тестирования
        user_config_dict = {
            'CUSTOM_STRATEGY_CONFIG': UserConfig.CUSTOM_STRATEGY_CONFIG
        }

        strategy = CustomStrategy(None, None, user_config_dict)
        print("✅ Стратегия создана")

        # Получение данных
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=6)

        df = data_fetcher.get_kline(
            symbol='ETHUSDT',
            interval='5',
            start_time=int(start_time.timestamp()),
            end_time=int(end_time.timestamp())
        )

        if df is None or len(df) == 0:
            print("❌ Нет данных")
            return

        print(f"✅ Получено {len(df)} свечей")
        print(f"📈 Цена: ${df['close'].iloc[-1]:.2f}")

        # Тестирование генерации сигналов
        signals = strategy.generate_signals(df)

        if signals:
            print(f"✅ Сигналы сгенерированы: {len(signals)}")
            print(f"   RSI: {signals.get('rsi', 0):.1f}")
            print(f"   Volume Ratio: {signals.get('volume_ratio', 0):.2f}")
            print(f"   EMA Fast: {signals.get('ema_fast', 0):.2f}")
            print(f"   EMA Slow: {signals.get('ema_slow', 0):.2f}")

            # Тестирование условий входа
            long_valid, long_score, long_reasons = strategy._check_long_entry_conditions(signals)
            short_valid, short_score, short_reasons = strategy._check_short_entry_conditions(signals)

            print(f"\n🎯 АНАЛИЗ УСЛОВИЙ:")
            print(
                f"   Long: {long_score:.1f}/{strategy.MIN_CONDITIONS_REQUIRED} ({'✅ Валиден' if long_valid else '❌ Не валиден'})")
            print(f"   Long причины: {long_reasons}")
            print(
                f"   Short: {short_score:.1f}/{strategy.MIN_CONDITIONS_REQUIRED} ({'✅ Валиден' if short_valid else '❌ Не валиден'})")
            print(f"   Short причины: {short_reasons}")

            if long_valid or short_valid:
                print("🎉 СИГНАЛ ДОЛЖЕН ГЕНЕРИРОВАТЬСЯ!")

                # Показываем что именно должно произойти
                if long_valid:
                    print(f"   📈 LONG сигнал: {long_score} условий выполнено")
                    print(f"   💡 Причины: {long_reasons}")
                if short_valid:
                    print(f"   📉 SHORT сигнал: {short_score} условий выполнено")
                    print(f"   💡 Причины: {short_reasons}")
            else:
                print("⚠️ Условия не выполнены для генерации сигнала")
                print(f"   📊 Long: {long_score}/2 условий ({'✅' if long_valid else '❌'})")
                print(f"   📊 Short: {short_score}/2 условий ({'✅' if short_valid else '❌'})")
                print(f"   💡 Нужно минимум {strategy.MIN_CONDITIONS_REQUIRED} условий")

        else:
            print("❌ Сигналы не сгенерированы")

    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_strategy_simple()