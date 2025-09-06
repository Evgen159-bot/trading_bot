#!/usr/bin/env python3
"""
Простая проверка логов без использования pathlib
"""

import os
import sys
from datetime import datetime


def check_logs():
    """Простая проверка последних логов"""
    print("🔍 БЫСТРАЯ ПРОВЕРКА ЛОГОВ")
    print("=" * 50)

    # Ищем файлы логов
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        print("❌ Папка logs не найдена")
        return

    # Ищем последний лог файл
    log_files = []
    for file in os.listdir(logs_dir):
        if file.startswith("trading_") and file.endswith(".log"):
            log_files.append(file)

    if not log_files:
        print("❌ Файлы логов не найдены")
        return

    # Берем последний файл
    latest_log = sorted(log_files)[-1]
    log_path = os.path.join(logs_dir, latest_log)

    print(f"📄 Анализируем: {latest_log}")
    print("-" * 50)

    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Последние 30 строк
        recent_lines = lines[-30:]

        # Статистика
        total_lines = len(lines)
        errors = sum(1 for line in lines if "ERROR" in line)
        open_signals = sum(1 for line in lines if "Strategy result" in line and "OPEN" in line)
        close_signals = sum(1 for line in lines if "Strategy result" in line and "CLOSE" in line)

        print(f"📊 СТАТИСТИКА:")
        print(f"   Всего записей: {total_lines}")
        print(f"   Ошибок: {errors}")
        print(f"   OPEN сигналов: {open_signals}")
        print(f"   CLOSE сигналов: {close_signals}")
        print()

        print("📝 ПОСЛЕДНИЕ 30 ЗАПИСЕЙ:")
        print("-" * 50)
        for line in recent_lines:
            line = line.strip()
            if line:
                # Цветовое выделение
                if "ERROR" in line:
                    print(f"❌ {line}")
                elif "Strategy result" in line:
                    if "OPEN" in line:
                        print(f"🟢 {line}")
                    elif "CLOSE" in line:
                        print(f"🔴 {line}")
                    else:
                        print(f"⚪ {line}")
                elif "Trading cycle started" in line:
                    print(f"🔄 {line}")
                else:
                    print(f"   {line}")

        print("\n" + "=" * 50)

        # Рекомендации
        if errors > 0:
            print("⚠️  НАЙДЕНЫ ОШИБКИ - нужно исправить!")

        if open_signals > 0 and close_signals == 0:
            print("🎯 МНОГО OPEN, НЕТ CLOSE - проверьте логику закрытия")

        if open_signals == 0:
            print("🔍 НЕТ СИГНАЛОВ - проверьте условия стратегии")

    except Exception as e:
        print(f"❌ Ошибка чтения лога: {e}")


if __name__ == "__main__":
    check_logs()