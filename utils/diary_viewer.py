"""
Утилита для просмотра дневника трейдинга
🎯 Способы просмотра дневника:
1. Через утилиту просмотра дневника:
python utils/diary_viewer.py
Эта утилита предоставляет интерактивное меню:
📅 Показать сегодняшний день
📋 Показать конкретный день
📊 Недельная сводка
📂 Список доступных дней
Для экспорта в Excel/CSV:
# В Python консоли или скрипте
from utils.diary_viewer import DiaryViewer
viewer = DiaryViewer()
# Экспорт будет в папке data/diary/
"""
import json
import os
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd


class DiaryViewer:
    """Просмотрщик дневника трейдинга"""

    def __init__(self):
        self.diary_dir = Path("data/diary")

    def show_today(self) -> None:
        """Показать сегодняшний дневник"""
        today = date.today()
        self.show_day(today)

    def show_day(self, target_date: date) -> None:
        """Показать дневник за конкретный день"""
        try:
            filename = f"diary_{target_date.isoformat()}.json"
            filepath = self.diary_dir / filename

            if not filepath.exists():
                print(f"❌ Дневник за {target_date.strftime('%d.%m.%Y')} не найден")
                return

            with open(filepath, 'r', encoding='utf-8') as f:
                day_data = json.load(f)

            self._print_day_report(day_data)

        except Exception as e:
            print(f"❌ Ошибка при чтении дневника: {e}")

    def show_week(self) -> None:
        """Показать недельную сводку"""
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=7)

            print("\n" + "=" * 70)
            print("📊 НЕДЕЛЬНАЯ СВОДКА ТРЕЙДИНГА")
            print("=" * 70)
            print(f"📅 Период: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}")
            print("-" * 70)

            total_return = 0.0
            total_trades = 0
            trading_days = 0
            daily_returns = []

            current_date = start_date
            while current_date <= end_date:
                filename = f"diary_{current_date.isoformat()}.json"
                filepath = self.diary_dir / filename

                if filepath.exists():
                    with open(filepath, 'r', encoding='utf-8') as f:
                        day_data = json.load(f)

                    daily_return = day_data.get('daily_return', 0.0)
                    trades_count = day_data.get('daily_stats', {}).get('total_trades', 0)

                    total_return += daily_return
                    total_trades += trades_count
                    trading_days += 1
                    daily_returns.append(daily_return)

                    return_emoji = "📈" if daily_return >= 0 else "📉"
                    print(
                        f"{current_date.strftime('%d.%m')}: {return_emoji} ${daily_return:+.2f} | Сделок: {trades_count}")

                current_date += timedelta(days=1)

            print("-" * 70)
            print(f"💰 Общий результат: ${total_return:+.2f}")
            print(f"📊 Всего сделок: {total_trades}")
            print(f"📅 Торговых дней: {trading_days}")

            if trading_days > 0:
                avg_daily = total_return / trading_days
                print(f"📈 Средний дневной результат: ${avg_daily:+.2f}")

                profitable_days = len([r for r in daily_returns if r > 0])
                win_rate = (profitable_days / trading_days) * 100
                print(f"🎯 Прибыльных дней: {profitable_days}/{trading_days} ({win_rate:.1f}%)")

            print("=" * 70)

        except Exception as e:
            print(f"❌ Ошибка при генерации недельной сводки: {e}")

    def _print_day_report(self, day_data: Dict[str, Any]) -> None:
        """Печать дневного отчета"""
        try:
            date_str = datetime.fromisoformat(day_data['date']).strftime('%d.%m.%Y')

            print("\n" + "=" * 60)
            print(f"📔 ДНЕВНИК ТРЕЙДИНГА - {date_str}")
            print("=" * 60)

            # Время сессии
            if day_data.get('session_start'):
                start_time = datetime.fromisoformat(day_data['session_start']).strftime('%H:%M')
                end_time = "активна"
                if day_data.get('session_end'):
                    end_time = datetime.fromisoformat(day_data['session_end']).strftime('%H:%M')
                print(f"⏰ Время сессии: {start_time} - {end_time}")

            # Баланс
            start_balance = day_data.get('start_balance', 0.0)
            end_balance = day_data.get('end_balance', day_data.get('current_balance', 0.0))
            daily_return = day_data.get('daily_return', end_balance - start_balance)
            return_pct = day_data.get('daily_return_pct', 0.0)

            print(f"💰 Начальный баланс: ${start_balance:.2f}")
            print(f"💰 Конечный баланс: ${end_balance:.2f}")

            return_emoji = "📈" if daily_return >= 0 else "📉"
            print(f"{return_emoji} Результат дня: ${daily_return:+.2f} ({return_pct:+.2f}%)")

            print("-" * 60)

            # Статистика сделок
            stats = day_data.get('daily_stats', {})
            total_trades = stats.get('total_trades', 0)

            if total_trades > 0:
                print("📊 СТАТИСТИКА СДЕЛОК:")
                print(f"   Всего сделок: {total_trades}")
                print(f"   Прибыльных: {stats.get('winning_trades', 0)} ({stats.get('win_rate', 0):.1f}%)")
                print(f"   Убыточных: {stats.get('losing_trades', 0)}")
                print(f"   Общий P&L: ${stats.get('total_pnl', 0):.2f}")
                print(f"   Комиссии: ${stats.get('total_fees', 0):.2f}")

                if stats.get('max_profit', 0) > 0:
                    print(f"   Лучшая сделка: ${stats.get('max_profit', 0):.2f}")
                if stats.get('max_loss', 0) < 0:
                    print(f"   Худшая сделка: ${stats.get('max_loss', 0):.2f}")

                print("-" * 60)

            # Детали сделок
            trades = day_data.get('trades', [])
            if trades:
                print("📈 ДЕТАЛИ СДЕЛОК:")
                for i, trade in enumerate(trades, 1):
                    pnl_emoji = "💚" if trade.get('net_pnl', 0) > 0 else "❤️"
                    open_time = datetime.fromisoformat(trade['open_time']).strftime('%H:%M')
                    close_time = datetime.fromisoformat(trade['close_time']).strftime('%H:%M')

                    print(f"   {i}. {trade['symbol']} {trade['direction']}")
                    print(f"      ⏰ {open_time} - {close_time} ({trade.get('duration', 'N/A')})")
                    print(f"      💵 ${trade['entry_price']:.4f} → ${trade['exit_price']:.4f}")
                    print(
                        f"      {pnl_emoji} P&L: ${trade.get('net_pnl', 0):.2f} | ROI: {trade.get('roi_pct', 0):+.2f}%")
                    print(f"      📝 Причина: {trade.get('close_reason', 'N/A')}")
                    print()

            # Открытые позиции
            positions = day_data.get('positions', [])
            open_positions = [p for p in positions if p.get('status') == 'OPEN']

            if open_positions:
                print("🔄 ОТКРЫТЫЕ ПОЗИЦИИ:")
                for pos in open_positions:
                    open_time = datetime.fromisoformat(pos['open_time']).strftime('%H:%M')
                    print(f"   • {pos['symbol']} {pos['direction']} | "
                          f"Размер: {pos['size']} | "
                          f"Цена: ${pos['entry_price']:.4f} | "
                          f"Время: {open_time}")
                print()

            print("=" * 60)

        except Exception as e:
            print(f"❌ Ошибка при печати отчета: {e}")

    def list_available_days(self, days: int = 30) -> None:
        """Показать доступные дни в дневнике"""
        try:
            print("\n📅 ДОСТУПНЫЕ ДНИ В ДНЕВНИКЕ:")
            print("-" * 40)

            end_date = date.today()
            start_date = end_date - timedelta(days=days)

            available_days = []
            current_date = start_date

            while current_date <= end_date:
                filename = f"diary_{current_date.isoformat()}.json"
                filepath = self.diary_dir / filename

                if filepath.exists():
                    available_days.append(current_date)

                current_date += timedelta(days=1)

            if available_days:
                for day in sorted(available_days, reverse=True):
                    print(f"📔 {day.strftime('%d.%m.%Y (%A)')}")
            else:
                print("❌ Нет доступных записей в дневнике")

            print("-" * 40)

        except Exception as e:
            print(f"❌ Ошибка при получении списка дней: {e}")


def main():
    """Главная функция для просмотра дневника"""
    viewer = DiaryViewer()

    while True:
        print("\n📔 ПРОСМОТР ДНЕВНИКА ТРЕЙДИНГА")
        print("1. Показать сегодня")
        print("2. Показать конкретный день")
        print("3. Недельная сводка")
        print("4. Список доступных дней")
        print("0. Выход")

        choice = input("\nВыберите опцию: ").strip()

        if choice == "1":
            viewer.show_today()
        elif choice == "2":
            date_str = input("Введите дату (YYYY-MM-DD): ").strip()
            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                viewer.show_day(target_date)
            except ValueError:
                print("❌ Неверный формат даты")
        elif choice == "3":
            viewer.show_week()
        elif choice == "4":
            viewer.list_available_days()
        elif choice == "0":
            break
        else:
            print("❌ Неверный выбор")


if __name__ == "__main__":
    main()