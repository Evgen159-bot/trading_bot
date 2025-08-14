#!/usr/bin/env python3
"""
🚀 ПОЛЬЗОВАТЕЛЬСКАЯ КОНФИГУРАЦИЯ ТОРГОВОГО БОТА
===============================================

Этот файл предназначен для настройки торгового бота конечными пользователями.
Здесь вы можете изменить все основные параметры без изменения кода бота.

⚠️  ВАЖНО: Сохраните резервную копию этого файла перед изменениями!
"""

import os
from typing import Dict, Any, List
from datetime import time


class UserConfig:
    """Пользовательская конфигурация торгового бота"""

    # ========================================================================
    # 🔑 API НАСТРОЙКИ (ОБЯЗАТЕЛЬНО К ЗАПОЛНЕНИЮ!)
    # ========================================================================

    # Ваши API ключи от ByBit (получите на https://www.bybit.com/app/user/api-management)
    BYBIT_API_KEY = "bVnEkHGAs1t90HbTmR"  # 🔴 ЗАМЕНИТЕ НА ВАШ API КЛЮЧ!
    BYBIT_API_SECRET = "A91FxgRB0WdIYXR3l7AaShnR0UQOx6cUb2dy"  # 🔴 ЗАМЕНИТЕ НА ВАШ SECRET!

    # Режим работы (True = тестовая сеть, False = реальная торговля)
    USE_TESTNET = True  # 🟡 Установите False для реальной торговли

    # ========================================================================
    # 🎯 ВЫБОР ТОРГОВОЙ СТРАТЕГИИ
    # ========================================================================

    # Выберите стратегию для торговли
    SELECTED_STRATEGY = 'custom'  # Временно переключаем на более активную стратегию для тестирования

    # Описания доступных стратегий
    AVAILABLE_STRATEGIES = {
        'custom': {
            'name': 'Пользовательская стратегия',
            'description': 'Настраиваемая мульти-индикаторная стратегия с полным контролем параметров',
            'type': 'configurable',
            'risk_level': 'medium',
            'timeframe': 'any',
            'best_for': 'Опытные трейдеры, которые хотят полный контроль'
        },
        'smart_money': {
            'name': 'Smart Money Strategy',
            'description': 'Стратегия на основе концепций Smart Money: структура рынка, ликвидность, институциональные уровни',
            'type': 'automatic',
            'risk_level': 'low',
            'timeframe': '5m-1h',
            'best_for': 'Консервативная торговля с высоким качеством сигналов'
        },
        'trend_following': {
            'name': 'Trend Following Strategy',
            'description': 'Классическая стратегия следования тренду с ADX и множественными EMA',
            'type': 'automatic',
            'risk_level': 'medium',
            'timeframe': '15m-4h',
            'best_for': 'Стабильная прибыль в трендовых рынках'
        },
        'scalping': {
            'name': 'Scalping Strategy',
            'description': 'Быстрая скальпинговая стратегия для краткосрочной торговли',
            'type': 'automatic',
            'risk_level': 'high',
            'timeframe': '1m-5m',
            'best_for': 'Активная торговля с быстрыми прибылями'
        },
        'swing': {
            'name': 'Swing Trading Strategy',
            'description': 'Среднесрочная стратегия для удержания позиций от нескольких часов до дней',
            'type': 'automatic',
            'risk_level': 'low',
            'timeframe': '4h-1d',
            'best_for': 'Пассивная торговля с меньшим количеством сделок'
        },
        'breakout': {
            'name': 'Breakout Strategy',
            'description': 'Стратегия пробоя уровней поддержки/сопротивления с объемным подтверждением',
            'type': 'automatic',
            'risk_level': 'medium',
            'timeframe': '15m-1h',
            'best_for': 'Торговля на волатильности и пробоях'
        },
        'mean_reversion': {
            'name': 'Mean Reversion Strategy',
            'description': 'Стратегия возврата к среднему с использованием Bollinger Bands и RSI',
            'type': 'automatic',
            'risk_level': 'medium',
            'timeframe': '5m-30m',
            'best_for': 'Торговля в боковых трендах'
        },
        'momentum': {
            'name': 'Momentum Strategy',
            'description': 'Стратегия импульса с использованием MACD, RSI и объемных индикаторов',
            'type': 'automatic',
            'risk_level': 'high',
            'timeframe': '5m-15m',
            'best_for': 'Торговля на сильных движениях рынка'
        }
    }

    # ========================================================================
    # 🛠️ НАСТРОЙКИ ПОЛЬЗОВАТЕЛЬСКОЙ СТРАТЕГИИ (только для 'custom')
    # ========================================================================

    CUSTOM_STRATEGY_CONFIG = {
        # Основные параметры
        'name': 'MyCustomStrategy',
        'description': 'Моя персональная торговая стратегия',

        # Параметры RSI
        'rsi_settings': {
            'enabled': True,
            'period': 14,
            'oversold_lower': 30,  # Более мягкие условия для тестирования
            'oversold_upper': 45,  # Более мягкие условия
            'overbought_lower': 55,  # Более мягкие условия
            'overbought_upper': 70,  # Более мягкие условия
            'weight': 1.0  # Вес индикатора (0.0-2.0)
        },

        # Параметры MACD
        'macd_settings': {
            'enabled': True,
            'fast_period': 12,
            'slow_period': 26,
            'signal_period': 9,
            'histogram_threshold': 0.0002,
            'weight': 1.0
        },

        # Параметры EMA
        'ema_settings': {
            'enabled': True,
            'fast_period': 9,  # Быстрая EMA
            'slow_period': 21,  # Медленная EMA
            'trend_period': 50,  # Трендовая EMA
            'weight': 1.0
        },

        # Параметры Bollinger Bands
        'bollinger_settings': {
            'enabled': True,
            'period': 20,
            'std_deviation': 2.0,
            'weight': 0.8
        },

        # Параметры объема
        'volume_settings': {
            'enabled': True,
            'sma_period': 20,
            'min_ratio': 0.8,  # Снижаем требования к объему
            'surge_threshold': 2.5,  # Порог всплеска объема
            'weight': 0.7
        },

        # Параметры Stochastic
        'stochastic_settings': {
            'enabled': True,
            'k_period': 14,
            'd_period': 3,
            'smooth_k': 3,
            'oversold': 25,
            'overbought': 75,
            'weight': 0.8
        },

        # Параметры ATR
        'atr_settings': {
            'enabled': True,
            'period': 14,
            'stop_loss_multiplier': 2.0,  # Множитель для стоп-лосса
            'take_profit_multiplier': 2.5,  # Множитель для тейк-профита
            'trailing_multiplier': 1.5  # Множитель для трейлинг-стопа
        },

        # Настройки входа в позицию
        'entry_conditions': {
            'min_conditions_required': 1,  # Еще больше снижаем для активности
            'trend_strength_threshold': 0.3,  # Минимальная сила тренда
            'volume_confirmation': True,  # Требовать подтверждение объемом
            'signal_cooldown': 60  # Еще больше уменьшаем cooldown
        },

        # Настройки выхода из позиции
        'exit_conditions': {
            'use_trailing_stop': True,
            'emergency_rsi_long': 80,  # RSI для экстренного выхода из лонга
            'emergency_rsi_short': 20,  # RSI для экстренного выхода из шорта
            'profit_exit_rsi_long': 65,  # RSI для выхода из прибыльного лонга
            'profit_exit_rsi_short': 35  # RSI для выхода из прибыльного шорта
        },

        # Управление рисками
        'risk_management': {
            'risk_per_trade': 0.02,  # Увеличиваем до 2% для тестирования
            'max_stop_loss_pct': 0.08,  # 8% максимальный стоп-лосс
            'min_take_profit_pct': 0.12,  # 12% минимальный тейк-профит
            'max_take_profit_pct': 0.25,  # 25% максимальный тейк-профит
            'leverage': 3,  # Плечо
            'max_position_value_pct': 0.3  # 30% максимум от баланса на позицию
        }
    }

    # ========================================================================
    # 💰 УПРАВЛЕНИЕ КАПИТАЛОМ И РИСКАМИ
    # ========================================================================

    # Начальный баланс для работы (будет проверен при запуске)
    INITIAL_BALANCE = 1000.0  # USD

    # Минимальный баланс для продолжения торговли
    MIN_BALANCE_THRESHOLD = 100.0  # USD

    # Риск-менеджмент
    RISK_SETTINGS = {
        'risk_per_trade': 0.02,  # 2% от баланса на сделку
        'max_daily_loss': 0.05,  # 5% максимальная дневная потеря
        'max_positions': 4,  # Максимум открытых позиций (увеличено до 4)
        'max_daily_trades': 15,  # Максимум сделок в день
        'emergency_stop_loss': 0.10,  # 10% экстренный стоп-лосс
        'drawdown_limit': 0.15,  # 15% лимит просадки
        'position_sizing_method': 'risk_based',  # 'risk_based' или 'fixed'
        'max_leverage': 5  # Максимальное плечо
    }

    # ========================================================================
    # 📊 ТОРГОВЫЕ ПАРЫ И ИХ НАСТРОЙКИ (7 доступных пар, максимум 4 активных)
    # ========================================================================

    TRADING_PAIRS = {
        'ETHUSDT': {
            'enabled': True,  # Включить торговлю по этой паре
            'weight': 0.25,  # Вес в портфеле (25%)
            'leverage': 3,  # Плечо для этой пары
            'min_position': 0.001,  # Минимальный размер позиции
            'max_position': 5.0,  # Максимальный размер позиции
            'stop_loss_pct': 0.025,  # 2.5% стоп-лосс
            'take_profit_pct': 0.05,  # 5% тейк-профит
            'priority': 'high',  # Приоритет торговли
            'description': 'Ethereum - стабильная и ликвидная пара'
        },
        'SOLUSDT': {
            'enabled': True,
            'weight': 0.25,  # Вес в портфеле (25%)
            'leverage': 3,
            'min_position': 0.01,
            'max_position': 10.0,
            'stop_loss_pct': 0.03,
            'take_profit_pct': 0.06,
            'priority': 'high',
            'description': 'Solana - высокая волатильность и потенциал роста'
        },
        'BTCUSDT': {
            'enabled': True,  # 🆕 Новая пара
            'weight': 0.25,  # Вес в портфеле (25%)
            'leverage': 2,  # Более консервативное плечо для BTC
            'min_position': 0.0001,  # Минимальный размер позиции
            'max_position': 1.0,  # Максимальный размер позиции
            'stop_loss_pct': 0.02,  # 2% стоп-лосс (BTC менее волатилен)
            'take_profit_pct': 0.04,  # 4% тейк-профит
            'priority': 'high',
            'description': 'Bitcoin - король криптовалют, низкая волатильность'
        },
        'DOGEUSDT': {
            'enabled': True,  # 🆕 Новая пара
            'weight': 0.25,  # Вес в портфеле (25%)
            'leverage': 4,  # Среднее плечо
            'min_position': 1.0,  # Минимальный размер позиции
            'max_position': 1000.0,  # Максимальный размер позиции
            'stop_loss_pct': 0.035,  # 3.5% стоп-лосс (DOGE волатилен)
            'take_profit_pct': 0.07,  # 7% тейк-профит
            'priority': 'medium',
            'description': 'Dogecoin - мемная монета с высокой волатильностью'
        },
        'XRPUSDT': {
            'enabled': False,  # 🔴 Отключена по умолчанию
            'weight': 0.0,  # Вес 0 для отключенных пар
            'leverage': 2,
            'min_position': 1.0,
            'max_position': 500.0,
            'stop_loss_pct': 0.025,
            'take_profit_pct': 0.05,
            'priority': 'medium',
            'description': 'Ripple - стабильная пара для консервативной торговли'
        },
        '1000PEPEUSDT': {
            'enabled': False,  # 🔴 Отключена по умолчанию
            'weight': 0.0,  # Вес 0 для отключенных пар
            'leverage': 5,  # Высокое плечо для мемкоина
            'min_position': 1000.0,  # Минимальный размер позиции
            'max_position': 100000.0,  # Максимальный размер позиции
            'stop_loss_pct': 0.05,  # 5% стоп-лосс (очень волатилен)
            'take_profit_pct': 0.10,  # 10% тейк-профит
            'priority': 'low',
            'description': 'PEPE - мемкоин с экстремальной волатильностью'
        },
        'SUIUSDT': {
            'enabled': False,
            'weight': 0.0,
            'leverage': 4,
            'min_position': 0.1,
            'max_position': 100.0,
            'stop_loss_pct': 0.04,
            'take_profit_pct': 0.08,
            'priority': 'medium',
            'description': 'Sui - новая L1 блокчейн платформа'
        },
        'ADAUSDT': {
            'enabled': False,
            'weight': 0.0,
            'leverage': 3,
            'min_position': 1.0,
            'max_position': 1000.0,
            'stop_loss_pct': 0.03,
            'take_profit_pct': 0.06,
            'priority': 'medium',
            'description': 'Cardano - академический подход к блокчейну'
        }
    }

    # ========================================================================
    # 📈 НАСТРОЙКИ ТЕХНИЧЕСКИХ ИНДИКАТОРОВ (для пользовательской стратегии)
    # ========================================================================

    INDICATORS_CONFIG = {
        # RSI (Индекс относительной силы)
        'rsi': {
            'enabled': True,
            'period': 14,
            'oversold': 30,  # Уровень перепроданности
            'overbought': 70,  # Уровень перекупленности
            'extreme_oversold': 20,  # Экстремальная перепроданность
            'extreme_overbought': 80,  # Экстремальная перекупленность
            'weight': 1.0  # Вес индикатора в стратегии
        },

        # MACD (Схождение-расхождение скользящих средних)
        'macd': {
            'enabled': True,
            'fast_period': 12,
            'slow_period': 26,
            'signal_period': 9,
            'histogram_threshold': 0.0002,
            'weight': 1.0
        },

        # EMA (Экспоненциальные скользящие средние)
        'ema': {
            'enabled': True,
            'fast_period': 8,
            'medium_period': 21,
            'slow_period': 50,
            'trend_period': 200,
            'weight': 1.0
        },

        # Bollinger Bands (Полосы Боллинджера)
        'bollinger': {
            'enabled': True,
            'period': 20,
            'std_deviation': 2.0,
            'squeeze_threshold': 0.1,
            'weight': 0.8
        },

        # Volume (Объем)
        'volume': {
            'enabled': True,
            'sma_period': 20,
            'min_threshold': 1.2,  # Минимальный объем для сигнала
            'surge_threshold': 3.0,  # Всплеск объема
            'weight': 0.7
        },

        # ATR (Средний истинный диапазон)
        'atr': {
            'enabled': True,
            'period': 14,
            'multiplier': 2.0,
            'trailing_multiplier': 1.5,
            'weight': 0.5
        },

        # Stochastic (Стохастический осциллятор)
        'stochastic': {
            'enabled': True,
            'k_period': 14,
            'd_period': 3,
            'smooth_k': 3,
            'oversold': 20,
            'overbought': 80,
            'weight': 0.8
        }
    }

    # ========================================================================
    # 🎯 НАСТРОЙКИ ТОРГОВОЙ СТРАТЕГИИ
    # ========================================================================

    STRATEGY_SETTINGS = {
        # Основные параметры стратегии
        'strategy_name': 'SmartMoneyStrategy',  # Будет переопределено на основе SELECTED_STRATEGY
        'min_conditions_required': 3,  # Минимум условий для входа (из 6)
        'signal_confirmation_required': 3,  # Больше подтверждений
        'trend_strength_threshold': 0.6,  # Повышенная сила тренда
        'min_signal_confidence': 0.75,  # Повышенная уверенность (75%)

        # Фильтры стратегии (включить/выключить)
        'filters': {
            'trend_filter': True,  # Фильтр тренда
            'volume_filter': True,  # Фильтр объема
            'time_filter': True,  # Временной фильтр
            'volatility_filter': True,  # Фильтр волатильности
            'correlation_filter': True,  # Фильтр корреляции
            'news_filter': False,  # 🔴 Фильтр новостей (отключен)
            'market_hours_filter': True,  # Фильтр торговых часов
            'smart_money_filter': True  # 🆕 Smart Money фильтр
        },

        # Параметры входа в позицию
        'entry_settings': {
            'max_slippage': 0.0005,  # Уменьшенное проскальзывание
            'order_timeout': 30,  # Таймаут ордера (секунды)
            'partial_fill_allowed': True,  # Разрешить частичное исполнение
            'min_profit_potential': 0.04,  # Увеличенный потенциал прибыли
            'signal_cooldown': 300  # 🆕 5 минут между сигналами
        },

        # Параметры выхода из позиции
        'exit_settings': {
            'trailing_stop_enabled': True,  # Включить трейлинг-стоп
            'trailing_stop_distance': 0.015,  # Более близкий трейлинг-стоп
            'partial_close_enabled': True,  # Частичное закрытие позиций
            'profit_taking_levels': [0.3, 0.6],  # Более ранняя фиксация
            'max_position_time': 12 * 3600,  # Уменьшенное время (12 часов)
            'emergency_exit_loss': 0.08  # 🆕 Экстренный выход при 8% убытке
        }
    }

    # ========================================================================
    # ⏰ ВРЕМЕННЫЕ НАСТРОЙКИ
    # ========================================================================

    TIME_SETTINGS = {
        # Торговые часы (UTC)
        'trading_hours': {
            'start': '00:00',
            'end': '23:59',
            'maintenance_start': '08:00',  # Техобслуживание биржи
            'maintenance_end': '08:15',
            'weekend_trading': False  # Торговля на выходных
        },

        # Интервалы работы
        'intervals': {
            'cycle_interval': 30,  # Более частые проверки
            'data_update_interval': 30,  # Обновление данных (сек)
            'position_check_interval': 15,  # Проверка позиций (сек)
            'heartbeat_interval': 300  # Heartbeat (сек)
        },

        # Таймфреймы для анализа
        'timeframes': {
            'primary': '5',  # Основной таймфрейм (5 минут)
            'trend': '15',  # Анализ тренда (15 минут)
            'confirmation': '1',  # Подтверждение сигналов (1 минута)
            'long_term': '60'  # Долгосрочный анализ (1 час)
        }
    }

    # ========================================================================
    # 🔔 УВЕДОМЛЕНИЯ И МОНИТОРИНГ
    # ========================================================================

    NOTIFICATIONS = {
        # Telegram уведомления
        'telegram': {
            'enabled': False,  # 🔴 Отключено по умолчанию
            'bot_token': '',  # Токен Telegram бота
            'chat_id': '',  # ID чата для уведомлений
            'events': {
                'position_opened': True,
                'position_closed': True,
                'stop_loss_hit': True,
                'take_profit_hit': True,
                'daily_summary': True,
                'error_occurred': True
            }
        },

        # Email уведомления
        'email': {
            'enabled': False,  # 🔴 Отключено по умолчанию
            'smtp_server': '',
            'smtp_port': 587,
            'email_address': '',
            'email_password': '',
            'recipient': ''
        },

        # Консольные уведомления
        'console': {
            'enabled': True,
            'detailed_logs': True,
            'color_output': True
        }
    }

    # ========================================================================
    # 📊 НАСТРОЙКИ ЛОГИРОВАНИЯ И ДАННЫХ
    # ========================================================================

    LOGGING_SETTINGS = {
        'log_level': 'INFO',  # Информационное логирование (DEBUG слишком много)
        'max_log_size_mb': 100,
        'max_log_files': 10,
        'log_to_file': True,
        'log_to_console': True,
        'detailed_trading_logs': True,
        'performance_logging': True
    }

    DATA_SETTINGS = {
        'save_performance_data': True,
        'save_trading_diary': True,
        'export_format': 'csv',  # csv, json, excel
        'data_retention_days': 90,
        'backup_enabled': True,
        'backup_interval_hours': 24
    }

    # ========================================================================
    # 🛡️ БЕЗОПАСНОСТЬ И ЗАЩИТА
    # ========================================================================

    SECURITY_SETTINGS = {
        'api_rate_limit_buffer': 0.1,  # 10% буфер для rate limit
        'max_api_retries': 3,
        'api_timeout': 30,
        'connection_check_interval': 300,  # Проверка соединения (сек)
        'auto_restart_on_error': True,
        'max_restart_attempts': 5
    }

    # ========================================================================
    # 🎛️ ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ
    # ========================================================================

    ADVANCED_SETTINGS = {
        # Оптимизация производительности
        'performance': {
            'cache_enabled': True,
            'cache_timeout': 60,
            'parallel_processing': False,
            'memory_limit_mb': 512
        },

        # Режимы работы
        'modes': {
            'demo_mode': False,  # Демо режим (без реальных ордеров)
            'paper_trading': False,  # Бумажная торговля
            'backtesting_mode': False,  # Режим бэктестинга
            'strategy_validation': True  # Валидация стратегии при запуске
        },

        # Экспериментальные функции
        'experimental': {
            'ai_signals': False,  # AI сигналы (в разработке)
            'sentiment_analysis': False,  # Анализ настроений (в разработке)
            'multi_exchange': False,  # Мульти-биржевая торговля (в разработке)
            'portfolio_rebalancing': False  # Ребалансировка портфеля (в разработке)
        }
    }

    # ========================================================================
    # 🔧 МЕТОДЫ ВАЛИДАЦИИ И ПРОВЕРКИ
    # ========================================================================

    @classmethod
    def validate_config(cls) -> tuple[bool, list[str]]:
        """
        Валидация пользовательской конфигурации

        Returns:
            tuple: (is_valid, list_of_errors)
        """
        errors = []

        # Проверка API ключей
        if cls.BYBIT_API_KEY == "YOUR_API_KEY_HERE":
            errors.append("🔴 API ключ не настроен! Замените YOUR_API_KEY_HERE на ваш реальный ключ")

        if cls.BYBIT_API_SECRET == "YOUR_API_SECRET_HERE":
            errors.append("🔴 API секрет не настроен! Замените YOUR_API_SECRET_HERE на ваш реальный секрет")

        # Проверка выбранной стратегии
        if cls.SELECTED_STRATEGY not in cls.AVAILABLE_STRATEGIES:
            errors.append(f"🔴 Неизвестная стратегия: {cls.SELECTED_STRATEGY}")

        # Проверка баланса
        if cls.INITIAL_BALANCE <= 0:
            errors.append("🔴 Начальный баланс должен быть больше 0")

        if cls.MIN_BALANCE_THRESHOLD >= cls.INITIAL_BALANCE:
            errors.append("🔴 Минимальный баланс не может быть больше начального")

        # Проверка торговых пар
        enabled_pairs = [pair for pair, config in cls.TRADING_PAIRS.items() if config['enabled']]
        if not enabled_pairs:
            errors.append("🔴 Нет включенных торговых пар! Включите хотя бы одну пару")

        # Проверка весов портфеля
        total_weight = sum(config['weight'] for config in cls.TRADING_PAIRS.values() if config['enabled'])
        if abs(total_weight - 1.0) > 0.01:
            errors.append(f"⚠️ Веса портфеля не равны 1.0 (текущий: {total_weight:.2f})")

        # Проверка риск-менеджмента
        if cls.RISK_SETTINGS['risk_per_trade'] > 0.1:
            errors.append("⚠️ Риск на сделку больше 10% - это очень рискованно!")

        if cls.RISK_SETTINGS['max_daily_loss'] > 0.2:
            errors.append("⚠️ Максимальная дневная потеря больше 20% - это крайне рискованно!")

        # Проверка пользовательской стратегии
        if cls.SELECTED_STRATEGY == 'custom':
            custom_config = cls.CUSTOM_STRATEGY_CONFIG

            # Проверка параметров риска
            risk_mgmt = custom_config['risk_management']
            if risk_mgmt['risk_per_trade'] > 0.05:
                errors.append("⚠️ Риск на сделку в пользовательской стратегии больше 5%")

            if risk_mgmt['max_stop_loss_pct'] > 0.15:
                errors.append("⚠️ Максимальный стоп-лосс больше 15%")

            # Проверка включенных индикаторов
            enabled_indicators = [name for name, config in custom_config.items()
                                  if name.endswith('_settings') and config.get('enabled', False)]
            if len(enabled_indicators) < 3:
                errors.append("⚠️ В пользовательской стратегии включено менее 3 индикаторов")

        # Проверка индикаторов (для совместимости)
        enabled_indicators = [name for name, config in cls.INDICATORS_CONFIG.items() if config['enabled']]
        if len(enabled_indicators) < 3:
            errors.append("⚠️ Включено менее 3 индикаторов - рекомендуется использовать больше")

        return len(errors) == 0, errors

    @classmethod
    def get_enabled_pairs(cls) -> dict:
        """Получить только включенные торговые пары"""
        return {pair: config for pair, config in cls.TRADING_PAIRS.items() if config['enabled']}

    @classmethod
    def get_enabled_indicators(cls) -> dict:
        """Получить только включенные индикаторы"""
        return {name: config for name, config in cls.INDICATORS_CONFIG.items() if config['enabled']}

    @classmethod
    def get_strategy_info(cls) -> dict:
        """Получить информацию о выбранной стратегии"""
        return cls.AVAILABLE_STRATEGIES.get(cls.SELECTED_STRATEGY, {})

    @classmethod
    def get_strategy_config(cls) -> dict:
        """Получить конфигурацию для выбранной стратегии"""
        if cls.SELECTED_STRATEGY == 'custom':
            return cls.CUSTOM_STRATEGY_CONFIG
        else:
            # Для автоматических стратегий возвращаем базовые настройки
            return {
                'strategy_name': cls.AVAILABLE_STRATEGIES[cls.SELECTED_STRATEGY]['name'],
                'type': 'automatic',
                'risk_level': cls.AVAILABLE_STRATEGIES[cls.SELECTED_STRATEGY]['risk_level']
            }

    @classmethod
    def print_config_summary(cls):
        """Вывести сводку конфигурации"""
        print("\n" + "=" * 70)
        print("🚀 СВОДКА ПОЛЬЗОВАТЕЛЬСКОЙ КОНФИГУРАЦИИ")
        print("=" * 70)

        print(f"🔑 Режим: {'TESTNET' if cls.USE_TESTNET else '🔴 РЕАЛЬНАЯ ТОРГОВЛЯ'}")
        print(f"💰 Начальный баланс: ${cls.INITIAL_BALANCE:,.2f}")
        print(f"📊 Включенных пар: {len(cls.get_enabled_pairs())}")
        print(f"📈 Включенных индикаторов: {len(cls.get_enabled_indicators())}")
        print(f"🎯 Риск на сделку: {cls.RISK_SETTINGS['risk_per_trade'] * 100:.1f}%")
        print(f"🛡️ Макс. дневная потеря: {cls.RISK_SETTINGS['max_daily_loss'] * 100:.1f}%")

        # Информация о стратегии
        strategy_info = cls.get_strategy_info()
        print(f"\n🎯 ВЫБРАННАЯ СТРАТЕГИЯ:")
        print(f"   📋 Название: {strategy_info.get('name', 'Unknown')}")
        print(f"   📝 Описание: {strategy_info.get('description', 'No description')}")
        print(f"   ⚙️ Тип: {'Настраиваемая' if strategy_info.get('type') == 'configurable' else 'Автоматическая'}")
        print(f"   🎚️ Уровень риска: {strategy_info.get('risk_level', 'unknown').upper()}")
        print(f"   ⏰ Таймфрейм: {strategy_info.get('timeframe', 'any')}")
        print(f"   🎯 Подходит для: {strategy_info.get('best_for', 'general trading')}")

        enabled_pairs = cls.get_enabled_pairs()
        if enabled_pairs:
            print(f"\n📊 Активные торговые пары:")
            for pair, config in enabled_pairs.items():
                print(f"   • {pair}: вес {config['weight'] * 100:.0f}%, плечо {config['leverage']}x")

        print("=" * 70)

    @classmethod
    def print_strategy_list(cls):
        """Вывести список доступных стратегий"""
        print("\n" + "=" * 70)
        print("📋 ДОСТУПНЫЕ ТОРГОВЫЕ СТРАТЕГИИ")
        print("=" * 70)

        for strategy_id, info in cls.AVAILABLE_STRATEGIES.items():
            selected_mark = "👉 " if strategy_id == cls.SELECTED_STRATEGY else "   "
            risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(info['risk_level'], "⚪")
            type_emoji = "🛠️" if info['type'] == 'configurable' else "🤖"

            print(f"{selected_mark}{type_emoji} {info['name']} {risk_emoji}")
            print(f"     📝 {info['description']}")
            print(f"   ⏰ Таймфрейм: {info['timeframe']} | 🎯 Подходит для: {info['best_for']}")
            print()

        print("💡 Для изменения стратегии измените SELECTED_STRATEGY в этом файле")
        print("=" * 70)


# ========================================================================
# 🚨 ВАЖНЫЕ ИНСТРУКЦИИ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ
# ========================================================================

INSTRUCTIONS = """
🚀 ИНСТРУКЦИИ ПО НАСТРОЙКЕ ТОРГОВОГО БОТА
==========================================

1. 🎯 ВЫБОР СТРАТЕГИИ:
   - Измените SELECTED_STRATEGY на нужную стратегию
   - Доступные стратегии: 'custom', 'smart_money', 'trend_following', 'scalping', 'swing', 'breakout', 'mean_reversion', 'momentum'
   - Для просмотра всех стратегий: python user_config.py --strategies

2. 🛠️ НАСТРОЙКА ПОЛЬЗОВАТЕЛЬСКОЙ СТРАТЕГИИ (только для 'custom'):
   - Отредактируйте CUSTOM_STRATEGY_CONFIG
   - Настройте параметры каждого индикатора
   - Установите уровни стоп-лосса и тейк-профита
   - Настройте условия входа и выхода

3. 🔑 НАСТРОЙКА API (ОБЯЗАТЕЛЬНО!):
   - Зарегистрируйтесь на ByBit: https://www.bybit.com
   - Создайте API ключи в разделе "API Management"
   - Замените значения BYBIT_API_KEY и BYBIT_API_SECRET
   - Для начала оставьте USE_TESTNET = True

4. 💰 НАСТРОЙКА КАПИТАЛА:
   - Установите INITIAL_BALANCE согласно вашему депозиту
   - Настройте RISK_SETTINGS под ваш уровень риска
   - Рекомендуется начинать с малых сумм

5. 📊 ВЫБОР ТОРГОВЫХ ПАР:
   - Включите/выключите пары в TRADING_PAIRS
   - Настройте веса портфеля (сумма должна быть 1.0)
   - Установите подходящие стоп-лоссы и тейк-профиты

6. 🔔 УВЕДОМЛЕНИЯ (ОПЦИОНАЛЬНО):
   - Настройте Telegram или Email уведомления
   - Получайте уведомления о важных событиях

⚠️  ВАЖНЫЕ ПРЕДУПРЕЖДЕНИЯ:
- ВСЕГДА тестируйте на TESTNET перед реальной торговлей!
- Начинайте с малых сумм
- Регулярно проверяйте работу бота
- Торговля криптовалютами связана с высокими рисками

🆘 ПОДДЕРЖКА:
- Проверьте логи в папке logs/
- Убедитесь в правильности API ключей
- Проверьте интернет соединение
- Используйте валидацию конфигурации: python user_config.py
"""

if __name__ == "__main__":
    import sys

    # Проверяем аргументы командной строки
    if len(sys.argv) > 1 and sys.argv[1] == '--strategies':
        UserConfig.print_strategy_list()
        sys.exit(0)

    # Запуск валидации конфигурации
    print(INSTRUCTIONS)
    print("\n🔍 Проверка конфигурации...")

    is_valid, errors = UserConfig.validate_config()

    if is_valid:
        print("✅ Конфигурация корректна!")
        UserConfig.print_config_summary()
    else:
        print("❌ Найдены ошибки в конфигурации:")
        for error in errors:
            print(f"   {error}")
        print("\n🔧 Исправьте ошибки и запустите проверку снова")

    print("\n💡 Для просмотра всех стратегий: python user_config.py --strategies")