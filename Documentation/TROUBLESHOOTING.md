# 🆘 Руководство по устранению неполадок

## 🔍 Диагностика проблем

### Быстрая диагностика:

```bash
# Простой тест стратегии
python utils/simple_strategy_test.py

# Полная проверка системы
python -c "
print('🔍 ДИАГНОСТИКА ТОРГОВОГО БОТА')
print('=' * 50)

# 1. Проверка Python
import sys
print(f'Python версия: {sys.version.split()[0]}')
if sys.version_info < (3, 8):
    print('❌ Требуется Python 3.8+')
else:
    print('✅ Python версия OK')

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
        for error in errors[:3]:  # Показываем первые 3 ошибки
            print(f'  ❌ {error}')
except Exception as e:
    print(f'❌ Ошибка конфигурации: {e}')

# 4. Проверка API
try:
    from modules.data_fetcher import DataFetcher
    df = DataFetcher()
    if df.health_check():
        print('✅ API подключение: OK')
    else:
        print('❌ API подключение: ОШИБКА')
except Exception as e:
    print(f'❌ API ошибка: {e}')

print('=' * 50)
"
```

---

## 🚨 Частые ошибки и решения

### 0. Бот не генерирует сигналы (НОВАЯ ПРОБЛЕМА)

#### ❌ "Бот работает, но не открывает сделки"
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

**Быстрое решение:**
```python
# В user_config.py измените:
SELECTED_STRATEGY = 'custom'  # ✅ УЖЕ НАСТРОЕНО!

CUSTOM_STRATEGY_CONFIG = {
    'volume_settings': {
        'min_ratio': 0.8,          # Снижаем требования к объему
    },
    'entry_conditions': {
        'min_conditions_required': 1,  # Только 1 условие!
        'signal_cooldown': 60,         # Каждую минуту
    }
}
```

### 1. Ошибки импорта модулей

#### `ModuleNotFoundError: No module named 'ta'`

**Решение:**
```bash
# Установка отсутствующего модуля
pip install ta

# Или переустановка всех зависимостей
pip install -r requirements.txt

# Проверка установки
python -c "import ta; print('✅ ta установлен')"
```

#### `ModuleNotFoundError: No module named 'pybit'`

**Решение:**
```bash
# Установка pybit
pip install pybit>=5.6.0

# Проверка версии
python -c "import pybit; print(f'pybit версия: {pybit.__version__}')"
```

### 2. Ошибки конфигурации

### Если что-то пошло не так

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

#### `API ключ не настроен`

**Проблема:** В user_config.py остались значения по умолчанию

**Решение:**
```python
# В user_config.py замените:
BYBIT_API_KEY = "bVnEkHGAs1t90HbTmR"    # ❌ ПРИМЕР (замените на свой!)
BYBIT_API_SECRET = "A91FxgRB0WdIYXR3l7AaShnR0UQOx6cUb2dy" # ❌ ПРИМЕР (замените на свой!)

# На ваши реальные ключи (получите на ByBit):
BYBIT_API_KEY = "ваш_реальный_api_ключ"    # ✅ ПРАВИЛЬНО
BYBIT_API_SECRET = "ваш_реальный_секрет"   # ✅ ПРАВИЛЬНО
```

#### `Веса портфеля не равны 1.0`

**Проблема:** Сумма весов включенных торговых пар не равна 1.0

**Решение:**
```python
# Проверьте веса включенных пар:
TRADING_PAIRS = {
    'ETHUSDT': {
        'enabled': True,
        'weight': 0.4,      # 40%
    },
    'SOLUSDT': {
        'enabled': True,
        'weight': 0.6,      # 60%
    },
    # Сумма: 0.4 + 0.6 = 1.0 ✅
}
```

### 3. Ошибки API подключения

#### `Connection failed` или `Timeout`

**Возможные причины:**
- Проблемы с интернетом
- Неправильные API ключи
- Блокировка IP
- Технические работы на ByBit

**Решения:**
```bash
# 1. Проверка интернета
ping google.com

# 2. Проверка доступности ByBit
ping api.bybit.com

# 3. Тест API ключей
python -c "
from pybit.unified_trading import HTTP
client = HTTP(testnet=True, api_key='ваш_ключ', api_secret='ваш_секрет')
response = client.get_server_time()
print(f'Ответ сервера: {response}')
"
```

#### `Invalid signature` или `Invalid API key`

**Решение:**
1. **Проверьте правильность ключей** (нет лишних пробелов)
2. **Пересоздайте API ключи** на ByBit
3. **Проверьте права доступа** (Read + Trade)

### 4. Ошибки стратегий

#### `Strategy validation FAILED`

**Решение:**
```python
# Запуск детальной валидации
from config_loader import load_user_configuration

try:
    loader = load_user_configuration()
    print("✅ Стратегия валидна")
except Exception as e:
    print(f"❌ Ошибка стратегии: {e}")
```

#### `Unknown strategy: название_стратегии`

**Решение:**
```python
# Проверьте правильность названия в user_config.py
# Доступные стратегии:
AVAILABLE_STRATEGIES = [
    'custom',           # Настраиваемая
    'smart_money',      # Smart Money (рекомендуется)
    'trend_following',  # Следование тренду
    'scalping',         # Скальпинг
    'swing',            # Свинг торговля
    'breakout',         # Пробои
    'mean_reversion',   # Возврат к среднему
    'momentum'          # Импульсная торговля
]

# Просмотр всех стратегий:
python user_config.py --strategies

# Проверка всех доступных пар
python -c '
from user_config import UserConfig
print("📊 Все доступные пары:")
for pair, config in UserConfig.TRADING_PAIRS.items():
    status = "✅ Включена" if config["enabled"] else "❌ Отключена"
    print(f"• {pair}: {status} | {config.get(\"description\", \"Нет описания\")}")
'
```

#### `No signals generated`

**Это нормально!** Качественные стратегии не генерируют сигналы постоянно.

**Если хотите больше сигналов:**
```python
# Переключитесь на настраиваемую стратегию
SELECTED_STRATEGY = 'custom'

CUSTOM_STRATEGY_CONFIG = {
    'min_conditions_required': 2,  # Было 3
    'min_confidence': 0.5,          # Было 0.6
}

# Или выберите более активную автоматическую стратегию
SELECTED_STRATEGY = 'momentum'  # Вместо smart_money
```

---

## 🔧 Проблемы с производительностью

### Медленная работа бота

**Причины и решения:**

1. **Медленный интернет:**
```python
# Увеличьте таймауты
SECURITY_SETTINGS = {
    'api_timeout': 60,  # Было 30
}
```

2. **Много торговых пар:**
```python
# Отключите ненужные пары
TRADING_PAIRS = {
    'ETHUSDT': {'enabled': True},
    'SOLUSDT': {'enabled': False},  # Отключили
}
```

3. **Частые проверки:**
```python
# Увеличьте интервал
TIME_SETTINGS = {
    'intervals': {
        'cycle_interval': 120,  # Было 60 секунд
    }
}
```

### Высокое потребление памяти

**Решения:**
```python
# Ограничьте память
ADVANCED_SETTINGS = {
    'performance': {
        'memory_limit_mb': 256,     # Было 512
        'cache_timeout': 30,        # Было 60
    }
}
```

```bash
# Очистка логов
find logs/ -name "*.log" -mtime +7 -delete

# Очистка данных
find data/ -name "*.csv" -mtime +30 -delete
```

---

## 📊 Проблемы с данными

### `Insufficient data for analysis`

**Причины:**
- Недостаточно исторических данных
- Проблемы с получением данных с биржи

**Решения:**
```python
# 1. Увеличьте период получения данных
# В modules/data_fetcher.py измените:
start_time = end_time - timedelta(days=2)  # Было days=1

# 2. Проверьте доступность символа
from modules.data_fetcher import DataFetcher
df = DataFetcher()
price = df.get_current_price('ETHUSDT')
print(f"ETH цена: {price}")
```

### `NaN values in indicators`

**Решение:**
```python
# Проверка качества данных
import pandas as pd
from modules.data_fetcher import DataFetcher

df = DataFetcher()
data = df.get_kline('ETHUSDT', '5', start_time, end_time)

if data is not None:
    print(f"Строк данных: {len(data)}")
    print(f"NaN значений: {data.isnull().sum().sum()}")
    print(f"Колонки: {list(data.columns)}")
else:
    print("❌ Данные не получены")
```

---

## 🔄 Проблемы с логированием

### Логи не создаются

**Проверка:**
```bash
# Проверка прав на запись
ls -la logs/
touch logs/test.log  # Должно создать файл

# Создание папки если отсутствует
mkdir -p logs/{strategies,validation,trades}
```

### Логи слишком большие

**Решение:**
```python
# В user_config.py настройте ротацию
LOGGING_SETTINGS = {
    'max_log_size_mb': 50,      # Было 100
    'max_log_files': 5,         # Было 10
}
```

```bash
# Ручная очистка старых логов
find logs/ -name "*.log" -mtime +7 -delete
```

---

## 🚨 Критические ошибки

### `Emergency stop triggered`

**Причины:**
- Превышен дневной лимит потерь
- Слишком много убыточных сделок подряд
- Критическая просадка

**Действия:**
1. **Проанализируйте причину** в логах
2. **Проверьте рыночные условия**
3. **Скорректируйте настройки риска**
4. **Перезапустите бота** после исправлений

```python
# Сброс экстренного стопа (если уверены)
from modules.risk_manager import RiskManager
risk_mgr = RiskManager()
risk_mgr.reset_emergency_stop()
```

### `Database corruption` или ошибки данных

**Решение:**
```bash
# Создание бэкапа
cp -r data/ data_backup_$(date +%Y%m%d)/

# Очистка поврежденных данных
rm -rf data/performance/*
rm -rf data/diary/*

# Перезапуск бота (создаст новые файлы)
python main.py
```

---

## 🔧 Инструменты диагностики

### Скрипт полной диагностики:

```python
# diagnosis.py
import sys
import os
import traceback
from datetime import datetime

def run_full_diagnosis():
    print("🔍 ПОЛНАЯ ДИАГНОСТИКА ТОРГОВОГО БОТА")
    print("=" * 60)
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Платформа: {sys.platform}")
    print(f"Python: {sys.version.split()[0]}")
    print()
    
    # 1. Проверка файловой системы
    print("📁 Проверка файловой системы:")
    required_dirs = ['logs', 'data', 'config', 'strategies', 'modules', 'utils']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ - ОТСУТСТВУЕТ")
    
    # 2. Проверка ключевых файлов
    print("\n📄 Проверка ключевых файлов:")
    required_files = [
        'main.py', 'user_config.py', 'config_loader.py',
        'modules/data_fetcher.py', 'strategies/smart_money_strategy.py'
    ]
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} - ОТСУТСТВУЕТ")
    
    # 3. Проверка зависимостей
    print("\n📦 Проверка зависимостей:")
    dependencies = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'), 
        ('ta', 'ta'),
        ('pybit', 'pybit'),
        ('requests', 'requests'),
        ('dotenv', 'python-dotenv')
    ]
    
    for display_name, import_name in dependencies:
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {display_name} ({version})")
        except ImportError:
            print(f"❌ {display_name} - НЕ УСТАНОВЛЕН")
    
    # 4. Проверка конфигурации
    print("\n⚙️ Проверка конфигурации:")
    try:
        from user_config import UserConfig
        is_valid, errors = UserConfig.validate_config()
        
        if is_valid:
            print("✅ Конфигурация валидна")
            
            # Показываем основные настройки
            print(f"  🔑 Testnet: {UserConfig.USE_TESTNET}")
            print(f"  💰 Баланс: ${UserConfig.INITIAL_BALANCE}")
            print(f"  🎯 Стратегия: {UserConfig.SELECTED_STRATEGY}")
            print(f"  📊 Активных пар: {len(UserConfig.get_enabled_pairs())}")
        else:
            print("❌ Ошибки в конфигурации:")
            for error in errors:
                print(f"    {error}")
                
    except Exception as e:
        print(f"❌ Критическая ошибка конфигурации: {e}")
        traceback.print_exc()
    
    # 5. Проверка API
    print("\n🔌 Проверка API подключения:")
    try:
        from modules.data_fetcher import DataFetcher
        df = DataFetcher()
        
        # Тест подключения
        if df.health_check():
            print("✅ API подключение работает")
            
            # Тест получения данных
            balance = df.get_account_balance()
            if balance is not None:
                print(f"✅ Баланс получен: ${balance:.2f}")
            else:
                print("⚠️ Не удалось получить баланс")
                
            # Тест цены
            price = df.get_current_price('ETHUSDT')
            if price is not None:
                print(f"✅ Цена ETH получена: ${price:.2f}")
            else:
                print("⚠️ Не удалось получить цену")
        else:
            print("❌ API подключение не работает")
            
    except Exception as e:
        print(f"❌ Ошибка API: {e}")
        traceback.print_exc()
    
    # 6. Проверка стратегии
    print("\n🎯 Проверка стратегии:")
    try:
        from strategies.strategy_factory import StrategyFactory
        factory = StrategyFactory()
        
        available = factory.get_available_strategies()
        print(f"✅ Доступно стратегий: {len(available)}")
        
        from user_config import UserConfig
        selected = UserConfig.SELECTED_STRATEGY
        
        if factory.validate_strategy_name(selected):
            print(f"✅ Выбранная стратегия валидна: {selected}")
        else:
            print(f"❌ Неизвестная стратегия: {selected}")
            print(f"Доступные: {', '.join(available)}")
            
    except Exception as e:
        print(f"❌ Ошибка стратегии: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Диагностика завершена")

if __name__ == "__main__":
    run_full_diagnosis()
```

---

## 🐛 Специфические ошибки

### Windows специфические проблемы

#### `UnicodeDecodeError`

**Решение:**
```python
# В начало main.py добавьте:
import sys
import locale
import os

# Установка кодировки UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
```

#### Проблемы с путями

**Решение:**
```python
# Используйте pathlib вместо os.path
from pathlib import Path

# Вместо:
log_file = "logs\\trading.log"  # ❌

# Используйте:
log_file = Path("logs") / "trading.log"  # ✅
```

### Linux/macOS специфические проблемы

#### Проблемы с правами доступа

**Решение:**
```bash
# Исправление прав
chmod +x start_bot.sh
chmod 755 utils/*.py
chmod 644 *.py

# Создание папок с правильными правами
mkdir -p logs data config
chmod 755 logs data config
```

#### `Permission denied` при записи логов

**Решение:**
```bash
# Проверка владельца папок
ls -la logs/

# Изменение владельца (если нужно)
sudo chown -R $USER:$USER logs/ data/
```

---

## 📊 Проблемы с данными и логами

### Логи не пишутся

**Диагностика:**
```python
# test_logging.py
import logging
import os

# Проверка создания лог-файла
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("test")
handler = logging.FileHandler(f"{log_dir}/test.log", encoding='utf-8')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("Тестовое сообщение")
print(f"✅ Лог создан: {log_dir}/test.log")

# Проверка содержимого
with open(f"{log_dir}/test.log", 'r', encoding='utf-8') as f:
    content = f.read()
    print(f"Содержимое: {content}")
```

### Данные производительности не сохраняются

**Решение:**
```python
# Проверка настроек сохранения
DATA_SETTINGS = {
    'save_performance_data': True,      # Должно быть True
    'save_trading_diary': True,         # Должно быть True
}

# Ручное сохранение
from modules.performance_tracker import PerformanceTracker
tracker = PerformanceTracker()
tracker.save_performance_data()
```

---

## 🔄 Восстановление после сбоев

### Восстановление конфигурации

```bash
# Если испортили user_config.py
git checkout user_config.py  # Восстановить из git

# Или скопировать из бэкапа
cp user_config_backup.py user_config.py
```

### Восстановление данных

```bash
# Восстановление из бэкапа
tar -xzf backup_20250807.tar.gz

# Или создание чистой структуры
rm -rf data/ logs/
python setup_directories.py
```

### Полный сброс

```bash
# ВНИМАНИЕ: Удаляет ВСЕ данные!
rm -rf logs/ data/ temp/
python setup_directories.py
python main.py
```

---

## 📞 Получение помощи

### Сбор информации для поддержки

```bash
# Создание отчета о проблеме
python -c "
import sys
import platform
from datetime import datetime

print('🆘 ОТЧЕТ О ПРОБЛЕМЕ')
print('=' * 40)
print(f'Дата: {datetime.now()}')
print(f'ОС: {platform.system()} {platform.release()}')
print(f'Python: {sys.version}')
print(f'Рабочая папка: {os.getcwd()}')

# Последние строки лога
try:
    with open('logs/trading_$(date +%Y%m%d).log', 'r') as f:
        lines = f.readlines()
        print('\nПоследние 10 строк лога:')
        for line in lines[-10:]:
            print(line.strip())
except:
    print('Логи недоступны')
" > problem_report.txt

echo "📄 Отчет сохранен в problem_report.txt"
```

### Контакты поддержки

- **📧 Email:** support@yourbot.com
- **💬 Telegram:** @YourBotSupport  
- **🐛 GitHub Issues:** [Создать issue](https://github.com/yourrepo/issues)
- **📚 Wiki:** [Документация](https://github.com/yourrepo/wiki)

### Информация для поддержки

При обращении укажите:
1. **Версию Python** (`python --version`)
2. **Операционную систему**
3. **Текст ошибки** полностью
4. **Последние строки логов**
5. **Что делали** перед ошибкой
6. **Конфигурацию** (без API ключей!)

---

## 🎯 Профилактика проблем

### Регулярное обслуживание

```bash
# Еженедельно
python user_config.py  # Проверка конфигурации
find logs/ -name "*.log" -mtime +7 -delete  # Очистка старых логов

# Ежемесячно  
pip install --upgrade -r requirements.txt  # Обновление зависимостей
tar -czf backup_$(date +%Y%m%d).tar.gz data/ user_config.py  # Бэкап

# При проблемах
python diagnosis.py  # Полная диагностика
```

### Мониторинг здоровья бота

```python
# health_check.py - запускайте периодически
from main import TradingBot
from datetime import datetime

try:
    bot = TradingBot()
    status = bot.get_bot_status()
    
    print(f"🤖 Статус бота: {'✅ Работает' if status['is_running'] else '❌ Остановлен'}")
    print(f"🔄 Циклов выполнено: {status['cycle_count']}")
    print(f"💓 Последний heartbeat: {status['last_heartbeat']}")
    print(f"📊 Торговых пар: {len(status['trading_pairs'])}")
    print(f"🎯 Стратегия: {status['strategy_name']}")
    
    if status.get('last_validation'):
        val = status['last_validation']
        print(f"✅ Валидация: {val.get('score', 0)}/100")
    
except Exception as e:
    print(f"❌ Ошибка проверки статуса: {e}")
```

---

**🎯 Если проблема не решена, создайте [issue на GitHub](https://github.com/yourrepo/issues) с подробным описанием!**