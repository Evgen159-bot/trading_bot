# 🧪 Руководство по долгосрочному тестированию торгового бота

## 🎯 Стратегия тестирования на 2-3 месяца

### 📋 План тестирования:

**Месяц 1:** Базовое тестирование и настройка  
**Месяц 2:** Оптимизация и A/B тестирование  
**Месяц 3:** Финальная настройка и подготовка к продакшену  

---

## 💻 Настройка тестового ноутбука

### 🖥️ Рекомендуемые характеристики БУ ноутбука:

**Минимальные требования:**
- **CPU:** Intel i3 / AMD Ryzen 3 (любого поколения)
- **RAM:** 4GB (достаточно для бота)
- **SSD:** 128GB (для ОС, бота и логов)
- **Интернет:** Стабильное Wi-Fi подключение
- **Цена:** $200-400

**Рекомендуемые характеристики:**
- **CPU:** Intel i5 / AMD Ryzen 5
- **RAM:** 8GB (комфортная работа)
- **SSD:** 256GB (больше места для данных)
- **Цена:** $400-600

### 🐧 Выбор операционной системы:

#### Вариант 1: Ubuntu 22.04 LTS (Рекомендуется)
```bash
# Преимущества:
✅ Бесплатная и стабильная
✅ Отличная поддержка Python
✅ Низкое потребление ресурсов
✅ Удаленное управление через SSH
✅ Автоматические обновления безопасности

# Установка Python и зависимостей:
sudo apt update
sudo apt install python3.10 python3-pip git htop screen
```

#### Вариант 2: Windows 10/11
```bash
# Преимущества:
✅ Привычный интерфейс
✅ Удаленный рабочий стол
✅ Простая настройка

# Установка:
# Скачайте Python 3.10+ с python.org
# Установите Git for Windows
```

---

## 🔧 Настройка окружения для долгосрочного тестирования

### 1. Базовая настройка системы:

```bash
# Ubuntu setup script
#!/bin/bash
echo "🚀 Настройка тестового сервера для торгового бота"

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install -y python3.10 python3-pip git htop screen vim curl wget

# Настройка автозапуска
sudo systemctl enable ssh
sudo ufw enable
sudo ufw allow ssh

# Создание пользователя для бота
sudo useradd -m -s /bin/bash trader
sudo usermod -aG sudo trader

echo "✅ Базовая настройка завершена"
```

### 2. Установка бота:

```bash
# Переключение на пользователя trader
sudo su - trader

# Клонирование проекта
git clone https://github.com/your-repo/trading-bot.git
cd trading-bot

# Создание виртуального окружения
python3 -m venv .venv
source .venv/bin/activate

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Настройка автозапуска
python setup_directories.py
```

### 3. Настройка автозапуска и мониторинга:

```bash
# Создание systemd сервиса
sudo tee /etc/systemd/system/trading-bot.service > /dev/null <<EOF
[Unit]
Description=ByBit Trading Bot
After=network.target

[Service]
Type=simple
User=trader
WorkingDirectory=/home/trader/trading-bot
Environment=PATH=/home/trader/trading-bot/.venv/bin
ExecStart=/home/trader/trading-bot/.venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Активация сервиса
sudo systemctl daemon-reload
sudo systemctl enable trading-bot
sudo systemctl start trading-bot

# Проверка статуса
sudo systemctl status trading-bot
```

---

## 📊 Конфигурация для долгосрочного тестирования

### 1. Настройка user_config.py для тестирования:

```python
class UserConfig:
    # API настройки для тестирования
    BYBIT_API_KEY = "ваш_testnet_api_ключ"
    BYBIT_API_SECRET = "ваш_testnet_секрет"
    USE_TESTNET = True  # ОБЯЗАТЕЛЬНО для тестирования!
    
    # Тестовый баланс
    INITIAL_BALANCE = 10000.0  # $10,000 виртуальных для полноценного теста
    MIN_BALANCE_THRESHOLD = 1000.0
    
    # Рекомендуемая стратегия для тестирования
    SELECTED_STRATEGY = 'custom'  # Более активная для получения данных
    
    # Настройки для тестирования всех 4 пар
    TRADING_PAIRS = {
        'ETHUSDT': {'enabled': True, 'weight': 0.25},   # 25%
        'BTCUSDT': {'enabled': True, 'weight': 0.25},   # 25%
        'SOLUSDT': {'enabled': True, 'weight': 0.25},   # 25%
        'DOGEUSDT': {'enabled': True, 'weight': 0.25},  # 25%
        # Остальные для второго этапа тестирования
        'XRPUSDT': {'enabled': False, 'weight': 0.0},
        '1000PEPEUSDT': {'enabled': False, 'weight': 0.0},
        'SUIUSDT': {'enabled': False, 'weight': 0.0}
    }
    
    # Настройки для активного тестирования
    RISK_SETTINGS = {
        'risk_per_trade': 0.02,      # 2% риск
        'max_daily_loss': 0.06,      # 6% дневной лимит
        'max_positions': 4,          # 4 позиции одновременно
        'max_daily_trades': 20,      # До 20 сделок в день
    }
    
    # Настройки пользовательской стратегии для тестирования
    CUSTOM_STRATEGY_CONFIG = {
        'entry_conditions': {
            'min_conditions_required': 2,  # Снижаем для получения сигналов
            'signal_cooldown': 120,        # 2 минуты между сигналами
        },
        'rsi_settings': {
            'oversold_upper': 45,          # Более мягкие условия
            'overbought_lower': 55,
        }
    }
    
    # Настройки для непрерывной работы
    TIME_SETTINGS = {
        'intervals': {
            'cycle_interval': 60,        # Каждую минуту
            'heartbeat_interval': 300,   # Heartbeat каждые 5 минут
        }
    }
    
    # Расширенное логирование для анализа
    LOGGING_SETTINGS = {
        'log_level': 'DEBUG',           # Детальные логи для анализа
        'detailed_trading_logs': True,
        'performance_logging': True,
    }
    
    # Автоматическое сохранение данных
    DATA_SETTINGS = {
        'save_performance_data': True,
        'save_trading_diary': True,
        'backup_enabled': True,
        'backup_interval_hours': 6,     # Бэкап каждые 6 часов
    }
```

---

## 📅 План тестирования по месяцам

### 🗓️ **Месяц 1: Базовое тестирование (недели 1-4)**

#### Неделя 1: Custom Strategy (активная настройка)
```python
SELECTED_STRATEGY = 'custom'
CUSTOM_STRATEGY_CONFIG = {
    'entry_conditions': {'min_conditions_required': 2}
}
# 4 основные пары: ETH, BTC, SOL, DOGE
```

#### Неделя 2: Momentum Strategy  
```python
SELECTED_STRATEGY = 'momentum'
# Те же 4 пары
```

#### Неделя 3: Smart Money Strategy (если нужны качественные сигналы)
```python
SELECTED_STRATEGY = 'smart_money'
# ВНИМАНИЕ: Может генерировать мало сигналов
```

#### Неделя 4: Breakout Strategy
```python
SELECTED_STRATEGY = 'breakout'
# Хорошо для волатильных рынков
```

#### Анализ месяца:
```bash
# Сравнение результатов
python utils/diary_viewer.py
# Выберите недельную сводку для каждой недели
```

### 🗓️ **Месяц 2: Оптимизация (недели 5-8)**

#### Неделя 5-6: Тестирование новых пар
```python
# Замените 2 пары на новые
TRADING_PAIRS = {
    'ETHUSDT': {'enabled': True, 'weight': 0.25},
    'BTCUSDT': {'enabled': True, 'weight': 0.25},
    'XRPUSDT': {'enabled': True, 'weight': 0.25},    # Включаем
    'SUIUSDT': {'enabled': True, 'weight': 0.25},    # Включаем
    # Отключаем DOGE и SOL для сравнения
}
```

#### Неделя 7-8: Экстремальное тестирование
```python
# Тест с мемкоинами
TRADING_PAIRS = {
    'DOGEUSDT': {'enabled': True, 'weight': 0.3},
    '1000PEPEUSDT': {'enabled': True, 'weight': 0.2},  # Включаем PEPE
    'SOLUSDT': {'enabled': True, 'weight': 0.3},
    'SUIUSDT': {'enabled': True, 'weight': 0.2},
}

# Увеличиваем стоп-лоссы для волатильных пар
```

### 🗓️ **Месяц 3: Финализация (недели 9-12)**

#### Неделя 9-10: Лучшая комбинация
```python
# На основе результатов предыдущих тестов
# Выберите 4 лучшие пары
```

#### Неделя 11-12: Стресс-тестирование
```python
# Увеличиваем нагрузку
RISK_SETTINGS = {
    'max_daily_trades': 50,      # Больше сделок
    'cycle_interval': 30,        # Чаще проверки
}
```

---

## 🛠️ Инструменты для долгосрочного тестирования

### 1. Скрипт автоматического мониторинга:

#### 🆕 Новые инструменты диагностики (2025):

```bash
# Детальная отладка стратегии с полным анализом
python utils/strategy_debug_tool.py ETHUSDT

# Анализ логов с выявлением проблем и рекомендациями
python utils/log_analyzer.py

# Оптимизация объемных фильтров
python utils/volume_optimizer.py

# Пример использования в мониторинге:
#!/bin/bash
# enhanced_monitoring.sh

echo "🔍 РАСШИРЕННАЯ ДИАГНОСТИКА БОТА"
echo "=" * 50

# Анализ логов
python utils/log_analyzer.py

# Отладка стратегии для каждой пары
for pair in ETHUSDT SOLUSDT BTCUSDT DOGEUSDT; do
    echo "Анализ $pair:"
    python utils/strategy_debug_tool.py $pair
    echo "---"
done

# Оптимизация объемов
python utils/volume_optimizer.py
```

#### Классический мониторинг:
```python
# monitoring_daemon.py
import time
import os
import subprocess
import logging
from datetime import datetime, timedelta
import json

class BotMonitor:
    def __init__(self):
        self.setup_logging()
        self.bot_process = None
        self.restart_count = 0
        self.max_restarts = 10
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('monitoring.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def start_monitoring(self):
        """Запуск мониторинга бота"""
        self.logger.info("🔍 Запуск мониторинга торгового бота")
        
        while True:
            try:
                # Проверка процесса бота
                if not self.is_bot_running():
                    self.logger.warning("🚨 Бот не запущен, перезапускаем...")
                    self.restart_bot()
                
                # Проверка здоровья каждые 5 минут
                time.sleep(300)
                self.health_check()
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Мониторинг остановлен пользователем")
                break
            except Exception as e:
                self.logger.error(f"❌ Ошибка мониторинга: {e}")
                time.sleep(60)
    
    def is_bot_running(self):
        """Проверка запущен ли бот"""
        try:
            result = subprocess.run(['pgrep', '-f', 'main.py'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def restart_bot(self):
        """Перезапуск бота"""
        if self.restart_count >= self.max_restarts:
            self.logger.critical("🚨 Превышено максимальное количество перезапусков!")
            return False
            
        try:
            # Запуск бота в screen сессии
            subprocess.run([
                'screen', '-dmS', 'trading_bot', 
                'python', '/home/trader/trading-bot/main.py'
            ])
            
            self.restart_count += 1
            self.logger.info(f"🔄 Бот перезапущен (попытка {self.restart_count})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка перезапуска: {e}")
            return False
    
    def health_check(self):
        """Проверка здоровья бота"""
        try:
            # Проверка размера логов
            log_size = os.path.getsize('logs/trading_' + datetime.now().strftime('%Y%m%d') + '.log')
            if log_size > 100 * 1024 * 1024:  # 100MB
                self.logger.warning(f"⚠️ Большой размер лога: {log_size/1024/1024:.1f}MB")
            
            # Проверка свободного места
            disk_usage = subprocess.run(['df', '-h', '.'], capture_output=True, text=True)
            self.logger.info(f"💾 Использование диска: {disk_usage.stdout.split()[-2]}")
            
            # Проверка последней активности
            try:
                with open('logs/trading_' + datetime.now().strftime('%Y%m%d') + '.log', 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1]
                        self.logger.info(f"📝 Последняя активность: {last_line.strip()}")
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"❌ Ошибка health check: {e}")

if __name__ == "__main__":
    monitor = BotMonitor()
    monitor.start_monitoring()
```

### 2. Скрипт ежедневных отчетов:

```python
# daily_report.py
import json
import os
from datetime import datetime, date, timedelta
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class DailyReporter:
    def __init__(self):
        self.diary_dir = Path("data/diary")
        
    def generate_daily_report(self, target_date=None):
        """Генерация ежедневного отчета"""
        if target_date is None:
            target_date = date.today()
            
        report = self.get_day_data(target_date)
        
        # Создание текстового отчета
        report_text = self.format_report(report, target_date)
        
        # Сохранение отчета
        report_file = f"reports/daily_report_{target_date.isoformat()}.txt"
        os.makedirs("reports", exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
            
        print(f"📊 Отчет сохранен: {report_file}")
        
        # Отправка по email (если настроено)
        self.send_email_report(report_text, target_date)
        
        return report_text
    
    def get_day_data(self, target_date):
        """Получение данных дня"""
        filename = f"diary_{target_date.isoformat()}.json"
        filepath = self.diary_dir / filename
        
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def format_report(self, data, target_date):
        """Форматирование отчета"""
        if not data:
            return f"📅 {target_date.strftime('%d.%m.%Y')}: Нет данных торговли"
            
        report = f"""
📊 ЕЖЕДНЕВНЫЙ ОТЧЕТ ТОРГОВОГО БОТА
{'='*50}
📅 Дата: {target_date.strftime('%d.%m.%Y')}
⏰ Период: {data.get('session_start', 'N/A')} - {data.get('session_end', 'активна')}

💰 ФИНАНСОВЫЕ РЕЗУЛЬТАТЫ:
   Начальный баланс: ${data.get('start_balance', 0):.2f}
   Конечный баланс:  ${data.get('end_balance', data.get('current_balance', 0)):.2f}
   Дневной P&L:      ${data.get('daily_return', 0):+.2f}
   Дневной ROI:      {data.get('daily_return_pct', 0):+.2f}%

📊 ТОРГОВАЯ СТАТИСТИКА:
   Всего сделок:     {data.get('daily_stats', {}).get('total_trades', 0)}
   Прибыльных:       {data.get('daily_stats', {}).get('winning_trades', 0)}
   Убыточных:        {data.get('daily_stats', {}).get('losing_trades', 0)}
   Win Rate:         {data.get('daily_stats', {}).get('win_rate', 0):.1f}%
   Общий P&L:        ${data.get('daily_stats', {}).get('total_pnl', 0):.2f}
   Комиссии:         ${data.get('daily_stats', {}).get('total_fees', 0):.2f}

🎯 ЛУЧШИЕ/ХУДШИЕ СДЕЛКИ:
   Лучшая сделка:    ${data.get('daily_stats', {}).get('max_profit', 0):.2f}
   Худшая сделка:    ${data.get('daily_stats', {}).get('max_loss', 0):.2f}

📈 ДЕТАЛИ СДЕЛОК:
"""
        
        # Добавляем детали сделок
        trades = data.get('trades', [])
        if trades:
            for i, trade in enumerate(trades, 1):
                pnl_emoji = "💚" if trade.get('net_pnl', 0) > 0 else "❤️"
                report += f"""
   {i}. {trade['symbol']} {trade['direction']} | {pnl_emoji} ${trade.get('net_pnl', 0):.2f}
      Время: {trade.get('duration', 'N/A')} | ROI: {trade.get('roi_pct', 0):+.2f}%
      Причина закрытия: {trade.get('close_reason', 'N/A')}"""
        
        report += f"\n{'='*50}\n"
        return report
    
    def send_email_report(self, report_text, target_date):
        """Отправка отчета по email"""
        # Настройте email в user_config.py если нужно
        pass

# Автоматический запуск ежедневных отчетов
if __name__ == "__main__":
    reporter = DailyReporter()
    
    # Генерация отчета за вчера
    yesterday = date.today() - timedelta(days=1)
    reporter.generate_daily_report(yesterday)
```

### 3. Скрипт еженедельного анализа:

```python
# weekly_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from datetime import date, timedelta

class WeeklyAnalyzer:
    def __init__(self):
        self.diary_dir = Path("data/diary")
        
    def analyze_week(self, weeks_back=0):
        """Анализ недели"""
        end_date = date.today() - timedelta(weeks=weeks_back)
        start_date = end_date - timedelta(days=7)
        
        print(f"📊 АНАЛИЗ НЕДЕЛИ: {start_date} - {end_date}")
        print("="*60)
        
        # Сбор данных за неделю
        week_data = self.collect_week_data(start_date, end_date)
        
        if not week_data:
            print("❌ Нет данных за эту неделю")
            return
            
        # Анализ производительности
        self.analyze_performance(week_data)
        
        # Анализ по парам
        self.analyze_by_pairs(week_data)
        
        # Анализ по стратегиям
        self.analyze_strategies(week_data)
        
        # Создание графиков
        self.create_charts(week_data, start_date, end_date)
    
    def collect_week_data(self, start_date, end_date):
        """Сбор данных за неделю"""
        week_data = []
        current_date = start_date
        
        while current_date <= end_date:
            filename = f"diary_{current_date.isoformat()}.json"
            filepath = self.diary_dir / filename
            
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    day_data = json.load(f)
                    week_data.append(day_data)
            
            current_date += timedelta(days=1)
            
        return week_data
    
    def analyze_performance(self, week_data):
        """Анализ производительности"""
        total_return = sum(day.get('daily_return', 0) for day in week_data)
        total_trades = sum(day.get('daily_stats', {}).get('total_trades', 0) for day in week_data)
        
        winning_days = len([day for day in week_data if day.get('daily_return', 0) > 0])
        
        print(f"💰 Общий результат недели: ${total_return:+.2f}")
        print(f"📊 Всего сделок: {total_trades}")
        print(f"📈 Прибыльных дней: {winning_days}/{len(week_data)}")
        print(f"🎯 Средний дневной результат: ${total_return/len(week_data):+.2f}")
        print()
    
    def analyze_by_pairs(self, week_data):
        """Анализ по торговым парам"""
        pair_stats = {}
        
        for day in week_data:
            for trade in day.get('trades', []):
                symbol = trade['symbol']
                if symbol not in pair_stats:
                    pair_stats[symbol] = {
                        'trades': 0, 'profit': 0, 'loss': 0, 'total_pnl': 0
                    }
                
                pair_stats[symbol]['trades'] += 1
                pnl = trade.get('net_pnl', 0)
                pair_stats[symbol]['total_pnl'] += pnl
                
                if pnl > 0:
                    pair_stats[symbol]['profit'] += 1
                else:
                    pair_stats[symbol]['loss'] += 1
        
        print("📊 АНАЛИЗ ПО ТОРГОВЫМ ПАРАМ:")
        for symbol, stats in sorted(pair_stats.items(), key=lambda x: x[1]['total_pnl'], reverse=True):
            win_rate = (stats['profit'] / stats['trades'] * 100) if stats['trades'] > 0 else 0
            print(f"   {symbol}: ${stats['total_pnl']:+.2f} | {stats['trades']} сделок | WR: {win_rate:.1f}%")
        print()
    
    def create_charts(self, week_data, start_date, end_date):
        """Создание графиков"""
        try:
            try:
                import matplotlib.pyplot as plt
            except ImportError:
                print("⚠️ matplotlib не установлен, графики недоступны")
                return
            
            # График дневной прибыли
            dates = []
            returns = []
            
            for day in week_data:
                dates.append(datetime.fromisoformat(day['date']).date())
                returns.append(day.get('daily_return', 0))
            
            plt.figure(figsize=(12, 6))
            
            # График 1: Дневная прибыль
            plt.subplot(1, 2, 1)
            colors = ['green' if r > 0 else 'red' for r in returns]
            plt.bar(dates, returns, color=colors, alpha=0.7)
            plt.title('Дневная прибыль')
            plt.ylabel('USD')
            plt.xticks(rotation=45)
            
            # График 2: Кумулятивная прибыль
            plt.subplot(1, 2, 2)
            cumulative = [sum(returns[:i+1]) for i in range(len(returns))]
            plt.plot(dates, cumulative, marker='o', linewidth=2)
            plt.title('Кумулятивная прибыль')
            plt.ylabel('USD')
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            
            # Сохранение графика
            chart_file = f"reports/week_chart_{start_date}_{end_date}.png"
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            print(f"📈 График сохранен: {chart_file}")
            
        except ImportError:
            print("⚠️ matplotlib не установлен, графики недоступны")
        except Exception as e:
            print(f"❌ Ошибка создания графиков: {e}")

if __name__ == "__main__":
    analyzer = WeeklyAnalyzer()
    
    # Анализ текущей недели
    analyzer.analyze_week(0)
    
    # Анализ прошлой недели
    analyzer.analyze_week(1)
```

### 4. Автоматический бэкап:

```bash
#!/bin/bash
# backup_script.sh - Автоматический бэкап

BACKUP_DIR="/home/trader/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BOT_DIR="/home/trader/trading-bot"

echo "💾 Создание бэкапа: $DATE"

# Создание директории бэкапов
mkdir -p $BACKUP_DIR

# Создание архива
tar -czf "$BACKUP_DIR/bot_backup_$DATE.tar.gz" \
    -C "$BOT_DIR" \
    user_config.py \
    logs/ \
    data/ \
    reports/ \
    --exclude="*.pyc" \
    --exclude="__pycache__"

# Удаление старых бэкапов (старше 30 дней)
find $BACKUP_DIR -name "bot_backup_*.tar.gz" -mtime +30 -delete

echo "✅ Бэкап создан: bot_backup_$DATE.tar.gz"

# Проверка размера
ls -lh "$BACKUP_DIR/bot_backup_$DATE.tar.gz"
```

---

## 🔄 Настройка автоматизации

### 1. Crontab для автоматических задач:

```bash
# Редактирование crontab
crontab -e

# Добавьте следующие строки:

# Ежедневный отчет в 23:55
55 23 * * * cd /home/trader/trading-bot && python daily_report.py

# Еженедельный анализ по воскресеньям в 23:00
0 23 * * 0 cd /home/trader/trading-bot && python weekly_analysis.py

# Бэкап каждые 6 часов
0 */6 * * * /home/trader/trading-bot/backup_script.sh

# Очистка старых логов каждую неделю
0 2 * * 1 find /home/trader/trading-bot/logs -name "*.log" -mtime +7 -delete

# Проверка места на диске ежедневно
0 1 * * * df -h /home/trader > /home/trader/disk_usage.log
```

### 2. Настройка удаленного доступа:

```bash
# SSH настройка для удаленного мониторинга
sudo nano /etc/ssh/sshd_config

# Добавьте/измените:
Port 2222                    # Нестандартный порт для безопасности
PermitRootLogin no          # Запрет root доступа
PasswordAuthentication yes   # Разрешить пароли (или используйте ключи)

# Перезапуск SSH
sudo systemctl restart ssh

# Настройка firewall
sudo ufw allow 2222/tcp
```

### 3. Screen сессии для постоянной работы:

```bash
# Создание именованной screen сессии
screen -S trading_bot

# Внутри screen запуск бота
cd /home/trader/trading-bot
source .venv/bin/activate
python main.py

# Отключение от screen (бот продолжит работать)
# Нажмите Ctrl+A, затем D

# Подключение к существующей сессии
screen -r trading_bot

# Просмотр всех сессий
screen -ls
```

---

## 📊 План A/B тестирования

### Этап 1: Тестирование стратегий (недели 1-4)

```python
# test_schedule.py
test_schedule = {
    'week_1': {
        'strategy': 'smart_money',
        'pairs': ['ETHUSDT', 'BTCUSDT', 'SOLUSDT', 'DOGEUSDT'],
        'risk_per_trade': 0.02,
        'description': 'Базовое тестирование Smart Money'
    },
    'week_2': {
        'strategy': 'trend_following', 
        'pairs': ['ETHUSDT', 'BTCUSDT', 'SOLUSDT', 'DOGEUSDT'],
        'risk_per_trade': 0.02,
        'description': 'Тестирование Trend Following'
    },
    'week_3': {
        'strategy': 'custom',
        'pairs': ['ETHUSDT', 'BTCUSDT', 'SOLUSDT', 'DOGEUSDT'],
        'risk_per_trade': 0.02,
        'custom_config': {
            'min_conditions_required': 3,
            'min_confidence': 0.65
        },
        'description': 'Консервативная настраиваемая стратегия'
    },
    'week_4': {
        'strategy': 'momentum',
        'pairs': ['ETHUSDT', 'BTCUSDT', 'SOLUSDT', 'DOGEUSDT'], 
        'risk_per_trade': 0.025,
        'description': 'Тестирование Momentum стратегии'
    }
}
```

### Этап 2: Тестирование пар (недели 5-8)

```python
pair_tests = {
    'week_5': {
        'strategy': 'smart_money',  # Лучшая из этапа 1
        'pairs': ['ETHUSDT', 'BTCUSDT', 'XRPUSDT', 'SUIUSDT'],
        'description': 'Тест стабильных пар'
    },
    'week_6': {
        'strategy': 'smart_money',
        'pairs': ['SOLUSDT', 'DOGEUSDT', '1000PEPEUSDT', 'SUIUSDT'],
        'description': 'Тест волатильных пар'
    },
    'week_7': {
        'strategy': 'smart_money',
        'pairs': ['ETHUSDT', 'SOLUSDT', 'DOGEUSDT', '1000PEPEUSDT'],
        'description': 'Смешанный портфель'
    },
    'week_8': {
        'strategy': 'smart_money',
        'pairs': ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'SUIUSDT'],
        'description': 'Консервативный портфель'
    }
}
```

---

## 🛠️ Инструменты мониторинга

### 1. Dashboard для мониторинга:

```python
# dashboard.py - Простой веб-интерфейс
from flask import Flask, render_template, jsonify
import json
from datetime import date, datetime
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Главная страница дашборда"""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """API для получения статуса бота"""
    try:
        # Получение статуса из дневника
        today = date.today()
        diary_file = Path(f"data/diary/diary_{today.isoformat()}.json")
        
        if diary_file.exists():
            with open(diary_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            return jsonify({
                'status': 'running',
                'balance': data.get('current_balance', 0),
                'daily_return': data.get('daily_return', 0),
                'trades_today': data.get('daily_stats', {}).get('total_trades', 0),
                'open_positions': len([p for p in data.get('positions', []) if p.get('status') == 'OPEN']),
                'last_update': datetime.now().isoformat()
            })
        else:
            return jsonify({'status': 'no_data'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/performance/<int:days>')
def get_performance(days):
    """Получение данных производительности"""
    try:
        performance_data = []
        
        for i in range(days):
            target_date = date.today() - timedelta(days=i)
            diary_file = Path(f"data/diary/diary_{target_date.isoformat()}.json")
            
            if diary_file.exists():
                with open(diary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    performance_data.append({
                        'date': target_date.isoformat(),
                        'return': data.get('daily_return', 0),
                        'trades': data.get('daily_stats', {}).get('total_trades', 0)
                    })
        
        return jsonify(performance_data)
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### 2. HTML шаблон для дашборда:

```html
<!-- templates/dashboard.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Trading Bot Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .status-running { color: #28a745; }
        .status-stopped { color: #dc3545; }
        .metric { display: inline-block; margin: 10px 20px 10px 0; }
        .metric-value { font-size: 24px; font-weight: bold; }
        .metric-label { font-size: 14px; color: #666; }
        .positive { color: #28a745; }
        .negative { color: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Trading Bot Dashboard</h1>
        
        <div class="card">
            <h2>📊 Текущий статус</h2>
            <div id="status">Загрузка...</div>
        </div>
        
        <div class="card">
            <h2>📈 Производительность (7 дней)</h2>
            <canvas id="performanceChart" width="800" height="400"></canvas>
        </div>
        
        <div class="card">
            <h2>🔄 Последние обновления</h2>
            <div id="updates">Загрузка...</div>
        </div>
    </div>

    <script>
        // Обновление статуса каждые 30 секунд
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const statusDiv = document.getElementById('status');
                    
                    if (data.status === 'running') {
                        statusDiv.innerHTML = `
                            <div class="status-running">🟢 Бот работает</div>
                            <div class="metric">
                                <div class="metric-value">$${data.balance.toFixed(2)}</div>
                                <div class="metric-label">Текущий баланс</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value ${data.daily_return >= 0 ? 'positive' : 'negative'}">
                                    $${data.daily_return >= 0 ? '+' : ''}${data.daily_return.toFixed(2)}
                                </div>
                                <div class="metric-label">Дневной P&L</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">${data.trades_today}</div>
                                <div class="metric-label">Сделок сегодня</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">${data.open_positions}</div>
                                <div class="metric-label">Открытых позиций</div>
                            </div>
                        `;
                    } else {
                        statusDiv.innerHTML = '<div class="status-stopped">🔴 Бот остановлен</div>';
                    }
                })
                .catch(error => {
                    document.getElementById('status').innerHTML = '❌ Ошибка загрузки статуса';
                });
        }
        
        // Обновление каждые 30 секунд
        updateStatus();
        setInterval(updateStatus, 30000);
    </script>
</body>
</html>
```

---

## 📱 Удаленный мониторинг

### 1. Telegram бот для мониторинга:

```python
# telegram_monitor.py
import asyncio
from telegram import Bot
from telegram.ext import Application, CommandHandler
import json
from datetime import date
from pathlib import Path

class TelegramMonitor:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = Bot(token=bot_token)
        
    async def send_daily_summary(self):
        """Отправка ежедневной сводки"""
        try:
            today = date.today()
            diary_file = Path(f"data/diary/diary_{today.isoformat()}.json")
            
            if diary_file.exists():
                with open(diary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                message = f"""
📊 *Дневная сводка бота*
📅 {today.strftime('%d.%m.%Y')}

💰 *Финансы:*
• Баланс: ${data.get('current_balance', 0):.2f}
• Дневной P&L: ${data.get('daily_return', 0):+.2f}
• ROI: {data.get('daily_return_pct', 0):+.2f}%

📊 *Торговля:*
• Сделок: {data.get('daily_stats', {}).get('total_trades', 0)}
• Win Rate: {data.get('daily_stats', {}).get('win_rate', 0):.1f}%
• Открытых позиций: {len([p for p in data.get('positions', []) if p.get('status') == 'OPEN'])}

🎯 *Лучшая сделка:* ${data.get('daily_stats', {}).get('max_profit', 0):.2f}
📉 *Худшая сделка:* ${data.get('daily_stats', {}).get('max_loss', 0):.2f}
"""
                
                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"❌ Ошибка отправки сводки: {e}"
            )

# Автоматическая отправка сводки
async def main():
    monitor = TelegramMonitor("ваш_bot_token", "ваш_chat_id")
    await monitor.send_daily_summary()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🎯 Рекомендации по тестовому ноутбуку

### 💻 **Конкретные модели (примеры):**

**Бюджетные варианты ($200-350):**
- ThinkPad T460/T470 (Intel i5, 8GB RAM)
- Dell Latitude 5480 (Intel i5, 8GB RAM)  
- HP EliteBook 840 G3 (Intel i5, 8GB RAM)

**Оптимальные варианты ($350-500):**
- ThinkPad T480 (Intel i5-8250U, 8GB RAM)
- Dell Latitude 7480 (Intel i7, 8GB RAM)
- MacBook Air 2017 (Intel i5, 8GB RAM)

### 🔧 **Настройка после покупки:**

```bash
# 1. Установка Ubuntu 22.04 LTS
# Скачайте с ubuntu.com/download/desktop

# 2. Первоначальная настройка
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.10 python3-pip git screen htop curl

# 3. Настройка SSH для удаленного доступа
sudo apt install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh

# 4. Настройка автозапуска
sudo systemctl set-default multi-user.target  # Без GUI для экономии ресурсов
```

---

## 📊 Метрики для отслеживания

### 1. Ключевые показатели эффективности (KPI):

```python
# kpi_tracker.py
class KPITracker:
    def __init__(self):
        self.kpis = {
            'daily_return_target': 0.5,      # 0.5% в день
            'weekly_return_target': 3.0,     # 3% в неделю  
            'monthly_return_target': 12.0,   # 12% в месяц
            'max_drawdown_limit': 15.0,      # 15% максимальная просадка
            'min_win_rate': 55.0,            # 55% минимальный win rate
            'min_profit_factor': 1.3,        # 1.3 минимальный profit factor
            'max_consecutive_losses': 5,     # 5 убытков подряд максимум
        }
    
    def check_performance(self, period_data):
        """Проверка соответствия KPI"""
        results = {}
        
        # Проверка каждого KPI
        for kpi_name, target in self.kpis.items():
            actual = self.calculate_kpi(kpi_name, period_data)
            results[kpi_name] = {
                'target': target,
                'actual': actual,
                'status': 'PASS' if self.meets_target(kpi_name, actual, target) else 'FAIL'
            }
        
        return results
    
    def generate_kpi_report(self, results):
        """Генерация отчета по KPI"""
        print("📊 KPI ОТЧЕТ")
        print("="*50)
        
        for kpi_name, data in results.items():
            status_emoji = "✅" if data['status'] == 'PASS' else "❌"
            print(f"{status_emoji} {kpi_name}: {data['actual']:.2f} (цель: {data['target']:.2f})")
```

### 2. Автоматические алерты:

```python
# alert_system.py
class AlertSystem:
    def __init__(self):
        self.alert_conditions = {
            'high_drawdown': 10.0,           # Просадка больше 10%
            'low_balance': 5000.0,           # Баланс меньше $5000
            'no_trades_hours': 24,           # Нет сделок 24 часа
            'consecutive_losses': 5,         # 5 убытков подряд
            'daily_loss_limit': 300.0,       # Дневной убыток больше $300
        }
    
    def check_alerts(self):
        """Проверка условий для алертов"""
        alerts = []
        
        # Проверка каждого условия
        for condition, threshold in self.alert_conditions.items():
            if self.check_condition(condition, threshold):
                alerts.append(self.create_alert(condition, threshold))
        
        # Отправка алертов
        for alert in alerts:
            self.send_alert(alert)
    
    def send_alert(self, alert):
        """Отправка алерта"""
        print(f"🚨 АЛЕРТ: {alert['message']}")
        # Здесь можно добавить отправку в Telegram/Email
```

---

## 🔄 Процедуры обслуживания

### Ежедневные задачи:
```bash
#!/bin/bash
# daily_maintenance.sh

echo "🔧 Ежедневное обслуживание бота"

# Проверка статуса
systemctl is-active trading-bot

# Проверка размера логов
du -sh logs/

# Проверка свободного места
df -h

# Генерация отчета
python daily_report.py

# Проверка ошибок в логах
grep -i "error\|critical" logs/trading_$(date +%Y%m%d).log | tail -10

echo "✅ Обслуживание завершено"
```

### Еженедельные задачи:
```bash
#!/bin/bash
# weekly_maintenance.sh

echo "🔧 Еженедельное обслуживание"

# Создание бэкапа
./backup_script.sh

# Анализ производительности
python weekly_analysis.py

# Очистка старых логов
find logs/ -name "*.log" -mtime +7 -delete

# Обновление системы
sudo apt update && sudo apt list --upgradable

echo "✅ Еженедельное обслуживание завершено"
```

---

## 📈 Критерии успешности тестирования

### ✅ **Положительные результаты:**
- 📊 **Месячная прибыльность:** > 5%
- 🎯 **Win Rate:** > 55%
- 📉 **Максимальная просадка:** < 15%
- 🔄 **Стабильность:** < 5 перезапусков в месяц
- ⏱️ **Время работы:** > 95% uptime

### ⚠️ **Сигналы для корректировки:**
- 📉 **Убыточность:** > 2 недель подряд
- 🎯 **Низкий Win Rate:** < 45%
- 📊 **Высокая просадка:** > 20%
- 🔄 **Частые сбои:** > 10 перезапусков в неделю

### 🚨 **Критерии остановки тестирования:**
- 💰 **Критические потери:** > 30% от начального баланса
- 🔄 **Системная нестабильность:** Постоянные сбои
- 📊 **Неработающая стратегия:** Win Rate < 30% месяц подряд

---

## 🎯 **Итоговые рекомендации:**

1. **💻 Купите ноутбук** с характеристиками выше
2. **🐧 Установите Ubuntu** для стабильности
3. **📊 Настройте мониторинг** и автоматизацию
4. **🧪 Следуйте плану тестирования** по неделям
5. **📱 Настройте удаленный доступ** для контроля
6. **💾 Автоматизируйте бэкапы** и отчеты

Такой подход даст вам полную картину работы бота в реальных условиях! 🚀