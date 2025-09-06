#!/usr/bin/env python3
"""
Анализатор логов для выявления проблем и паттернов
"""

import re
from datetime import datetime
from collections import Counter
from pathlib import Path


class LogAnalyzer:
    """Анализатор логов торгового бота"""

    def __init__(self, log_file: str = None):
        if log_file is None:
            log_file = f"logs/trading_{datetime.now().strftime('%Y%m%d')}.log"
        self.log_file = Path(log_file)

    def analyze_logs(self):
        """Полный анализ логов"""
        if not self.log_file.exists():
            print(f"❌ Лог файл не найден: {self.log_file}")
            return

        print("📊 АНАЛИЗ ЛОГОВ ТОРГОВОГО БОТА")
        print("=" * 50)

        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Основная статистика
        self._analyze_basic_stats(lines)

        # Анализ ошибок
        self._analyze_errors(lines)

        # Анализ сигналов
        self._analyze_signals(lines)

        # Анализ производительности
        self._analyze_performance(lines)

        # Рекомендации
        self._provide_recommendations(lines)

    def _analyze_basic_stats(self, lines):
        """Базовая статистика"""
        print("\n📈 БАЗОВАЯ СТАТИСТИКА:")

        total_lines = len(lines)
        info_lines = len([l for l in lines if ' - INFO - ' in l])
        error_lines = len([l for l in lines if ' - ERROR - ' in l])
        warning_lines = len([l for l in lines if ' - WARNING - ' in l])

        print(f"   Всего записей: {total_lines}")
        print(f"   INFO: {info_lines}")
        print(f"   ERROR: {error_lines}")
        print(f"   WARNING: {warning_lines}")

        # Анализ циклов
        cycle_starts = len([l for l in lines if 'Trading cycle started' in l])
        processed_pairs = len([l for l in lines if 'Processed 4/4 pairs' in l])

        print(f"   Торговых циклов: {cycle_starts}")
        print(f"   Завершенных циклов: {processed_pairs}")

        if processed_pairs > 0:
            # Анализ времени выполнения
            times = []
            for line in lines:
                if 'Processed 4/4 pairs in' in line:
                    match = re.search(r'in (\d+\.\d+)s', line)
                    if match:
                        times.append(float(match.group(1)))

            if times:
                avg_time = sum(times) / len(times)
                print(f"   Среднее время цикла: {avg_time:.2f}с")
                print(f"   Мин/Макс время: {min(times):.2f}с / {max(times):.2f}с")

    def _analyze_errors(self, lines):
        """Анализ ошибок"""
        print("\n🚨 АНАЛИЗ ОШИБОК:")

        errors = [l for l in lines if ' - ERROR - ' in l]

        if not errors:
            print("   ✅ Ошибок не найдено")
            return

        # Группировка ошибок
        error_types = Counter()
        for error in errors:
            if 'account balance' in error.lower():
                error_types['Account Balance Error'] += 1
            elif 'api' in error.lower():
                error_types['API Error'] += 1
            elif 'connection' in error.lower():
                error_types['Connection Error'] += 1
            else:
                error_types['Other Error'] += 1

        print(f"   Всего ошибок: {len(errors)}")
        for error_type, count in error_types.most_common():
            print(f"   {error_type}: {count}")

        # Показываем последние ошибки
        print(f"\n   📋 Последние ошибки:")
        for error in errors[-3:]:
            timestamp = error.split(' - ')[0]
            message = error.split(' - ERROR - ')[1].strip()
            print(f"      {timestamp}: {message}")

    def _analyze_signals(self, lines):
        """Анализ торговых сигналов"""
        print("\n🎯 АНАЛИЗ ТОРГОВЫХ СИГНАЛОВ:")

        # Подсчет сигналов OPEN
        open_signals = [l for l in lines if 'Strategy result for' in l and ': OPEN' in l]

        # Группировка по парам
        pair_signals = Counter()
        for signal in open_signals:
            for pair in ['ETHUSDT', 'SOLUSDT', 'BTCUSDT', 'DOGEUSDT']:
                if pair in signal:
                    pair_signals[pair] += 1
                    break

        print(f"   Всего OPEN сигналов: {len(open_signals)}")

        if pair_signals:
            print(f"   По парам:")
            for pair, count in pair_signals.most_common():
                print(f"      {pair}: {count} сигналов")
        else:
            print("   ❌ Сигналы OPEN не найдены")

        # Анализ частоты сигналов
        if open_signals:
            # Извлекаем временные метки
            timestamps = []
            for signal in open_signals:
                time_str = signal.split(' - ')[0]
                try:
                    timestamp = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                    timestamps.append(timestamp)
                except:
                    pass

            if len(timestamps) > 1:
                time_diff = (timestamps[-1] - timestamps[0]).total_seconds()
                frequency = len(timestamps) / (time_diff / 60)  # сигналов в минуту
                print(f"   Частота сигналов: {frequency:.2f} сигналов/мин")

    def _analyze_performance(self, lines):
        """Анализ производительности"""
        print("\n⚡ АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ:")

        # Анализ времени выполнения циклов
        execution_times = []
        for line in lines:
            if 'Processed 4/4 pairs in' in line:
                match = re.search(r'in (\d+\.\d+)s', line)
                if match:
                    execution_times.append(float(match.group(1)))

        if execution_times:
            avg_time = sum(execution_times) / len(execution_times)
            print(f"   Среднее время цикла: {avg_time:.2f}с")

            # Классификация производительности
            fast_cycles = len([t for t in execution_times if t < 10])
            slow_cycles = len([t for t in execution_times if t > 30])

            print(f"   Быстрые циклы (<10с): {fast_cycles}")
            print(f"   Медленные циклы (>30с): {slow_cycles}")

            if slow_cycles > fast_cycles:
                print("   ⚠️ Много медленных циклов - возможны проблемы с API")

        # Анализ баланса
        balance_lines = [l for l in lines if 'Account balance:' in l]
        if balance_lines:
            print(f"   Проверок баланса: {len(balance_lines)}")
            # Извлекаем последний баланс
            last_balance_line = balance_lines[-1]
            match = re.search(r'\$(\d+\.\d+)', last_balance_line)
            if match:
                balance = float(match.group(1))
                print(f"   Последний баланс: ${balance:.2f}")

    def _provide_recommendations(self, lines):
        """Рекомендации по улучшению"""
        print("\n💡 РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ:")

        errors = [l for l in lines if ' - ERROR - ' in l]
        open_signals = [l for l in lines if 'Strategy result for' in l and ': OPEN' in l]

        # Проблема с балансом
        balance_errors = [e for e in errors if 'account balance' in e.lower()]
        if balance_errors:
            print("   🔧 Исправить ошибку получения баланса:")
            print("      - Проверить API ключи")
            print("      - Добавить fallback для testnet")

        # Слишком много сигналов OPEN
        if len(open_signals) > 50:
            print("   ⚠️ Слишком много OPEN сигналов:")
            print("      - Увеличить min_conditions_required")
            print("      - Добавить cooldown между сигналами")
            print("      - Ужесточить фильтры")

        # Нет реальных сделок
        close_signals = [l for l in lines if 'Strategy result for' in l and ': CLOSE' in l]
        if len(open_signals) > 0 and len(close_signals) == 0:
            print("   🎯 Много OPEN, но нет CLOSE сигналов:")
            print("      - Проверить логику закрытия позиций")
            print("      - Добавить таймауты для позиций")
            print("      - Проверить условия выхода")


def main():
    """Главная функция"""
    analyzer = LogAnalyzer()
    analyzer.analyze_logs()


if __name__ == "__main__":
    main()