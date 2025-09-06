from typing import Dict, Any, Optional
from datetime import time, datetime
import os
from dotenv import load_dotenv
import logging

# Загрузка переменных окружения
load_dotenv('config/config.env')

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TradingConfig:
    """Конфигурация торгового бота"""

    # API настройки
    API_KEY = os.getenv('BYBIT_API_KEY')
    API_SECRET = os.getenv('BYBIT_API_SECRET')
    TESTNET = os.getenv('BYBIT_TESTNET', 'True').lower() == 'true'  # Читаем из .env

    # Настройки подключения
    CONNECTION_SETTINGS = {
        'timeout': 30,
        'max_retries': 3,
        'retry_delay': 5,
        'recv_window': 5000,
        'rate_limit_buffer': 0.1  # 10% буфер для rate limit
    }

    # Настройки риск-менеджмента
    RISK_MANAGEMENT = {
        'max_daily_loss': 0.05,  # 5% максимальная дневная потеря
        'risk_per_trade': 0.005,  # 0.5% риск на сделку
        'max_positions': 4,  # Максимум открытых позиций
        'max_daily_trades': 32,  # Максимум сделок в день (8 на пару)
        'min_risk_reward': 1.5,  # Минимальное соотношение риск/прибыль
        'max_leverage': 5,  # Максимальное плечо
        'emergency_stop_loss': 0.10,  # Экстренный стоп-лосс 10%
        'drawdown_limit': 0.15,  # Лимит просадки 15%
        'position_sizing': {
            'method': 'risk_based',  # Метод расчета размера позиции
            'default_size': 0.1,  # Размер по умолчанию
            'max_position_value': 50,  # Максимальная стоимость позиции
            'min_position_value': 10  # Минимальная стоимость позиции
        }
    }

    # Настройки временных интервалов
    TIMEFRAMES = {
        'primary': '5',  # Основной таймфрейм для торговли
        'trend': '15',  # Таймфрейм для анализа тренда
        'confirmation': '1',  # Таймфрейм для подтверждения сигналов
        'long_term': '1h'  # Долгосрочный анализ
    }

    # Торговые часы (UTC)
    TRADING_HOURS = {
        'start': '00:00',
        'end': '23:59',
        'maintenance_start': '08:00',  # Время технического обслуживания биржи
        'maintenance_end': '08:15',
        'high_volatility_hours': ['14:00-16:00', '20:00-22:00']  # Часы высокой волатильности
    }

    # Торговые пары с расширенными настройками
    TRADING_PAIRS: Dict[str, Dict[str, Any]] = {
        'ETHUSDT': {
            'weight': 0.25,  # Вес в портфеле
            'min_volume': 100000,  # Минимальный объем для торговли
            'leverage': 5,  # Плечо
            'min_position': 0.001,  # Минимальный размер позиции
            'max_position': 5.0,  # Максимальный размер позиции
            'stop_loss_pct': 0.025,  # 2.5% стоп-лосс
            'take_profit_pct': 0.05,  # 5% тейк-профит
            'tick_size': 0.01,  # Минимальный шаг цены
            'lot_size': 0.001,  # Минимальный размер лота
            'max_slippage': 0.001,  # Максимальное проскальзывание
            'priority': 'high'  # Приоритет торговли
        },
        'SOLUSDT': {
            'weight': 0.25,
            'min_volume': 50000,
            'leverage': 5,
            'min_position': 0.01,
            'max_position': 10.0,
            'stop_loss_pct': 0.03,  # 3% стоп-лосс (SOL волатильнее)
            'take_profit_pct': 0.06,  # 6% тейк-профит
            'tick_size': 0.001,
            'lot_size': 0.01,
            'max_slippage': 0.002,
            'priority': 'high'
        },
        'BTCUSDT': {
            'weight': 0.25,
            'min_volume': 200000,  # Высокий объем для BTC
            'leverage': 5,  # Плечо 5x
            'min_position': 0.0001,
            'max_position': 1.0,
            'stop_loss_pct': 0.02,
            'take_profit_pct': 0.04,
            'tick_size': 0.01,
            'lot_size': 0.0001,
            'max_slippage': 0.0005,
            'priority': 'high'
        },
        'XRPUSDT': {
            'weight': 0.25,
            'min_volume': 30000,
            'leverage': 5,  # Плечо 5x
            'min_position': 1.0,
            'max_position': 500.0,
            'stop_loss_pct': 0.025,  # 2.5% стоп-лосс
            'take_profit_pct': 0.05,  # 5% тейк-профит
            'tick_size': 0.0001,
            'lot_size': 1.0,
            'max_slippage': 0.001,
            'priority': 'high'  # Повышен приоритет
        },
        'BTCUSDT': {
            'weight': 0.25,
            'min_volume': 200000,  # Высокий объем для BTC
            'leverage': 2,  # Консервативное плечо
            'min_position': 0.0001,
            'max_position': 1.0,
            'stop_loss_pct': 0.02,
            'take_profit_pct': 0.04,
            'tick_size': 0.01,
            'lot_size': 0.0001,
            'max_slippage': 0.0005,
            'priority': 'high'
        },
        'DOGEUSDT': {
            'weight': 0.25,
            'min_volume': 80000,
            'leverage': 4,
            'min_position': 1.0,
            'max_position': 1000.0,
            'stop_loss_pct': 0.035,
            'take_profit_pct': 0.07,
            'tick_size': 0.00001,
            'lot_size': 1.0,
            'max_slippage': 0.002,
            'priority': 'medium'
        },
        '1000PEPEUSDT': {
            'weight': 0.25,
            'min_volume': 50000,
            'leverage': 5,  # Высокое плечо для мемкоина
            'min_position': 1000.0,
            'max_position': 100000.0,
            'stop_loss_pct': 0.05,  # Высокий стоп для волатильности
            'take_profit_pct': 0.10,
            'tick_size': 0.0000001,
            'lot_size': 1000.0,
            'max_slippage': 0.003,
            'priority': 'low'
        },
        'SUIUSDT': {
            'weight': 0.25,
            'min_volume': 40000,
            'leverage': 4,
            'min_position': 0.1,
            'max_position': 100.0,
            'stop_loss_pct': 0.04,
            'take_profit_pct': 0.08,
            'tick_size': 0.0001,
            'lot_size': 0.1,
            'max_slippage': 0.002,
            'priority': 'medium'
        }
    }


    # Расширенные настройки индикаторов
    INDICATORS = {
        'ema': {
            'fast': 8,
            'medium': 21,
            'slow': 50,
            'trend': 200,
            'cross_confirmation': True
        },
        'rsi': {
            'period': 14,
            'oversold': 30,
            'overbought': 70,
            'divergence_period': 14,
            'extreme_oversold': 20,
            'extreme_overbought': 80
        },
        'macd': {
            'fast': 12,
            'slow': 26,
            'signal': 9,
            'histogram_threshold': 0.0002,
            'divergence_lookback': 20
        },
        'bollinger': {
            'period': 20,
            'std': 2.0,
            'squeeze_threshold': 0.1,
            'expansion_threshold': 0.15
        },
        'volume': {
            'sma_period': 20,
            'min_threshold': 1.5,
            'surge_threshold': 3.0,
            'volume_profile_periods': [10, 20, 50]
        },
        'atr': {
            'period': 14,
            'multiplier': 2.0,
            'trailing_multiplier': 1.5
        },
        'stochastic': {
            'k_period': 14,
            'd_period': 3,
            'smooth_k': 3,
            'oversold': 20,
            'overbought': 80
        },
        'support_resistance': {
            'lookback_period': 50,
            'min_touches': 2,
            'tolerance': 0.001
        }
    }

    # Настройки стратегии
    STRATEGY_SETTINGS = {
        'signal_confirmation_required': 2,  # Количество подтверждений сигнала
        'max_correlation_threshold': 0.8,  # Максимальная корреляция между позициями
        'trend_filter_enabled': True,  # Включить фильтр тренда
        'volume_filter_enabled': True,  # Включить фильтр объема
        'time_filter_enabled': True,  # Включить временной фильтр
        'news_filter_enabled': False,  # Фильтр новостей (пока отключен)
        'backtest_mode': False  # Режим бэктестинга
    }

    # Настройки уведомлений
    NOTIFICATIONS = {
        'enabled': True,
        'telegram': {
            'enabled': False,
            'bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
            'chat_id': os.getenv('TELEGRAM_CHAT_ID')
        },
        'email': {
            'enabled': False,
            'smtp_server': os.getenv('SMTP_SERVER'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'email': os.getenv('EMAIL_ADDRESS'),
            'password': os.getenv('EMAIL_PASSWORD')
        },
        'events': {
            'position_opened': True,
            'position_closed': True,
            'stop_loss_hit': True,
            'take_profit_hit': True,
            'error_occurred': True,
            'daily_summary': True
        }
    }

    # Дополнительные настройки
    CYCLE_INTERVAL = int(os.getenv('CYCLE_INTERVAL', '60'))  # Читаем из .env
    MAX_RETRIES = 3
    RETRY_DELAY = 5
    RECV_WINDOW = 5000

    # Настройки производительности
    PERFORMANCE_SETTINGS = {
        'save_interval': 300,  # Сохранять данные каждые 5 минут
        'cleanup_interval': 3600,  # Очистка старых данных каждый час
        'max_log_size_mb': 100,  # Максимальный размер лог-файла
        'max_history_days': 30  # Хранить историю 30 дней
    }

    # Настройки базы данных (если используется)
    DATABASE_SETTINGS = {
        'enabled': False,
        'type': 'sqlite',  # sqlite, postgresql, mysql
        'path': 'data/trading_bot.db',
        'backup_interval': 3600  # Бэкап каждый час
    }

    @classmethod
    def validate_config(cls) -> bool:
        """Валидация конфигурации с детальными проверками"""
        errors = []

        # Проверка API ключей
        if not cls.API_KEY or not cls.API_SECRET:
            errors.append("API keys not configured")

        # Проверка торговых пар
        if not cls.TRADING_PAIRS:
            errors.append("No trading pairs configured")

        # Проверка весов портфеля
        total_weight = sum(pair.get('weight', 0) for pair in cls.TRADING_PAIRS.values())
        if abs(total_weight - 1.0) > 0.01:
            errors.append(f"Portfolio weights don't sum to 1.0 (current: {total_weight})")

        # Проверка риск-менеджмента
        risk_settings = cls.RISK_MANAGEMENT
        if risk_settings['risk_per_trade'] > risk_settings['max_daily_loss']:
            errors.append("Risk per trade exceeds max daily loss")

        # Проверка временных интервалов
        if cls.CYCLE_INTERVAL < 5:
            errors.append("Cycle interval too short (minimum 5 seconds)")

        # Проверка плеча
        for symbol, config in cls.TRADING_PAIRS.items():
            if config.get('leverage', 1) > cls.RISK_MANAGEMENT['max_leverage']:
                errors.append(f"Leverage for {symbol} exceeds maximum allowed")

        if errors:
            for error in errors:
                logger.error(f"Configuration error: {error}")
            return False

        logger.info("Configuration validated successfully")
        return True

    @classmethod
    def get_pair_config(cls, symbol: str) -> Optional[Dict[str, Any]]:
        """Получить конфигурацию для конкретной торговой пары"""
        return cls.TRADING_PAIRS.get(symbol)

    @classmethod
    def is_trading_hours(cls) -> bool:
        """Проверить, находимся ли мы в торговых часах"""
        now = datetime.now().time()
        start_time = datetime.strptime(cls.TRADING_HOURS['start'], '%H:%M').time()
        end_time = datetime.strptime(cls.TRADING_HOURS['end'], '%H:%M').time()

        if start_time <= end_time:
            return start_time <= now <= end_time
        else:  # Переход через полночь
            return now >= start_time or now <= end_time

    @classmethod
    def is_maintenance_time(cls) -> bool:
        """Проверить, не время ли технического обслуживания"""
        now = datetime.now().time()
        start_time = datetime.strptime(cls.TRADING_HOURS['maintenance_start'], '%H:%M').time()
        end_time = datetime.strptime(cls.TRADING_HOURS['maintenance_end'], '%H:%M').time()

        return start_time <= now <= end_time

    @classmethod
    def get_active_pairs(cls) -> Dict[str, Dict[str, Any]]:
        """Получить активные торговые пары с учетом приоритета"""
        if not cls.is_trading_hours() or cls.is_maintenance_time():
            return {}

        # Сортируем по приоритету
        sorted_pairs = sorted(
            cls.TRADING_PAIRS.items(),
            key=lambda x: {'high': 3, 'medium': 2, 'low': 1}.get(x[1].get('priority', 'low'), 1),
            reverse=True
        )

        return dict(sorted_pairs)

    @classmethod
    def get_environment_info(cls) -> Dict[str, Any]:
        """Получить информацию об окружении"""
        return {
            'testnet': cls.TESTNET,
            'trading_pairs_count': len(cls.TRADING_PAIRS),
            'cycle_interval': cls.CYCLE_INTERVAL,
            'max_positions': cls.RISK_MANAGEMENT['max_positions'],
            'risk_per_trade': cls.RISK_MANAGEMENT['risk_per_trade'],
            'notifications_enabled': cls.NOTIFICATIONS['enabled']
        }