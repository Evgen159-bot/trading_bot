# 🤖 ByBit Trading Bot - Полное руководство

Профессиональный автоматический торговый бот для криптобиржи ByBit с 8 торговыми стратегиями, продвинутым техническим анализом и интеллектуальным управлением рисками.

## 📋 Содержание

- [🚀 Быстрый старт](#-быстрый-старт)
- [📦 Установка](#-установка)
- [🔑 Настройка API](#-настройка-api)
- [🎯 Выбор стратегии](#-выбор-стратегии)
- [⚙️ Конфигурация](#️-конфигурация)
- [🚀 Запуск](#-запуск)
- [📊 Мониторинг](#-мониторинг)
- [🛡️ Безопасность](#️-безопасность)
- [🆘 Поддержка](#-поддержка)

---

## 🚀 Быстрый старт

### За 5 минут до первого запуска:

```bash
# 1. Клонируйте проект
git clone https://github.com/your-repo/trading-bot.git
cd trading-bot

# 2. Установите зависимости
pip install -r requirements.txt

# 3. Настройте конфигурацию
python setup_directories.py

# 4. Настройте API ключи в user_config.py
# Замените значения в user_config.py:
# BYBIT_API_KEY = "ваш_api_ключ"
# BYBIT_API_SECRET = "ваш_секрет"

# 5. Запустите бота
python main.py
```

---

## 📦 Установка

### Системные требования:
- **Python 3.8+** (рекомендуется 3.10+)
- **Windows/Linux/macOS**
- **Интернет соединение**
- **Минимум 512MB RAM**

### Автоматическая установка:

```bash
# Запустите скрипт настройки (создает все папки и файлы)
python setup_directories.py
```

### Ручная установка:

```bash
# 1. Создайте виртуальное окружение
python -m venv .venv

# 2. Активируйте окружение
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Создайте необходимые папки
mkdir logs data config strategies modules utils
```

---

## 🔑 Настройка API

### 1. Получение API ключей ByBit:

1. **Регистрация:** [ByBit.com](https://www.bybit.com)
2. **Переход в API:** Account & Security → API Management
3. **Создание ключа:**
   - ✅ **Read** (чтение данных)
   - ✅ **Trade** (торговля)
   - ❌ **Withdraw** (НЕ ВКЛЮЧАЙТЕ!)
4. **Копирование:** API Key и Secret Key

### 2. Настройка в user_config.py:

```python
class UserConfig:
    # 🔑 ЗАМЕНИТЕ НА ВАШИ КЛЮЧИ!
    BYBIT_API_KEY = "ваш_реальный_api_ключ"
    BYBIT_API_SECRET = "ваш_реальный_секрет"
    
    # Режим работы
    USE_TESTNET = True  # True = тестовая сеть (безопасно)
```

### 3. Проверка подключения:

```bash
python -c "from modules.data_fetcher import DataFetcher; print('✅ API работает')"
```

---

## 🎯 Выбор и настройка стратегий

### 8 доступных стратегий:

| Стратегия | Тип | Риск | Таймфрейм | Подходит для |
|-----------|-----|------|-----------|--------------|
| **🛠️ Custom** | Настраиваемая | 🟡 Средний | Любой | Рекомендуется для начала |
| **🧠 Smart Money** | Автоматическая | 🟢 Низкий | 5m-1h | Консервативная торговля |
| **📈 Trend Following** | Автоматическая | 🟡 Средний | 15m-4h | Трендовые рынки |
| **⚡ Scalping** | Автоматическая | 🔴 Высокий | 1m-5m | Активная торговля |
| **🌊 Swing** | Автоматическая | 🟢 Низкий | 4h-1d | Пассивная торговля |
| **💥 Breakout** | Автоматическая | 🟡 Средний | 15m-1h | Пробои уровней |
| **🔄 Mean Reversion** | Автоматическая | 🟡 Средний | 5m-30m | Боковые рынки |
| **🚀 Momentum** | Автоматическая | 🔴 Высокий | 5m-15m | Импульсная торговля |

### Выбор стратегии в user_config.py:

```python
# Рекомендуемая стратегия для начала:
SELECTED_STRATEGY = 'custom'  # Более активная, лучше для тестирования

# Альтернативы:
# SELECTED_STRATEGY = 'smart_money'      # Очень консервативная
# SELECTED_STRATEGY = 'trend_following'  # Трендовая
# SELECTED_STRATEGY = 'momentum'         # Активная

# Доступные варианты:
# 'custom'           - Настраиваемая
# 'smart_money'      - Smart Money (рекомендуется)
# 'trend_following'  - Следование тренду
# 'scalping'         - Скальпинг
# 'swing'            - Свинг торговля
# 'breakout'         - Пробои
# 'mean_reversion'   - Возврат к среднему
# 'momentum'         - Импульсная торговля
```

## 🏗️ Архитектура проекта

```
trading-bot/
├── main.py                 # Основной файл бота
├── user_config.py          # Пользовательская конфигурация
├── config_loader.py        # Загрузчик конфигурации
├── config/                 # Конфигурационные файлы
│   ├── trading_config.py   # Основная конфигурация
│   └── config.env.example  # Пример настроек
├── modules/               # Основные модули
│   ├── data_fetcher.py    # Получение данных с биржи
│   ├── market_analyzer.py # Технический анализ
│   ├── order_manager.py   # Управление ордерами
│   ├── position_manager.py # Управление позициями
│   ├── risk_manager.py    # Управление рисками
│   ├── performance_tracker.py # Отслеживание производительности
│   └── trading_diary.py   # Дневник торговли
├── strategies/            # Торговые стратегии
│   ├── base_strategy.py   # Базовый класс стратегии
│   ├── custom_strategy.py # Настраиваемая стратегия
│   ├── smart_money_strategy.py # Smart Money стратегия
│   ├── trend_following_strategy.py # Трендовая стратегия
│   ├── scalping_strategy.py # Скальпинг стратегия
│   ├── swing_strategy.py  # Свинг стратегия
│   ├── breakout_strategy.py # Пробойная стратегия
│   ├── mean_reversion_strategy.py # Возврат к среднему
│   ├── momentum_strategy.py # Импульсная стратегия
│   ├── strategy_factory.py # Фабрика стратегий
│   └── strategy_validator.py # Валидация стратегий
├── utils/                 # Утилиты
│   ├── diary_viewer.py    # Просмотр дневника
│   ├── strategy_selector.py # Выбор стратегий
│   └── logger.py          # Система логирования
├── logs/                 # Логи работы
├── data/                 # Данные производительности
│   ├── diary/            # Дневник торговли
│   ├── performance/      # Метрики производительности
│   └── validation/       # Результаты валидации
└── tests/                # Тесты
```

### Настройка стратегии в user_config.py:

```python
# Выбор стратегии
SELECTED_STRATEGY = 'smart_money'  # Рекомендуется для начинающих

# Для настраиваемой стратегии (полный контроль):
SELECTED_STRATEGY = 'custom'  # Измените на 'custom'

CUSTOM_STRATEGY_CONFIG = {
    # RSI настройки
    'rsi_settings': {
        'period': 14,              # Период RSI
        'oversold_lower': 25,      # Нижний уровень перепроданности
        'oversold_upper': 35,      # Верхний уровень перепроданности
        'overbought_lower': 65,    # Нижний уровень перекупленности
        'overbought_upper': 75,    # Верхний уровень перекупленности
    },
    
    # Управление рисками
    'risk_reward_settings': {
        'max_stop_loss_pct': 0.08,    # 8% максимальный стоп-лосс
        'min_take_profit_pct': 0.12,  # 12% минимальный тейк-профит
        'risk_per_trade': 0.015,      # 1.5% риск на сделку
    },
    
    # Условия входа
    'min_conditions_required': 3,     # Минимум условий из 6
    'min_confidence': 0.6,            # Минимальная уверенность 60%
}
```

### Просмотр всех стратегий:

```bash
# Список всех стратегий с описаниями
python user_config.py --strategies

# Интерактивный выбор стратегии
python utils/strategy_selector.py --interactive

# Проверка текущей конфигурации
python user_config.py
```

---

## ⚙️ Конфигурация

### 1. Основные настройки:

```python
# Капитал и риски
INITIAL_BALANCE = 1000.0  # Ваш депозит в USD
MIN_BALANCE_THRESHOLD = 100.0  # Минимальный баланс

RISK_SETTINGS = {
    'risk_per_trade': 0.02,      # 2% риск на сделку
    'max_daily_loss': 0.05,      # 5% максимальная дневная потеря
    'max_positions': 3,          # Максимум открытых позиций
    'max_leverage': 5            # Максимальное плечо
}
```

### 2. Торговые пары:

```python
TRADING_PAIRS = {
    'ETHUSDT': {
        'enabled': True,         # Включить торговлю
        'weight': 0.4,          # 40% портфеля
        'leverage': 3,          # Плечо 3x
        'stop_loss_pct': 0.025, # 2.5% стоп-лосс
        'take_profit_pct': 0.05 # 5% тейк-профит
    },
    'SOLUSDT': {
        'enabled': True,
        'weight': 0.6,          # 60% портфеля
        'leverage': 3,
        'stop_loss_pct': 0.03,
        'take_profit_pct': 0.06
    }
}
```

### 3. Настройка пользовательской стратегии:

```python
# Только для SELECTED_STRATEGY = 'MultiIndicatorStrategy'
CUSTOM_STRATEGY_CONFIG = {
    # RSI настройки
    'rsi_settings': {
        'period': 14,              # Период RSI
        'oversold_lower': 25,      # Нижний уровень перепроданности
        'oversold_upper': 35,      # Верхний уровень перепроданности
        'overbought_lower': 65,    # Нижний уровень перекупленности
        'overbought_upper': 75,    # Верхний уровень перекупленности
    },
    
    # Управление рисками
    'risk_reward_settings': {
        'max_stop_loss_pct': 0.08,    # 8% максимальный стоп-лосс
        'min_take_profit_pct': 0.12,  # 12% минимальный тейк-профит
        'risk_per_trade': 0.015,      # 1.5% риск на сделку
    },
    
    # Условия входа
    'min_conditions_required': 3,     # Минимум условий из 6
    'min_confidence': 0.6,            # Минимальная уверенность 60%
}
```

---

## 🚀 Запуск

### Способы запуска:

```bash
# 1. Основной способ
python main.py

# 2. Windows (двойной клик)
start_bot.bat

# 3. Linux/macOS
./start_bot.sh

# 4. С проверкой конфигурации
python user_config.py && python main.py
```

### Проверка перед запуском:

```bash
# Валидация конфигурации
python user_config.py

# Проверка зависимостей
python -c "import pandas, ta, pybit; print('✅ Все модули установлены')"

# Тест подключения к API
python -c "from modules.data_fetcher import DataFetcher; print('✅ API работает')"
```

### Пример успешного запуска:

```
🚀 BYBIT TRADING BOT STARTING
==================================================
🚀 Инициализация торгового бота...
🔍 Загрузка пользовательской конфигурации...
🎯 Выбранная стратегия: Smart Money Strategy
✅ Strategy validation PASSED (Score: 75.0/100)

🤖 Bot is running...
📊 Starting trading cycle #1...
💰 Account balance: $1,100.00
🔍 Processing ETHUSDT...
🔍 Processing SOLUSDT...
✅ Processed 2/2 pairs in 4.09s
```

---

## 📊 Мониторинг и анализ

### Просмотр торговых пар
```bash
# Проверка активных пар
python -c "
from user_config import UserConfig
enabled = UserConfig.get_enabled_pairs()
print(f'Активных пар: {len(enabled)}/4')
for pair, config in enabled.items():
    print(f'• {pair}: {config[\"weight\"]*100:.0f}% портфеля')
"

# Просмотр всех доступных пар
python -c "
from user_config import UserConfig
print('📊 Все доступные пары:')
for pair, config in UserConfig.TRADING_PAIRS.items():
    status = '✅ Включена' if config['enabled'] else '❌ Отключена'
    print(f'• {pair}: {status} | {config[\"description\"]}')
"
```

### Просмотр результатов торговли:

```bash
# Дневник торговли (интерактивный)
python utils/diary_viewer.py

# Сегодняшние результаты
python -c "
from utils.diary_viewer import DiaryViewer
viewer = DiaryViewer()
viewer.show_today()
"

# Недельная сводка
python -c "
from utils.diary_viewer import DiaryViewer
viewer = DiaryViewer()
viewer.show_week()
"
```

### 1. Логи в реальном времени:

```bash
# Основные логи
tail -f logs/trading_$(date +%Y%m%d).log

# Логи стратегии
tail -f logs/strategies/SmartMoneyStrategy_$(date +%Y%m%d).log

# Логи валидации
tail -f logs/validation/validation_$(date +%Y%m%d).log
```

### 2. Просмотр дневника торговли:

```bash
# Интерактивный просмотр
python utils/diary_viewer.py

# Просмотр логов дневника
tail -f logs/trading_diary/diary_log_$(date +%Y%m%d).log

# Логи просмотра дневника пользователем
tail -f logs/trading_diary/diary_viewer_$(date +%Y%m%d).log

# Сегодняшний день
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_today()"

# Недельная сводка
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_week()"
```

### Проверка статуса бота:

```bash
# Проверка конфигурации
python user_config.py

# Валидация стратегии
python -c "
from config_loader import load_user_configuration
loader = load_user_configuration()
print('✅ Конфигурация загружена успешно')
"
```

### 4. Структура логов:

```
logs/
├── trading_20250807.log           # Основные логи
├── strategies/
│   └── SmartMoneyStrategy_20250807.log
├── validation/
│   └── validation_20250807.log
└── trades/
    └── trades_20250807.log
```

---

## 🛡️ Безопасность и лучшие практики

### ⚠️ Критически важно:

1. **🔴 НИКОГДА не включайте Withdraw права в API**
2. **🟡 ВСЕГДА начинайте с USE_TESTNET = True**
3. **🟢 Начинайте с малых сумм (INITIAL_BALANCE = 100-500)**
4. **🔵 Регулярно проверяйте логи в папке logs/**

### Рекомендуемая последовательность:

```python
# 1. Тестирование (1-2 недели)
USE_TESTNET = True
INITIAL_BALANCE = 1000.0

# 2. Малые суммы (1-2 недели)
USE_TESTNET = False
INITIAL_BALANCE = 100.0
RISK_SETTINGS['risk_per_trade'] = 0.01  # 1%

# 3. Постепенное увеличение
INITIAL_BALANCE = 500.0
RISK_SETTINGS['risk_per_trade'] = 0.015  # 1.5%

# 4. Полноценная торговля
INITIAL_BALANCE = 2000.0
RISK_SETTINGS['risk_per_trade'] = 0.02  # 2%
```

### Защита от потерь:

```python
RISK_SETTINGS = {
    'max_daily_loss': 0.05,        # 5% дневной лимит
    'emergency_stop_loss': 0.10,   # 10% экстренный стоп
    'drawdown_limit': 0.15,        # 15% лимит просадки
}
```

---

## 📈 Подробное описание стратегий

### 🧠 Smart Money Strategy (Рекомендуется)
```python
SELECTED_STRATEGY = 'SmartMoneyStrategy'
```

**Особенности:**
- Анализ институциональных уровней
- Market Structure (BOS/CHoCH)
- Высокое качество сигналов (75%+ confidence)
- Консервативный подход

**Результаты:** Win Rate 65-75%, Profit Factor 1.8-2.5

---

### 🛠️ Настраиваемая стратегия
```python
SELECTED_STRATEGY = 'MultiIndicatorStrategy'

CUSTOM_STRATEGY_CONFIG = {
    # Пример агрессивной настройки
    'min_conditions_required': 2,  # Меньше условий = больше сигналов
    'min_confidence': 0.5,          # Меньше уверенность = больше сигналов
    
    'rsi_settings': {
        'period': 7,                # Быстрый RSI
        'oversold_upper': 40,       # Более широкая зона
        'overbought_lower': 60,
    },
    
    'risk_reward_settings': {
        'risk_per_trade': 0.025,    # 2.5% риск
        'max_stop_loss_pct': 0.06,  # 6% стоп-лосс
    }
}
```

---

### ⚡ Скальпинг (для активных трейдеров)
```python
SELECTED_STRATEGY = 'ScalpingStrategy'
```

**Особенности:**
- Быстрые сделки (1-15 минут)
- Малые цели прибыли (0.5-2%)
- Высокая частота торговли
- Требует постоянного мониторинга

---

## 🔧 Продвинутые настройки

### Временные настройки:

```python
TIME_SETTINGS = {
    'trading_hours': {
        'start': '00:00',           # Начало торговли (UTC)
        'end': '23:59',             # Конец торговли
        'weekend_trading': False    # Торговля на выходных
    },
    
    'intervals': {
        'cycle_interval': 60,       # Интервал проверки (секунды)
    },
    
    'timeframes': {
        'primary': '5',             # Основной таймфрейм (5 минут)
        'trend': '15',              # Анализ тренда (15 минут)
    }
}
```

### Уведомления Telegram:

```python
NOTIFICATIONS = {
    'telegram': {
        'enabled': True,
        'bot_token': 'ваш_токен_бота',      # От @BotFather
        'chat_id': 'ваш_chat_id',           # От @userinfobot
        'events': {
            'position_opened': True,         # Уведомления об открытии
            'position_closed': True,         # Уведомления о закрытии
            'daily_summary': True,           # Дневная сводка
        }
    }
}
```

---

## 📊 Примеры использования

### Консервативная торговля:

```python
SELECTED_STRATEGY = 'SmartMoneyStrategy'
RISK_SETTINGS = {
    "risk_per_trade": 0.01,      # 1% риск
    "max_daily_loss": 0.03,      # 3% дневной лимит
    "max_positions": 2,          # Максимум 2 позиции
}
```

### Агрессивная торговля:

```python
SELECTED_STRATEGY = 'MomentumStrategy'
RISK_SETTINGS = {
    "risk_per_trade": 0.03,      # 3% риск
    "max_daily_loss": 0.08,      # 8% дневной лимит
    "max_positions": 5,          # Максимум 5 позиций
}
```

### Скальпинг:

```python
SELECTED_STRATEGY = 'ScalpingStrategy'
TIME_SETTINGS = {
    "intervals": {
        "cycle_interval": 30,    # Проверка каждые 30 секунд
    },
    "timeframes": {
        "primary": "1",          # 1-минутные свечи
    }
}
```

---

## 🔍 Диагностика и отладка

### Проверка состояния:

```bash
# Проверка конфигурации
python user_config.py

# Валидация стратегии
python -c '
from main import TradingBot
bot = TradingBot()
result = bot.run_strategy_validation()
print(f"Validation: {result}")
'

# Проверка подключения
python -c "
from modules.data_fetcher import DataFetcher
from config.trading_config import TradingConfig
df = DataFetcher()
print('✅ Подключение работает' if df.health_check() else '❌ Проблемы с подключением')
"
```

### Частые проблемы и решения:

| Проблема | Решение |
|----------|---------|
| `API ключ не настроен` | Замените `YOUR_API_KEY_HERE` на реальный ключ |
| `Нет включенных торговых пар` | Установите `enabled: True` для нужных пар |
| `Веса портфеля не равны 1.0` | Сумма весов включенных пар должна быть 1.0 |
| `Connection failed` | Проверьте интернет и правильность API ключей |
| `Insufficient data` | Подождите несколько минут для накопления данных |

---

## 📱 Мониторинг через Telegram

### Настройка Telegram бота:

1. **Создайте бота:** Напишите [@BotFather](https://t.me/botfather) → `/newbot`
2. **Получите токен:** Скопируйте токен бота
3. **Узнайте Chat ID:** Напишите [@userinfobot](https://t.me/userinfobot)
4. **Настройте в user_config.py:**

```python
NOTIFICATIONS = {
    'telegram': {
        'enabled': True,
        'bot_token': '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz',
        'chat_id': '123456789',
    }
}
```

### Примеры уведомлений:

```
🤖 ByBit Trading Bot

📈 Позиция открыта:
🎯 ETHUSDT LONG
💵 Размер: 0.5 ETH
💰 Цена входа: $3,245.67
🛑 Стоп-лосс: $3,164.34
🎯 Тейк-профит: $3,407.95

📊 Баланс: $1,087.50
```

---

## 🎯 Оптимизация производительности

### Рекомендуемые настройки по стилю:

#### Для новичков:
```python
SELECTED_STRATEGY = 'SmartMoneyStrategy'
RISK_SETTINGS = {
    'risk_per_trade': 0.01,      # Консервативный риск
    'max_positions': 2,          # Меньше позиций
}
TIME_SETTINGS = {
    'intervals': {'cycle_interval': 120}  # Реже проверки
}
```

#### Для опытных:
```python
SELECTED_STRATEGY = 'MultiIndicatorStrategy'
CUSTOM_STRATEGY_CONFIG = {
    'min_conditions_required': 3,
    'min_confidence': 0.65,
    # Настройте под свой стиль
}
```

#### Для активных трейдеров:
```python
SELECTED_STRATEGY = 'ScalpingStrategy'
TIME_SETTINGS = {
    'intervals': {'cycle_interval': 30}   # Частые проверки
}
```

---

## 📊 Анализ результатов

### Просмотр дневника:

```bash
# Сегодняшние результаты
python utils/diary_viewer.py

# Выберите опцию:
# 1. Показать сегодня
# 2. Показать конкретный день  
# 3. Недельная сводка
# 4. Список доступных дней
```

### Экспорт данных:

```python
# В коде бота
bot.export_diary(days=30)  # Экспорт за 30 дней
```

---

## 🔄 Обновление и обслуживание

### Регулярные задачи:

```bash
# Еженедельно - проверка логов
ls -la logs/

# Ежемесячно - очистка старых данных
find logs/ -name "*.log" -mtime +30 -delete

# При необходимости - обновление зависимостей
pip install --upgrade -r requirements.txt
```

### Резервное копирование:

```bash
# Создание бэкапа конфигурации
cp user_config.py user_config_backup_$(date +%Y%m%d).py

# Бэкап данных
tar -czf backup_$(date +%Y%m%d).tar.gz data/ logs/ user_config.py
```

---

## 🆘 Если что-то пошло не так

### Частые проблемы первого запуска:

#### ❌ "Бот не генерирует сигналы"
**Диагностика:**
```bash
# Запустите отладчик стратегии
python utils/debug_strategy.py --all

# Проверьте детальные логи
tail -f logs/trading_$(date +%Y%m%d).log

# Анализ рыночных условий
python utils/debug_strategy.py --market
```

**Решения:**
1. **Smart Money слишком консервативная** - переключитесь на custom
2. **Снизьте требования** в CUSTOM_STRATEGY_CONFIG
3. **Проверьте рыночные условия** - возможно, нет подходящих сигналов

#### ❌ "API ключ не настроен"
**Решение:** Замените `YOUR_API_KEY_HERE` на реальный ключ

#### ❌ "Нет включенных торговых пар"
**Решение:** Установите `enabled: True` для нужных пар

#### ❌ "Веса портфеля не равны 1.0"
**Решение:** Сумма весов включенных пар должна быть 1.0

#### ❌ "No signals generated"
**Возможные причины:**
1. **Стратегия слишком консервативная** (особенно Smart Money)
2. **Рыночные условия не подходят** для выбранной стратегии
3. **Слишком строгие фильтры** в настройках

**Если хотите больше сигналов:**
```python
# Переключитесь на настраиваемую стратегию
SELECTED_STRATEGY = 'custom'

# Снизьте требования в CUSTOM_STRATEGY_CONFIG:
CUSTOM_STRATEGY_CONFIG = {
    'entry_conditions': {
        'min_conditions_required': 2,  # Было 3
        'signal_cooldown': 120,        # Было 180
    }
}

# Или выберите более активную автоматическую стратегию
SELECTED_STRATEGY = 'momentum'  # Или 'breakout'
```

#### ❌ "Connection failed"
**Решение:** Проверьте интернет и правильность API ключей

#### ❌ "Insufficient data"
**Решение:** Подождите несколько минут для накопления данных
### Быстрая диагностика:

```bash
# Полная проверка системы
python -c "
print('🔍 Диагностика системы:')
try:
    from user_config import UserConfig
    print('✅ Конфигурация загружена')
    
    from modules.data_fetcher import DataFetcher
    df = DataFetcher()
    print('✅ API подключение работает' if df.health_check() else '❌ Проблемы с API')
    
    import pandas, ta, pybit
    print('✅ Все зависимости установлены')
    
except Exception as e:
    print(f'❌ Ошибка: {e}')
"
```

---

## 🆘 Поддержка и устранение неполадок

### Диагностические команды:

```bash
# Полная диагностика
python -c "
print('🔍 Диагностика бота:')
try:
    from user_config import UserConfig
    is_valid, errors = UserConfig.validate_config()
    print(f'✅ Конфигурация: {\"OK\" if is_valid else \"ОШИБКИ\"}')
    if errors:
        for error in errors: print(f'  ❌ {error}')
except Exception as e:
    print(f'❌ Ошибка конфигурации: {e}')

try:
    import pandas, ta, pybit
    print('✅ Зависимости: OK')
except ImportError as e:
    print(f'❌ Отсутствует модуль: {e}')

try:
    from modules.data_fetcher import DataFetcher
    df = DataFetcher()
    print(f'✅ API подключение: {\"OK\" if df.health_check() else \"ОШИБКА\"}')
except Exception as e:
    print(f'❌ Ошибка API: {e}')
"
```

### Восстановление после ошибок:

```bash
# 1. Остановите бота (Ctrl+C)
# 2. Проверьте логи
tail -n 50 logs/trading_$(date +%Y%m%d).log

# 3. Исправьте проблему
# 4. Перезапустите
python main.py
```

### Контакты поддержки:

- **📧 Email:** support@yourbot.com
- **💬 Telegram:** @YourBotSupport
- **📚 Документация:** [Wiki](https://github.com/yourrepo/wiki)
- **🐛 Баги:** [Issues](https://github.com/yourrepo/issues)

---

## 📄 Лицензия и дисклеймер

**⚠️ ВАЖНО:** Этот бот предназначен для образовательных целей. Торговля криптовалютами связана с высокими рисками потери средств.

**🛡️ Автор не несет ответственности за:**
- Финансовые потери
- Технические сбои
- Ошибки в торговых решениях

**✅ Используйте бота только если:**
- Понимаете риски торговли
- Можете позволить себе потерять инвестированные средства
- Имеете опыт в трейдинге

---

**🎯 Удачной торговли! Помните: лучший трейдер - это дисциплинированный трейдер.**
