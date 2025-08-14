# 📚 Примеры использования торгового бота

## 🎯 Готовые конфигурации для разных стилей торговли

### 👶 Конфигурация для новичков

```python
# user_config.py - Безопасная настройка для начинающих

class UserConfig:
    # API настройки
    BYBIT_API_KEY = "ваш_api_ключ"
    BYBIT_API_SECRET = "ваш_секрет"
    USE_TESTNET = True  # ОБЯЗАТЕЛЬНО для начала!
    
    # Выбор стратегии
    SELECTED_STRATEGY = 'smart_money'  # Консервативная стратегия
    
    # Капитал (начинайте с малого)
    # Рекомендуемая стратегия для начинающих
    SELECTED_STRATEGY = 'custom'  # Более активная для изучения
    
    # Очень консервативные риски
    RISK_SETTINGS = {
        "risk_per_trade": 0.01,      # 1% риск на сделку
        "max_daily_loss": 0.03,      # 3% максимальная дневная потеря
        "max_positions": 2,          # Максимум 2 позиции
        "max_daily_trades": 5,       # Максимум 5 сделок в день
        "max_leverage": 2            # Низкое плечо
    }
    
    # Только одна надежная пара
    TRADING_PAIRS = {
        "ETHUSDT": {
            "enabled": True,
            "weight": 1.0,           # 100% портфеля
            "leverage": 2,           # Низкое плечо
            "stop_loss_pct": 0.02,   # 2% стоп-лосс
            "take_profit_pct": 0.04, # 4% тейк-профит
            "priority": "high"
        },
        # Все остальные пары отключены для безопасности
        "SOLUSDT": {"enabled": False, "weight": 0.0},
        "BTCUSDT": {"enabled": False, "weight": 0.0},
        "DOGEUSDT": {"enabled": False, "weight": 0.0},
        "XRPUSDT": {"enabled": False, "weight": 0.0},
        "1000PEPEUSDT": {"enabled": False, "weight": 0.0},
        "SUIUSDT": {"enabled": False, "weight": 0.0}
    }
    
    # Медленные проверки
    TIME_SETTINGS = {
        "intervals": {
            "cycle_interval": 300,   # Проверка каждые 5 минут
        },
        "timeframes": {
            "primary": "15",         # 15-минутные свечи
        }
    }
```

**Ожидаемые результаты:**
- 📊 **Сделок в день:** 1-3
- 🎯 **Win Rate:** 60-70%
- 💰 **Средняя прибыль:** 2-4%
- 📉 **Максимальная просадка:** 5-8%

---

### 🎯 Конфигурация для опытных трейдеров

```python
# user_config.py - Сбалансированная настройка

class UserConfig:
    # API настройки
    USE_TESTNET = False  # Реальная торговля
    
    # Настраиваемая стратегия
    SELECTED_STRATEGY = 'custom'
    
    # Средний капитал
    INITIAL_BALANCE = 1000.0
    MIN_BALANCE_THRESHOLD = 200.0
    
    # Сбалансированные риски
    RISK_SETTINGS = {
        'risk_per_trade': 0.02,      # 2% риск на сделку
        'max_daily_loss': 0.06,      # 6% максимальная дневная потеря
        'max_positions': 3,          # 3 позиции одновременно
        'max_daily_trades': 12,      # До 12 сделок в день
        'max_leverage': 5            # Умеренное плечо
    }
    
    # Диверсифицированный портфель
    TRADING_PAIRS = {
        'ETHUSDT': {
            'enabled': True,
            'weight': 0.3,           # 30%
            'leverage': 3,
            'stop_loss_pct': 0.025,
            'take_profit_pct': 0.05,
        },
        'BTCUSDT': {
            'enabled': True,
            'weight': 0.3,           # 30%
            'leverage': 2,
            'stop_loss_pct': 0.02,
            'take_profit_pct': 0.04,
        },
        'SOLUSDT': {
            'enabled': True,
            'weight': 0.25,          # 25%
            'leverage': 3,
            'stop_loss_pct': 0.03,
            'take_profit_pct': 0.06,
        },
        'DOGEUSDT': {
    # Простая настройка - только 2 стабильные пары
            'weight': 0.15,          # 15%
        'ETHUSDT': {'enabled': True, 'weight': 0.6},    # 60% - стабильная
        'BTCUSDT': {'enabled': True, 'weight': 0.4},    # 40% - консервативная
        # Остальные отключены для безопасности
        'SOLUSDT': {'enabled': False, 'weight': 0.0},
        'DOGEUSDT': {'enabled': False, 'weight': 0.0},
        'XRPUSDT': {'enabled': False, 'weight': 0.0},
        '1000PEPEUSDT': {'enabled': False, 'weight': 0.0},
        'SUIUSDT': {'enabled': False, 'weight': 0.0}
    }

    # Очень консервативные риски

```python
    # Много торговых пар (максимум 4)
    TRADING_PAIRS = {
        'ETHUSDT': {'enabled': True, 'weight': 0.25, 'leverage': 5},
        'BTCUSDT': {'enabled': True, 'weight': 0.25, 'leverage': 3},
        'DOGEUSDT': {'enabled': True, 'weight': 0.25, 'leverage': 5},
        'SUIUSDT': {'enabled': True, 'weight': 0.25, 'leverage': 4},
        # Остальные отключены
        'SOLUSDT': {'enabled': False, 'weight': 0.0},
        'XRPUSDT': {'enabled': False, 'weight': 0.0},
        '1000PEPEUSDT': {'enabled': False, 'weight': 0.0}
        }
    }
    
    # Настройка пользовательской стратегии
    CUSTOM_STRATEGY_CONFIG = {
        'min_conditions_required': 3,   # 3 из 6 условий
        'min_confidence': 0.65,          # 65% уверенность
        'signal_cooldown': 240,          # 4 минуты между сигналами
        
        # Настроенные индикаторы
        'rsi_settings': {
            'period': 14,
            'oversold_lower': 28,        # Немного агрессивнее
            'oversold_upper': 38,
    # Настройки пользовательской стратегии (более активные)
    CUSTOM_STRATEGY_CONFIG = {
        'entry_conditions': {
            'min_conditions_required': 2,  # Только 2 условия
            'signal_cooldown': 120,        # 2 минуты между сигналами
        },
        'rsi_settings': {
            'oversold_upper': 45,          # Более мягкие условия
            'overbought_lower': 55,
        }
        },
```

**Ожидаемые результаты:**
- 📊 **Сделок в день:** 2-8
- 🎯 **Win Rate:** 55-65%
- 💰 **Средняя прибыль:** 1-3%
- 📉 **Максимальная просадка:** 8-12%

---

### 🔥 Конфигурация для активных трейдеров

```python
# user_config.py - Агрессивная настройка

class UserConfig:
    # Реальная торговля с большим капиталом
    USE_TESTNET = False
    INITIAL_BALANCE = 5000.0
    MIN_BALANCE_THRESHOLD = 1000.0
    
    # Активная стратегия
    SELECTED_STRATEGY = 'scalping'  # Или momentum
- 📊 **Сделок в день:** 5-15
    # Агрессивные риски
- 💰 **Средняя прибыль:** 2-5%
        'risk_per_trade': 0.03,      # 3% риск на сделку
        'max_daily_loss': 0.10,      # 10% дневной лимит
        'max_positions': 5,          # До 5 позиций
        'max_daily_trades': 50,      # До 50 сделок в день
        'max_leverage': 10           # Высокое плечо
    }
    
    # Много торговых пар
    TRADING_PAIRS = {
        'ETHUSDT': {'enabled': True, 'weight': 0.25, 'leverage': 5},
        'BTCUSDT': {'enabled': True, 'weight': 0.25, 'leverage': 3},
        'SOLUSDT': {'enabled': True, 'weight': 0.25, 'leverage': 5},
        'ADAUSDT': {'enabled': True, 'weight': 0.25, 'leverage': 4},
    # Выбор стратегии на основе опыта
    SELECTED_STRATEGY = 'momentum'  # Или 'breakout', 'custom'
    # Очень активная стратегия
    SELECTED_STRATEGY = 'scalping'  # Или 'momentum', 'custom'
        'intervals': {
            'cycle_interval': 30,        # Каждые 30 секунд
        },
        'timeframes': {
            'primary': '1',              # 1-минутные свечи
        'max_positions': 4,          # До 4 позиций (максимум)
        }
        'max_positions': 4,          # 4 позиции одновременно
    
    # Telegram уведомления
    # Все 4 активные пары (максимум)
        'telegram': {
        'SOLUSDT': {'enabled': True, 'weight': 0.3, 'leverage': 5},      # 30% - высокий потенциал
        'DOGEUSDT': {'enabled': True, 'weight': 0.25, 'leverage': 5},    # 25% - мемкоин
        'SUIUSDT': {'enabled': True, 'weight': 0.25, 'leverage': 4},     # 25% - новая технология
        '1000PEPEUSDT': {'enabled': True, 'weight': 0.2, 'leverage': 5}, # 20% - экстремальная волатильность
        'DOGEUSDT': {'enabled': True, 'weight': 0.25},
        'ETHUSDT': {'enabled': False, 'weight': 0.0},
        'BTCUSDT': {'enabled': False, 'weight': 0.0},
                'daily_summary': True,
    }
```

**Ожидаемые результаты:**
- 📊 **Сделок в день:** 20-50
- 🎯 **Win Rate:** 65-75%
- 💰 **Средняя прибыль:** 0.5-2%
- 📉 **Максимальная просадка:** 15-25%

---

## 🌊 Специализированные конфигурации

### Свинг торговля (для занятых людей)

```python
class UserConfig:
    SELECTED_STRATEGY = 'swing'
    
    # Большие позиции, редкие сделки
    RISK_SETTINGS = {
        'risk_per_trade': 0.04,      # 4% риск (больше из-за редкости)
        'max_positions': 2,          # Максимум 2 позиции
        'max_daily_trades': 3,       # Максимум 3 сделки в день
    }
    
    # Долгосрочные таймфреймы
    TIME_SETTINGS = {
        'intervals': {
            'cycle_interval': 1800,      # Проверка каждые 30 минут
        },
        'timeframes': {
            'primary': '1h',             # Часовые свечи
            'trend': '4h',               # 4-часовой тренд
        }
    }
    
    # Большие цели
    TRADING_PAIRS = {
        'ETHUSDT': {
            'enabled': True,
            'weight': 0.6,
            'stop_loss_pct': 0.04,       # 4% стоп-лосс
            'take_profit_pct': 0.12,     # 12% тейк-профит
        },
        'BTCUSDT': {
            'enabled': True,
            'weight': 0.4,
            'stop_loss_pct': 0.03,
            'take_profit_pct': 0.09,
        }
    }
```

### Скальпинг (для активных трейдеров)

```python
class UserConfig:
    SELECTED_STRATEGY = 'scalping'
    
    # Частые мелкие сделки
    RISK_SETTINGS = {
        'risk_per_trade': 0.015,     # 1.5% риск
        'max_positions': 3,          # Быстрая ротация
        'max_daily_trades': 100,     # Много сделок
    }
    
    # Быстрые интервалы
    TIME_SETTINGS = {
        'intervals': {
            'cycle_interval': 15,        # Каждые 15 секунд!
        },
        'timeframes': {
            'primary': '1',              # 1-минутные свечи
        }
    }
    
    # Малые цели
    TRADING_PAIRS = {
        'ETHUSDT': {
            'enabled': True,
            'weight': 1.0,
            'leverage': 5,
            'stop_loss_pct': 0.008,      # 0.8% стоп-лосс
            'take_profit_pct': 0.016,    # 1.6% тейк-профит
        }
    }
```

---

## 📊 Примеры мониторинга

### Ежедневный мониторинг

```bash
#!/bin/bash
# daily_check.sh - Ежедневная проверка

echo "📊 ЕЖЕДНЕВНАЯ ПРОВЕРКА БОТА"
echo "Дата: $(date)"
echo

# Проверка статуса
python -c '
from main import TradingBot
try:
    bot = TradingBot()
    status = bot.get_bot_status()
    print(f"🤖 Бот: {\"Работает\" if status[\"is_running\"] else \"Остановлен\"}")
    print(f"🔄 Циклов: {status[\"cycle_count\"]}")
    print(f"🎯 Стратегия: {status[\"strategy_name\"]}")
except Exception as e:
    print(f"❌ Ошибка: {e}")
'

# Показать сегодняшние результаты
python -c '
from utils.diary_viewer import DiaryViewer
viewer = DiaryViewer()
viewer.show_today()
'

# Проверка размера логов
echo "📄 Размер логов:"
du -sh logs/

echo "✅ Проверка завершена"
```

### Еженедельный анализ

```python
# weekly_analysis.py
from utils.diary_viewer import DiaryViewer
from modules.performance_tracker import PerformanceTracker
from datetime import datetime, timedelta

def weekly_analysis():
    print("📊 ЕЖЕНЕДЕЛЬНЫЙ АНАЛИЗ")
    print("=" * 50)
    
    # Дневник за неделю
    viewer = DiaryViewer()
    weekly_data = viewer.show_week()
    
    # Статистика производительности
    tracker = PerformanceTracker()
    metrics = tracker.get_performance_metrics()
    
    print(f"\n💰 ФИНАНСОВЫЕ РЕЗУЛЬТАТЫ:")
    print(f"Общий P&L: ${metrics.get('total_pnl', 0):.2f}")
    print(f"Win Rate: {metrics.get('win_rate', 0):.1f}%")
    print(f"Profit Factor: {metrics.get('profit_factor', 0):.2f}")
    print(f"Лучшая сделка: ${metrics.get('best_trade', 0):.2f}")
    print(f"Худшая сделка: ${metrics.get('worst_trade', 0):.2f}")
    
    print(f"\n📈 ТОРГОВАЯ АКТИВНОСТЬ:")
    print(f"Всего сделок: {metrics.get('total_trades', 0)}")
    print(f"Сделок в день: {metrics.get('trades_per_day', 0):.1f}")
    print(f"Средняя длительность: {metrics.get('avg_trade_duration', 'N/A')}")
    
    print(f"\n🎯 РЕКОМЕНДАЦИИ:")
    
    win_rate = metrics.get('win_rate', 0)
    if win_rate < 50:
        print("⚠️ Низкий Win Rate - рассмотрите смену стратегии")
    elif win_rate > 70:
        print("✅ Отличный Win Rate - стратегия работает хорошо")
    
    total_pnl = metrics.get('total_pnl', 0)
    if total_pnl < 0:
        print("🔴 Убыточная неделя - проанализируйте причины")
    elif total_pnl > 50:
        print("🟢 Прибыльная неделя - продолжайте в том же духе")

if __name__ == "__main__":
    weekly_analysis()
```

---

## 🎛️ Примеры настройки стратегий

### Пример 1: Агрессивная MultiIndicator

```python
SELECTED_STRATEGY = 'MultiIndicatorStrategy'

CUSTOM_STRATEGY_CONFIG = {
    # Агрессивные условия входа
    'min_conditions_required': 2,       # Только 2 условия из 6
    'min_confidence': 0.5,               # 50% уверенность
    'signal_cooldown': 60,               # 1 минута между сигналами
    
    # Быстрые индикаторы
    'rsi_settings': {
        'period': 7,                     # Быстрый RSI
        'oversold_lower': 20,            # Более широкие зоны
        'oversold_upper': 40,
        'overbought_lower': 60,
        'overbought_upper': 80,
    },
    
    'ema_settings': {
        'fast_period': 5,                # Очень быстрые EMA
        'slow_period': 13,
        'trend_period': 34,
    },
    
    # Агрессивный риск-менеджмент
    'risk_reward_settings': {
        'max_stop_loss_pct': 0.05,       # 5% стоп-лосс
        'min_take_profit_pct': 0.08,     # 8% тейк-профит
        'risk_per_trade': 0.025,         # 2.5% риск
    },
    
    # Минимальные фильтры
    'filters': {
        'trend_filter': False,           # Отключаем фильтр тренда
        'volume_filter': True,           # Оставляем объем
        'volatility_filter': False,      # Отключаем волатильность
    }
}
```

### Пример 2: Консервативная MultiIndicator

```python
SELECTED_STRATEGY = 'MultiIndicatorStrategy'

CUSTOM_STRATEGY_CONFIG = {
    # Строгие условия входа
    'min_conditions_required': 5,       # 5 из 6 условий
    'min_confidence': 0.8,               # 80% уверенность
    'signal_cooldown': 900,              # 15 минут между сигналами
    
    # Медленные индикаторы
    'rsi_settings': {
        'period': 21,                    # Медленный RSI
        'oversold_lower': 25,            # Узкие зоны
        'oversold_upper': 30,
        'overbought_lower': 70,
        'overbought_upper': 75,
    },
    
    'ema_settings': {
        'fast_period': 21,               # Медленные EMA
        'slow_period': 50,
        'trend_period': 200,
    },
    
    # Консервативный риск-менеджмент
    'risk_reward_settings': {
        'max_stop_loss_pct': 0.04,       # 4% стоп-лосс
        'min_take_profit_pct': 0.16,     # 16% тейк-профит (R:R = 4:1)
        'risk_per_trade': 0.01,          # 1% риск
    },
    
    # Все фильтры включены
    'filters': {
        'trend_filter': True,
        'volume_filter': True,
        'volatility_filter': True,
        'time_filter': True,
    }
}
```

---

## 🎯 Примеры для разных рыночных условий

### Трендовый рынок

```python
# Когда рынок в сильном тренде
SELECTED_STRATEGY = 'TrendFollowingStrategy'

# Или настройте MultiIndicator для трендов
CUSTOM_STRATEGY_CONFIG = {
    'ema_settings': {
        'fast_period': 8,                # Быстрая реакция на тренд
        'slow_period': 21,
        'trend_period': 50,
    },
    'filters': {
        'trend_filter': True,            # Обязательно включен
    }
}

TIME_SETTINGS = {
    'timeframes': {
        'primary': '15',                 # Более долгосрочный взгляд
        'trend': '1h',
    }
}
```

### Боковой рынок

```python
# Когда рынок в боковике
SELECTED_STRATEGY = 'MeanReversionStrategy'

# Или настройте MultiIndicator для range торговли
CUSTOM_STRATEGY_CONFIG = {
    'bollinger_settings': {
        'period': 20,
        'std_deviation': 2.5,            # Более широкие полосы
    },
    'rsi_settings': {
        'oversold_lower': 15,            # Экстремальные уровни
        'overbought_upper': 85,
    },
    'filters': {
        'trend_filter': False,           # Отключаем в боковике
    }
}
```

### Волатильный рынок

```python
# Когда высокая волатильность
SELECTED_STRATEGY = 'BreakoutStrategy'

# Увеличиваем стоп-лоссы
TRADING_PAIRS = {
    'ETHUSDT': {
        'enabled': True,
        'weight': 1.0,
        'stop_loss_pct': 0.04,           # Больше стоп-лосс
        'take_profit_pct': 0.12,         # Больше цели
    }
}

# Снижаем риски
RISK_SETTINGS = {
    'risk_per_trade': 0.015,             # Меньше риск
    'max_positions': 2,                  # Меньше позиций
}
```

---

## 📱 Примеры настройки уведомлений

### Telegram уведомления

```python
NOTIFICATIONS = {
    'telegram': {
        'enabled': True,
        'bot_token': '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz',
        'chat_id': '123456789',
        'events': {
            'position_opened': True,     # 📈 Позиция открыта
            'position_closed': True,     # 📉 Позиция закрыта
            'stop_loss_hit': True,       # 🛑 Сработал стоп-лосс
            'take_profit_hit': True,     # 🎯 Достигнут тейк-профит
            'daily_summary': True,       # 📊 Дневная сводка
            'error_occurred': True,      # ❌ Ошибки
        }
    }
}
```

**Пример уведомления:**
```
🤖 ByBit Trading Bot

📈 Позиция открыта
🎯 ETHUSDT LONG
💵 Размер: 0.5 ETH  
💰 Цена входа: $3,245.67
🛑 Стоп-лосс: $3,164.34
🎯 Тейк-профит: $3,407.95
📊 Уверенность: 78%
💼 Баланс: $1,087.50
```

### Email уведомления

```python
NOTIFICATIONS = {
    'email': {
        'enabled': True,
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'email_address': 'ваш_email@gmail.com',
        'email_password': 'ваш_app_password',  # Не обычный пароль!
        'recipient': 'уведомления@gmail.com'
    }
}
```

---

## 🔄 Примеры A/B тестирования

### Тест 1: Сравнение стратегий

```bash
# Неделя 1: Smart Money
# В user_config.py измените:
SELECTED_STRATEGY = 'smart_money'
python main.py  # Запуск на неделю

# Неделя 2: Trend Following
# В user_config.py измените:
SELECTED_STRATEGY = 'trend_following'
python main.py  # Запуск на неделю

# Сравнение результатов
python utils/diary_viewer.py  # Выберите недельную сводку
```

### Тест 2: Сравнение параметров риска

```python
# Конфигурация A: Консервативная
RISK_SETTINGS_A = {
    'risk_per_trade': 0.01,      # 1% риск
    'max_positions': 2,
}

# Конфигурация B: Агрессивная  
RISK_SETTINGS_B = {
    'risk_per_trade': 0.03,      # 3% риск
    'max_positions': 4,
}

# Тестируйте каждую конфигурацию по 2 недели
# Сравните результаты через diary_viewer.py
```

---

## 🎓 Обучающие примеры

### Пример 1: Изучение Smart Money

```python
# Настройка для изучения SMC концепций
SELECTED_STRATEGY = 'smart_money'

# Включаем детальное логирование
LOGGING_SETTINGS = {
    'log_level': 'DEBUG',               # Подробные логи
    'detailed_trading_logs': True,
}

# Уведомления о каждом сигнале
NOTIFICATIONS = {
    'telegram': {
        'enabled': True,
        'events': {
            'position_opened': True,     # Изучаем каждый вход
            'position_closed': True,     # Изучаем каждый выход
        }
    }
}
```

### Пример 2: Бэктестинг стратегии

```python
# Режим бэктестинга (в разработке)
ADVANCED_SETTINGS = {
    'modes': {
        'backtesting_mode': True,        # Включить бэктестинг
        'paper_trading': True,           # Бумажная торговля
    }
}

# Исторический период для тестирования
TIME_SETTINGS = {
    'backtest_period': {
        'start_date': '2024-01-01',
        'end_date': '2024-12-31',
    }
}
```

---

## 🔧 Примеры кастомизации

### Создание собственных индикаторов

```python
# В strategies/custom_strategy.py добавьте:

def calculate_custom_indicator(self, df):
    """Пример кастомного индикатора"""
    # Ваша логика
    df['custom_ma'] = df['close'].rolling(20).mean()
    df['custom_signal'] = df['close'] > df['custom_ma']
    return df

# Использование в условиях входа:
def _check_custom_conditions(self, signals):
    custom_bullish = signals.get('custom_signal', False)
    if custom_bullish:
        return True, "CUSTOM_BULLISH"
    return False, ""
```

### Добавление новых фильтров

```python
# Пример временного фильтра
def _check_time_filter(self):
    """Торговля только в определенные часы"""
    from datetime import datetime
    
    current_hour = datetime.now().hour
    
    # Торговля только с 9 до 17 UTC
    if 9 <= current_hour <= 17:
        return True
    return False

# Использование в стратегии:
if not self._check_time_filter():
    return None  # Пропускаем сигнал
```

---

## 📊 Примеры анализа результатов

### Анализ лучших сделок

```python
# analyze_best_trades.py
from utils.diary_viewer import DiaryViewer
import json
from pathlib import Path

def analyze_best_trades():
    diary_dir = Path("data/diary")
    all_trades = []
    
    # Собираем все сделки за месяц
    for diary_file in diary_dir.glob("diary_*.json"):
        with open(diary_file, 'r', encoding='utf-8') as f:
            day_data = json.load(f)
            all_trades.extend(day_data.get('trades', []))
    
    if not all_trades:
        print("❌ Нет данных о сделках")
        return
    
    # Сортируем по прибыльности
    profitable_trades = [t for t in all_trades if t.get('net_pnl', 0) > 0]
    profitable_trades.sort(key=lambda x: x.get('net_pnl', 0), reverse=True)
    
    print("🏆 ТОП-5 ЛУЧШИХ СДЕЛОК:")
    for i, trade in enumerate(profitable_trades[:5], 1):
        print(f"{i}. {trade['symbol']} {trade['direction']}")
        print(f"   💰 Прибыль: ${trade.get('net_pnl', 0):.2f}")
        print(f"   📊 ROI: {trade.get('roi_pct', 0):.1f}%")
        print(f"   ⏱️ Длительность: {trade.get('duration', 'N/A')}")
        print()
    
    # Анализ паттернов
    symbols = {}
    directions = {}
    
    for trade in profitable_trades:
        symbol = trade['symbol']
        direction = trade['direction']
        
        symbols[symbol] = symbols.get(symbol, 0) + 1
        directions[direction] = directions.get(direction, 0) + 1
    
    print("📊 АНАЛИЗ ПАТТЕРНОВ:")
    print(f"Лучшие пары: {sorted(symbols.items(), key=lambda x: x[1], reverse=True)}")
    print(f"Лучшие направления: {sorted(directions.items(), key=lambda x: x[1], reverse=True)}")

if __name__ == "__main__":
    analyze_best_trades()
```

### Анализ просадок

```python
# analyze_drawdowns.py
from modules.performance_tracker import PerformanceTracker
import pandas as pd

def analyze_drawdowns():
    tracker = PerformanceTracker()
    equity_df = tracker.get_equity_curve_df()
    
    if equity_df.empty:
        print("❌ Нет данных об эквити")
        return
    
    # Расчет просадок
    equity_df['peak'] = equity_df['balance'].cummax()
    equity_df['drawdown'] = (equity_df['peak'] - equity_df['balance']) / equity_df['peak'] * 100
    
    # Максимальная просадка
    max_dd = equity_df['drawdown'].max()
    max_dd_date = equity_df['drawdown'].idxmax()
    
    print(f"📉 АНАЛИЗ ПРОСАДОК:")
    print(f"Максимальная просадка: {max_dd:.2f}%")
    print(f"Дата максимальной просадки: {max_dd_date}")
    
    # Периоды просадок
    in_drawdown = equity_df['drawdown'] > 1  # Просадка больше 1%
    drawdown_periods = []
    
    start = None
    for date, is_dd in in_drawdown.items():
        if is_dd and start is None:
            start = date
        elif not is_dd and start is not None:
            drawdown_periods.append((start, date))
            start = None
    
    print(f"\n📊 Периоды просадок (>1%):")
    for i, (start, end) in enumerate(drawdown_periods[-5:], 1):  # Последние 5
        duration = (end - start).days
        print(f"{i}. {start.date()} - {end.date()} ({duration} дней)")

if __name__ == "__main__":
    analyze_drawdowns()
```

---

## 🎮 Интерактивные примеры

### Интерактивный выбор стратегии

```python
# interactive_setup.py
from user_config import UserConfig

def interactive_strategy_setup():
    print("🎯 ИНТЕРАКТИВНАЯ НАСТРОЙКА СТРАТЕГИИ")
    print("=" * 50)
    
    strategies = list(UserConfig.STRATEGY_DESCRIPTIONS.keys())
    
    print("Доступные стратегии:")
    for i, strategy in enumerate(strategies, 1):
        info = UserConfig.STRATEGY_DESCRIPTIONS[strategy]
        risk_emoji = {"низкий": "🟢", "средний": "🟡", "высокий": "🔴"}.get(info.get('risk_level', ''), "⚪")
        print(f"{i}. {info['name']} {risk_emoji}")
    
    while True:
        try:
            choice = int(input(f"\nВыберите стратегию (1-{len(strategies)}): "))
            if 1 <= choice <= len(strategies):
                selected = strategies[choice - 1]
                break
            else:
                print("❌ Неверный номер")
        except ValueError:
            print("❌ Введите число")
    
    print(f"\n✅ Выбрана стратегия: {selected}")
    
    # Настройка рисков
    print(f"\n💰 Настройка рисков:")
    balance = float(input("Ваш депозит в USD: "))
    risk = float(input("Риск на сделку в % (1-5): ")) / 100
    
    print(f"\n📋 РЕКОМЕНДУЕМАЯ КОНФИГУРАЦИЯ:")
    print(f"SELECTED_STRATEGY = '{selected}'")
    print(f"INITIAL_BALANCE = {balance}")
    print(f"RISK_SETTINGS = {{'risk_per_trade': {risk}}}")
    
    # Сохранение в файл
    with open('my_config.py', 'w') as f:
        f.write(f"# Моя конфигурация\n")
        f.write(f"SELECTED_STRATEGY = '{selected}'\n")
        f.write(f"INITIAL_BALANCE = {balance}\n")
        f.write(f"RISK_PER_TRADE = {risk}\n")
    
    print(f"\n💾 Конфигурация сохранена в my_config.py")

if __name__ == "__main__":
    interactive_strategy_setup()
```

### Интерактивный мониторинг

```python
# monitor.py
import time
import os
from datetime import datetime

def live_monitor():
    """Живой мониторинг бота"""
    print("📊 ЖИВОЙ МОНИТОРИНГ БОТА")
    print("Нажмите Ctrl+C для выхода")
    print("=" * 50)
    
    try:
        while True:
            # Очистка экрана
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"🕐 Время: {datetime.now().strftime('%H:%M:%S')}")
            
            # Статус бота
            try:
                from main import TradingBot
                bot = TradingBot()
                status = bot.get_bot_status()
                
                print(f"🤖 Статус: {'🟢 Работает' if status['is_running'] else '🔴 Остановлен'}")
                print(f"🔄 Циклов: {status['cycle_count']}")
                print(f"🎯 Стратегия: {status['strategy_name']}")
                
                # Последние результаты
                from utils.diary_viewer import DiaryViewer
                viewer = DiaryViewer()
                day_status = viewer.get_current_day_status()
                
                print(f"💰 Баланс: ${day_status.get('current_balance', 0):.2f}")
                print(f"📈 Дневной P&L: ${day_status.get('daily_return', 0):+.2f}")
                print(f"📊 Сделок сегодня: {day_status.get('completed_trades', 0)}")
                print(f"🔄 Открытых позиций: {day_status.get('open_positions', 0)}")
                
            except Exception as e:
                print(f"❌ Ошибка получения статуса: {e}")
            
            print("\n" + "=" * 50)
            time.sleep(10)  # Обновление каждые 10 секунд
            
    except KeyboardInterrupt:
        print("\n👋 Мониторинг остановлен")

if __name__ == "__main__":
    live_monitor()
```

---

## 🎯 Практические сценарии

### Сценарий 1: Первая неделя торговли

```python
# Настройка для первой недели
SELECTED_STRATEGY = 'SmartMoneyStrategy'  # Безопасная стратегия
USE_TESTNET = True                        # Тестовая сеть
INITIAL_BALANCE = 1000.0                  # Виртуальные $1000

RISK_SETTINGS = {
    'risk_per_trade': 0.01,               # Очень низкий риск
    'max_daily_loss': 0.02,               # 2% дневной лимит
    'max_positions': 1,                   # Только 1 позиция
}

# Только ETH для простоты
TRADING_PAIRS = {
    'ETHUSDT': {
        'enabled': True,
        'weight': 1.0,
        'leverage': 2,                    # Низкое плечо
    }
}
```

### Сценарий 2: Переход на реальную торговлю

```python
# После успешного тестирования
USE_TESTNET = False                       # Реальная торговля
INITIAL_BALANCE = 500.0                   # Начинаем с $500

RISK_SETTINGS = {
    'risk_per_trade': 0.015,              # 1.5% риск
    'max_daily_loss': 0.04,               # 4% дневной лимит
    'max_positions': 2,                   # 2 позиции
}

# Добавляем вторую пару
TRADING_PAIRS = {
    'ETHUSDT': {'enabled': True, 'weight': 0.7},
    'SOLUSDT': {'enabled': True, 'weight': 0.3},
}
```

### Сценарий 3: Масштабирование

```python
# После 3 месяцев успешной торговли
INITIAL_BALANCE = 2000.0                  # Увеличиваем капитал

RISK_SETTINGS = {
    'risk_per_trade': 0.02,               # 2% риск
    'max_daily_loss': 0.06,               # 6% дневной лимит
    'max_positions': 3,                   # 3 позиции
}

# Диверсификация
TRADING_PAIRS = {
    'ETHUSDT': {'enabled': True, 'weight': 0.4},
    'BTCUSDT': {'enabled': True, 'weight': 0.3},
    'SOLUSDT': {'enabled': True, 'weight': 0.3},
}

# Переход на более активную стратегию
SELECTED_STRATEGY = 'MultiIndicatorStrategy'
```

---

**🎯 Используйте эти примеры как отправную точку и адаптируйте под свой стиль торговли!**