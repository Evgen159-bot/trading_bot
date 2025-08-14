# 🔑 Подробное руководство по настройке API ByBit

## 📋 Пошаговая инструкция

### Шаг 1: Регистрация на ByBit

1. **Переходим на сайт:** [ByBit.com](https://www.bybit.com)
2. **Нажимаем "Sign Up"** в правом верхнем углу
3. **Заполняем форму регистрации:**
   - Email адрес
   - Пароль (минимум 8 символов)
   - Подтверждение пароля
4. **Подтверждаем email** (проверьте почту)
5. **Проходим верификацию** (загружаем документы)

### Шаг 2: Настройка безопасности

1. **Включаем 2FA:**
   - Account & Security → Two-Factor Authentication
   - Скачиваем Google Authenticator
   - Сканируем QR код
   - Вводим код подтверждения

2. **Настраиваем Anti-Phishing Code:**
   - Account & Security → Anti-Phishing Code
   - Придумываем уникальный код
   - Этот код будет в официальных письмах ByBit

---

## 🔐 Создание API ключей

### Шаг 1: Переход в API Management

1. **Заходим в аккаунт** на ByBit
2. **Переходим:** Account & Security → API Management
3. **Нажимаем:** "Create New Key"

### Шаг 2: Настройка прав доступа

**✅ ВКЛЮЧИТЕ:**
- **Read** - чтение данных аккаунта
- **Trade** - размещение и отмена ордеров

**❌ НЕ ВКЛЮЧАЙТЕ:**
- **Withdraw** - вывод средств (ОПАСНО!)
- **Transfer** - переводы между аккаунтами

### Шаг 3: Настройка IP ограничений

**Рекомендуется:**
- Добавьте свой IP адрес для дополнительной безопасности
- Узнать IP: [whatismyipaddress.com](https://whatismyipaddress.com)

**Или:**
- Оставьте пустым для доступа с любого IP (менее безопасно)

### Шаг 4: Получение ключей

1. **Вводим название:** например "Trading Bot"
2. **Нажимаем "Submit"**
3. **Копируем API Key** (публичный ключ)
4. **Копируем Secret Key** (приватный ключ)

**⚠️ ВАЖНО:** Secret Key показывается только один раз! Сохраните его надежно.

---

## 🛠️ Настройка в боте

### В файле user_config.py:

```python
class UserConfig:
    # 🔑 ЗАМЕНИТЕ НА ВАШИ РЕАЛЬНЫЕ КЛЮЧИ!
    BYBIT_API_KEY = "ваш_api_key_здесь"
    BYBIT_API_SECRET = "ваш_secret_key_здесь"
    
    # Режим работы
    USE_TESTNET = True  # True = тестовая сеть (безопасно для начала)
```

### Пример правильной настройки:

```python
# ✅ ПРАВИЛЬНО:
BYBIT_API_KEY = "bVnEkHGAs1t90HbTmR"
BYBIT_API_SECRET = "A91FxgRB0WdIYXR3l7AaShnR0UQOx6cUb2dy"

# ❌ НЕПРАВИЛЬНО:
BYBIT_API_KEY = "YOUR_API_KEY_HERE"  # Не заменили!
BYBIT_API_SECRET = ""                # Пустой ключ!
```

---

## 🧪 Тестирование подключения

### Проверка API ключей:

```bash
# Быстрая проверка
python -c "
from modules.data_fetcher import DataFetcher
try:
    df = DataFetcher()
    print('✅ API ключи работают корректно')
except Exception as e:
    print(f'❌ Ошибка API: {e}')
"
```

### Проверка баланса:

```python
# test_balance.py
from modules.data_fetcher import DataFetcher

df = DataFetcher()
balance = df.get_account_balance()

if balance is not None:
    print(f"✅ Баланс USDT: ${balance:.2f}")
else:
    print("❌ Не удалось получить баланс")
```

### Проверка торговых пар:

```python
# test_pairs.py
from modules.data_fetcher import DataFetcher

df = DataFetcher()

# Тестируем получение данных
for symbol in ['ETHUSDT', 'BTCUSDT']:
    price = df.get_current_price(symbol)
    if price:
        print(f"✅ {symbol}: ${price:.2f}")
    else:
        print(f"❌ {symbol}: Ошибка получения цены")
```

---

## 🔒 Безопасность API

### ✅ Правила безопасности:

1. **Никогда не включайте Withdraw права**
2. **Используйте IP ограничения**
3. **Регулярно меняйте ключи** (раз в 3-6 месяцев)
4. **Не делитесь ключами** ни с кем
5. **Храните ключи в безопасном месте**

### 🛡️ Дополнительная защита:

```python
# В user_config.py добавьте ограничения
SECURITY_SETTINGS = {
    'api_rate_limit_buffer': 0.1,       # Буфер для rate limit
    'max_api_retries': 3,               # Максимум попыток
    'api_timeout': 30,                  # Таймаут запросов
    'connection_check_interval': 300,   # Проверка соединения
}
```

### 🚨 Что делать при компрометации:

1. **Немедленно удалите** скомпрометированные ключи в ByBit
2. **Создайте новые ключи** с теми же правами
3. **Обновите конфигурацию** бота
4. **Проверьте историю** торговли на предмет подозрительной активности

---

## 🌐 Работа с Testnet

### Что такое Testnet:
- **Тестовая сеть** ByBit с виртуальными деньгами
- **Полная функциональность** без реальных рисков
- **Идеально для обучения** и тестирования стратегий

### Настройка Testnet:

1. **Переходим:** [Testnet.ByBit.com](https://testnet.bybit.com)
2. **Регистрируемся** (можно тот же email)
3. **Получаем тестовые средства:** Account → Assets → Trial Fund
4. **Создаем API ключи** (те же права: Read + Trade)

### В user_config.py:

```python
# Для Testnet
USE_TESTNET = True
BYBIT_API_KEY = "testnet_api_key"
BYBIT_API_SECRET = "testnet_secret_key"

# Для реальной торговли
USE_TESTNET = False
BYBIT_API_KEY = "real_api_key"
BYBIT_API_SECRET = "real_secret_key"
```

---

## 🔧 Устранение проблем с API

### Частые ошибки:

#### "Invalid API key":
```python
# Проверьте правильность ключей
from user_config import UserConfig
print(f"API Key: {UserConfig.BYBIT_API_KEY[:10]}...")  # Первые 10 символов
print(f"Secret длина: {len(UserConfig.BYBIT_API_SECRET)}")  # Должно быть ~40 символов
```

#### "IP not allowed":
- Добавьте ваш IP в настройки API на ByBit
- Или уберите IP ограничения (менее безопасно)

#### "Rate limit exceeded":
```python
# В user_config.py увеличьте задержки
SECURITY_SETTINGS = {
    'api_rate_limit_buffer': 0.2,  # Увеличьте буфер
}
```

#### "Insufficient permissions":
- Проверьте права API ключа (должны быть Read + Trade)
- Пересоздайте ключ с правильными правами

### Диагностика подключения:

```python
# full_api_test.py
from modules.data_fetcher import DataFetcher
from config.trading_config import TradingConfig
import traceback

print("🔍 Полная диагностика API:")
print(f"Testnet режим: {TradingConfig.TESTNET}")
print(f"API Key (первые 10): {TradingConfig.API_KEY[:10] if TradingConfig.API_KEY else 'НЕ НАСТРОЕН'}")

try:
    df = DataFetcher()
    
    # Тест 1: Время сервера
    server_time = df.get_server_time()
    print(f"✅ Время сервера: {server_time}")
    
    # Тест 2: Баланс
    balance = df.get_account_balance()
    print(f"✅ Баланс: ${balance:.2f}")
    
    # Тест 3: Цены
    eth_price = df.get_current_price('ETHUSDT')
    print(f"✅ ETH цена: ${eth_price:.2f}")
    
    # Тест 4: Исторические данные
    from datetime import datetime, timedelta
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    
    klines = df.get_kline(
        'ETHUSDT', '5', 
        int(start_time.timestamp()), 
        int(end_time.timestamp())
    )
    print(f"✅ Исторические данные: {len(klines) if klines is not None else 0} свечей")
    
    print("\n🎉 Все тесты прошли успешно!")
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    print("\nДетали ошибки:")
    traceback.print_exc()
```

---

## 📞 Поддержка ByBit

### Официальные каналы:

- **📧 Email:** support@bybit.com
- **💬 Live Chat:** На сайте ByBit (правый нижний угол)
- **📱 Telegram:** [@BybitRussian](https://t.me/BybitRussian)
- **📚 Документация:** [ByBit API Docs](https://bybit-exchange.github.io/docs/)

### Полезные ссылки:

- **API Management:** [ByBit API](https://www.bybit.com/app/user/api-management)
- **Testnet:** [Testnet.ByBit.com](https://testnet.bybit.com)
- **Статус API:** [ByBit Status](https://bybit-status.com)
- **Лимиты API:** [Rate Limits](https://bybit-exchange.github.io/docs/v5/rate-limit)

---

**🎯 После настройки API переходите к [выбору стратегии](STRATEGIES.md) и [первому запуску](README.md#-запуск)!**