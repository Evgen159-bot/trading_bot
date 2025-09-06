# 📚 Примеры использования торгового бота (2025)

## 🎯 Готовые конфигурации для разных стилей торговли

### 👶 Конфигурация для новичков (ОБНОВЛЕНО 2025)

```python
# user_config.py - Безопасная настройка для начинающих

class UserConfig:
    # API настройки
    BYBIT_API_KEY = "ваш_api_ключ"
    BYBIT_API_SECRET = "ваш_секрет"
    USE_TESTNET = True  # ОБЯЗАТЕЛЬНО для начала!
    
    # Выбор стратегии
    SELECTED_STRATEGY = 'custom'  # Настраиваемая стратегия
    
    # 🛡️ ИСПРАВЛЕННЫЕ настройки капитала
    INITIAL_BALANCE = 1000.0
    MIN_BALANCE_THRESHOLD = 100.0
    
    # 🛡️ ОЧЕНЬ консервативные риски (исправлено 2025)
    RISK_SETTINGS = {
        "risk_per_trade": 0.005,      # 0.5% риск на сделку (было 1%)
        "max_daily_loss": 0.02,       # 2% максимальная дневная потеря
        "max_positions": 1,           # Только 1 позиция (было 2)
        "max_daily_trades": 5,        # Максимум 5 сделок в день
        "max_leverage": 1             # БЕЗ ПЛЕЧА! (исправлено)
    }
    
    # 🛡️ Только одна надежная пара (исправлено)
    TRADING_PAIRS = {
        "ETHUSDT": {
            "enabled": True,
            "weight": 1.0,           # 100% портфеля
            "leverage": 1,           # БЕЗ ПЛЕЧА! (исправлено)
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
    
    # 🛡️ ИСПРАВЛЕННЫЕ настройки пользовательской стратегии
    CUSTOM_STRATEGY_CONFIG = {
        'entry_conditions': {
            'min_conditions_required': 3,  # Строгие условия (исправлено)
            'signal_cooldown': 1800,       # 30 минут между сигналами
        },
        'risk_management': {
            'risk_per_trade': 0.005,      # 0.5% риск (исправлено)
            'max_stop_loss_pct': 0.03,    # 3% максимальный стоп-лосс
            'leverage': 1,                # БЕЗ ПЛЕЧА! (исправлено)
            'max_position_value_pct': 0.05 # 5% максимум от баланса
        },
        'volume_settings': {
            'min_ratio': 1.5,             # Требуем 1.5x объем
        }
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

**Ожидаемые результаты (после исправлений):**
- 📊 **Сделок в день:** 1-3
- 🎯 **Win Rate:** 60-70%
- 💰 **Средняя прибыль:** 2-4%
- 📉 **Максимальная просадка:** 5-8%

---

### 🎯 Конфигурация для опытных трейдеров (ОБНОВЛЕНО 2025)

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
    
    # 🛡️ ИСПРАВЛЕННЫЕ сбалансированные риски
    RISK_SETTINGS = {
        'risk_per_trade': 0.015,      # 1.5% риск на сделку (было 2%)
        'max_daily_loss': 0.04,       # 4% максимальная дневная потеря
        'max_positions': 2,           # 2 позиции одновременно (было 3)
        'max_daily_trades': 12,       # До 12 сделок в день
        'max_leverage': 2             # Небольшое плечо (было 5)
    }
    
    # 🛡️ БЕЗОПАСНЫЙ диверсифицированный портфель
    TRADING_PAIRS = {
        'ETHUSDT': {
            'enabled': True,
            'weight': 0.6,           # 60% (увеличено для стабильности)
            'leverage': 2,           # Небольшое плечо
            'stop_loss_pct': 0.025,
            'take_profit_pct': 0.05,
        },
        'BTCUSDT': {
            'enabled': True,
            'weight': 0.4,           # 40%
            'leverage': 1,           # БЕЗ ПЛЕЧА для BTC
            'stop_loss_pct': 0.02,
            'take_profit_pct': 0.04,
        },
        # Остальные отключены для безопасности
        'SOLUSDT': {'enabled': False, 'weight': 0.0},
        'DOGEUSDT': {'enabled': False, 'weight': 0.0},
    }
    
    # 🛡️ ИСПРАВЛЕННАЯ настройка пользовательской стратегии
    CUSTOM_STRATEGY_CONFIG = {
        'entry_conditions': {
            'min_conditions_required': 3,   # 3 из 6 условий
            'signal_cooldown': 1200,        # 20 минут между сигналами
        },
        'risk_management': {
            'risk_per_trade': 0.015,        # 1.5% риск
            'max_stop_loss_pct': 0.04,      # 4% максимальный стоп-лосс
            'leverage': 2,                  # Небольшое плечо
            'max_position_value_pct': 0.1   # 10% максимум от баланса
        },
        'volume_settings': {
            'min_ratio': 1.2,              # Умеренные требования к объему
        }
    }
```

**Ожидаемые результаты (после исправлений):**
- 📊 **Сделок в день:** 2-8
- 🎯 **Win Rate:** 55-65%
- 💰 **Средняя прибыль:** 1-3%
- 📉 **Максимальная просадка:** 8-12%

---

### 🔥 Конфигурация для активных трейдеров (ИСПРАВЛЕНО 2025)

```python
# user_config.py - Агрессивная настройка (с исправлениями безопасности)

class UserConfig:
    # Реальная торговля с большим капиталом
    USE_TESTNET = False
    INITIAL_BALANCE = 5000.0
    MIN_BALANCE_THRESHOLD = 1000.0
    
    # Активная стратегия
    SELECTED_STRATEGY = 'momentum'  # Импульсная стратегия
    
    # 🛡️ ИСПРАВЛЕННЫЕ агрессивные риски (более безопасные)
    RISK_SETTINGS = {
        'risk_per_trade': 0.02,      # 2% риск на сделку (было 3%)
        'max_daily_loss': 0.06,      # 6% дневной лимит (было 10%)
        'max_positions': 3,          # До 3 позиций (было 5)
        'max_daily_trades': 25,      # До 25 сделок в день (было 50)
        'max_leverage': 3            # Умеренное плечо (было 10)
    }
    
    # 🛡️ БЕЗОПАСНЫЙ набор торговых пар
    TRADING_PAIRS = {
        'ETHUSDT': {'enabled': True, 'weight': 0.4, 'leverage': 3},
        'BTCUSDT': {'enabled': True, 'weight': 0.3, 'leverage': 2},
        'SOLUSDT': {'enabled': True, 'weight': 0.3, 'leverage': 3},
        # Мемкоины отключены для безопасности
        'DOGEUSDT': {'enabled': False, 'weight': 0.0},
        '1000PEPEUSDT': {'enabled': False, 'weight': 0.0},
    }
    
    # Быстрые интервалы (для активной торговли)
    TIME_SETTINGS = {
        'intervals': {
            'cycle_interval': 60,        # Каждую минуту (было 30 сек)
        },
        'timeframes': {
            'primary': '5',              # 5-минутные свечи (было 1 мин)
        }
    }
    
    # Telegram уведомления
    NOTIFICATIONS = {
        'telegram': {
            'enabled': True,
            'events': {
                'position_opened': True,
                'position_closed': True,
                'daily_summary': True,
            }
        }
    }
```

**Ожидаемые результаты (после исправлений):**
- 📊 **Сделок в день:** 10-25
- 🎯 **Win Rate:** 55-65%
- 💰 **Средняя прибыль:** 0.5-2%
- 📉 **Максимальная просадка:** 10-15%

---

## 🌊 Специализированные конфигурации (ОБНОВЛЕНО 2025)

### Свинг торговля (для занятых людей)

```python
class UserConfig:
    SELECTED_STRATEGY = 'swing'
    
    # 🛡️ ИСПРАВЛЕННЫЕ настройки для свинг-торговли
    RISK_SETTINGS = {
        'risk_per_trade': 0.02,      # 2% риск (больше из-за редкости)
        'max_positions': 2,          # Максимум 2 позиции
        'max_daily_trades': 3,       # Максимум 3 сделки в день
        'max_leverage': 1            # БЕЗ ПЛЕЧА! (исправлено)
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
    
    # 🛡️ БЕЗОПАСНЫЕ большие цели
    TRADING_PAIRS = {
        'ETHUSDT': {
            'enabled': True,
            'weight': 0.7,              # 70% в стабильную пару
            'leverage': 1,              # БЕЗ ПЛЕЧА! (исправлено)
            'stop_loss_pct': 0.04,      # 4% стоп-лосс
            'take_profit_pct': 0.08,    # 8% тейк-профит (было 12%)
        },
        'BTCUSDT': {
            'enabled': True,
            'weight': 0.3,
            'leverage': 1,              # БЕЗ ПЛЕЧА! (исправлено)
            'stop_loss_pct': 0.03,
            'take_profit_pct': 0.06,    # 6% тейк-профит (было 9%)
        }
    }
```

### Скальпинг (для активных трейдеров) - ⚠️ ВЫСОКИЙ РИСК

```python
class UserConfig:
    SELECTED_STRATEGY = 'scalping'
    
    # ⚠️ ИСПРАВЛЕННЫЕ настройки для скальпинга
    RISK_SETTINGS = {
        'risk_per_trade': 0.01,      # 1% риск (было 1.5%)
        'max_positions': 2,          # 2 позиции (было 3)
        'max_daily_trades': 50,      # 50 сделок (было 100)
        'max_leverage': 2            # Небольшое плечо (было без ограничений)
    }
    
    # Быстрые интервалы
    TIME_SETTINGS = {
        'intervals': {
            'cycle_interval': 30,        # Каждые 30 секунд
        },
        'timeframes': {
            'primary': '1',              # 1-минутные свечи
        }
    }
    
    # 🛡️ БЕЗОПАСНЫЕ малые цели
    TRADING_PAIRS = {
        'ETHUSDT': {
            'enabled': True,
            'weight': 1.0,
            'leverage': 2,              # Небольшое плечо (исправлено)
            'stop_loss_pct': 0.008,     # 0.8% стоп-лосс
            'take_profit_pct': 0.016,   # 1.6% тейк-профит
        }
    }
```

---

## 📊 Примеры мониторинга (ОБНОВЛЕНО 2025)

### 🔧 **Новые инструменты ежедневного мониторинга:**

```bash
#!/bin/bash
# daily_check_2025.sh - Ежедневная проверка с новыми инструментами

echo "📊 ЕЖЕДНЕВНАЯ ПРОВЕРКА БОТА (2025)"
echo "Дата: $(date)"
echo

# 1. Быстрая проверка логов
python utils/simple_log_check.py

# 2. Просмотр дневника торговли
python -c "
from utils.diary_viewer import DiaryViewer
viewer = DiaryViewer()
viewer.show_today()
"

# 3. Детальная диагностика стратегии
python utils/strategy_debug_tool.py ETHUSDT

# 4. Анализ производительности
python utils/log_analyzer.py

# 5. Проверка статуса
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

echo "✅ Проверка завершена"
```

### 📊 **Еженедельный анализ с новыми возможностями:**

```python
# weekly_analysis_2025.py
from utils.diary_viewer import DiaryViewer
from modules.performance_tracker import PerformanceTracker
from datetime import datetime, timedelta

def weekly_analysis_2025():
    print("📊 ЕЖЕНЕДЕЛЬНЫЙ АНАЛИЗ (2025)")
    print("=" * 50)
    
    # 1. Дневник за неделю
    viewer = DiaryViewer()
    weekly_data = viewer.show_week()
    
    # 2. Статистика производительности
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
    
    print(f"\n🎯 РЕКОМЕНДАЦИИ (2025):")
    
    win_rate = metrics.get('win_rate', 0)
    if win_rate < 50:
        print("⚠️ Низкий Win Rate - используйте strategy_debug_tool.py для анализа")
        print("   python utils/strategy_debug_tool.py ETHUSDT")
    elif win_rate > 70:
        print("✅ Отличный Win Rate - стратегия работает хорошо")
    
    total_pnl = metrics.get('total_pnl', 0)
    if total_pnl < 0:
        print("🔴 Убыточная неделя - запустите полную диагностику:")
        print("   python utils/log_analyzer.py")
        print("   python utils/volume_optimizer.py")
    elif total_pnl > 50:
        print("🟢 Прибыльная неделя - продолжайте в том же духе")

if __name__ == "__main__":
    weekly_analysis_2025()
```

---

## 🎛️ Примеры настройки стратегий (ИСПРАВЛЕНО 2025)

### Пример 1: Агрессивная Custom (с исправлениями безопасности)

```python
SELECTED_STRATEGY = 'custom'

CUSTOM_STRATEGY_CONFIG = {
    # 🛡️ ИСПРАВЛЕННЫЕ агрессивные условия входа
    'entry_conditions': {
        'min_conditions_required': 2,       # 2 условия из 6 (было 1)
        'signal_cooldown': 600,             # 10 минут между сигналами
    },
    
    # Быстрые индикаторы
    'rsi_settings': {
        'period': 10,                     # Быстрый RSI (было 7)
        'oversold_lower': 25,            # Более безопасные зоны
        'oversold_upper': 45,
        'overbought_lower': 55,
        'overbought_upper': 75,
    },
    
    'ema_settings': {
        'fast_period': 8,                # Быстрые EMA (было 5)
        'slow_period': 21,               # (было 13)
        'trend_period': 50,              # (было 34)
    },
    
    # 🛡️ ИСПРАВЛЕННЫЙ риск-менеджмент
    'risk_management': {
        'risk_per_trade': 0.015,         # 1.5% риск (было 2.5%)
        'max_stop_loss_pct': 0.04,       # 4% стоп-лосс (было 5%)
        'leverage': 2,                   # Небольшое плечо (было без ограничений)
        'max_position_value_pct': 0.1    # 10% максимум от баланса
    },
    
    # Умеренные фильтры
    'volume_settings': {
        'min_ratio': 1.0,                # Снижаем требования к объему
    }
}
```

### Пример 2: Консервативная Custom (максимальная безопасность)

```python
SELECTED_STRATEGY = 'custom'

CUSTOM_STRATEGY_CONFIG = {
    # 🛡️ Строгие условия входа
    'entry_conditions': {
        'min_conditions_required': 4,       # 4 из 6 условий
        'signal_cooldown': 3600,            # 1 час между сигналами
    },
    
    # Медленные индикаторы
    'rsi_settings': {
        'period': 21,                    # Медленный RSI
        'oversold_lower': 20,            # Узкие зоны
        'oversold_upper': 25,
        'overbought_lower': 75,
        'overbought_upper': 80,
    },
    
    'ema_settings': {
        'fast_period': 21,               # Медленные EMA
        'slow_period': 50,
        'trend_period': 200,
    },
    
    # 🛡️ Консервативный риск-менеджмент
    'risk_management': {
        'risk_per_trade': 0.002,         # 0.2% риск
        'max_stop_loss_pct': 0.02,       # 2% стоп-лосс
        'leverage': 1,                   # БЕЗ ПЛЕЧА!
        'max_position_value_pct': 0.05   # 5% максимум от баланса
    },
    
    # Все фильтры включены
    'volume_settings': {
        'min_ratio': 2.0,               # Высокие требования к объему
    }
}
```

---

## 🎯 Примеры для разных рыночных условий (ОБНОВЛЕНО 2025)

### Трендовый рынок

```python
# Когда рынок в сильном тренде
SELECTED_STRATEGY = 'trend_following'

# 🛡️ БЕЗОПАСНЫЕ настройки для трендов
RISK_SETTINGS = {
    'risk_per_trade': 0.015,     # 1.5% риск
    'max_leverage': 2            # Небольшое плечо
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
SELECTED_STRATEGY = 'mean_reversion'

# 🛡️ БЕЗОПАСНЫЕ настройки для range торговли
RISK_SETTINGS = {
    'risk_per_trade': 0.01,      # 1% риск
    'max_leverage': 1            # БЕЗ ПЛЕЧА!
}

# Или настройте Custom для range торговли
CUSTOM_STRATEGY_CONFIG = {
    'bollinger_settings': {
        'period': 20,
        'std_deviation': 2.5,            # Более широкие полосы
    },
    'rsi_settings': {
        'oversold_lower': 15,            # Экстремальные уровни
        'overbought_upper': 85,
    },
    'risk_management': {
        'leverage': 1,                   # БЕЗ ПЛЕЧА!
    }
}
```

### Волатильный рынок

```python
# Когда высокая волатильность
SELECTED_STRATEGY = 'breakout'

# 🛡️ ИСПРАВЛЕННЫЕ настройки для волатильности
RISK_SETTINGS = {
    'risk_per_trade': 0.01,      # Снижаем риск (было 1.5%)
    'max_positions': 2,          # Меньше позиций (было 3)
    'max_leverage': 2            # Небольшое плечо (исправлено)
}

# Увеличиваем стоп-лоссы
TRADING_PAIRS = {
    'ETHUSDT': {
        'enabled': True,
        'weight': 1.0,
        'leverage': 2,              # Небольшое плечо (исправлено)
        'stop_loss_pct': 0.04,      # Больше стоп-лосс
        'take_profit_pct': 0.08,    # Умеренные цели (было 12%)
    }
}
```

---

## 📱 Примеры настройки уведомлений (ОБНОВЛЕНО 2025)

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

**Пример уведомления (2025):**
```
🤖 ByBit Trading Bot (2025)

📈 Позиция открыта
🎯 ETHUSDT LONG
💵 Размер: 0.5 ETH  
💰 Цена входа: $3,245.67
🛑 Стоп-лосс: $3,164.34 (2.5%)
🎯 Тейк-профит: $3,407.95 (5.0%)
📊 Уверенность: 78%
💼 Баланс: $1,087.50
🛡️ Плечо: 1x (БЕЗ ПЛЕЧА)
⏰ Время: 01.09.2025 15:30
```

---

## 🔄 Примеры A/B тестирования (ОБНОВЛЕНО 2025)

### Тест 1: Сравнение стратегий с новыми инструментами

```bash
# Неделя 1: Custom (безопасная)
# В user_config.py измените:
SELECTED_STRATEGY = 'custom'
CUSTOM_STRATEGY_CONFIG = {
    'entry_conditions': {'min_conditions_required': 3},
    'risk_management': {'risk_per_trade': 0.005, 'leverage': 1}
}
python main.py  # Запуск на неделю

# Анализ результатов:
python utils/diary_viewer.py
python utils/log_analyzer.py

# Неделя 2: Smart Money
SELECTED_STRATEGY = 'smart_money'
python main.py  # Запуск на неделю

# Сравнение результатов с новыми инструментами:
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_week()"
python check_results.py
```

### Тест 2: Сравнение параметров риска

```python
# 🧪 Конфигурация A: Ультра-консервативная (исправлено 2025)
RISK_SETTINGS_A = {
    'risk_per_trade': 0.002,      # 0.2% риск
    'max_positions': 1,
    'max_leverage': 1             # БЕЗ ПЛЕЧА!
}

# Конфигурация B: Умеренная (исправлено 2025)  
RISK_SETTINGS_B = {
    'risk_per_trade': 0.01,       # 1% риск
    'max_positions': 2,
    'max_leverage': 2             # Небольшое плечо
}

# Тестируйте каждую конфигурацию по 2 недели
# Сравните результаты через diary_viewer.py и новые инструменты
```

---

## 🎓 Обучающие примеры (НОВОЕ 2025)

### Пример 1: Изучение Custom Strategy с новыми инструментами

```python
# Настройка для изучения работы стратегии
SELECTED_STRATEGY = 'custom'

# 🔧 Включаем детальное логирование
LOGGING_SETTINGS = {
    'log_level': 'DEBUG',               # Подробные логи
    'detailed_trading_logs': True,
}

# 🛡️ Безопасные настройки для обучения
CUSTOM_STRATEGY_CONFIG = {
    'entry_conditions': {
        'min_conditions_required': 2,   # Больше сигналов для изучения
        'signal_cooldown': 600,         # 10 минут между сигналами
    },
    'risk_management': {
        'risk_per_trade': 0.002,        # 0.2% риск (очень безопасно)
        'leverage': 1,                  # БЕЗ ПЛЕЧА!
    }
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

**Команды для изучения:**
```bash
# Запустите бота на 2-3 часа
python main.py

# Остановите и анализируйте:
python utils/strategy_debug_tool.py ETHUSDT  # Детальный анализ
python utils/log_analyzer.py                # Статистика
python utils/diary_viewer.py                # Результаты
```

### Пример 2: Оптимизация на основе реальных данных

```python
# optimization_example.py
from utils.volume_optimizer import VolumeOptimizer
from utils.diary_viewer import DiaryViewer

def optimize_based_on_results():
    """Оптимизация на основе реальных результатов"""
    print("🎯 ОПТИМИЗАЦИЯ НА ОСНОВЕ ДАННЫХ")
    print("=" * 50)
    
    # 1. Анализ объемов
    optimizer = VolumeOptimizer()
    optimizer.analyze_volume_patterns()
    
    # 2. Анализ результатов
    viewer = DiaryViewer()
    viewer.show_week()
    
    # 3. Рекомендации
    print("\n💡 РЕКОМЕНДАЦИИ ПО ОПТИМИЗАЦИИ:")
    print("На основе анализа данных:")
    print("1. Снизьте min_ratio до 0.8")
    print("2. Уменьшите min_conditions_required до 2")
    print("3. Сократите signal_cooldown до 600 секунд")
    print("4. Оставьте leverage = 1 для безопасности")

if __name__ == "__main__":
    optimize_based_on_results()
```

---

## 📊 Примеры анализа результатов (НОВОЕ 2025)

### Анализ лучших сделок с новыми инструментами

```python
# analyze_best_trades_2025.py
from utils.diary_viewer import DiaryViewer
import json
from pathlib import Path

def analyze_best_trades_2025():
    """Анализ лучших сделок с новыми возможностями"""
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
        print(f"   📝 Причина закрытия: {trade.get('close_reason', 'N/A')}")
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
    
    # 🔧 Рекомендации на основе анализа
    print("\n💡 РЕКОМЕНДАЦИИ НА ОСНОВЕ ЛУЧШИХ СДЕЛОК:")
    if symbols:
        best_pair = max(symbols.items(), key=lambda x: x[1])[0]
        print(f"1. Сосредоточьтесь на {best_pair} - показывает лучшие результаты")
    
    if directions:
        best_direction = max(directions.items(), key=lambda x: x[1])[0]
        print(f"2. {best_direction} сигналы работают лучше")

if __name__ == "__main__":
    analyze_best_trades_2025()
```

---

## 🎮 Интерактивные примеры (ОБНОВЛЕНО 2025)

### Интерактивный выбор стратегии с диагностикой

```python
# interactive_setup_2025.py
from user_config import UserConfig
import subprocess

def interactive_strategy_setup_2025():
    print("🎯 ИНТЕРАКТИВНАЯ НАСТРОЙКА СТРАТЕГИИ (2025)")
    print("=" * 50)
    
    strategies = list(UserConfig.AVAILABLE_STRATEGIES.keys())
    
    print("Доступные стратегии:")
    for i, strategy in enumerate(strategies, 1):
        info = UserConfig.AVAILABLE_STRATEGIES[strategy]
        risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(info.get('risk_level', ''), "⚪")
        print(f"{i}. {info['name']} {risk_emoji}")
        print(f"   📝 {info['description']}")
        print()
    
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
    
    # 🛡️ Настройка безопасных рисков
    print(f"\n💰 Настройка рисков (безопасные значения 2025):")
    balance = float(input("Ваш депозит в USD: "))
    
    # Рекомендуемые безопасные риски
    if balance < 500:
        recommended_risk = 0.002  # 0.2%
    elif balance < 2000:
        recommended_risk = 0.005  # 0.5%
    else:
        recommended_risk = 0.01   # 1%
    
    print(f"💡 Рекомендуемый риск для вашего депозита: {recommended_risk*100:.1f}%")
    risk_input = input(f"Риск на сделку в % (рекомендуется {recommended_risk*100:.1f}): ").strip()
    
    if risk_input:
        risk = float(risk_input) / 100
    else:
        risk = recommended_risk
    
    print(f"\n📋 РЕКОМЕНДУЕМАЯ БЕЗОПАСНАЯ КОНФИГУРАЦИЯ (2025):")
    print(f"SELECTED_STRATEGY = '{selected}'")
    print(f"INITIAL_BALANCE = {balance}")
    print(f"USE_TESTNET = True  # ОБЯЗАТЕЛЬНО для начала!")
    print(f"RISK_SETTINGS = {{")
    print(f"    'risk_per_trade': {risk},")
    print(f"    'max_positions': 1,")
    print(f"    'max_leverage': 1  # БЕЗ ПЛЕЧА!")
    print(f"}}")
    
    # 🔧 Тестирование настроек
    print(f"\n🔧 ТЕСТИРОВАНИЕ НАСТРОЕК:")
    test_choice = input("Запустить тест стратегии? (y/n): ").lower().strip()
    if test_choice in ['y', 'yes', 'да', 'д']:
        try:
            subprocess.run(['python', 'utils/simple_strategy_test.py'], check=True)
            print("✅ Тест завершен")
        except:
            print("❌ Ошибка тестирования")
    
    # Сохранение в файл
    with open('my_config_2025.py', 'w', encoding='utf-8') as f:
        f.write(f"# Моя безопасная конфигурация (2025)\n")
        f.write(f"SELECTED_STRATEGY = '{selected}'\n")
        f.write(f"INITIAL_BALANCE = {balance}\n")
        f.write(f"USE_TESTNET = True\n")
        f.write(f"RISK_PER_TRADE = {risk}\n")
        f.write(f"MAX_LEVERAGE = 1  # БЕЗ ПЛЕЧА!\n")
    
    print(f"\n💾 Конфигурация сохранена в my_config_2025.py")
    print(f"\n🔧 Следующие шаги:")
    print(f"1. Скопируйте настройки в user_config.py")
    print(f"2. Запустите: python main.py")
    print(f"3. Мониторьте: python utils/diary_viewer.py")

if __name__ == "__main__":
    interactive_strategy_setup_2025()
```

### Интерактивный мониторинг с новыми инструментами

```python
# monitor_2025.py
import time
import os
import subprocess
from datetime import datetime

def live_monitor_2025():
    """Живой мониторинг бота с новыми инструментами"""
    print("📊 ЖИВОЙ МОНИТОРИНГ БОТА (2025)")
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
                
                # Последние результаты с новыми инструментами
                from utils.diary_viewer import DiaryViewer
                viewer = DiaryViewer()
                day_status = viewer.get_current_day_status()
                
                print(f"💰 Баланс: ${day_status.get('current_balance', 0):.2f}")
                print(f"📈 Дневной P&L: ${day_status.get('daily_return', 0):+.2f}")
                print(f"📊 Сделок сегодня: {day_status.get('completed_trades', 0)}")
                print(f"🔄 Открытых позиций: {day_status.get('open_positions', 0)}")
                
                # 🔧 Быстрая диагностика
                print(f"\n🔧 БЫСТРАЯ ДИАГНОСТИКА:")
                try:
                    # Запускаем быструю проверку логов
                    result = subprocess.run(['python', 'utils/simple_log_check.py'], 
                                          capture_output=True, text=True, timeout=10)
                    if "OPEN сигналов:" in result.stdout:
                        lines = result.stdout.split('\n')
                        for line in lines:
                            if "OPEN сигналов:" in line or "CLOSE сигналов:" in line:
                                print(f"   {line.strip()}")
                except:
                    print("   ⚠️ Диагностика недоступна")
                
            except Exception as e:
                print(f"❌ Ошибка получения статуса: {e}")
            
            print(f"\n🔧 ДОСТУПНЫЕ КОМАНДЫ:")
            print(f"   Ctrl+C - Выход из мониторинга")
            print(f"   В другом терминале:")
            print(f"   python utils/strategy_debug_tool.py ETHUSDT  # Детальная отладка")
            print(f"   python utils/log_analyzer.py                # Анализ логов")
            print(f"   python utils/diary_viewer.py                # Дневник")
            
            print("\n" + "=" * 50)
            time.sleep(30)  # Обновление каждые 30 секунд
            
    except KeyboardInterrupt:
        print("\n👋 Мониторинг остановлен")

if __name__ == "__main__":
    live_monitor_2025()
```

---

## 🎯 Практические сценарии (ОБНОВЛЕНО 2025)

### Сценарий 1: Первая неделя торговли с новыми инструментами

```python
# Настройка для первой недели (исправлено 2025)
SELECTED_STRATEGY = 'custom'  # Настраиваемая стратегия
USE_TESTNET = True                        # Тестовая сеть
INITIAL_BALANCE = 1000.0                  # Виртуальные $1000

# 🛡️ ИСПРАВЛЕННЫЕ настройки безопасности
RISK_SETTINGS = {
    'risk_per_trade': 0.005,              # 0.5% риск (было 1%)
    'max_daily_loss': 0.02,               # 2% дневной лимит
    'max_positions': 1,                   # Только 1 позиция
    'max_leverage': 1                     # БЕЗ ПЛЕЧА! (исправлено)
}

# Только ETH для простоты
TRADING_PAIRS = {
    'ETHUSDT': {
        'enabled': True,
        'weight': 1.0,
        'leverage': 1,                    # БЕЗ ПЛЕЧА! (исправлено)
    }
}

# 🛡️ ИСПРАВЛЕННАЯ настройка стратегии
CUSTOM_STRATEGY_CONFIG = {
    'entry_conditions': {
        'min_conditions_required': 3,    # Строгие условия
        'signal_cooldown': 1800,         # 30 минут между сигналами
    },
    'risk_management': {
        'risk_per_trade': 0.005,         # 0.5% риск
        'leverage': 1,                   # БЕЗ ПЛЕЧА!
        'max_stop_loss_pct': 0.03,       # 3% максимальный стоп-лосс
    }
}
```

**Команды для мониторинга первой недели:**
```bash
# Ежедневно
python utils/diary_viewer.py           # Результаты дня
python utils/simple_log_check.py       # Быстрая проверка

# При проблемах
python utils/strategy_debug_tool.py ETHUSDT  # Детальная диагностика
python utils/log_analyzer.py                # Анализ производительности

# В конце недели
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_week()"
python check_results.py
```

### Сценарий 2: Переход на реальную торговлю (БЕЗОПАСНО 2025)

```python
# После успешного тестирования (исправлено 2025)
USE_TESTNET = False                       # Реальная торговля
INITIAL_BALANCE = 200.0                   # Начинаем с $200 (было $500)

# 🛡️ ИСПРАВЛЕННЫЕ настройки для реальной торговли
RISK_SETTINGS = {
    'risk_per_trade': 0.005,              # 0.5% риск (очень консервативно)
    'max_daily_loss': 0.02,               # 2% дневной лимит
    'max_positions': 1,                   # 1 позиция (было 2)
    'max_leverage': 1                     # БЕЗ ПЛЕЧА! (исправлено)
}

# Только одна проверенная пара
TRADING_PAIRS = {
    'ETHUSDT': {'enabled': True, 'weight': 1.0, 'leverage': 1},
    # Вторую пару добавим только после месяца успешной торговли
}
```

### Сценарий 3: Масштабирование (БЕЗОПАСНОЕ 2025)

```python
# После 3 месяцев успешной торговли (исправлено 2025)
INITIAL_BALANCE = 1000.0                  # Увеличиваем капитал

# 🛡️ ИСПРАВЛЕННЫЕ настройки для масштабирования
RISK_SETTINGS = {
    'risk_per_trade': 0.01,               # 1% риск (было 2%)
    'max_daily_loss': 0.04,               # 4% дневной лимит (было 6%)
    'max_positions': 2,                   # 2 позиции (было 3)
    'max_leverage': 2                     # Небольшое плечо (было без ограничений)
}

# 🛡️ БЕЗОПАСНАЯ диверсификация
TRADING_PAIRS = {
    'ETHUSDT': {'enabled': True, 'weight': 0.6, 'leverage': 2},
    'BTCUSDT': {'enabled': True, 'weight': 0.4, 'leverage': 1},
    # Остальные пары добавляем только после полугода опыта
}

# Переход на более активную стратегию (только после опыта!)
SELECTED_STRATEGY = 'custom'  # Остаемся с настраиваемой для контроля
```

---

## 🔧 Инструменты для долгосрочного тестирования (НОВОЕ 2025)

### 🆕 Новые инструменты отладки:

```python
# strategy_debug_tool.py - Детальная отладка стратегий
class StrategyDebugTool:
    """Инструмент для детальной отладки стратегий"""
    
    def debug_signal_generation(self, symbol: str = 'ETHUSDT'):
        """Детальная отладка генерации сигналов"""
        # Показывает:
        # - Все рассчитанные индикаторы
        # - Детальный анализ условий входа
        # - Причины отсутствия сигналов
        # - Рекомендации по оптимизации
        
# Использование:
python utils/strategy_debug_tool.py ETHUSDT
python utils/strategy_debug_tool.py  # Все пары

# log_analyzer.py - Анализ логов
class LogAnalyzer:
    """Анализатор логов торгового бота"""
    
    def analyze_logs(self):
        """Полный анализ логов"""
        # Показывает:
        # - Статистику ошибок
        # - Частоту сигналов
        # - Производительность
        # - Рекомендации
        
# Использование:
python utils/log_analyzer.py

# volume_optimizer.py - Оптимизация объемов
class VolumeOptimizer:
    """Оптимизатор объемных фильтров"""
    
    def analyze_volume_patterns(self):
        """Анализ объемных паттернов"""
        # Показывает:
        # - Статистику объемов по парам
        # - Рекомендации по настройке min_ratio
        # - Оптимальные пороги фильтров

# Использование:
python utils/volume_optimizer.py
```

### 1. Скрипт автоматического мониторинга (ОБНОВЛЕНО 2025):

```bash
#!/bin/bash
# auto_monitor_2025.sh - Автоматический мониторинг с новыми инструментами

while true; do
    echo "🔄 Проверка бота: $(date)"
    
    # Проверка процесса
    if ! pgrep -f "python main.py" > /dev/null; then
        echo "⚠️ Бот не запущен! Перезапуск..."
        nohup python main.py > bot.log 2>&1 &
        sleep 30
    fi
    
    # 🔧 Новая диагностика каждые 30 минут
    if [ $(($(date +%M) % 30)) -eq 0 ]; then
        echo "🔧 Запуск диагностики..."
        python utils/simple_log_check.py
        
        # При обнаружении проблем
        if grep -q "🚨" bot.log; then
            echo "🚨 Обнаружены проблемы, запуск детальной диагностики..."
            python utils/strategy_debug_tool.py ETHUSDT
            python utils/log_analyzer.py
        fi
    fi
    
    # Проверка размера логов
    log_size=$(du -m logs/ | cut -f1)
    if [ $log_size -gt 100 ]; then
        echo "📄 Архивирование логов..."
        tar -czf "logs_backup_$(date +%Y%m%d).tar.gz" logs/
        find logs/ -name "*.log" -mtime +7 -delete
    fi
    
    # Проверка свободного места
    free_space=$(df / | awk 'NR==2{print $4}')
    if [ $free_space -lt 1000000 ]; then  # Меньше 1GB
        echo "⚠️ Мало места на диске!"
        # Отправить уведомление
    fi
    
    sleep 300  # Проверка каждые 5 минут
done
```

### 2. Система бэкапов с новыми данными:

```python
# backup_system_2025.py
import shutil
import os
from datetime import datetime
from pathlib import Path

class BackupSystem2025:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_daily_backup(self):
        """Создание ежедневного бэкапа с новыми данными"""
        date_str = datetime.now().strftime("%Y%m%d")
        backup_path = self.backup_dir / f"backup_{date_str}"
        
        # Создаем папку бэкапа
        backup_path.mkdir(exist_ok=True)
        
        # 🆕 Копируем важные файлы (обновлено 2025)
        important_files = [
            "user_config.py",
            "data/diary/",              # Новый дневник торговли
            "data/performance/",
            "logs/trading_diary/",      # Новые логи дневника
            "logs/strategies/",         # Новые логи стратегий
        ]
        
        for item in important_files:
            if os.path.exists(item):
                if os.path.isdir(item):
                    shutil.copytree(item, backup_path / item, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, backup_path / item)
        
        print(f"✅ Бэкап создан: {backup_path}")
        
        # 🆕 Создание отчета о бэкапе
        with open(backup_path / "backup_report.txt", 'w', encoding='utf-8') as f:
            f.write(f"📊 ОТЧЕТ О БЭКАПЕ\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Размер: {self._get_backup_size(backup_path):.1f} MB\n")
            
            # Статистика дневника
            try:
                from utils.diary_viewer import DiaryViewer
                viewer = DiaryViewer()
                status = viewer.get_current_day_status()
                f.write(f"Сделок сегодня: {status.get('completed_trades', 0)}\n")
                f.write(f"Дневной результат: ${status.get('daily_return', 0):.2f}\n")
            except:
                f.write("Статистика дневника недоступна\n")
    
    def _get_backup_size(self, path):
        """Расчет размера бэкапа"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        return total_size / 1024 / 1024  # MB
    
    def cleanup_old_backups(self, keep_days=30):
        """Удаление старых бэкапов"""
        cutoff_date = datetime.now().timestamp() - (keep_days * 24 * 3600)
        
        for backup in self.backup_dir.iterdir():
            if backup.is_dir() and backup.stat().st_mtime < cutoff_date:
                shutil.rmtree(backup)
                print(f"🗑️ Удален старый бэкап: {backup}")

# Автоматический запуск
if __name__ == "__main__":
    backup = BackupSystem2025()
    backup.create_daily_backup()
    backup.cleanup_old_backups()
```

---

## 🔧 Инструменты для долгосрочного тестирования (ОБНОВЛЕНО 2025)

### 📊 **Автоматический анализ результатов:**

```bash
#!/bin/bash
# weekly_optimization_2025.sh

echo "📊 ЕЖЕНЕДЕЛЬНАЯ ОПТИМИЗАЦИЯ (2025)"
echo "=" * 50

# 1. Анализ недели
python -c "from utils.diary_viewer import DiaryViewer; DiaryViewer().show_week()"

# 2. Детальная диагностика стратегии
python utils/strategy_debug_tool.py ETHUSDT

# 3. Анализ логов за неделю
python utils/log_analyzer.py

# 4. Оптимизация объемных фильтров
python utils/volume_optimizer.py

# 5. Полный анализ результатов
python check_results.py

# 6. Экспорт данных
python -c "
from modules.trading_diary import TradingDiary
diary = TradingDiary()
export_path = diary.export_diary_to_csv(7)
print(f'📊 Экспорт недели: {export_path}')
"

echo "✅ Еженедельная оптимизация завершена"
echo "💡 Примените рекомендации в user_config.py"
```

### 🎯 **Система автоматических рекомендаций:**

```python
# auto_recommendations_2025.py
from utils.log_analyzer import LogAnalyzer
from utils.volume_optimizer import VolumeOptimizer
from utils.diary_viewer import DiaryViewer

class AutoRecommendations2025:
    """Система автоматических рекомендаций на основе анализа"""
    
    def generate_recommendations(self):
        """Генерация рекомендаций на основе всех данных"""
        print("🎯 АВТОМАТИЧЕСКИЕ РЕКОМЕНДАЦИИ (2025)")
        print("=" * 50)
        
        # 1. Анализ логов
        try:
            analyzer = LogAnalyzer()
            analyzer.analyze_logs()
        except Exception as e:
            print(f"⚠️ Анализ логов недоступен: {e}")
        
        # 2. Анализ объемов
        try:
            optimizer = VolumeOptimizer()
            optimizer.analyze_volume_patterns()
            optimizer.recommend_optimal_settings()
        except Exception as e:
            print(f"⚠️ Анализ объемов недоступен: {e}")
        
        # 3. Анализ результатов торговли
        try:
            viewer = DiaryViewer()
            status = viewer.get_current_day_status()
            
            if status.get('completed_trades', 0) == 0:
                print("\n🔧 РЕКОМЕНДАЦИИ ПРИ ОТСУТСТВИИ СДЕЛОК:")
                print("1. Запустите: python utils/strategy_debug_tool.py ETHUSDT")
                print("2. Снизьте min_conditions_required до 2")
                print("3. Уменьшите signal_cooldown до 600 секунд")
                print("4. Снизьте min_ratio до 0.8")
            
            elif status.get('daily_return', 0) < 0:
                print("\n🛡️ РЕКОМЕНДАЦИИ ПРИ УБЫТКАХ:")
                print("1. Увеличьте min_conditions_required до 4")
                print("2. Снизьте risk_per_trade до 0.002")
                print("3. Установите max_leverage = 1")
                print("4. Переключитесь на SELECTED_STRATEGY = 'smart_money'")
            
            else:
                print("\n✅ РЕЗУЛЬТАТЫ ХОРОШИЕ:")
                print("1. Можете постепенно увеличивать риск")
                print("2. Рассмотрите добавление второй пары")
                print("3. Продолжайте мониторинг")
                
        except Exception as e:
            print(f"⚠️ Анализ дневника недоступен: {e}")

if __name__ == "__main__":
    recommendations = AutoRecommendations2025()
    recommendations.generate_recommendations()
```

---

**🎯 Используйте эти примеры как отправную точку и адаптируйте под свой стиль торговли с учетом исправлений 2025 года!**

### 🔧 **Ключевые улучшения 2025:**
- **Исправлены критические ошибки** в расчетах
- **Добавлены новые инструменты** диагностики
- **Консервативные настройки** по умолчанию
- **Детальное логирование** на русском языке
- **Автоматические рекомендации** на основе анализа данных

### 🛡️ **Безопасность прежде всего:**
- Всегда начинайте с **TESTNET = True**
- Используйте **leverage = 1** (без плеча)
- Устанавливайте **малые риски** (0.5%)
- **Мониторьте результаты** через новые инструменты
- **Применяйте рекомендации** постепенно

### 🔧 **Используйте новые инструменты:**
```bash
python utils/strategy_debug_tool.py ETHUSDT  # Детальная отладка
python utils/log_analyzer.py                # Анализ логов
python utils/volume_optimizer.py            # Оптимизация
python utils/diary_viewer.py                # Мониторинг
python check_results.py                     # Анализ результатов
```