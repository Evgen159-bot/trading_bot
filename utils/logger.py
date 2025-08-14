"""
Улучшенная система логирования для торгового бота
"""
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class TradingLogger:
    """Настройщик логирования для торгового бота"""

    @staticmethod
    def setup_logger(name: str, log_file: Optional[str] = None,
                     level: int = logging.INFO,
                     console_output: bool = True) -> logging.Logger:
        """
        Настройка логгера с файловым и консольным выводом

        Args:
            name: Имя логгера
            log_file: Путь к файлу лога (опционально)
            level: Уровень логирования
            console_output: Выводить ли в консоль

        Returns:
            Настроенный логгер
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Очищаем существующие обработчики
        logger.handlers.clear()

        # Форматтер
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Файловый обработчик
        if log_file:
            # Создаем директорию если её нет
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(level)
            logger.addHandler(file_handler)

        # Консольный обработчик
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(level)
            logger.addHandler(console_handler)

        return logger

    @staticmethod
    def setup_trading_loggers() -> Dict[str, logging.Logger]:
        """Настройка всех логгеров для торгового бота"""
        loggers = {}

        # Основной логгер бота
        loggers['main'] = TradingLogger.setup_logger(
            'trading_bot',
            f'logs/trading_{datetime.now().strftime("%Y%m%d")}.log'
        )

        # Логгер стратегий
        loggers['strategy'] = TradingLogger.setup_logger(
            'strategy',
            f'logs/strategies/strategy_{datetime.now().strftime("%Y%m%d")}.log',
            console_output=False
        )

        # Логгер сделок
        loggers['trades'] = TradingLogger.setup_logger(
            'trades',
            f'logs/trades/trades_{datetime.now().strftime("%Y%m%d")}.log',
            console_output=False
        )

        # Логгер валидации
        loggers['validation'] = TradingLogger.setup_logger(
            'validation',
            f'logs/validation/validation_{datetime.now().strftime("%Y%m%d")}.log',
            console_output=False
        )

        return loggers


class ColoredFormatter(logging.Formatter):
    """Цветной форматтер для консольного вывода"""

    # Цветовые коды ANSI
    COLORS = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[32m',  # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'  # Reset
    }

    def format(self, record):
        # Добавляем цвет к уровню логирования
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"

        return super().format(record)


def setup_colored_logging():
    """Настройка цветного логирования для консоли"""
    logger = logging.getLogger()

    # Удаляем существующие обработчики
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Создаем цветной обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    colored_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(colored_formatter)

    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

    return logger