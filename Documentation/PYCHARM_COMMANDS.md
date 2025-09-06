# 🖥️ Справка по командам PyCharm для торгового бота (2025)

## 📋 Содержание

- [🚀 Основные команды запуска](#-основные-команды-запуска)
- [🔧 Новые инструменты отладки (2025)](#-новые-инструменты-отладки-2025)
- [🔍 Диагностика и отладка](#-диагностика-и-отладка)
- [📊 Мониторинг и анализ](#-мониторинг-и-анализ)
- [⚙️ Настройка и конфигурация](#️-настройка-и-конфигурация)
- [🧪 Тестирование](#-тестирование)
- [📁 Управление файлами](#-управление-файлами)
- [🆘 Устранение неполадок](#-устранение-неполадок)

---

## 🚀 Основные команды запуска

### Запуск торгового бота

```bash
# Основной запуск бота
python main.py

# Запуск с детальным логированием
python -u main.py

# Запуск в фоновом режиме (Windows)
start /B python main.py

# Проверка перед запуском
python user_config.py && python main.py
```

### Остановка бота

```bash
# Graceful shutdown (в терминале с ботом)
Ctrl+C

# Принудительная остановка процесса
# Найти процесс: tasklist | findstr python
# Убить процесс: taskkill /PID <process_id> /F
```

---

## 🔧 Новые инструменты отладки (2025)

### 🎯 **Детальная отладка стратегий:**

```bash
# Детальная отладка конкретной пары
python utils/strategy_debug_tool.py ETHUSDT

# Отладка всех активных пар
python utils/strategy_debug_tool.py

# Что показывает:
# - Все рассчитанные индикаторы (RSI, MACD, EMA, Volume)
# - Детальный анализ условий входа для Long/Short
# - Причины отсутствия сигналов
# - Рекомендации по оптимизации параметров

# Пример использования:
# 🔍 ДЕТАЛЬНАЯ ОТЛАДКА СИГНАЛОВ ДЛЯ ETHUSDT
# ✅ Индикаторы рассчитаны: 10 значений
#    RSI: 45.2
#    MACD: 0.000123 vs Signal: 0.000156
#    Volume Ratio: 0.85
# 
# 🎯 АНАЛИЗ УСЛОВИЙ:
#    Long условия: 2.0/3 выполнено (нужно 3)
#    Long валидность: ❌ Нет
# 
# 💡 РЕКОМЕНДАЦИИ:
#    - Снизьте min_conditions_required до 2
#    - Снизьте min_ratio до 0.8
```

### 📊 **Анализ логов:**

```bash
# Полный анализ логов с рекомендациями
python utils/log_analyzer.py

# Анализ конкретного файла
python utils/log_analyzer.py logs/trading_20250901.log

# Что показывает:
# - Статистику ошибок и предупреждений
# - Частоту генерации сигналов
# - Производительность торговых циклов
# - Рекомендации по улучшению

# Пример использования:
# 📊 АНАЛИЗ ЛОГОВ ТОРГОВОГО БОТА
# 📈 БАЗОВАЯ СТАТИСТИКА:
#    Всего записей: 29275
#    ERROR: 55
#    OPEN сигналов: 8
#    CLOSE сигналов: 558
#    Торговых циклов: 1497
#    Среднее время цикла: 6.45с
# 
# 💡 РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ:
#    🔧 Для увеличения количества сигналов:
#       - Снизьте min_conditions_required до 2
#       - Снизьте min_ratio до 0.8
```

### 🎯 **Оптимизация объемов:**

```bash
# Анализ объемных паттернов
python utils/volume_optimizer.py

# Что показывает:
# - Анализ объемных паттернов для каждой пары
# - Процент свечей с достаточным объемом
# - Рекомендации по настройке min_ratio
# - Оптимальные пороги фильтров

# Пример использования:
# 📊 АНАЛИЗ ОБЪЕМНЫХ ПАТТЕРНОВ
# 
# 📈 Анализ ETHUSDT:
#    📊 Средний Volume Ratio: 1.15
#    ✅ Свечей с объемом > 1.1: 35.2%
#    ✅ Свечей с объемом > 0.8: 67.8%
#    💡 Рекомендация: Снизить min_ratio до 0.8
# 
# 💡 РЕКОМЕНДАЦИИ ПО ОПТИМИЗАЦИИ:
# 1. 📉 Снизить требования к объему:
#    'min_ratio': 0.8,  # Вместо 1.5
# 2. 🎯 Снизить требования к условиям:
#    'min_conditions_required': 2,  # Вместо 3
```

### 🔍 **Быстрая проверка:**

```bash
# Быстрый анализ без загрузки больших файлов
python utils/simple_log_check.py

# Что показывает:
# - Статистику последних записей
# - Количество OPEN/CLOSE сигналов
# - Последние 30 записей с цветовым выделением
# - Быстрые рекомендации

# Пример использования:
# 🔍 БЫСТРЫЙ АНАЛИЗ ЛОГОВ
# 📊 СТАТИСТИКА:
#    Всего записей: 29275
#    Ошибок: 55
#    OPEN сигналов: 8
#    CLOSE сигналов: 558
# 
# 🎯 АНАЛИЗ ПАТТЕРНОВ СИГНАЛОВ:
#    ETHUSDT: OPEN=3, CLOSE=180, NO_ACTION=1314
#    🚨 DOGEUSDT: Много OPEN, нет CLOSE - проблема с логикой!
```

### 📊 **Анализ результатов работы:**

```bash
# Полный анализ результатов работы бота
python check_results.py

# Что показывает:
# - Анализ логов за день
# - Статистику сигналов и ошибок
# - Данные дневника торговли
# - Рекомендации по улучшению

# Пример использования:
# 📊 АНАЛИЗ РЕЗУЛЬТАТОВ РАБОТЫ БОТА
# 📄 АНАЛИЗ ЛОГОВ:
#    📝 Всего записей: 29275
#    🔄 Торговых циклов: 1497
#    📈 OPEN сигналов: 8
#    📉 CLOSE сигналов: 558
# 
# 📔 АНАЛИЗ ДНЕВНИКА:
#    💰 Начальный баланс: $1100.00
#    💰 Текущий баланс: $-1868.42
#    📈 Дневной результат: $-2968.42
#    📊 Всего сделок: 13
# 
# 💡 РЕКОМЕНДАЦИИ:
#    ✅ Сигналы генерируются - стратегия работает!
#    🎯 Попыток открыть позицию: 8
#    ⚠️ Проблемы с расчетом PnL - исправлено в 2025
```

---

## 🔍 Диагностика и отладка

### Проверка конфигурации

```bash
# Валидация пользовательской конфигурации
python user_config.py

# Показать все доступные стратегии
python user_config.py --strategies

# Проверка API подключения
python -c "from modules.data_fetcher import DataFetcher; df = DataFetcher(); print('✅ API работает' if df.health_check() else '❌ Проблемы с API')"

# Полная диагностика системы
python -c "
print('🔍 ДИАГНОСТИКА ТОРГОВОГО БОТА')
print('=' * 50)

# 1. Проверка Python
import sys
print(f'Python версия: {sys.version.split()[0]}')

# 2. Проверка модулей
modules = ['pandas', 'numpy', 'ta', 'pybit', 'requests']
for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}')
    except ImportError:
        print(f'❌ {module} - НЕ УСТАНОВЛЕН')

# 3. Проверка конфигурации
try:
    from user_config import UserConfig
    is_valid, errors = UserConfig.validate_config()
    print(f'✅ Конфигурация: {\"OK\" if is_valid else \"ОШИБКИ\"}')
    if errors:
        for error in errors[:3]:
            print(f'  ❌ {error}')
except Exception as e:
    print(f'❌ Ошибка конфигурации: {e}')

print('=' * 50)
"
```

### Отладка стратегий

```bash
# 🔧 НОВЫЕ инструменты отладки (2025):

# Детальная отладка стратегии
python utils/strategy_debug_tool.py ETHUSDT

# Анализ логов
python utils/log_analyzer.py

# Оптимизация объемов
python utils/volume_optimizer.py

# Быстрая проверка
python utils/simple_log_check.py

# Анализ результатов
python check_results.py

# 📊 СТАНДАРТНЫЕ инструменты:

# Простой тест стратегии
python utils/simple_strategy_test.py

# Полная отладка стратегии
python utils/debug_strategy.py --all

# Отладка конкретной пары
python utils/debug_strategy.py --symbol=ETHUSDT

# Анализ рыночных условий
python utils/debug_strategy.py --market

# Тест анализатора рынка
python utils/market_analyzer_test.py

# Тест с сигналами
python utils/market_analyzer_test.py --signals
```

---

## 📊 Мониторинг и анализ

### Просмотр дневника торговли (ОБНОВЛЕНО 2025)

```bash
# 📔 Интерактивный просмотр дневника
python utils/diary_viewer.py

# Быстрые команды
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_today()"
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_week()"
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().list_available_days()"

# Проверка логов дневника
python -c "
import os
from datetime import datetime
log_file = f'logs/trading_diary/diary_log_{datetime.now().strftime(\"%Y%m%d\")}.log'
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print('📔 ПОСЛЕДНИЕ 20 ЗАПИСЕЙ ДНЕВНИКА:')
        for line in lines[-20:]:
            print(line.strip())
else:
    print('❌ Лог дневника не найден')
"

# Экспорт дневника в CSV
python -c "
from modules.trading_diary import TradingDiary
diary = TradingDiary()
export_path = diary.export_diary_to_csv(30)  # За 30 дней
print(f'📊 Дневник экспортирован: {export_path}' if export_path else '❌ Ошибка экспорта')
"

# Конкретный день (замените дату)
python -c "
from utils.diary_viewer import DiaryViewer
from datetime import date
viewer = DiaryViewer()
viewer.show_day(date(2025, 9, 1))
"
```

### Статус бота

```bash
# Проверка статуса бота (если запущен)
python -c "
from main import TradingBot
try:
    bot = TradingBot()
    status = bot.get_bot_status()
    print(f'🤖 Статус: {\"Работает\" if status[\"is_running\"] else \"Остановлен\"}')
    print(f'🔄 Циклов: {status[\"cycle_count\"]}')
    print(f'🎯 Стратегия: {status[\"strategy_name\"]}')
    print(f'📊 Торговых пар: {len(status[\"trading_pairs\"])}')
except Exception as e:
    print(f'❌ Ошибка: {e}')
"

# Валидация стратегии
python -c "
from main import TradingBot
bot = TradingBot()
result = bot.run_strategy_validation()
print(f'Валидация: Score {result.get(\"score\", 0)}/100')
"

# Статистика производительности стратегии
python -c "
from main import TradingBot
bot = TradingBot()
stats = bot.get_strategy_performance()
print(f'Статистика стратегии: {stats}')
"
```

### Просмотр логов

```bash
# 🔧 НОВЫЕ команды для анализа логов (2025):

# Быстрая проверка логов
python utils/simple_log_check.py

# Полный анализ логов
python utils/log_analyzer.py

# 📊 СТАНДАРТНЫЕ команды:

# Последние 50 строк основного лога
python -c "
import os
from datetime import datetime
log_file = f'logs/trading_{datetime.now().strftime(\"%Y%m%d\")}.log'
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[-50:]:
            print(line.strip())
else:
    print('❌ Лог файл не найден')
"

# Поиск ошибок в логах
python -c "
import os
from datetime import datetime
log_file = f'logs/trading_{datetime.now().strftime(\"%Y%m%d\")}.log'
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        errors = [line for line in lines if 'ERROR' in line or 'CRITICAL' in line]
        if errors:
            print('🚨 НАЙДЕННЫЕ ОШИБКИ:')
            for error in errors[-10:]:
                print(error.strip())
        else:
            print('✅ Ошибок не найдено')
else:
    print('❌ Лог файл не найден')
"

# Статистика сигналов
python -c "
import os
from datetime import datetime
log_file = f'logs/trading_{datetime.now().strftime(\"%Y%m%d\")}.log'
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
        long_signals = content.count('CUSTOM LONG signal')
        short_signals = content.count('CUSTOM SHORT signal')
        print(f'📊 Сигналы за день:')
        print(f'   📈 Long: {long_signals}')
        print(f'   📉 Short: {short_signals}')
        print(f'   📊 Всего: {long_signals + short_signals}')
else:
    print('❌ Лог файл не найден')
"
```

---

## ⚙️ Настройка и конфигурация

### Выбор стратегий

```bash
# Интерактивный выбор стратегии
python utils/strategy_selector.py --interactive

# Список всех стратегий
python utils/strategy_selector.py --list

# Настройка пользовательской стратегии
python utils/strategy_selector.py --custom
```

### Проверка торговых пар

```bash
# Активные торговые пары
python -c "
from user_config import UserConfig
enabled = UserConfig.get_enabled_pairs()
print(f'Активных пар: {len(enabled)}/7')
for pair, config in enabled.items():
    print(f'• {pair}: {config[\"weight\"]*100:.0f}% портфеля, плечо {config[\"leverage\"]}x')
"

# Все доступные пары
python -c "
from user_config import UserConfig
print('📊 Все доступные пары:')
for pair, config in UserConfig.TRADING_PAIRS.items():
    status = '✅ Включена' if config['enabled'] else '❌ Отключена'
    print(f'• {pair}: {status} | {config.get(\"description\", \"Нет описания\")}')
"

# Проверка весов портфеля
python -c "
from user_config import UserConfig
enabled = UserConfig.get_enabled_pairs()
total_weight = sum(config['weight'] for config in enabled.values())
print(f'📊 Сумма весов: {total_weight:.2f} (должно быть 1.0)')
if abs(total_weight - 1.0) > 0.01:
    print('⚠️ Веса портфеля не равны 1.0!')
else:
    print('✅ Веса портфеля корректны')
"
```

### Настройка рисков

```bash
# Текущие настройки рисков
python -c "
from user_config import UserConfig
risk = UserConfig.RISK_SETTINGS
print('🛡️ НАСТРОЙКИ РИСКОВ:')
print(f'   Риск на сделку: {risk[\"risk_per_trade\"]*100:.1f}%')
print(f'   Макс. дневная потеря: {risk[\"max_daily_loss\"]*100:.1f}%')
print(f'   Макс. позиций: {risk[\"max_positions\"]}')
print(f'   Макс. сделок в день: {risk[\"max_daily_trades\"]}')
print(f'   Макс. плечо: {risk[\"max_leverage\"]}x')
"

# Проверка баланса
python -c "
from user_config import UserConfig
print(f'💰 Начальный баланс: ${UserConfig.INITIAL_BALANCE:,.2f}')
print(f'🚨 Минимальный порог: ${UserConfig.MIN_BALANCE_THRESHOLD:,.2f}')
print(f'🔑 Режим: {\"TESTNET\" if UserConfig.USE_TESTNET else \"РЕАЛЬНАЯ ТОРГОВЛЯ\"}')
"
```

---

## 🧪 Тестирование

### Тестирование компонентов

```bash
# 🔧 НОВЫЕ тесты (2025):

# Простое тестирование стратегии
python utils/simple_strategy_test.py

# Детальная отладка стратегии
python utils/strategy_debug_tool.py ETHUSDT

# 📊 СТАНДАРТНЫЕ тесты:

# Тест получения данных
python -c "
from modules.data_fetcher import DataFetcher
from datetime import datetime, timedelta
df = DataFetcher()
end_time = datetime.now()
start_time = end_time - timedelta(hours=1)
data = df.get_kline('ETHUSDT', '5', int(start_time.timestamp()), int(end_time.timestamp()))
print(f'✅ Получено {len(data) if data is not None else 0} свечей')
"

# Тест баланса
python -c "
from modules.data_fetcher import DataFetcher
df = DataFetcher()
balance = df.get_account_balance()
print(f'💰 Баланс: ${balance:.2f}' if balance else '❌ Ошибка получения баланса')
"

# Тест цен
python -c "
from modules.data_fetcher import DataFetcher
from user_config import UserConfig
df = DataFetcher()
enabled_pairs = UserConfig.get_enabled_pairs()
print('📊 ТЕКУЩИЕ ЦЕНЫ:')
for symbol in enabled_pairs:
    price = df.get_current_price(symbol)
    print(f'   {symbol}: ${price:.4f}' if price else f'   {symbol}: ❌ Ошибка')
"

# Тест стратегии
python -c "
from config_loader import load_user_configuration
try:
    loader = load_user_configuration()
    print('✅ Стратегия загружена успешно')
    print(f'🎯 Выбранная стратегия: {loader.get_strategy_name()}')
except Exception as e:
    print(f'❌ Ошибка стратегии: {e}')
"
```

### Валидация стратегии

```bash
# Запуск валидации
python -c "
from main import TradingBot
bot = TradingBot()
result = bot.run_strategy_validation(strict_mode=False)
print(f'📊 Результат валидации:')
print(f'   Валидна: {\"✅ Да\" if result.get(\"is_valid\") else \"❌ Нет\"}')
print(f'   Балл: {result.get(\"score\", 0)}/100')
if result.get(\"errors\"):
    print(f'   Ошибки: {len(result[\"errors\"])}')
if result.get(\"recommendations\"):
    print(f'   Рекомендации: {len(result[\"recommendations\"])}')
"

# Строгая валидация
python -c "
from main import TradingBot
bot = TradingBot()
result = bot.run_strategy_validation(strict_mode=True)
print(f'🔍 Строгая валидация: {\"PASSED\" if result.get(\"is_valid\") else \"FAILED\"}')
"
```

---

## 📊 Мониторинг и анализ

### Анализ производительности

```bash
# 🔧 НОВЫЕ команды анализа (2025):

# Полный анализ результатов
python check_results.py

# Анализ дневника торговли
python utils/diary_viewer.py

# 📊 СТАНДАРТНЫЕ команды:

# Метрики производительности
python -c "
from modules.performance_tracker import PerformanceTracker
tracker = PerformanceTracker()
metrics = tracker.get_performance_metrics()
print('📊 МЕТРИКИ ПРОИЗВОДИТЕЛЬНОСТИ:')
print(f'   Общий P&L: ${metrics.get(\"total_pnl\", 0):.2f}')
print(f'   Win Rate: {metrics.get(\"win_rate\", 0):.1f}%')
print(f'   Всего сделок: {metrics.get(\"total_trades\", 0)}')
print(f'   Лучшая сделка: ${metrics.get(\"best_trade\", 0):.2f}')
print(f'   Худшая сделка: ${metrics.get(\"worst_trade\", 0):.2f}')
"

# Анализ по символам
python -c "
from modules.performance_tracker import PerformanceTracker
tracker = PerformanceTracker()
symbol_report = tracker.get_symbol_report()
if not symbol_report.empty:
    print('📊 ПРОИЗВОДИТЕЛЬНОСТЬ ПО ПАРАМ:')
    print(symbol_report.to_string())
else:
    print('❌ Нет данных по символам')
"

# Дневной отчет
python -c "
from modules.performance_tracker import PerformanceTracker
tracker = PerformanceTracker()
daily_report = tracker.get_daily_report()
if not daily_report.empty:
    print('📅 ДНЕВНОЙ ОТЧЕТ:')
    print(daily_report.tail(7).to_string())
else:
    print('❌ Нет дневных данных')
"
```

### Статус текущего дня

```bash
# 🔧 НОВЫЕ команды статуса (2025):

# Статус торгового дня
python -c "
from modules.trading_diary import TradingDiary
diary = TradingDiary()
status = diary.get_current_day_status()
print('📔 СТАТУС ТОРГОВОГО ДНЯ:')
print(f'   📅 Дата: {status[\"date\"]}')
print(f'   💰 Начальный баланс: ${status[\"start_balance\"]:.2f}')
print(f'   💰 Текущий баланс: ${status[\"current_balance\"]:.2f}')
print(f'   📈 Дневной результат: ${status[\"daily_return\"]:.2f}')
print(f'   🔄 Открытых позиций: {status[\"open_positions\"]}')
print(f'   ✅ Завершенных сделок: {status[\"completed_trades\"]}')
"

# Экспорт дневника в CSV
python -c "
from modules.trading_diary import TradingDiary
diary = TradingDiary()
export_path = diary.export_diary_to_csv(30)  # За 30 дней
print(f'📊 Дневник экспортирован: {export_path}' if export_path else '❌ Ошибка экспорта')
"
```

---

## ⚙️ Настройка и конфигурация

### Управление стратегиями

```bash
# Информация о текущей стратегии
python -c "
from user_config import UserConfig
strategy_info = UserConfig.get_strategy_info()
print(f'🎯 ТЕКУЩАЯ СТРАТЕГИЯ:')
print(f'   Название: {strategy_info.get(\"name\", \"Unknown\")}')
print(f'   Тип: {strategy_info.get(\"type\", \"unknown\")}')
print(f'   Риск: {strategy_info.get(\"risk_level\", \"unknown\")}')
print(f'   Таймфрейм: {strategy_info.get(\"timeframe\", \"unknown\")}')
"

# Конфигурация пользовательской стратегии
python -c "
from user_config import UserConfig
if UserConfig.SELECTED_STRATEGY == 'custom':
    config = UserConfig.CUSTOM_STRATEGY_CONFIG
    print('🛠️ НАСТРОЙКИ ПОЛЬЗОВАТЕЛЬСКОЙ СТРАТЕГИИ:')
    print(f'   Мин. условий: {config[\"entry_conditions\"][\"min_conditions_required\"]}')
    print(f'   Cooldown: {config[\"entry_conditions\"][\"signal_cooldown\"]}с')
    print(f'   Риск на сделку: {config[\"risk_management\"][\"risk_per_trade\"]*100:.1f}%')
    print(f'   Макс. стоп-лосс: {config[\"risk_management\"][\"max_stop_loss_pct\"]*100:.1f}%')
    print(f'   Плечо: {config[\"risk_management\"][\"leverage\"]}x')
    print(f'   Volume порог: {config[\"volume_settings\"][\"min_ratio\"]}')
else:
    print(f'ℹ️ Используется автоматическая стратегия: {UserConfig.SELECTED_STRATEGY}')
"
```

### Проверка настроек времени

```bash
# Временные настройки
python -c "
from user_config import UserConfig
time_settings = UserConfig.TIME_SETTINGS
print('⏰ ВРЕМЕННЫЕ НАСТРОЙКИ:')
print(f'   Интервал цикла: {time_settings[\"intervals\"][\"cycle_interval\"]}с')
print(f'   Основной таймфрейм: {time_settings[\"timeframes\"][\"primary\"]}м')
print(f'   Торговые часы: {time_settings[\"trading_hours\"][\"start\"]} - {time_settings[\"trading_hours\"][\"end\"]}')
print(f'   Торговля на выходных: {\"Да\" if time_settings[\"trading_hours\"][\"weekend_trading\"] else \"Нет\"}')
"

# Проверка уведомлений
python -c "
from user_config import UserConfig
notifications = UserConfig.NOTIFICATIONS
print('🔔 НАСТРОЙКИ УВЕДОМЛЕНИЙ:')
print(f'   Telegram: {\"✅ Включен\" if notifications[\"telegram\"][\"enabled\"] else \"❌ Отключен\"}')
print(f'   Email: {\"✅ Включен\" if notifications[\"email\"][\"enabled\"] else \"❌ Отключен\"}')
print(f'   Консоль: {\"✅ Включена\" if notifications[\"console\"][\"enabled\"] else \"❌ Отключена\"}')
"
```

---

## 🧪 Тестирование

### Создание тестовых данных

```bash
# Создание тестового дневника
python -c "
from modules.trading_diary import TradingDiary
from datetime import datetime
diary = TradingDiary()
diary.start_trading_session(1000.0)
print('✅ Тестовая сессия создана')
"

# Симуляция сделки
python -c "
from modules.trading_diary import TradingDiary
diary = TradingDiary()
diary.start_trading_session(1000.0)
diary.log_position_opened('ETHUSDT', 'BUY', 0.1, 3000.0, 2900.0, 3200.0)
diary.log_position_closed('ETHUSDT', 3100.0, 10.0, 1.0, 'take_profit')
report = diary.end_trading_session()
print('✅ Тестовая сделка создана')
"
```

### Бэкап и восстановление

```bash
# Создание бэкапа конфигурации
python -c "
import shutil
from datetime import datetime
backup_name = f'user_config_backup_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.py'
shutil.copy('user_config.py', backup_name)
print(f'💾 Бэкап создан: {backup_name}')
"

# Создание полного бэкапа
python -c "
import os
import tarfile
from datetime import datetime
backup_name = f'bot_backup_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.tar.gz'
with tarfile.open(backup_name, 'w:gz') as tar:
    tar.add('user_config.py')
    tar.add('data/', recursive=True)
    tar.add('logs/', recursive=True)
print(f'💾 Полный бэкап создан: {backup_name}')
"
```

---

## 📁 Управление файлами

### Очистка данных

```bash
# Очистка старых логов (старше 7 дней)
python -c "
import os
import time
from pathlib import Path
log_dir = Path('logs')
if log_dir.exists():
    deleted = 0
    for log_file in log_dir.glob('*.log'):
        if time.time() - log_file.stat().st_mtime > 7 * 24 * 3600:
            log_file.unlink()
            deleted += 1
    print(f'🗑️ Удалено {deleted} старых лог-файлов')
else:
    print('❌ Папка logs не найдена')
"

# Размер данных
python -c "
import os
def get_dir_size(path):
    total = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total += os.path.getsize(filepath)
    except:
        pass
    return total

print('📁 РАЗМЕР ДАННЫХ:')
print(f'   Логи: {get_dir_size(\"logs\") / 1024 / 1024:.1f} MB')
print(f'   Данные: {get_dir_size(\"data\") / 1024 / 1024:.1f} MB')
print(f'   Всего: {(get_dir_size(\"logs\") + get_dir_size(\"data\")) / 1024 / 1024:.1f} MB')
"

# Проверка структуры проекта
python -c "
import os
required_dirs = ['logs', 'data', 'config', 'strategies', 'modules', 'utils']
required_files = ['main.py', 'user_config.py', 'config_loader.py', 'requirements.txt']

print('📁 СТРУКТУРА ПРОЕКТА:')
print('Директории:')
for dir_name in required_dirs:
    status = '✅' if os.path.exists(dir_name) else '❌'
    print(f'   {status} {dir_name}/')

print('Файлы:')
for file_name in required_files:
    status = '✅' if os.path.exists(file_name) else '❌'
    print(f'   {status} {file_name}')
"
```

---

## 🆘 Устранение неполадок

### Диагностика проблем

```bash
# 🔧 НОВАЯ полная диагностика (2025)
python -c "
import sys
import os
import platform
from datetime import datetime

print('🔍 ПОЛНАЯ ДИАГНОСТИКА ТОРГОВОГО БОТА (2025)')
print('=' * 60)
print(f'Время: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}')
print(f'Платформа: {platform.system()} {platform.release()}')
print(f'Python: {sys.version.split()[0]}')
print(f'Рабочая папка: {os.getcwd()}')
print()

# Проверка файловой системы
print('📁 Проверка файловой системы:')
required_dirs = ['logs', 'data', 'config', 'strategies', 'modules', 'utils']
for dir_name in required_dirs:
    if os.path.exists(dir_name):
        print(f'✅ {dir_name}/')
    else:
        print(f'❌ {dir_name}/ - ОТСУТСТВУЕТ')

print()
print('📄 Проверка ключевых файлов:')
required_files = ['main.py', 'user_config.py', 'config_loader.py']
for file_name in required_files:
    if os.path.exists(file_name):
        print(f'✅ {file_name}')
    else:
        print(f'❌ {file_name} - ОТСУТСТВУЕТ')

print('=' * 60)
"

# Проверка API ключей
python -c "
from user_config import UserConfig
print('🔑 ПРОВЕРКА API:')
api_key = UserConfig.BYBIT_API_KEY
api_secret = UserConfig.BYBIT_API_SECRET
print(f'   API Key: {api_key[:10] if api_key else \"НЕ НАСТРОЕН\"}...')
print(f'   Secret длина: {len(api_secret) if api_secret else 0} символов')
print(f'   Testnet: {\"Да\" if UserConfig.USE_TESTNET else \"Нет\"}')

if api_key == 'YOUR_API_KEY_HERE':
    print('❌ API ключ не настроен!')
if api_secret == 'YOUR_API_SECRET_HERE':
    print('❌ API секрет не настроен!')
"

# Проверка последних ошибок
python -c "
import os
from datetime import datetime
log_file = f'logs/trading_{datetime.now().strftime(\"%Y%m%d\")}.log'
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        errors = [line for line in lines if 'ERROR' in line or 'CRITICAL' in line]
        if errors:
            print('🚨 ПОСЛЕДНИЕ ОШИБКИ:')
            for error in errors[-5:]:
                print(f'   {error.strip()}')
        else:
            print('✅ Критических ошибок не найдено')
else:
    print('❌ Лог файл не найден')
"
```

### Исправление проблем

```bash
# 🔧 НОВЫЕ команды исправления (2025):

# Анализ и исправление проблем
python utils/strategy_debug_tool.py ETHUSDT  # Диагностика стратегии
python utils/log_analyzer.py                # Анализ логов
python utils/volume_optimizer.py            # Оптимизация настроек

# 📊 СТАНДАРТНЫЕ команды:

# Сброс дневника (при проблемах)
python -c "
import os
import shutil
from datetime import date
diary_file = f'data/diary/diary_{date.today().isoformat()}.json'
if os.path.exists(diary_file):
    backup_file = f'{diary_file}.backup'
    shutil.copy(diary_file, backup_file)
    os.remove(diary_file)
    print(f'🔄 Дневник сброшен, бэкап: {backup_file}')
else:
    print('ℹ️ Дневник не найден')
"

# Очистка кэша Python
python -c "
import os
import shutil
cache_dirs = []
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        cache_dirs.append(os.path.join(root, '__pycache__'))

for cache_dir in cache_dirs:
    shutil.rmtree(cache_dir)
    print(f'🗑️ Удален кэш: {cache_dir}')

print(f'✅ Очищено {len(cache_dirs)} кэш-директорий')
"

# Восстановление конфигурации по умолчанию
python -c "
import shutil
import os
from datetime import datetime

# Создаем бэкап текущей конфигурации
if os.path.exists('user_config.py'):
    backup_name = f'user_config_backup_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.py'
    shutil.copy('user_config.py', backup_name)
    print(f'💾 Бэкап создан: {backup_name}')

print('⚠️ Для восстановления конфигурации по умолчанию:')
print('   1. Скопируйте настройки из user_config copy.py')
print('   2. Или восстановите из бэкапа')
"
```

---

## 🎯 Быстрые команды (закладки PyCharm)

### Ежедневные команды (ОБНОВЛЕНО 2025)

```bash
# 🔧 НОВАЯ утренняя проверка (2025)
python utils/diary_viewer.py && python utils/simple_log_check.py

# Запуск бота
python main.py

# 🔧 НОВАЯ быстрая диагностика (2025)
python utils/strategy_debug_tool.py ETHUSDT

# Статус дня
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_today()"
```

### Команды для отладки (ОБНОВЛЕНО 2025)

```bash
# 🔧 НОВЫЕ инструменты отладки (2025):

# Детальная отладка стратегии
python utils/strategy_debug_tool.py ETHUSDT

# Анализ логов с рекомендациями
python utils/log_analyzer.py

# Оптимизация объемных фильтров
python utils/volume_optimizer.py

# Быстрая проверка логов
python utils/simple_log_check.py

# Полный анализ результатов
python check_results.py

# 📊 СТАНДАРТНЫЕ инструменты:

# Полная отладка
python utils/debug_strategy.py --all

# Тест API
python -c "from modules.data_fetcher import DataFetcher; print('✅ OK' if DataFetcher().health_check() else '❌ ERROR')"

# Проверка конфигурации
python -c "from user_config import UserConfig; is_valid, errors = UserConfig.validate_config(); print('✅ OK' if is_valid else f'❌ Ошибки: {errors}')"
```

### Команды мониторинга (ОБНОВЛЕНО 2025)

```bash
# 🔧 НОВЫЕ команды мониторинга (2025):

# Интерактивный дневник
python utils/diary_viewer.py

# Быстрый статус дня
python -c "
from modules.trading_diary import TradingDiary
diary = TradingDiary()
status = diary.get_current_day_status()
print(f'📅 {status[\"date\"]}')
print(f'💰 Баланс: ${status[\"current_balance\"]:.2f}')
print(f'📈 Результат: ${status[\"daily_return\"]:.2f}')
print(f'📊 Сделок: {status[\"completed_trades\"]}')
"

# 📊 СТАНДАРТНЫЕ команды:

# Текущий статус
python -c "from modules.trading_diary import TradingDiary; print(TradingDiary().get_current_day_status())"

# Недельная сводка
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_week()"

# Последние логи
python -c "
import os
from datetime import datetime
log_file = f'logs/trading_{datetime.now().strftime(\"%Y%m%d\")}.log'
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[-20:]:
            print(line.strip())
"
```

---

## 🔧 Настройка PyCharm

### Полезные конфигурации Run/Debug (ОБНОВЛЕНО 2025)

1. **Основной бот:**
   - Script path: `main.py`
   - Working directory: `$ProjectFileDir$`

2. **🔧 Новая диагностика стратегии:**
   - Script path: `utils/strategy_debug_tool.py`
   - Parameters: `ETHUSDT`
   - Working directory: `$ProjectFileDir$`

3. **📊 Анализ логов:**
   - Script path: `utils/log_analyzer.py`
   - Working directory: `$ProjectFileDir$`

4. **🎯 Оптимизация объемов:**
   - Script path: `utils/volume_optimizer.py`
   - Working directory: `$ProjectFileDir$`

5. **📔 Дневник торговли:**
   - Script path: `utils/diary_viewer.py`
   - Working directory: `$ProjectFileDir$`

6. **🔍 Быстрая проверка:**
   - Script path: `utils/simple_log_check.py`
   - Working directory: `$ProjectFileDir$`

7. **📊 Анализ результатов:**
   - Script path: `check_results.py`
   - Working directory: `$ProjectFileDir$`

### Полезные External Tools (ОБНОВЛЕНО 2025)

**Tools → External Tools → Add:**

1. **🔧 Детальная отладка стратегии:**
   - Program: `python`
   - Arguments: `utils/strategy_debug_tool.py ETHUSDT`
   - Working directory: `$ProjectFileDir$`

2. **📊 Анализ логов:**
   - Program: `python`
   - Arguments: `utils/log_analyzer.py`
   - Working directory: `$ProjectFileDir$`

3. **🎯 Оптимизация объемов:**
   - Program: `python`
   - Arguments: `utils/volume_optimizer.py`
   - Working directory: `$ProjectFileDir$`

4. **📔 Просмотр дневника:**
   - Program: `python`
   - Arguments: `utils/diary_viewer.py`
   - Working directory: `$ProjectFileDir$`

5. **🔍 Быстрая проверка:**
   - Program: `python`
   - Arguments: `utils/simple_log_check.py`
   - Working directory: `$ProjectFileDir$`

6. **📊 Анализ результатов:**
   - Program: `python`
   - Arguments: `check_results.py`
   - Working directory: `$ProjectFileDir$`

7. **⚙️ Проверка конфигурации:**
   - Program: `python`
   - Arguments: `user_config.py`
   - Working directory: `$ProjectFileDir$`

---

## 📚 Полезные сочетания команд (ОБНОВЛЕНО 2025)

### Утренняя рутина (НОВОЕ 2025)

```bash
# 🔧 НОВАЯ утренняя рутина с инструментами 2025:

# 1. Проверка результатов
python utils/diary_viewer.py

# 2. Быстрая проверка логов
python utils/simple_log_check.py

# 3. При проблемах - детальная диагностика
python utils/strategy_debug_tool.py ETHUSDT

# 4. Анализ производительности
python utils/log_analyzer.py

# 5. Запуск на новый день
python main.py
```

### Еженедельный анализ (НОВОЕ 2025)

```bash
# 🔧 НОВЫЙ еженедельный анализ с инструментами 2025:

# 1. Недельная сводка
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_week()"

# 2. Анализ логов за неделю
python utils/log_analyzer.py

# 3. Оптимизация объемных фильтров
python utils/volume_optimizer.py

# 4. Экспорт данных
python -c "
from modules.trading_diary import TradingDiary
diary = TradingDiary()
export_path = diary.export_diary_to_csv(7)
print(f'📊 Экспорт: {export_path}')
"

# 5. Бэкап
python -c "
import shutil
from datetime import datetime
backup_name = f'weekly_backup_{datetime.now().strftime(\"%Y%m%d\")}.py'
shutil.copy('user_config.py', backup_name)
print(f'💾 Еженедельный бэкап: {backup_name}')
"
```

### При критических проблемах (НОВОЕ 2025)

```bash
# 🚨 ЭКСТРЕННАЯ диагностика при убытках:

# 1. Остановите бота (Ctrl+C)

# 2. Полный анализ проблемы
python check_results.py

# 3. Просмотр дневника
python utils/diary_viewer.py

# 4. Детальная диагностика стратегии
python utils/strategy_debug_tool.py ETHUSDT

# 5. Анализ логов
python utils/log_analyzer.py

# 6. Создание отчета о проблеме
python -c "
print('🆘 ОТЧЕТ О ПРОБЛЕМЕ')
print('=' * 40)

# Основная информация
from datetime import datetime
print(f'Время: {datetime.now()}')

# Конфигурация
try:
    from user_config import UserConfig
    print(f'Стратегия: {UserConfig.SELECTED_STRATEGY}')
    print(f'Риск: {UserConfig.RISK_SETTINGS[\"risk_per_trade\"]*100:.1f}%')
    print(f'Плечо: {UserConfig.RISK_SETTINGS[\"max_leverage\"]}x')
except Exception as e:
    print(f'Ошибка конфигурации: {e}')

# Последние результаты
try:
    from utils.diary_viewer import DiaryViewer
    viewer = DiaryViewer()
    status = viewer.get_current_day_status()
    print(f'Дневной результат: ${status.get(\"daily_return\", 0):.2f}')
    print(f'Сделок: {status.get(\"completed_trades\", 0)}')
except Exception as e:
    print(f'Ошибка дневника: {e}')

print('=' * 40)
" > problem_report_$(date +%Y%m%d).txt

echo "📄 Отчет сохранен в problem_report_$(date +%Y%m%d).txt"
```

---

## 🎯 Быстрые команды для разных задач (2025)

### 🔧 **Диагностика проблем:**
```bash
# Быстрая оценка ситуации
python utils/simple_log_check.py

# Детальная диагностика
python utils/strategy_debug_tool.py ETHUSDT

# Анализ производительности
python utils/log_analyzer.py

# Оптимизация настроек
python utils/volume_optimizer.py

# Полный анализ
python check_results.py
```

### 📊 **Мониторинг результатов:**
```bash
# Сегодняшние результаты
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_today()"

# Недельная сводка
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_week()"

# Статус дня
python -c "
from modules.trading_diary import TradingDiary
diary = TradingDiary()
status = diary.get_current_day_status()
print(f'💰 Баланс: ${status[\"current_balance\"]:.2f}')
print(f'📈 Результат: ${status[\"daily_return\"]:.2f}')
print(f'📊 Сделок: {status[\"completed_trades\"]}')
"
```

### ⚙️ **Настройка и конфигурация:**
```bash
# Проверка конфигурации
python user_config.py

# Список стратегий
python user_config.py --strategies

# Интерактивный выбор стратегии
python utils/strategy_selector.py --interactive

# Проверка активных пар
python -c "
from user_config import UserConfig
enabled = UserConfig.get_enabled_pairs()
for pair, config in enabled.items():
    print(f'{pair}: {config[\"weight\"]*100:.0f}%, плечо {config[\"leverage\"]}x')
"
```

### 🧪 **Тестирование:**
```bash
# Простое тестирование
python utils/simple_strategy_test.py

# Тест API
python -c "from modules.data_fetcher import DataFetcher; print('✅ OK' if DataFetcher().health_check() else '❌ ERROR')"

# Валидация стратегии
python -c "
from main import TradingBot
bot = TradingBot()
result = bot.run_strategy_validation()
print(f'Валидация: {result.get(\"score\", 0)}/100')
"
```

---

## 🔧 Настройка PyCharm для работы с новыми инструментами

### Создание Run Configurations для новых инструментов:

1. **Run → Edit Configurations → Add New → Python**

2. **Настройте конфигурации:**

#### 🔧 **Strategy Debug Tool:**
- Name: `Strategy Debug - ETHUSDT`
- Script path: `utils/strategy_debug_tool.py`
- Parameters: `ETHUSDT`
- Working directory: `$ProjectFileDir$`

#### 📊 **Log Analyzer:**
- Name: `Log Analyzer`
- Script path: `utils/log_analyzer.py`
- Working directory: `$ProjectFileDir$`

#### 🎯 **Volume Optimizer:**
- Name: `Volume Optimizer`
- Script path: `utils/volume_optimizer.py`
- Working directory: `$ProjectFileDir$`

#### 📔 **Diary Viewer:**
- Name: `Diary Viewer`
- Script path: `utils/diary_viewer.py`
- Working directory: `$ProjectFileDir$`

#### 🔍 **Quick Log Check:**
- Name: `Quick Log Check`
- Script path: `utils/simple_log_check.py`
- Working directory: `$ProjectFileDir$`

#### 📊 **Results Analyzer:**
- Name: `Results Analyzer`
- Script path: `check_results.py`
- Working directory: `$ProjectFileDir$`

### Настройка горячих клавиш:

**File → Settings → Keymap → External Tools:**

- **Ctrl+Alt+D** → Strategy Debug Tool
- **Ctrl+Alt+L** → Log Analyzer
- **Ctrl+Alt+V** → Volume Optimizer
- **Ctrl+Alt+R** → Diary Viewer
- **Ctrl+Alt+Q** → Quick Log Check
- **Ctrl+Alt+A** → Results Analyzer

---

## 📚 Полезные сочетания команд для разных сценариев

### 🚨 **При критических убытках:**
```bash
# 1. Остановите бота (Ctrl+C)

# 2. Экстренный анализ
python check_results.py
python utils/diary_viewer.py

# 3. Диагностика причин
python utils/strategy_debug_tool.py ETHUSDT
python utils/log_analyzer.py

# 4. Создание безопасной конфигурации
# Редактируйте user_config.py:
# SELECTED_STRATEGY = 'smart_money'
# RISK_SETTINGS = {'risk_per_trade': 0.001, 'max_leverage': 1}

# 5. Валидация изменений
python user_config.py

# 6. Тестирование
python utils/simple_strategy_test.py
```

### 🔍 **При отсутствии сигналов:**
```bash
# 1. Детальная диагностика
python utils/strategy_debug_tool.py ETHUSDT

# 2. Анализ объемных паттернов
python utils/volume_optimizer.py

# 3. Анализ логов
python utils/log_analyzer.py

# 4. Применение рекомендаций в user_config.py

# 5. Тестирование изменений
python utils/simple_strategy_test.py
python main.py  # Тест на 1-2 часа
```

### 📊 **Еженедельная оптимизация:**
```bash
# 1. Анализ недели
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_week()"

# 2. Анализ производительности
python utils/log_analyzer.py

# 3. Оптимизация фильтров
python utils/volume_optimizer.py

# 4. Детальная диагностика
python utils/strategy_debug_tool.py ETHUSDT

# 5. Экспорт данных
python -c "
from modules.trading_diary import TradingDiary
diary = TradingDiary()
export_path = diary.export_diary_to_csv(7)
print(f'📊 Экспорт: {export_path}')
"

# 6. Бэкап конфигурации
cp user_config.py user_config_backup_$(date +%Y%m%d).py
```

---

## 🎯 Создание собственных команд

### Создание пользовательского скрипта диагностики:

```python
# my_diagnosis.py
def my_daily_check():
    """Моя ежедневная проверка бота"""
    print("🔍 МОЯ ЕЖЕДНЕВНАЯ ПРОВЕРКА")
    print("=" * 40)
    
    # 1. Быстрая проверка
    import subprocess
    try:
        result = subprocess.run(['python', 'utils/simple_log_check.py'], 
                              capture_output=True, text=True)
        print("📊 БЫСТРАЯ ПРОВЕРКА:")
        print(result.stdout)
    except:
        print("❌ Ошибка быстрой проверки")
    
    # 2. Статус дня
    try:
        from modules.trading_diary import TradingDiary
        diary = TradingDiary()
        status = diary.get_current_day_status()
        
        print("📔 СТАТУС ДНЯ:")
        print(f"   💰 Баланс: ${status['current_balance']:.2f}")
        print(f"   📈 Результат: ${status['daily_return']:.2f}")
        print(f"   📊 Сделок: {status['completed_trades']}")
        
        # Рекомендации
        if status['daily_return'] < 0:
            print("\n🚨 УБЫТОЧНЫЙ ДЕНЬ:")
            print("   1. Запустите: python utils/strategy_debug_tool.py ETHUSDT")
            print("   2. Проанализируйте: python utils/log_analyzer.py")
            print("   3. Рассмотрите снижение рисков")
        elif status['completed_trades'] == 0:
            print("\n🔍 НЕТ СДЕЛОК:")
            print("   1. Запустите: python utils/strategy_debug_tool.py ETHUSDT")
            print("   2. Оптимизируйте: python utils/volume_optimizer.py")
        else:
            print("\n✅ ДЕНЬ ПРОШЕЛ НОРМАЛЬНО")
            
    except Exception as e:
        print(f"❌ Ошибка анализа дня: {e}")

if __name__ == "__main__":
    my_daily_check()
```

### Добавление в PyCharm:
- **Script path:** `my_diagnosis.py`
- **Working directory:** `$ProjectFileDir$`
- **Горячая клавиша:** `Ctrl+Alt+M`

---

**🎯 Сохраните этот файл в закладки PyCharm для быстрого доступа к командам!**

### 🔧 **Быстрый доступ к новым инструментам (2025):**
```bash
python utils/strategy_debug_tool.py ETHUSDT  # Детальная отладка
python utils/log_analyzer.py                # Анализ логов
python utils/volume_optimizer.py            # Оптимизация
python utils/diary_viewer.py                # Дневник
python utils/simple_log_check.py            # Быстрая проверка
python check_results.py                     # Анализ результатов
```

### 🛡️ **Безопасные команды для новичков:**
```bash
# Проверка конфигурации
python user_config.py

# Простое тестирование
python utils/simple_strategy_test.py

# Быстрая проверка
python utils/simple_log_check.py

# Просмотр результатов
python utils/diary_viewer.py
```

### 🎯 **Команды для оптимизации:**
```bash
# Детальная диагностика
python utils/strategy_debug_tool.py ETHUSDT

# Анализ производительности
python utils/log_analyzer.py

# Оптимизация фильтров
python utils/volume_optimizer.py

# Применение изменений
python user_config.py  # Валидация
python main.py         # Тестирование
```

---

**🚀 Используйте новые инструменты 2025 года для эффективной работы с торговым ботом!**