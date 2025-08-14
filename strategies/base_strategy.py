from abc import ABC, abstractmethod
import logging
import os
from typing import Dict, Optional, Any, List, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config.trading_config import TradingConfig


class BaseStrategy(ABC):
    """Базовый класс для всех торговых стратегий"""

    def __init__(self, name: str = "BaseStrategy", config: Dict[str, Any] = None):
        """
        Инициализация базовой стратегии

        Args:
            name: Название стратегии
            config: Конфигурация стратегии
        """
        self.name = name

        # Настройка логгера
        self.logger = self._setup_logger()

        # Конфигурация стратегии (объединяем с глобальной конфигурацией)
        self.config = self._merge_configs(config or {})

        # Статистика стратегии
        self.stats = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_profit': 0.0,
            'total_loss': 0.0,
            'max_drawdown': 0.0,
            'max_profit': 0.0,
            'win_rate': 0.0,
            'profit_factor': 0.0,
            'avg_win': 0.0,
            'avg_loss': 0.0,
            'consecutive_wins': 0,
            'consecutive_losses': 0,
            'max_consecutive_wins': 0,
            'max_consecutive_losses': 0,
            'last_trade_time': None,
            'strategy_start_time': datetime.now()
        }

        # Кэш для оптимизации
        self.cache = {}
        self.cache_timeout = 60  # секунд

        # Состояние стратегии
        self.is_active = True
        self.last_signal_time = None
        self.signal_cooldown = self.config.get('signal_cooldown', 30)  # секунд между сигналами

        self.logger.info(f"Strategy {self.name} initialized successfully")

    def _setup_logger(self) -> logging.Logger:
        """Настройка логгера для стратегии"""
        logger = logging.getLogger(f"strategy.{self.name}")
        logger.setLevel(logging.INFO)

        # Очищаем существующие обработчики
        logger.handlers.clear()

        # Создаем директорию для логов
        log_dir = "logs/strategies"
        os.makedirs(log_dir, exist_ok=True)

        # Файловый обработчик
        log_file = os.path.join(log_dir, f"{self.name}_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(file_handler)

        return logger

    def _merge_configs(self, strategy_config: Dict[str, Any]) -> Dict[str, Any]:
        """Объединение конфигурации стратегии с глобальной"""
        try:
            # Базовая конфигурация из TradingConfig
            base_config = {
                'risk_management': TradingConfig.RISK_MANAGEMENT,
                'indicators': TradingConfig.INDICATORS,
                'strategy_settings': TradingConfig.STRATEGY_SETTINGS,
                'timeframes': TradingConfig.TIMEFRAMES
            }

            # Объединяем с конфигурацией стратегии
            merged_config = {**base_config, **strategy_config}

            return merged_config

        except Exception as e:
            self.logger.error(f"Error merging configs: {e}")
            return strategy_config

    @abstractmethod
    def generate_signal(self, data: pd.DataFrame, symbol: str = None) -> Optional[Dict[str, Any]]:
        """
        Генерация торгового сигнала на основе данных

        Args:
            data: DataFrame с рыночными данными и индикаторами
            symbol: Торговая пара (опционально)

        Returns:
            Dict с сигналом или None, если сигнал отсутствует
        """
        pass

    def validate_signal(self, signal: Dict[str, Any]) -> bool:
        """
        Валидация торгового сигнала

        Args:
            signal: Словарь с данными сигнала

        Returns:
            bool: True если сигнал валиден, False в противном случае
        """
        try:
            # Базовые проверки
            required_fields = ['action', 'entry_price', 'timestamp']
            if not all(field in signal for field in required_fields):
                missing_fields = [f for f in required_fields if f not in signal]
                self.logger.warning(f"Signal missing required fields: {missing_fields}")
                return False

            # Проверка времени сигнала
            if isinstance(signal['timestamp'], datetime):
                signal_time = signal['timestamp']
            else:
                signal_time = datetime.fromtimestamp(signal['timestamp'])

            max_age = self.config.get('max_signal_age', 60)
            if (datetime.now() - signal_time).total_seconds() > max_age:
                self.logger.warning("Signal too old")
                return False

            # Проверка цены
            if signal['entry_price'] <= 0:
                self.logger.warning("Invalid entry price in signal")
                return False

            # Проверка действия
            valid_actions = ['OPEN', 'CLOSE', 'BUY', 'SELL', 'LONG', 'SHORT']
            if signal['action'] not in valid_actions:
                self.logger.warning(f"Invalid action: {signal['action']}")
                return False

            # Проверка cooldown между сигналами
            if self.last_signal_time:
                time_since_last = (datetime.now() - self.last_signal_time).total_seconds()
                if time_since_last < self.signal_cooldown:
                    self.logger.debug(f"Signal cooldown active: {time_since_last}s < {self.signal_cooldown}s")
                    return False

            return True

        except Exception as e:
            self.logger.error(f"Error validating signal: {e}")
            return False

    def calculate_position_size(self, signal: Dict[str, Any], account_balance: float,
                                symbol: str = None) -> float:
        """
        Расчет размера позиции с учетом риск-менеджмента

        Args:
            signal: Словарь с данными сигнала
            account_balance: Текущий баланс аккаунта
            symbol: Торговая пара

        Returns:
            float: Размер позиции
        """
        try:
            if account_balance <= 0:
                self.logger.warning("Invalid account balance")
                return 0.0

            risk_config = self.config.get('risk_management', {})

            # Базовый риск на сделку
            risk_per_trade = risk_config.get('risk_per_trade', 0.02)

            # Максимальный размер позиции
            max_position_size = risk_config.get('max_position_size', 0.1)

            # Расчет на основе стоп-лосса
            entry_price = signal.get('entry_price', 0)
            stop_loss = signal.get('stop_loss', 0)

            if entry_price > 0 and stop_loss > 0:
                # Расчет на основе риска и стоп-лосса
                risk_amount = account_balance * risk_per_trade
                price_diff = abs(entry_price - stop_loss)

                if price_diff > 0:
                    position_size = risk_amount / price_diff
                else:
                    # Fallback к процентному методу
                    position_size = account_balance * risk_per_trade / entry_price
            else:
                # Простой процентный расчет
                position_size = account_balance * risk_per_trade / entry_price

            # Применение волатильности
            volatility = signal.get('volatility', 1.0)
            if volatility > 0:
                volatility_adjustment = min(2.0, max(0.5, 1.0 / volatility))
                position_size *= volatility_adjustment

            # Ограничение размера позиции
            max_value = account_balance * max_position_size
            if position_size * entry_price > max_value:
                position_size = max_value / entry_price

            # Применение настроек символа
            if symbol:
                symbol_config = TradingConfig.TRADING_PAIRS.get(symbol, {})
                min_pos = symbol_config.get('min_position', 0.001)
                max_pos = symbol_config.get('max_position', float('inf'))
                position_size = max(min_pos, min(position_size, max_pos))

            return round(position_size, 8)

        except Exception as e:
            self.logger.error(f"Error calculating position size: {e}")
            return 0.0

    def should_close_position(self, position: Dict[str, Any], current_data: pd.DataFrame,
                              current_price: float = None) -> Tuple[bool, str]:
        """
        Проверка необходимости закрытия позиции

        Args:
            position: Текущая позиция
            current_data: Текущие рыночные данные
            current_price: Текущая цена (опционально)

        Returns:
            Tuple[bool, str]: (нужно ли закрыть, причина)
        """
        try:
            if not position or current_data.empty:
                return False, "no_data"

            if current_price is None:
                current_price = current_data['close'].iloc[-1]

            entry_price = position.get('entry_price', 0)
            direction = position.get('direction', '')

            # Проверка стоп-лосса
            stop_loss = position.get('stop_loss')
            if stop_loss:
                if direction == 'BUY' and current_price <= stop_loss:
                    return True, "stop_loss"
                elif direction == 'SELL' and current_price >= stop_loss:
                    return True, "stop_loss"

            # Проверка тейк-профита
            take_profit = position.get('take_profit')
            if take_profit:
                if direction == 'BUY' and current_price >= take_profit:
                    return True, "take_profit"
                elif direction == 'SELL' and current_price <= take_profit:
                    return True, "take_profit"

            # Проверка времени в позиции
            entry_time = position.get('entry_time')
            if entry_time:
                if isinstance(entry_time, str):
                    entry_time = datetime.fromisoformat(entry_time)

                max_time = self.config.get('max_position_time', 24 * 3600)  # 24 часа
                if (datetime.now() - entry_time).total_seconds() > max_time:
                    return True, "max_time"

            # Проверка максимального убытка
            if entry_price > 0:
                pnl_pct = ((current_price - entry_price) / entry_price) * 100
                if direction == 'SELL':
                    pnl_pct = -pnl_pct

                max_loss_pct = self.config.get('max_loss_percent', 10)
                if pnl_pct < -max_loss_pct:
                    return True, "max_loss"

            return False, "hold"

        except Exception as e:
            self.logger.error(f"Error checking position close conditions: {e}")
            return True, "error"

    def calculate_volatility(self, data: pd.DataFrame, window: int = 20) -> float:
        """
        Расчет волатильности

        Args:
            data: DataFrame с ценовыми данными
            window: Окно для расчета волатильности

        Returns:
            float: Значение волатильности
        """
        try:
            if isinstance(data, pd.DataFrame) and not data.empty and len(data) >= window:
                returns = np.log(data['close'] / data['close'].shift(1))
                volatility = returns.rolling(window=window).std().iloc[-1]
                return float(volatility * np.sqrt(252)) if not pd.isna(volatility) else 1.0
            return 1.0
        except Exception as e:
            self.logger.error(f"Error calculating volatility: {e}")
            return 1.0

    def update_stats(self, trade_result: Dict[str, Any]) -> None:
        """
        Обновление статистики торговли

        Args:
            trade_result: Результат сделки
        """
        try:
            profit = trade_result.get('pnl', 0)

            self.stats['total_trades'] += 1
            self.stats['last_trade_time'] = datetime.now()

            if profit > 0:
                self.stats['winning_trades'] += 1
                self.stats['total_profit'] += profit
                self.stats['consecutive_wins'] += 1
                self.stats['consecutive_losses'] = 0
                self.stats['max_consecutive_wins'] = max(
                    self.stats['max_consecutive_wins'],
                    self.stats['consecutive_wins']
                )
                self.stats['max_profit'] = max(self.stats['max_profit'], profit)
            else:
                self.stats['losing_trades'] += 1
                self.stats['total_loss'] += abs(profit)
                self.stats['consecutive_losses'] += 1
                self.stats['consecutive_wins'] = 0
                self.stats['max_consecutive_losses'] = max(
                    self.stats['max_consecutive_losses'],
                    self.stats['consecutive_losses']
                )

            # Обновление производных метрик
            if self.stats['total_trades'] > 0:
                self.stats['win_rate'] = (self.stats['winning_trades'] / self.stats['total_trades']) * 100

            if self.stats['winning_trades'] > 0:
                self.stats['avg_win'] = self.stats['total_profit'] / self.stats['winning_trades']

            if self.stats['losing_trades'] > 0:
                self.stats['avg_loss'] = self.stats['total_loss'] / self.stats['losing_trades']

            if self.stats['total_loss'] > 0:
                self.stats['profit_factor'] = self.stats['total_profit'] / self.stats['total_loss']

            self.logger.info(f"Stats updated: {self.stats['total_trades']} trades, "
                             f"{self.stats['win_rate']:.1f}% win rate")

        except Exception as e:
            self.logger.error(f"Error updating stats: {e}")

    def get_performance_summary(self) -> Dict[str, Any]:
        """Получение сводки производительности стратегии"""
        try:
            runtime = datetime.now() - self.stats['strategy_start_time']

            return {
                'strategy_name': self.name,
                'runtime': str(runtime),
                'is_active': self.is_active,
                'total_trades': self.stats['total_trades'],
                'win_rate': round(self.stats['win_rate'], 2),
                'profit_factor': round(self.stats['profit_factor'], 2),
                'net_profit': round(self.stats['total_profit'] - self.stats['total_loss'], 2),
                'max_consecutive_wins': self.stats['max_consecutive_wins'],
                'max_consecutive_losses': self.stats['max_consecutive_losses'],
                'last_trade': self.stats['last_trade_time'].isoformat() if self.stats['last_trade_time'] else None
            }
        except Exception as e:
            self.logger.error(f"Error getting performance summary: {e}")
            return {'error': str(e)}

    def reset_stats(self) -> None:
        """Сброс статистики стратегии"""
        self.stats = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_profit': 0.0,
            'total_loss': 0.0,
            'max_drawdown': 0.0,
            'max_profit': 0.0,
            'win_rate': 0.0,
            'profit_factor': 0.0,
            'avg_win': 0.0,
            'avg_loss': 0.0,
            'consecutive_wins': 0,
            'consecutive_losses': 0,
            'max_consecutive_wins': 0,
            'max_consecutive_losses': 0,
            'last_trade_time': None,
            'strategy_start_time': datetime.now()
        }
        self.logger.info("Strategy statistics reset")

    def activate(self) -> None:
        """Активация стратегии"""
        self.is_active = True
        self.logger.info(f"Strategy {self.name} activated")

    def deactivate(self) -> None:
        """Деактивация стратегии"""
        self.is_active = False
        self.logger.info(f"Strategy {self.name} deactivated")

    @abstractmethod
    def execute(self, symbol: str, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Выполнение стратегии

        Args:
            symbol: Торговая пара
            market_data: Словарь с рыночными данными

        Returns:
            Dict с результатом выполнения или None
        """
        pass

    def __str__(self) -> str:
        """Строковое представление стратегии"""
        return f"Strategy({self.name}, trades={self.stats['total_trades']}, " \
               f"win_rate={self.stats['win_rate']:.1f}%, active={self.is_active})"

    def __repr__(self) -> str:
        """Представление для отладки"""
        return self.__str__()