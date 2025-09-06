#!/usr/bin/env python3
"""
Быстрая проверка логов без загрузки больших файлов
"""

import os
from datetime import datetime
from pathlib import Path


def quick_log_analysis():
    """Быстрый анализ последних логов"""
    print("🔍 БЫСТРЫЙ АНАЛИЗ ЛОГОВ")
    print("=" * 40)

    # Найти последний лог файл
    log_dir = Path("logs")
    if not log_dir.exists():
        print("❌ Папка logs не найдена")
        return

    log_files = list(log_dir.glob("trading_*.log"))
    if not log_files:
        print("❌ Лог файлы не найдены")
        return

    latest_log = max(log_files, key=lambda x: x.stat().st_mtime)
    print(f"📄 Анализируем: {latest_log}")

    try:
        with open(latest_log, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Последние 50 строк
        recent_lines = lines[-50:]

        print(f"\n📊 ПОСЛЕДНИЕ 50 ЗАПИСЕЙ:")
        print("-" * 40)

        open_signals = 0
        close_signals = 0
        errors = 0

        for line in recent_lines:
            if 'Strategy result' in line and 'OPEN' in line:
                open_signals += 1
                print(f"📈 {line.strip()}")
            elif 'Strategy result' in line and 'CLOSE' in line:
                close_signals += 1
                print(f"📉 {line.strip()}")
            elif 'ERROR' in line:
                errors += 1
                print(f"❌ {line.strip()}")
            elif 'No action for' in line:
                print(f"⏸️  {line.strip()}")

        print("-" * 40)
        print(f"📊 СВОДКА ПОСЛЕДНИХ ЗАПИСЕЙ:")
        print(f"   📈 OPEN сигналов: {open_signals}")
        print(f"   📉 CLOSE сигналов: {close_signals}")
        print(f"   ❌ Ошибок: {errors}")

        # Проверка на зацикливание
        if open_signals > 20 and close_signals == 0:
            print(f"\n🚨 ПРОБЛЕМА: Слишком много OPEN сигналов без CLOSE!")
            print(f"   Рекомендация: Увеличить min_conditions_required")

    except Exception as e:
        print(f"❌ Ошибка чтения лога: {e}")


def check_signal_patterns():
    """Проверка паттернов сигналов"""
    print(f"\n🎯 АНАЛИЗ ПАТТЕРНОВ СИГНАЛОВ:")

    try:
        log_dir = Path("logs")
        log_files = list(log_dir.glob("trading_*.log"))
        latest_log = max(log_files, key=lambda x: x.stat().st_mtime)

        with open(latest_log, 'r', encoding='utf-8') as f:
            content = f.read()

        # Подсчет сигналов по парам
        pairs = ['ETHUSDT', 'SOLUSDT', 'BTCUSDT', 'DOGEUSDT']

        for pair in pairs:
            open_count = content.count(f'Strategy result for {pair}: OPEN')
            close_count = content.count(f'Strategy result for {pair}: CLOSE')
            no_action = content.count(f'No action for {pair}')

            print(f"   {pair}: OPEN={open_count}, CLOSE={close_count}, NO_ACTION={no_action}")

            if open_count > 100 and close_count == 0:
                print(f"      🚨 {pair}: Много OPEN, нет CLOSE - проблема с логикой!")

    except Exception as e:
        print(f"❌ Ошибка анализа паттернов: {e}")


if __name__ == "__main__":
    quick_log_analysis()
    check_signal_patterns()