# 🚀 РУКОВОДСТВО ПО НАСТРОЙКЕ ТОРГОВОГО БОТА

## 📋 Быстрый старт

### 1. Первоначальная настройка

1. **Откройте файл `user_config.py`**
2. **Замените API ключи:**
   ```python
   BYBIT_API_KEY = "ваш_реальный_api_ключ"
   BYBIT_API_SECRET = "ваш_реальный_секрет"
   ```
3. **Установите начальный баланс:**
   ```python
   INITIAL_BALANCE = 1000.0  # Ваш депозит в USD
   ```

### 2. Получение API ключей ByBit

1. Зарегистрируйтесь на [ByBit](https://www.bybit.com)
2. Перейдите в **Account & Security** → **API Management**
3. Создайте новый API ключ с правами:
   - ✅ Read
   - ✅ Trade
   - ❌ Withdraw (НЕ включайте!)
4. Скопируйте **API Key** и **Secret Key**

### 3. Настройка торговых пар

```python
TRADING_PAIRS = {
    'ETHUSDT': {
        'enabled': True,           # Включить торговлю
        'weight': 0.4,            # 40% портфеля
        'leverage': 3,            # Плечо 3x
        'stop_loss_pct': 0.025,   # 2.5% стоп-лосс
        'take_profit_pct': 0.05,  # 5% тейк-профит
    }
}
```

### 4. Настройка риск-менеджмента

```python
RISK_SETTINGS = {
    'risk_per_trade': 0.02,        # 2% риск на сделку
    'max_daily_loss': 0.05,        # 5% максимальная дневная потеря
    'max_positions': 3,            # Максимум 3 позиции
}
```

### 5. Выбор стратегии

```python
# Доступные стратегии:
SELECTED_STRATEGY = 'custom'           # Настраиваемая (рекомендуется для начала)
SELECTED_STRATEGY = 'smart_money'      # Очень консервативная
SELECTED_STRATEGY = 'trend_following'  # Трендовая
SELECTED_STRATEGY = 'scalping'         # Скальпинг
SELECTED_STRATEGY = 'swing'            # Свинг
SELECTED_STRATEGY = 'breakout'         # Пробои
SELECTED_STRATEGY = 'mean_reversion'   # Возврат к среднему
SELECTED_STRATEGY = 'momentum'         # Импульсная
```

## 🎯 Детальные настройки

### Индикаторы

Каждый индикатор можно включить/выключить и настроить:

```python
INDICATORS_CONFIG = {
    'rsi': {
        'enabled': True,
        'period': 14,
        'oversold': 30,
        'overbought': 70,
    }
}
```

### Стратегия

```python
STRATEGY_SETTINGS = {
    'min_conditions_required': 3,    # Минимум условий для входа
    'filters': {
        'trend_filter': True,         # Фильтр тренда
        'volume_filter': True,        # Фильтр объема
        'news_filter': False,         # Фильтр новостей (отключен)
    }
}
```

## 🔔 Уведомления

### Telegram (опционально)

1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен бота
3. Узнайте свой Chat ID через [@userinfobot](https://t.me/userinfobot)

```python
NOTIFICATIONS = {
    'telegram': {
        'enabled': True,
        'bot_token': 'ваш_токен_бота',
        'chat_id': 'ваш_chat_id',
    }
}
```

## ⚠️ Важные предупреждения

### 🔴 Безопасность
- **НИКОГДА** не включайте права на вывод средств в API
- **ВСЕГДА** тестируйте на TESTNET перед реальной торговлей
- **НЕ ДЕЛИТЕСЬ** своими API ключами

### 💰 Управление рисками
- Начинайте с малых сумм
- Не рискуйте деньгами, которые не можете позволить себе потерять
- Регулярно проверяйте работу бота

### 🧪 Тестирование
```python
USE_TESTNET = True  # Обязательно для начала!
```

## 🚀 Запуск бота

1. **Проверьте конфигурацию:**
   ```bash
   python user_config.py
   ```

2. **Запустите бота:**
   ```bash
   python main.py
   ```

3. **Мониторинг:**
   - Проверяйте логи в папке `logs/`
   - Используйте `python utils/diary_viewer.py` для просмотра результатов

4. **Просмотр стратегий:**
   ```bash
   # Список всех стратегий
   python user_config.py --strategies
   
   # Интерактивный выбор
   python utils/strategy_selector.py --interactive
   ```

## 🆘 Поддержка

### Частые проблемы:

1. **"API ключ не настроен"** → Замените YOUR_API_KEY_HERE на реальный ключ
2. **"Нет включенных торговых пар"** → Установите `enabled: True` для нужных пар
3. **"Веса портфеля не равны 1.0"** → Сумма весов всех включенных пар должна быть 1.0

### Проверка конфигурации:
```bash
python user_config.py
```

---

**🎯 Помните: Успешная торговля требует терпения, дисциплины и постоянного обучения!**