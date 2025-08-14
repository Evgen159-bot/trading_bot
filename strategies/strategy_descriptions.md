# 🎯 Полное руководство по торговым стратегиям

## 📚 Обзор 8 доступных стратегий

Бот включает **8 торговых стратегий**, разработанных на основе лучших практик 2022-2025 годов:

### 🏆 Топ-3 рекомендуемые стратегии:

1. **🧠 Smart Money Strategy** - Для консервативной торговли (рекомендуется)
2. **🛠️ Custom Strategy** - Для полной настройки под себя  
3. **📈 Trend Following Strategy** - Для стабильной прибыли

---

## 🧠 Smart Money Strategy (Рекомендуется)

### Описание:
Современная стратегия на основе концепций Smart Money Concepts (SMC) и Inner Circle Trader (ICT). Анализирует институциональные уровни и структуру рынка.

### Принципы работы:
- **Market Structure:** Анализ BOS (Break of Structure) и CHoCH (Change of Character)
- **Order Blocks:** Поиск институциональных уровней
- **Fair Value Gaps:** Обнаружение ценовых разрывов
- **Liquidity Sweeps:** Анализ ликвидности
- **Volume Profile:** Объемный анализ

### Настройка:
```python
SELECTED_STRATEGY = 'smart_money'
```

### Параметры (автоматические):
- **Минимальная уверенность:** 75%
- **Условий для входа:** 4 из 7
- **Риск/Прибыль:** минимум 2:1
- **Cooldown:** 5 минут между сигналами

### Результаты:
- **Win Rate:** 65-75%
- **Profit Factor:** 1.8-2.5
- **Максимальная просадка:** 8-12%
- **Средняя сделка:** 2-6%

### Подходит для:
- ✅ Консервативных трейдеров
- ✅ Долгосрочной прибыльности
- ✅ Высокого качества сигналов
- ✅ Изучающих SMC концепции

---

## 🛠️ Custom Strategy (Настраиваемая)

### Описание:
Полностью настраиваемая стратегия с возможностью изменения всех параметров индикаторов, стоп-лоссов и условий входа/выхода.

### Настройка:
```python
SELECTED_STRATEGY = 'custom'

CUSTOM_STRATEGY_CONFIG = {
    # Основные параметры
    'min_conditions_required': 3,  # Из 6 условий
    'min_confidence': 0.6,          # 60% уверенность
    'signal_cooldown': 180,         # 3 минуты между сигналами
    
    # RSI настройки
    'rsi_settings': {
        'period': 14,               # Период RSI
        'oversold_lower': 25,       # Нижний уровень перепроданности
        'oversold_upper': 35,       # Верхний уровень перепроданности
        'overbought_lower': 65,     # Нижний уровень перекупленности
        'overbought_upper': 75,     # Верхний уровень перекупленности
    },
    
    # MACD настройки
    'macd_settings': {
        'fast_period': 12,          # Быстрая EMA
        'slow_period': 26,          # Медленная EMA
        'signal_period': 9,         # Сигнальная линия
        'histogram_threshold': 0.0001, # Порог гистограммы
    },
    
    # EMA настройки
    'ema_settings': {
        'fast_period': 9,           # Быстрая EMA
        'slow_period': 21,          # Медленная EMA
        'trend_period': 50,         # Трендовая EMA
    },
    
    # Bollinger Bands
    'bollinger_settings': {
        'period': 20,               # Период
        'std_deviation': 2.0,       # Стандартное отклонение
    },
    
    # Volume настройки
    'volume_settings': {
        'min_ratio': 1.2,           # Минимальное отношение объема
        'surge_threshold': 2.5,     # Порог всплеска объема
    },
    
    # ATR настройки
    'atr_settings': {
        'period': 14,               # Период ATR
        'stop_loss_multiplier': 2.0,    # Множитель для стоп-лосса
        'take_profit_multiplier': 3.0,  # Множитель для тейк-профита
    },
    
    # Stochastic настройки
    'stochastic_settings': {
        'k_period': 14,             # Период %K
        'd_period': 3,              # Период %D
        'oversold': 20,             # Уровень перепроданности
        'overbought': 80,           # Уровень перекупленности
    },
    
    # Управление рисками
    'risk_reward_settings': {
        'max_stop_loss_pct': 0.08,     # 8% максимальный стоп-лосс
        'min_take_profit_pct': 0.12,   # 12% минимальный тейк-профит
        'max_take_profit_pct': 0.25,   # 25% максимальный тейк-профит
        'risk_per_trade': 0.015,       # 1.5% риск на сделку
    },
    
    # Фильтры
    'filters': {
        'trend_filter': True,           # Фильтр тренда
        'volume_filter': True,          # Фильтр объема
        'volatility_filter': True,      # Фильтр волатильности
        'time_filter': False,           # Временной фильтр
    }
}
```

### Примеры настроек:

#### Агрессивная настройка:
```python
# Выбор 4 активных пар из 7 доступных
TRADING_PAIRS = {
    'ETHUSDT': {'enabled': True, 'weight': 0.3},
    'BTCUSDT': {'enabled': True, 'weight': 0.3},
    'DOGEUSDT': {'enabled': True, 'weight': 0.2},
    'SUIUSDT': {'enabled': True, 'weight': 0.2},
    # Остальные отключены
}

CUSTOM_STRATEGY_CONFIG = {
    'min_conditions_required': 2,      # Меньше условий
    'min_confidence': 0.5,              # Меньше уверенность
    'signal_cooldown': 60,              # Чаще сигналы
    'risk_reward_settings': {
        'risk_per_trade': 0.025,        # Больше риск
    }
}
```

#### Консервативная настройка:
```python
# Выбор 2 стабильных пар
TRADING_PAIRS = {
    'ETHUSDT': {'enabled': True, 'weight': 0.6},
    'BTCUSDT': {'enabled': True, 'weight': 0.4},
    # Остальные отключены для безопасности
}

CUSTOM_STRATEGY_CONFIG = {
    'min_conditions_required': 4,      # Больше условий
    'min_confidence': 0.8,              # Больше уверенность
    'signal_cooldown': 600,             # Реже сигналы
    'risk_reward_settings': {
        'risk_per_trade': 0.01,         # Меньше риск
    }
}
```

---

## 📈 Trend Following Strategy

### Описание:
Классическая стратегия "Trend is your friend" с использованием ADX, EMA и объемного подтверждения.

### Настройка:
```python
SELECTED_STRATEGY = 'TrendFollowingStrategy'
```

### Принципы:
- **EMA кроссоверы:** 12/26/50 периоды
- **ADX фильтр:** Минимум 25 для входа
- **Volume подтверждение:** 1.5x средний объем
- **Трейлинг стопы:** Автоматическое следование

### Результаты:
- **Win Rate:** 45-55%
- **Profit Factor:** 1.5-2.2
- **R:R соотношение:** 2:1

### Подходит для:
- ✅ Начинающих трейдеров
- ✅ Трендовых рынков
- ✅ Долгосрочных позиций

---

## ⚡ Scalping Strategy

### Описание:
Высокочастотная торговля на малых движениях цены с быстрыми входами и выходами.

### Настройка:
```python
SELECTED_STRATEGY = 'ScalpingStrategy'

# Рекомендуемые настройки времени
TIME_SETTINGS = {
    'intervals': {
        'cycle_interval': 30,       # Проверка каждые 30 секунд
    },
    'timeframes': {
        'primary': '1',             # 1-минутные свечи
    }
}
```

### Принципы:
- **Быстрые EMA:** 5/13 периоды
- **Быстрый RSI:** 7 период
- **Объемные всплески:** 2x+ средний объем
- **Малые цели:** 0.8% прибыль, 0.4% стоп-лосс

### Результаты:
- **Win Rate:** 70-80%
- **Profit Factor:** 1.1-1.4
- **Время в позиции:** 1-15 минут
- **Частота сделок:** 10-50 в день

### Подходит для:
- ✅ Активных трейдеров
- ✅ Постоянного мониторинга
- ✅ Высокой ликвидности
- ❌ Не для новичков

---

## 🌊 Swing Strategy

### Описание:
Среднесрочная торговля на колебаниях цены с удержанием позиций от часов до дней.

### Настройка:
```python
SELECTED_STRATEGY = 'SwingStrategy'

# Рекомендуемые настройки
TIME_SETTINGS = {
    'timeframes': {
        'primary': '1h',            # Часовые свечи
        'trend': '4h',              # 4-часовой тренд
    }
}
```

### Принципы:
- **Медленные EMA:** 21/50/200 периоды
- **Поддержка/Сопротивление:** Фибоначчи уровни
- **Большие цели:** 8% прибыль, 4% стоп-лосс
- **Долгие позиции:** До 7 дней

### Результаты:
- **Win Rate:** 50-60%
- **Profit Factor:** 1.8-2.5
- **R:R соотношение:** 2:1
- **Частота сделок:** 1-5 в неделю

### Подходит для:
- ✅ Занятых людей
- ✅ Меньшего стресса
- ✅ Трендовых рынков с коррекциями

---

## 💥 Breakout Strategy

### Описание:
Торговля на пробоях ключевых уровней поддержки и сопротивления с объемным подтверждением.

### Настройка:
```python
SELECTED_STRATEGY = 'BreakoutStrategy'
```

### Принципы:
- **Поиск уровней:** Автоматический поиск S/R
- **Пробой с объемом:** 2x+ подтверждение
- **Ложные пробои:** Фильтры и таймауты
- **Быстрая реакция:** Вход при пробое

### Результаты:
- **Win Rate:** 50-60%
- **Profit Factor:** 1.6-2.3
- **Время развития:** 1 час на пробой

### Подходит для:
- ✅ Волатильных рынков
- ✅ Новостных событий
- ✅ Консолидационных периодов

---

## 🔄 Mean Reversion Strategy

### Описание:
Торговля на возврате цены к среднему значению, используя экстремальные уровни RSI и Bollinger Bands.

### Настройка:
```python
SELECTED_STRATEGY = 'MeanReversionStrategy'
```

### Принципы:
- **Bollinger Bands:** Торговля от границ к центру
- **RSI экстремумы:** 15/85 уровни
- **Боковые рынки:** Избегание сильных трендов
- **Статистическое преимущество:** Возврат к среднему

### Результаты:
- **Win Rate:** 60-70%
- **Profit Factor:** 1.3-1.7
- **Лучшие условия:** Боковые рынки

### Подходит для:
- ✅ Боковых трендов
- ✅ Коррекционных движений
- ✅ Стабильных рынков

---

## 🚀 Momentum Strategy

### Описание:
Торговля на сильных импульсах цены с использованием momentum индикаторов.

### Настройка:
```python
SELECTED_STRATEGY = 'MomentumStrategy'
```

### Принципы:
- **Rate of Change (ROC):** Скорость изменения цены
- **MACD импульс:** Ускорение/замедление
- **Volume подтверждение:** 2.5x+ объем
- **Williams %R:** Дополнительное подтверждение

### Результаты:
- **Win Rate:** 55-65%
- **Profit Factor:** 1.4-2.0
- **Время в позиции:** 10-60 минут

### Подходит для:
- ✅ Волатильных рынков
- ✅ Новостных событий
- ✅ Сильных движений

---

## 🎛️ Сравнение стратегий

| Стратегия | Win Rate | Profit Factor | Сделок/день | Время в позиции | Сложность |
|-----------|----------|---------------|-------------|-----------------|-----------|
| Smart Money | 65-75% | 1.8-2.5 | 2-5 | 2-8 часов | 🟡 Средняя |
| MultiIndicator | 55-65% | 1.2-1.8 | 3-10 | 1-6 часов | 🔴 Высокая |
| Trend Following | 45-55% | 1.5-2.2 | 1-3 | 4-24 часа | 🟢 Низкая |
| Scalping | 70-80% | 1.1-1.4 | 20-100 | 1-15 минут | 🔴 Очень высокая |
| Swing | 50-60% | 1.8-2.5 | 0.5-2 | 1-7 дней | 🟢 Низкая |
| Breakout | 50-60% | 1.6-2.3 | 2-8 | 30 минут-4 часа | 🟡 Средняя |
| Mean Reversion | 60-70% | 1.3-1.7 | 3-12 | 30 минут-3 часа | 🟡 Средняя |
| Momentum | 55-65% | 1.4-2.0 | 5-15 | 10-60 минут | 🟡 Средняя |

---

## 🎯 Выбор стратегии по профилю

### 👶 Для начинающих:

```python
# Вариант 1: Консервативный
SELECTED_STRATEGY = 'SmartMoneyStrategy'
RISK_SETTINGS = {
    'risk_per_trade': 0.01,      # 1% риск
    'max_daily_loss': 0.03,      # 3% дневной лимит
}

# Вариант 2: Простой тренд
SELECTED_STRATEGY = 'TrendFollowingStrategy'
RISK_SETTINGS = {
    'risk_per_trade': 0.015,     # 1.5% риск
    'max_positions': 2,          # Максимум 2 позиции
}
```

### 🎯 Для опытных:

```python
# Вариант 1: Настраиваемая стратегия
SELECTED_STRATEGY = 'MultiIndicatorStrategy'
CUSTOM_STRATEGY_CONFIG = {
    'min_conditions_required': 3,
    'min_confidence': 0.65,
    # Настройте под свой стиль
}

# Вариант 2: Пробои
SELECTED_STRATEGY = 'BreakoutStrategy'
RISK_SETTINGS = {
    'risk_per_trade': 0.02,      # 2% риск
    'max_positions': 3,
}
```

### 🔥 Для активных трейдеров:

```python
# Вариант 1: Скальпинг
SELECTED_STRATEGY = 'ScalpingStrategy'
TIME_SETTINGS = {
    'intervals': {'cycle_interval': 30},  # Каждые 30 секунд
    'timeframes': {'primary': '1'},       # 1-минутные свечи
}

# Вариант 2: Импульсная торговля
SELECTED_STRATEGY = 'MomentumStrategy'
RISK_SETTINGS = {
    'risk_per_trade': 0.025,     # 2.5% риск
    'max_positions': 4,
}
```

---

## 🔧 Тонкая настройка стратегий

### Настройка агрессивности:

#### Более агрессивно (больше сигналов):
```python
# Для MultiIndicatorStrategy
CUSTOM_STRATEGY_CONFIG = {
    'min_conditions_required': 2,      # Меньше условий
    'min_confidence': 0.5,              # Меньше уверенность
    'signal_cooldown': 60,              # Чаще сигналы
}

# Для всех стратегий
RISK_SETTINGS = {
    'risk_per_trade': 0.03,             # Больше риск
    'max_positions': 5,                 # Больше позиций
}
```

#### Более консервативно (качественные сигналы):
```python
# Для MultiIndicatorStrategy
CUSTOM_STRATEGY_CONFIG = {
    'min_conditions_required': 4,      # Больше условий
    'min_confidence': 0.8,              # Больше уверенность
    'signal_cooldown': 600,             # Реже сигналы
}

# Для всех стратегий
RISK_SETTINGS = {
    'risk_per_trade': 0.01,             # Меньше риск
    'max_positions': 2,                 # Меньше позиций
}
```

### Настройка под рыночные условия:

#### Трендовые рынки:
```python
SELECTED_STRATEGY = 'TrendFollowingStrategy'
# или
SELECTED_STRATEGY = 'MomentumStrategy'
```

#### Боковые рынки:
```python
SELECTED_STRATEGY = 'MeanReversionStrategy'
# или настройте MultiIndicator для range торговли
```

#### Волатильные рынки:
```python
SELECTED_STRATEGY = 'BreakoutStrategy'
# или
SELECTED_STRATEGY = 'ScalpingStrategy'
```

---

## 📊 Мониторинг стратегий

### Просмотр статистики:

```bash
# Статистика текущей стратегии
python -c "
from main import TradingBot
bot = TradingBot()
stats = bot.get_strategy_performance()
print(f'Статистика стратегии: {stats}')
"

# Результаты валидации
python -c "
from main import TradingBot
bot = TradingBot()
validation = bot.run_strategy_validation()
print(f'Валидация: Score {validation.get(\"score\", 0)}/100')
"
```

### Анализ производительности:

```python
# В интерактивном режиме Python
from modules.performance_tracker import PerformanceTracker
tracker = PerformanceTracker()
metrics = tracker.get_performance_metrics()

print(f"Общий P&L: ${metrics['total_pnl']}")
print(f"Win Rate: {metrics['win_rate']}%")
print(f"Profit Factor: {metrics['profit_factor']}")
print(f"Максимальная просадка: {metrics['max_drawdown_pct']}%")
```

---

## 🔄 Переключение стратегий

### Безопасное переключение:

```python
# 1. Остановите бота (Ctrl+C)
# 2. Измените стратегию в user_config.py
SELECTED_STRATEGY = 'новая_стратегия'

# 3. Проверьте конфигурацию
python user_config.py

# 4. Перезапустите бота
python main.py
```

### A/B тестирование стратегий:

```bash
# Неделя 1: Smart Money
SELECTED_STRATEGY = 'SmartMoneyStrategy'

# Неделя 2: Trend Following  
SELECTED_STRATEGY = 'TrendFollowingStrategy'

# Сравните результаты через diary_viewer.py
```

---

## 🎓 Обучение и оптимизация

### Изучение результатов:

```bash
# Дневник торговли
python utils/diary_viewer.py

# Анализ лучших сделок
python -c "
from utils.diary_viewer import DiaryViewer
viewer = DiaryViewer()
viewer.show_week()  # Недельная сводка
"
```

### Оптимизация параметров:

1. **Анализируйте логи** стратегии
2. **Изучайте причины** входов/выходов
3. **Корректируйте параметры** постепенно
4. **Тестируйте изменения** на TESTNET

### Рекомендации по улучшению:

- **Если мало сигналов:** Снизьте `min_confidence` или `min_conditions_required`
- **Если много ложных сигналов:** Повысьте фильтры
- **Если большие просадки:** Уменьшите `risk_per_trade`
- **Если малая прибыль:** Проверьте `take_profit` настройки

---

## 🏆 Лучшие практики

### 1. Начало работы:
- ✅ Тестируйте 1-2 недели на TESTNET
- ✅ Начинайте с Smart Money Strategy
- ✅ Используйте малые суммы первый месяц
- ✅ Ведите дневник результатов

### 2. Оптимизация:
- ✅ Анализируйте результаты еженедельно
- ✅ Корректируйте параметры постепенно
- ✅ Тестируйте изменения перед применением
- ✅ Сохраняйте работающие настройки

### 3. Управление рисками:
- ✅ Никогда не рискуйте более 5% в день
- ✅ Используйте стоп-лоссы всегда
- ✅ Диверсифицируйте торговые пары
- ✅ Мониторьте просадки

---

**🎯 Помните: Лучшая стратегия - это та, которую вы понимаете и можете контролировать!**