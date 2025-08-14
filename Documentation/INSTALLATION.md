# 📦 Подробное руководство по установке

## 🎯 Системные требования

### Минимальные требования:
- **Python:** 3.8+ (рекомендуется 3.10+)
- **ОС:** Windows 10+, Ubuntu 18+, macOS 10.15+
- **RAM:** 512MB свободной памяти
- **Диск:** 1GB свободного места
- **Интернет:** Стабильное подключение

### Рекомендуемые требования:
- **Python:** 3.11+
- **RAM:** 2GB+
- **Диск:** 5GB+ (для логов и данных)
- **CPU:** 2+ ядра

---

## 🚀 Автоматическая установка

### Windows:

```batch
# 1. Скачайте проект
git clone https://github.com/your-repo/bybit-trading-bot.git
cd trading-bot

# 2. Запустите автоустановку
python setup_directories.py

# 3. Запустите бота
start_bot.bat
```

### Linux/macOS:

```bash
# 1. Скачайте проект
git clone https://github.com/your-repo/bybit-trading-bot.git
cd trading-bot

# 2. Запустите автоустановку
python3 setup_directories.py

# 3. Сделайте скрипт исполняемым и запустите
chmod +x start_bot.sh
./start_bot.sh
```

---

## 🔧 Ручная установка

### Шаг 1: Подготовка окружения

```bash
# Создание виртуального окружения
python -m venv .venv

# Активация окружения
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Обновление pip
python -m pip install --upgrade pip
```

### Шаг 2: Установка зависимостей

```bash
# Основные зависимости
pip install -r requirements.txt

# Проверка установки
python -c "import pandas, ta, pybit; print('✅ Все модули установлены')"
```

### Шаг 3: Создание структуры папок

```bash
# Создание необходимых директорий
mkdir -p logs/{strategies,validation,trades}
mkdir -p data/{diary,performance,validation}
mkdir -p config
mkdir -p exports
mkdir -p temp

# Создание __init__.py файлов
touch modules/__init__.py
touch strategies/__init__.py
touch utils/__init__.py
touch config/__init__.py
```

### Шаг 4: Настройка конфигурации

```bash
# Настройка пользовательской конфигурации
# Отредактируйте user_config.py:
nano user_config.py  # или любой текстовый редактор

# Замените API ключи:
# BYBIT_API_KEY = "ваш_реальный_ключ"
# BYBIT_API_SECRET = "ваш_реальный_секрет"
```

---

## 🐳 Установка через Docker

### Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создание необходимых директорий
RUN mkdir -p logs data config exports temp

# Запуск
CMD ["python", "main.py"]
```

### Docker Compose:

```yaml
version: '3.8'

services:
  trading-bot:
    build: .
    container_name: bybit-trading-bot
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
      - ./config:/app/config
      - ./user_config.py:/app/user_config.py
    environment:
      - PYTHONUNBUFFERED=1
    networks:
      - trading-network

networks:
  trading-network:
    driver: bridge
```

### Запуск через Docker:

```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

---

## 🔧 Установка зависимостей по частям

### Если возникают проблемы с requirements.txt:

```bash
# Основные зависимости
pip install pandas>=2.1.4
pip install numpy>=1.26.2
pip install pybit>=5.4.0

# Технический анализ
pip install ta>=0.11.0
pip install pandas_ta>=0.3.14b0

# HTTP клиенты
pip install aiohttp>=3.9.1
pip install requests>=2.31.0

# Утилиты
pip install python-dotenv>=1.0.0
pip install colorlog>=6.8.0
pip install tqdm>=4.66.1

# Опциональные (для графиков)
pip install matplotlib>=3.8.2
pip install plotly>=5.17.0

# Для уведомлений
pip install python-telegram-bot>=20.7
```

---

## 🧪 Проверка установки

### Тест 1: Импорт модулей

```python
# test_imports.py
try:
    import pandas as pd
    import numpy as np
    import ta
    import pybit
    from datetime import datetime
    print("✅ Все основные модули импортированы успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
```

### Тест 2: Подключение к API

```python
# test_api.py
from modules.data_fetcher import DataFetcher

try:
    df = DataFetcher()
    if df.health_check():
        print("✅ API подключение работает")
    else:
        print("❌ Проблемы с API подключением")
except Exception as e:
    print(f"❌ Ошибка API: {e}")
```

### Тест 3: Валидация стратегии

```python
# test_strategy.py
from config_loader import load_user_configuration

try:
    loader = load_user_configuration()
    print("✅ Конфигурация загружена успешно")
except Exception as e:
    print(f"❌ Ошибка конфигурации: {e}")
```

---

## 🔄 Обновление бота

### Обновление кода:

```bash
# Сохранение конфигурации
cp user_config.py user_config_backup.py

# Получение обновлений
git pull origin main

# Восстановление конфигурации
cp user_config_backup.py user_config.py

# Обновление зависимостей
pip install --upgrade -r requirements.txt
```

### Миграция данных:

```bash
# Создание бэкапа перед обновлением
tar -czf backup_$(date +%Y%m%d).tar.gz data/ logs/ user_config.py

# После обновления - проверка совместимости
python -c "from user_config import UserConfig; UserConfig.validate_config()"
```

---

## 🐛 Устранение неполадок

### Проблемы с Python:

```bash
# Проверка версии Python
python --version

# Если версия < 3.8, обновите Python
# Windows: скачайте с python.org
# Ubuntu: sudo apt update && sudo apt install python3.11
# macOS: brew install python@3.11
```

### Проблемы с зависимостями:

```bash
# Очистка кэша pip
pip cache purge

# Переустановка зависимостей
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Установка конкретных версий
pip install pandas==2.1.4 numpy==1.26.2 ta==0.11.0
```

### Проблемы с правами доступа:

```bash
# Linux/macOS - исправление прав
chmod +x start_bot.sh
chmod 755 utils/*.py

# Windows - запуск от администратора
# Правый клик на start_bot.bat → "Запуск от имени администратора"
```

---

## 📋 Чек-лист успешной установки

- [ ] Python 3.8+ установлен
- [ ] Виртуальное окружение создано и активировано
- [ ] Все зависимости установлены без ошибок
- [ ] Структура папок создана
- [ ] API ключи настроены в user_config.py
- [ ] Конфигурация прошла валидацию
- [ ] Тестовое подключение к API работает
- [ ] Бот запускается без ошибок
- [ ] Логи создаются в папке logs/
- [ ] Стратегия выбрана и валидирована

### Финальная проверка:

```bash
python -c "
print('🔍 Финальная проверка установки:')
try:
    from user_config import UserConfig
    is_valid, errors = UserConfig.validate_config()
    print(f'✅ Конфигурация: {\"OK\" if is_valid else \"ОШИБКИ\"}')
    
    from main import TradingBot
    bot = TradingBot()
    print('✅ Бот инициализирован: OK')
    
    print('🎉 Установка завершена успешно!')
    print('🚀 Запустите: python main.py')
    
except Exception as e:
    print(f'❌ Ошибка: {e}')
    print('🔧 Проверьте установку зависимостей')
"
```

---

**🎯 После успешной установки переходите к [настройке стратегий](STRATEGIES.md) и [первому запуску](README.md#-запуск)!**