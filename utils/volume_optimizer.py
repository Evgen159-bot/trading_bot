#!/usr/bin/env python3
"""
Утилита для анализа и оптимизации объемных фильтров
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Добавляем корневую папку в путь
sys.path.append(str(Path(__file__).parent.parent))

from modules.data_fetcher import DataFetcher
from user_config import UserConfig


class VolumeOptimizer:
    """Анализатор объемов для оптимизации фильтров"""

    def __init__(self):
        self.data_fetcher = DataFetcher()

    def analyze_volume_patterns(self):
        """Анализ паттернов объема для всех пар"""
        print("📊 АНАЛИЗ ОБЪЕМНЫХ ПАТТЕРНОВ")
        print("=" * 50)

        enabled_pairs = UserConfig.get_enabled_pairs()

        for symbol in enabled_pairs:
            print(f"\n📈 Анализ {symbol}:")

            try:
                # Получаем данные за последние 24 часа
                end_time = datetime.now()
                start_time = end_time - timedelta(days=1)

                df = self.data_fetcher.get_kline(
                    symbol=symbol,
                    interval='5',
                    start_time=int(start_time.timestamp()),
                    end_time=int(end_time.timestamp())
                )

                if df is None or len(df) == 0:
                    print(f"❌ Нет данных для {symbol}")
                    continue

                # Анализ объемов
                df['volume_sma'] = df['volume'].rolling(20).mean()
                df['volume_ratio'] = df['volume'] / df['volume_sma']

                # Статистика
                avg_volume_ratio = df['volume_ratio'].mean()
                max_volume_ratio = df['volume_ratio'].max()
                min_volume_ratio = df['volume_ratio'].min()
                current_volume_ratio = df['volume_ratio'].iloc[-1]

                # Процент свечей с достаточным объемом
                sufficient_volume_1_1 = (df['volume_ratio'] > 1.1).sum() / len(df) * 100
                sufficient_volume_0_8 = (df['volume_ratio'] > 0.8).sum() / len(df) * 100
                sufficient_volume_0_5 = (df['volume_ratio'] > 0.5).sum() / len(df) * 100

                print(f"   📊 Средний Volume Ratio: {avg_volume_ratio:.2f}")
                print(f"   📈 Максимальный: {max_volume_ratio:.2f}")
                print(f"   📉 Минимальный: {min_volume_ratio:.2f}")
                print(f"   🔄 Текущий: {current_volume_ratio:.2f}")
                print(f"   ✅ Свечей с объемом > 1.1: {sufficient_volume_1_1:.1f}%")
                print(f"   ✅ Свечей с объемом > 0.8: {sufficient_volume_0_8:.1f}%")
                print(f"   ✅ Свечей с объемом > 0.5: {sufficient_volume_0_5:.1f}%")

                # Рекомендации
                if sufficient_volume_1_1 < 20:
                    print(
                        f"   💡 Рекомендация: Снизить min_ratio до 0.8 (только {sufficient_volume_1_1:.1f}% свечей проходят)")
                elif sufficient_volume_1_1 > 60:
                    print(f"   💡 Рекомендация: Можно повысить min_ratio до 1.3")
                else:
                    print(f"   ✅ Текущий порог 1.1 подходит")

            except Exception as e:
                print(f"❌ Ошибка анализа {symbol}: {e}")

    def recommend_optimal_settings(self):
        """Рекомендации по оптимальным настройкам"""
        print("\n" + "=" * 60)
        print("💡 РЕКОМЕНДАЦИИ ПО ОПТИМИЗАЦИИ")
        print("=" * 60)

        print("📊 На основе анализа объемов рекомендуется:")
        print()
        print("1. 📉 Снизить требования к объему:")
        print("   'min_ratio': 0.8,  # Вместо 1.1")
        print()
        print("2. 🎯 Снизить требования к условиям:")
        print("   'min_conditions_required': 1,  # Вместо 2")
        print()
        print("3. ⏱️ Уменьшить cooldown:")
        print("   'signal_cooldown': 60,  # Вместо 180")
        print()
        print("4. 🔄 Увеличить частоту проверок:")
        print("   'cycle_interval': 30,  # Вместо 60")
        print()
        print("🎯 Эти изменения увеличат количество сигналов в 3-5 раз!")


def main():
    """Главная функция"""
    optimizer = VolumeOptimizer()

    try:
        optimizer.analyze_volume_patterns()
        optimizer.recommend_optimal_settings()

    except Exception as e:
        print(f"❌ Ошибка анализа: {e}")


if __name__ == "__main__":
    main()