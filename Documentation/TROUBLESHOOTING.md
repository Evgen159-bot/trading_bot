# 🆘 Руководство по устранению неполадок (2025)

## 🔍 Диагностика проблем

### 🔧 **Новые инструменты отладки (2025):**

```bash
# 1. Детальная отладка стратегии
python utils/strategy_debug_tool.py ETHUSDT

# 2. Анализ логов с рекомендациями
python utils/log_analyzer.py

# 3. Оптимизация объемных фильтров
python utils/volume_optimizer.py

# 4. Анализ результатов работы
python check_results.py

# 5. Быстрая проверка логов
python utils/simple_log_check.py
```

### 📊 **Стандартные инструменты:**

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

## 🚨 Критические проблемы (2025)

### 🚨 **КРИТИЧЕСКИЕ ПРОБЛЕМЫ:**

#### ❌ "Бот генерирует большие убытки"
**Немедленные действия:**
1. **Остановите бота** (Ctrl+C)
2. **Проверьте настройки риска:**
   ```bash
   python -c "
   from user_config import UserConfig
   risk = UserConfig.RISK_SETTINGS
   print(f'🎯 Риск на сделку: {risk[\"risk_per_trade\"]*100:.1f}%')
   print(f'🛡️ Макс. позиций: {risk[\"max_positions\"]}')
   print(f'⚡ Плечо: {risk[\"max_leverage\"]}x')
   "
   ```
3. **Снизьте риски:**
   ```python
   # В user_config.py измените:
   RISK_SETTINGS = {
       'risk_per_trade': 0.001,  # 0.1% риск
       'max_positions': 1,       # Только 1 позиция
       'max_leverage': 1         # БЕЗ ПЛЕЧА!
   }
   ```
4. **Переключитесь на консервативную стратегию:**
   ```python
   SELECTED_STRATEGY = 'smart_money'  # Очень консервативная
   ```

#### ❌ "Неправильный расчет размера позиции"
**Диагностика:**
```bash
python -c "
from strategies.custom_strategy import CustomStrategy
# Проверка расчета размера позиции
strategy = CustomStrategy(None, None, {'CUSTOM_STRATEGY_CONFIG': {}})
size = strategy.calculate_position_size(1000.0, 100.0)  # $1000 баланс, $100 цена
print(f'📊 Размер позиции: {size}')
print(f'💵 Стоимость: ${size * 100:.2f}')
"
```

**Решение:**
```python
# Проверьте настройки в user_config.py:
CUSTOM_STRATEGY_CONFIG = {
    'risk_management': {
        'risk_per_trade': 0.005,      # 0.5% риск
        'leverage': 1,                # БЕЗ ПЛЕЧА!
        'max_position_value_pct': 0.05 # 5% максимум от баланса
    }
}
```

#### ❌ "ROI: -300.00%" или аномальные значения
**Причина:** Ошибки в расчетах PnL (исправлено в 2025)

**Решение:**
```python
# Обновленные безопасные настройки уже применены:
CUSTOM_STRATEGY_CONFIG = {
    'risk_management': {
        'leverage': 1,                # БЕЗ ПЛЕЧА!
        'max_stop_loss_pct': 0.03,    # Максимум 3% стоп-лосс
    }
}
```

---

## 📊 Стандартные проблемы

### ❌ "Бот не генерирует сигналы"
**Диагностика:**
```bash
# 🔧 Детальная диагностика
python utils/strategy_debug_tool.py ETHUSDT

# 📊 Анализ объемов
python utils/volume_optimizer.py

# 📈 Анализ логов
python utils/log_analyzer.py
```

**Решения:**
1. **Снизьте требования:**
   ```python
   CUSTOM_STRATEGY_CONFIG = {
       'entry_conditions': {
           'min_conditions_required': 2,  # Было 3
           'signal_cooldown': 600,        # 10 минут
       },
       'volume_settings': {
           'min_ratio': 0.8,             # Было 1.5
       }
   }
   ```

2. **Переключитесь на активную стратегию:**
   ```python
   SELECTED_STRATEGY = 'momentum'  # Или 'breakout'
   ```

#### ❌ "Слишком много убыточных сделок"
**Диагностика:**
```bash
# Анализ дневника
python utils/diary_viewer.py

# Детальная отладка
python utils/strategy_debug_tool.py ETHUSDT

# Анализ логов
python utils/log_analyzer.py
```

**Решения:**
1. **Увеличьте строгость условий:**
   ```python
   CUSTOM_STRATEGY_CONFIG = {
       'entry_conditions': {
           'min_conditions_required': 4,  # Было 3
           'signal_cooldown': 3600,       # 1 час между сигналами
       }
   }
   ```

2. **Снизьте риски:**
   ```python
   RISK_SETTINGS = {
       'risk_per_trade': 0.002,        # 0.2% риск
       'max_leverage': 1               # БЕЗ ПЛЕЧА!
   }
   ```

3. **Переключитесь на Smart Money:**
   ```python
   SELECTED_STRATEGY = 'smart_money'  # Очень консервативная
   ```

#### ❌ "Volume Ratio = 0.00"
**Это нормально для TESTNET!** В тестовой сети объемы могут быть нулевыми.

**Решения:**
```python
# Снизьте требования к объему
CUSTOM_STRATEGY_CONFIG = {
    'volume_settings': {
        'min_ratio': 0.5,  # Очень низкий порог для testnet
    }
}

# Или отключите объемный фильтр
CUSTOM_STRATEGY_CONFIG = {
    'volume_settings': {
        'enabled': False,  # Отключить объемный фильтр
    }
}
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
# 🛡️ Используйте только одну пару для начала
TRADING_PAIRS = {
    'ETHUSDT': {'enabled': True, 'weight': 1.0},
    'SOLUSDT': {'enabled': False, 'weight': 0.0},  # Отключено
    'BTCUSDT': {'enabled': False, 'weight': 0.0},  # Отключено
    'DOGEUSDT': {'enabled': False, 'weight': 0.0}, # Отключено
}
```

3. **Частые проверки:**
```python
# Увеличьте интервал
TIME_SETTINGS = {
    'intervals': {
        'cycle_interval': 60,   # Оптимальный интервал
    }
}
```

---

## 📊 Проблемы с данными

### `Insufficient data for analysis`

**Причины:**
- Недостаточно исторических данных
- Проблемы с получением данных с биржи

**Решения:**
```python
# Проверьте получение данных
python -c "
from modules.data_fetcher import DataFetcher
from datetime import datetime, timedelta
df = DataFetcher()
end_time = datetime.now()
start_time = end_time - timedelta(hours=6)
data = df.get_kline('ETHUSDT', '5', int(start_time.timestamp()), int(end_time.timestamp()))
print(f'📊 Получено данных: {len(data) if data is not None else 0} свечей')
"
```

### `NaN values in indicators`

**Решение:**
```python
# Проверка качества данных
python -c "
from modules.data_fetcher import DataFetcher
from datetime import datetime, timedelta
df = DataFetcher()
end_time = datetime.now()
start_time = end_time - timedelta(hours=6)
data = df.get_kline('ETHUSDT', '5', int(start_time.timestamp()), int(end_time.timestamp()))
if data is not None:
    print(f'📊 Строк данных: {len(data)}')
    print(f'❌ NaN значений: {data.isnull().sum().sum()}')
    print(f'📋 Колонки: {list(data.columns)}')
else:
    print('❌ Данные не получены')
"
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

## 🔧 Новые инструменты диагностики (2025)

### 🎯 **strategy_debug_tool.py** - Детальная отладка
```bash
# Анализ конкретной пары
python utils/strategy_debug_tool.py ETHUSDT

# Показывает:
# - Все рассчитанные индикаторы
# - Детальный анализ условий входа
# - Причины отсутствия сигналов
# - Рекомендации по оптимизации
```

### 📊 **log_analyzer.py** - Анализ логов
```bash
# Анализ текущих логов
python utils/log_analyzer.py

# Показывает:
# - Статистику ошибок
# - Частоту сигналов
# - Производительность циклов
# - Рекомендации по улучшению
```

### 🎯 **volume_optimizer.py** - Оптимизация объемов
```bash
# Анализ объемных паттернов
python utils/volume_optimizer.py

# Показывает:
# - Анализ объемов для каждой пары
# - Рекомендации по настройке min_ratio
# - Оптимальные пороги фильтров
```

### 🔍 **simple_log_check.py** - Быстрая проверка
```bash
# Быстрый анализ последних логов
python utils/simple_log_check.py

# Показывает:
# - Статистику сигналов
# - Последние записи
# - Быстрые рекомендации
```

### 📊 **check_results.py** - Анализ результатов
```bash
# Полный анализ результатов работы
python check_results.py

# Показывает:
# - Анализ логов за день
# - Статистику сигналов и ошибок
# - Данные дневника торговли
# - Рекомендации по улучшению
```

---

## 🔧 Исправленные проблемы (2025)

### ✅ **Что исправлено:**

#### 1. **Критические ошибки в расчетах:**
- **Исправлен расчет размера позиции** (убрано двойное применение плеча)
- **Исправлен расчет PnL** (убрано плечо из расчета прибыли)
- **Добавлены ограничения** на аномальные значения
- **Улучшена валидация** входных данных

#### 2. **Проблемы с API:**
- **Добавлены fallback балансы** при проблемах с API
- **Улучшена обработка ошибок** подключения
- **Добавлены таймауты** и повторные попытки

#### 3. **Ошибки в коде:**
- **Убраны вызовы** несуществующих методов
- **Исправлены импорты** и зависимости
- **Добавлена проверка** на None значения

#### 4. **Проблемы безопасности:**
- **Консервативные настройки** по умолчанию
- **Только одна пара** активна изначально
- **Без плеча** по умолчанию
- **Строгие условия** входа

---

## 🛠️ Инструменты диагностики

### Скрипт полной диагностики:

```bash
# Создание отчета о проблеме
python -c "
import sys
import os
import traceback
from datetime import datetime

print('🔍 ПОЛНАЯ ДИАГНОСТИКА ТОРГОВОГО БОТА')
print('=' * 60)
print(f'Время: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}')
print(f'Платформа: {sys.platform}')
print(f'Python: {sys.version.split()[0]}')
print()

# 1. Проверка файловой системы
print('📁 Проверка файловой системы:')
required_dirs = ['logs', 'data', 'config', 'strategies', 'modules', 'utils']
for dir_name in required_dirs:
    if os.path.exists(dir_name):
        print(f'✅ {dir_name}/')
    else:
        print(f'❌ {dir_name}/ - ОТСУТСТВУЕТ')

# 2. Проверка ключевых файлов
print('\\n📄 Проверка ключевых файлов:')
required_files = [
    'main.py', 'user_config.py', 'config_loader.py',
    'modules/data_fetcher.py', 'strategies/custom_strategy.py'
]
for file_name in required_files:
    if os.path.exists(file_name):
        print(f'✅ {file_name}')
    else:
        print(f'❌ {file_name} - ОТСУТСТВУЕТ')

# 3. Проверка зависимостей
print('\\n📦 Проверка зависимостей:')
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
        print(f'✅ {display_name} ({version})')
    except ImportError:
        print(f'❌ {display_name} - НЕ УСТАНОВЛЕН')

# 4. Проверка конфигурации
print('\\n⚙️ Проверка конфигурации:')
try:
    from user_config import UserConfig
    is_valid, errors = UserConfig.validate_config()
    
    if is_valid:
        print('✅ Конфигурация валидна')
        
        # Показываем основные настройки
        print(f'  🔑 Testnet: {UserConfig.USE_TESTNET}')
        print(f'  💰 Баланс: ${UserConfig.INITIAL_BALANCE}')
        print(f'  🎯 Стратегия: {UserConfig.SELECTED_STRATEGY}')
        print(f'  📊 Активных пар: {len(UserConfig.get_enabled_pairs())}')
    else:
        print('❌ Ошибки в конфигурации:')
        for error in errors:
            print(f'    {error}')
            
except Exception as e:
    print(f'❌ Критическая ошибка конфигурации: {e}')
    traceback.print_exc()

# 5. Проверка API
print('\\n🔌 Проверка API подключения:')
try:
    from modules.data_fetcher import DataFetcher
    df = DataFetcher()
    
    # Тест подключения
    if df.health_check():
        print('✅ API подключение работает')
        
        # Тест получения данных
        balance = df.get_account_balance()
        if balance is not None:
            print(f'✅ Баланс получен: ${balance:.2f}')
        else:
            print('⚠️ Не удалось получить баланс')
            
        # Тест цены
        price = df.get_current_price('ETHUSDT')
        if price is not None:
            print(f'✅ Цена ETH получена: ${price:.2f}')
        else:
            print('⚠️ Не удалось получить цену')
    else:
        print('❌ API подключение не работает')
        
except Exception as e:
    print(f'❌ Ошибка API: {e}')
    traceback.print_exc()

print('\\n' + '=' * 60)
print('🎯 Диагностика завершена')
"
```

---

## 🆘 Экстренные процедуры

### 🚨 **При критических убытках:**

1. **Немедленно остановите бота:** Ctrl+C
2. **Проверьте дневник:**
   ```bash
   python utils/diary_viewer.py
   ```
3. **Анализируйте причины:**
   ```bash
   python utils/log_analyzer.py
   python utils/strategy_debug_tool.py ETHUSDT
   ```
4. **Создайте безопасную конфигурацию:**
   ```python
   # Экстренные настройки
   SELECTED_STRATEGY = 'smart_money'
   RISK_SETTINGS = {
       'risk_per_trade': 0.001,  # 0.1% риск
       'max_positions': 1,       # Только 1 позиция
       'max_leverage': 1         # БЕЗ ПЛЕЧА!
   }
   # Только ETHUSDT включена
   ```

### 🔧 **При технических проблемах:**

```bash
# Полная переустановка зависимостей
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Очистка кэша Python
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# Восстановление структуры
python setup_directories.py
```

---

## 💡 Лучшие практики (2025)

### ✅ **Делайте:**
- **Начинайте с TESTNET** и малых рисков
- **Используйте новые инструменты** диагностики
- **Регулярно анализируйте** результаты через дневник
- **Постепенно увеличивайте** сложность настроек
- **Ведите бэкапы** конфигурации

### ❌ **Не делайте:**
- **Не используйте плечо** без опыта
- **Не включайте много пар** сразу
- **Не игнорируйте** убыточные результаты
- **Не запускайте** без тестирования на TESTNET
- **Не оставляйте** без мониторинга

---

## 🔧 Порядок диагностики при проблемах

### 🎯 **Рекомендуемая последовательность:**
1. `python utils/simple_log_check.py` - быстрая оценка ситуации
2. `python utils/strategy_debug_tool.py ETHUSDT` - детальная диагностика
3. `python utils/log_analyzer.py` - анализ производительности
4. `python utils/volume_optimizer.py` - оптимизация настроек
5. `python check_results.py` - полный анализ результатов

### 🔧 **При критических проблемах:**
1. **Остановите бота** (Ctrl+C)
2. **Запустите диагностику:** `python check_results.py`
3. **Анализируйте дневник:** `python utils/diary_viewer.py`
4. **Исправьте настройки** в user_config.py
5. **Протестируйте:** `python utils/simple_strategy_test.py`
6. **Перезапустите:** `python main.py`

---

## 📞 Получение помощи

### 🔧 **Быстрая диагностика для поддержки:**

```bash
# Полная диагностика одной командой
python -c "
print('🔍 ЭКСПРЕСС-ДИАГНОСТИКА')
print('=' * 40)

# 1. Конфигурация
try:
    from user_config import UserConfig
    enabled_pairs = UserConfig.get_enabled_pairs()
    print(f'✅ Активных пар: {len(enabled_pairs)}')
    print(f'🎯 Стратегия: {UserConfig.SELECTED_STRATEGY}')
    print(f'🛡️ Риск: {UserConfig.RISK_SETTINGS[\"risk_per_trade\"]*100:.1f}%')
    print(f'⚡ Плечо: {UserConfig.RISK_SETTINGS[\"max_leverage\"]}x')
except Exception as e:
    print(f'❌ Конфигурация: {e}')

# 2. API
try:
    from modules.data_fetcher import DataFetcher
    df = DataFetcher()
    balance = df.get_account_balance()
    print(f'✅ API: OK, баланс ${balance:.2f}' if balance else '❌ API: Проблемы')
except Exception as e:
    print(f'❌ API: {e}')

# 3. Последние результаты
try:
    from utils.diary_viewer import DiaryViewer
    viewer = DiaryViewer()
    status = viewer.get_current_day_status()
    print(f'📊 Сделок сегодня: {status.get(\"completed_trades\", 0)}')
    print(f'💰 Дневной результат: ${status.get(\"daily_return\", 0):.2f}')
except Exception as e:
    print(f'❌ Дневник: {e}')

print('=' * 40)
"
```

### 🆘 **При обращении в поддержку приложите:**
1. **Результаты диагностики:** `python utils/strategy_debug_tool.py ETHUSDT`
2. **Анализ логов:** `python utils/log_analyzer.py`
3. **Конфигурацию:** `python user_config.py` (без API ключей!)
4. **Дневник:** `python utils/diary_viewer.py`
5. **Отчет о проблеме:** `python check_results.py`

---

## 🎯 Профилактика проблем

### 🛡️ **Ежедневные проверки:**

```bash
# Утренняя рутина
python utils/diary_viewer.py           # Результаты дня
python utils/simple_log_check.py       # Проверка логов
python user_config.py                  # Валидация конфигурации

# При проблемах
python utils/strategy_debug_tool.py ETHUSDT  # Детальная диагностика
python utils/log_analyzer.py                # Анализ производительности
```

### 📊 **Еженедельные задачи:**

```bash
# Анализ недели
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_week()"

# Экспорт данных
python -c "
from modules.trading_diary import TradingDiary
diary = TradingDiary()
export_path = diary.export_diary_to_csv(7)
print(f'📊 Экспорт недели: {export_path}')
"

# Бэкап конфигурации
cp user_config.py user_config_backup_$(date +%Y%m%d).py

# Очистка старых логов
find logs/ -name "*.log" -mtime +7 -delete
```

### 🔧 **Мониторинг здоровья бота:**

```bash
# Проверка статуса (если бот запущен)
python -c "
try:
    from main import TradingBot
    bot = TradingBot()
    status = bot.get_bot_status()
    print(f'🤖 Статус: {\"Работает\" if status[\"is_running\"] else \"Остановлен\"}')
    print(f'🔄 Циклов: {status[\"cycle_count\"]}')
    print(f'🎯 Стратегия: {status[\"strategy_name\"]}')
    
    if status.get('last_validation'):
        val = status['last_validation']
        print(f'✅ Валидация: {val.get(\"score\", 0)}/100')
except Exception as e:
    print(f'❌ Ошибка проверки: {e}')
"
```

---

## 📚 Дополнительные ресурсы

### 📖 **Обучающие материалы:**
- **[📋 strategies/strategy_descriptions.md](strategies/strategy_descriptions.md)** - Подробные описания стратегий
- **[🔧 utils/README.md](utils/README.md)** - Описание всех утилит
- **[📊 TRADING_PAIRS_GUIDE.md](TRADING_PAIRS_GUIDE.md)** - Руководство по торговым парам

### 🛠️ **Инструменты разработчика:**
```bash
# Создание собственной стратегии
cp strategies/custom_strategy.py strategies/my_strategy.py

# Тестирование новой стратегии
python utils/simple_strategy_test.py

# Валидация стратегии
python -c "
from main import TradingBot
bot = TradingBot()
result = bot.run_strategy_validation(strict_mode=True)
print(f'Строгая валидация: {result}')
"
```

---

**🎯 Используйте новые инструменты диагностики для быстрого решения проблем!**

### 🔧 **Порядок диагностики:**
1. `python utils/simple_log_check.py` - быстрая проверка
2. `python utils/strategy_debug_tool.py ETHUSDT` - детальная отладка
3. `python utils/log_analyzer.py` - анализ производительности
4. `python utils/volume_optimizer.py` - оптимизация фильтров
5. `python check_results.py` - полный анализ результатов

### Контакты поддержки

- **📧 Email:** support@yourbot.com
- **💬 Telegram:** @YourBotSupport
- **📚 Документация:** [Wiki](https://github.com/yourrepo/wiki)
- **🐛 Баги:** [Issues](https://github.com/yourrepo/issues)

### Информация для поддержки

При обращении укажите:
1. **Версию Python** (`python --version`)
2. **Операционную систему**
3. **Текст ошибки** полностью
4. **Последние строки логов**
5. **Что делали** перед ошибкой
6. **Конфигурацию** (без API ключей!)
7. **Результаты диагностики** из новых инструментов

---

**🎯 Если проблема не решена, создайте [issue на GitHub](https://github.com/yourrepo/issues) с подробным описанием!**