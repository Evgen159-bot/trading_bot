#!/usr/bin/env python3
"""
Анализ результатов работы торгового бота
"""

import os
import json
from datetime import datetime, date
from pathlib import Path


def analyze_bot_results():
    """Анализ результатов работы бота"""
    print("📊 АНАЛИЗ РЕЗУЛЬТАТОВ РАБОТЫ БОТА")
    print("=" * 60)

    # 1. Проверка логов
    print("\n📄 АНАЛИЗ ЛОГОВ:")
    log_file = f"logs/trading_{datetime.now().strftime('%Y%m%d')}.log"

    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total_lines = len(lines)
        errors = len([l for l in lines if "ERROR" in l])
        open_signals = len([l for l in lines if "Strategy result" in l and "OPEN" in l])
        close_signals = len([l for l in lines if "Strategy result" in l and "CLOSE" in l])
        cycles = len([l for l in lines if "Trading cycle started" in l])

        print(f"   📝 Всего записей: {total_lines}")
        print(f"   🔄 Торговых циклов: {cycles}")
        print(f"   📈 OPEN сигналов: {open_signals}")
        print(f"   📉 CLOSE сигналов: {close_signals}")
        print(f"   ❌ Ошибок: {errors}")

        # Показываем последние сигналы
        print(f"\n🎯 ПОСЛЕДНИЕ СИГНАЛЫ:")
        signal_lines = [l for l in lines if "Strategy result" in l][-10:]
        for line in signal_lines:
            print(f"   {line.strip()}")

        # Показываем последние ошибки
        if errors > 0:
            print(f"\n🚨 ПОСЛЕДНИЕ ОШИБКИ:")
            error_lines = [l for l in lines if "ERROR" in l][-5:]
            for line in error_lines:
                print(f"   {line.strip()}")
    else:
        print(f"   ❌ Лог файл не найден: {log_file}")

    # 2. Проверка дневника
    print(f"\n📔 АНАЛИЗ ДНЕВНИКА:")
    diary_file = f"data/diary/diary_{date.today().isoformat()}.json"

    if os.path.exists(diary_file):
        with open(diary_file, 'r', encoding='utf-8') as f:
            diary_data = json.load(f)

        start_balance = diary_data.get('start_balance', 0)
        current_balance = diary_data.get('current_balance', 0)
        daily_return = diary_data.get('daily_return', 0)
        trades = diary_data.get('trades', [])
        positions = diary_data.get('positions', [])

        print(f"   💰 Начальный баланс: ${start_balance:.2f}")
        print(f"   💰 Текущий баланс: ${current_balance:.2f}")
        print(f"   📈 Дневной результат: ${daily_return:.2f}")
        print(f"   📊 Всего сделок: {len(trades)}")
        print(f"   🔄 Позиций: {len(positions)}")

        # Детали сделок
        if trades:
            print(f"\n💼 ДЕТАЛИ СДЕЛОК:")
            for i, trade in enumerate(trades, 1):
                pnl_emoji = "💚" if trade.get('net_pnl', 0) > 0 else "❤️"
                print(f"   {i}. {trade['symbol']} {trade['direction']} | "
                      f"{pnl_emoji} ${trade.get('net_pnl', 0):.2f} | "
                      f"ROI: {trade.get('roi_pct', 0):+.2f}%")

        # Открытые позиции
        open_positions = [p for p in positions if p.get('status') == 'OPEN']
        if open_positions:
            print(f"\n🔄 ОТКРЫТЫЕ ПОЗИЦИИ:")
            for pos in open_positions:
                print(f"   • {pos['symbol']} {pos['direction']} | "
                      f"Размер: {pos['size']} | "
                      f"Цена: ${pos['entry_price']:.4f}")
    else:
        print(f"   ❌ Дневник не найден: {diary_file}")

    # 3. Рекомендации
    print(f"\n💡 РЕКОМЕНДАЦИИ:")

    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Анализ проблем
        if "Volume Ratio: 0.00" in content:
            print("   📊 Объем = 0 во всех парах - это нормально для TESTNET")

        if "LONG ANALYSIS: 2.0/1 conditions met" in content:
            print("   ✅ Сигналы генерируются - стратегия работает!")

        if "balance=0.0" in content:
            print("   💰 Используется fallback баланс - API ключи могут быть новыми")

        open_attempts = content.count("ATTEMPTING TO OPEN POSITION")
        if open_attempts > 0:
            print(f"   🎯 Попыток открыть позицию: {open_attempts}")

        if "TESTNET ORDER PLACED" in content:
            print("   ✅ Ордера размещались успешно!")
        elif open_attempts > 0:
            print("   ⚠️ Попытки были, но ордера не размещались - проверим логику")

    print(f"\n🎯 СЛЕДУЮЩИЕ ШАГИ:")
    print("   1. Проверьте дневник: python utils/diary_viewer.py")
    print("   2. Анализ логов: python utils/log_analyzer.py")
    print("   3. Если нет сделок - снизим требования в user_config.py")


if __name__ == "__main__":
    analyze_bot_results()