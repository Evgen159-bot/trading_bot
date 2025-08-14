# 📊 Руководство по торговым парам

## 🎯 Доступные торговые пары (7 пар)

Бот поддерживает **7 торговых пар** с возможностью выбора **максимум 4 активных** одновременно.

### 📋 Полный список пар:

| Пара | Описание | Волатильность | Рекомендуемое плечо | Приоритет |
|------|----------|---------------|-------------------|-----------|
| **ETHUSDT** | Ethereum - стабильная и ликвидная | Средняя | 2-3x | Высокий |
| **BTCUSDT** | Bitcoin - король криптовалют | Низкая | 2x | Высокий |
| **SOLUSDT** | Solana - высокий потенциал роста | Высокая | 3-4x | Высокий |
| **DOGEUSDT** | Dogecoin - мемная монета | Очень высокая | 3-5x | Средний |
| **XRPUSDT** | Ripple - стабильная пара | Средняя | 2-3x | Средний |
| **1000PEPEUSDT** | PEPE - экстремальная волатильность | Экстремальная | 5x | Низкий |
| **SUIUSDT** | Sui - новая L1 платформа | Высокая | 3-4x | Средний |

---

## ⚙️ Настройка торговых пар

### В файле `user_config.py`:

```python
TRADING_PAIRS = {
    'ETHUSDT': {
        'enabled': True,           # Включить/выключить торговлю
        'weight': 0.25,           # Вес в портфеле (25%)
        'leverage': 3,            # Плечо для этой пары
        'min_position': 0.001,    # Минимальный размер позиции
        'max_position': 5.0,      # Максимальный размер позиции
        'stop_loss_pct': 0.025,   # 2.5% стоп-лосс
        'take_profit_pct': 0.05,  # 5% тейк-профит
        'priority': 'high',       # Приоритет торговли
        'description': 'Ethereum - стабильная и ликвидная пара'
    },
    # ... остальные пары
}
```

### 🎯 Правила выбора пар:

1. **Максимум 4 активных пары** (`enabled: True`)
2. **Сумма весов = 1.0** для включенных пар
3. **Отключенные пары** должны иметь `weight: 0.0`

---

## 🏆 Рекомендуемые комбинации

### 👶 Для начинающих (2 пары):
```python
TRADING_PAIRS = {
    "ETHUSDT": {"enabled": True, "weight": 0.6},  # 60% - стабильная
    "BTCUSDT": {"enabled": True, "weight": 0.4},  # 40% - консервативная
    # Остальные отключены
    "SOLUSDT": {"enabled": False, "weight": 0.0},
    "DOGEUSDT": {"enabled": False, "weight": 0.0},
    "XRPUSDT": {"enabled": False, "weight": 0.0},
    "1000PEPEUSDT": {"enabled": False, "weight": 0.0},
    "SUIUSDT": {"enabled": False, "weight": 0.0}
}
```

### 🎯 Сбалансированный портфель (4 пары):
```python
TRADING_PAIRS = {
    "ETHUSDT": {"enabled": True, "weight": 0.25},  # 25% - стабильная основа
    "BTCUSDT": {"enabled": True, "weight": 0.25},  # 25% - консервативная
    "SOLUSDT": {"enabled": True, "weight": 0.25},  # 25% - рост потенциал
    "DOGEUSDT": {"enabled": True, "weight": 0.25}, # 25% - спекулятивная
    # Остальные отключены
    "XRPUSDT": {"enabled": False, "weight": 0.0},
    "1000PEPEUSDT": {"enabled": False, "weight": 0.0},
    "SUIUSDT": {"enabled": False, "weight": 0.0}
}
```

### 🔥 Агрессивный портфель (4 пары):
```python
TRADING_PAIRS = {
    "SOLUSDT": {"enabled": True, "weight": 0.25},     # 25% - высокий потенциал
    "DOGEUSDT": {"enabled": True, "weight": 0.25},    # 25% - мемкоин
    "SUIUSDT": {"enabled": True, "weight": 0.3},      # 30% - новая технология
    "1000PEPEUSDT": {"enabled": True, "weight": 0.2}, # 20% - экстремальная волатильность
    # Остальные отключены
    "ETHUSDT": {"enabled": False, "weight": 0.0},
    "BTCUSDT": {"enabled": False, "weight": 0.0},
    "XRPUSDT": {"enabled": False, "weight": 0.0}
}
```

### 💎 Консервативный портфель (3 пары):
```python
TRADING_PAIRS = {
    "BTCUSDT": {"enabled": True, "weight": 0.5},   # 50% - самая стабильная
    "ETHUSDT": {"enabled": True, "weight": 0.35},  # 35% - проверенная
    "XRPUSDT": {"enabled": True, "weight": 0.15},  # 15% - стабильная альткоин
    # Остальные отключены
    "SOLUSDT": {"enabled": False, "weight": 0.0},
    "DOGEUSDT": {"enabled": False, "weight": 0.0},
    "1000PEPEUSDT": {"enabled": False, "weight": 0.0},
    "SUIUSDT": {"enabled": False, "weight": 0.0}
}
```

---

## 📊 Характеристики пар

### 🟢 Низкий риск:
- **BTCUSDT**: Самая стабильная, низкая волатильность
- **ETHUSDT**: Высокая ликвидность, предсказуемые движения
- **XRPUSDT**: Стабильные колебания, хорошо для новичков

### 🟡 Средний риск:
- **SOLUSDT**: Высокий потенциал роста, умеренная волатильность
- **SUIUSDT**: Новая технология, растущий интерес
- **DOGEUSDT**: Мемкоин с периодическими всплесками

### 🔴 Высокий риск:
- **1000PEPEUSDT**: Экстремальная волатильность, высокие риски и прибыли

---

## 🔧 Настройка параметров пар

### Основные параметры:

```python
'ETHUSDT': {
    'enabled': True,              # Включить торговлю
    'weight': 0.25,              # Вес в портфеле (25%)
    'leverage': 3,               # Плечо (1-10x)
    'min_position': 0.001,       # Минимальный размер позиции
    'max_position': 5.0,         # Максимальный размер позиции
    'stop_loss_pct': 0.025,      # 2.5% стоп-лосс
    'take_profit_pct': 0.05,     # 5% тейк-профит
    'priority': 'high',          # Приоритет: high/medium/low
    'description': 'Описание пары'
}
```

### Рекомендуемые настройки по парам:

#### BTCUSDT (консервативная):
```python
'BTCUSDT': {
    'leverage': 2,               # Низкое плечо
    'stop_loss_pct': 0.02,       # 2% стоп-лосс
    'take_profit_pct': 0.04,     # 4% тейк-профит
}
```

#### DOGEUSDT (волатильная):
```python
'DOGEUSDT': {
    'leverage': 4,               # Среднее плечо
    'stop_loss_pct': 0.035,      # 3.5% стоп-лосс
    'take_profit_pct': 0.07,     # 7% тейк-профит
}
```

#### 1000PEPEUSDT (экстремальная):
```python
'1000PEPEUSDT': {
    'leverage': 5,               # Высокое плечо
    'stop_loss_pct': 0.05,       # 5% стоп-лосс
    'take_profit_pct': 0.10,     # 10% тейк-профит
}
```

---

## ⚠️ Важные правила

### ✅ Обязательные требования:
1. **Максимум 4 активных пары** одновременно
2. **Сумма весов включенных пар = 1.0**
3. **Отключенные пары имеют weight = 0.0**
4. **Начинайте с 1-2 пар** для изучения

### 🚨 Предупреждения:
- **Мемкоины** (DOGE, PEPE) очень волатильны
- **Новые проекты** (SUI) могут быть непредсказуемы
- **Не включайте все пары сразу** - начните с проверенных

---

## 🔄 Переключение пар

### Безопасное изменение:

1. **Остановите бота** (Ctrl+C)
2. **Измените настройки** в `user_config.py`
3. **Проверьте конфигурацию:**
   ```bash
   python user_config.py
   ```
4. **Перезапустите бота:**
   ```bash
   python main.py
   ```

### Пример изменения:

```python
# Было (2 пары):
'ETHUSDT': {'enabled': True, 'weight': 0.6},
'SOLUSDT': {'enabled': True, 'weight': 0.4},

# Стало (4 пары):
'ETHUSDT': {'enabled': True, 'weight': 0.25},
'BTCUSDT': {'enabled': True, 'weight': 0.25},
'SOLUSDT': {'enabled': True, 'weight': 0.25},
'DOGEUSDT': {'enabled': True, 'weight': 0.25},
```

---

## 📈 Мониторинг пар

### Просмотр активности по парам:

```bash
# Дневник торговли
python utils/diary_viewer.py

# Проверка текущих позиций
python -c "
from main import TradingBot
bot = TradingBot()
status = bot.get_bot_status()
print(f'Активные пары: {status[\"trading_pairs\"]}')
"
```

### Анализ производительности по парам:

```python
# В интерактивном режиме Python
from modules.performance_tracker import PerformanceTracker
tracker = PerformanceTracker()
symbol_report = tracker.get_symbol_report()
print(symbol_report)
```

---

## 🎯 Стратегии выбора пар

### По рыночным условиям:

#### Бычий рынок:
```python
# Акцент на рост потенциал
"SOLUSDT": {"enabled": True, "weight": 0.3},
"SUIUSDT": {"enabled": True, "weight": 0.3},
"DOGEUSDT": {"enabled": True, "weight": 0.2},
"ETHUSDT": {"enabled": True, "weight": 0.2}
```

#### Медвежий рынок:
```python
# Акцент на стабильность
"BTCUSDT": {"enabled": True, "weight": 0.4},
"ETHUSDT": {"enabled": True, "weight": 0.3},
"XRPUSDT": {"enabled": True, "weight": 0.3}
```

#### Боковой рынок:
```python
# Сбалансированный подход
"ETHUSDT": {"enabled": True, "weight": 0.25},
"BTCUSDT": {"enabled": True, "weight": 0.25},
"SOLUSDT": {"enabled": True, "weight": 0.25},
"XRPUSDT": {"enabled": True, "weight": 0.25}
```

---

**🎯 Помните: Диверсификация снижает риски, но не гарантирует прибыль!**