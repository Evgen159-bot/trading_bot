import logging
import os
from datetime import datetime
import asyncio
from typing import Optional, Dict, Any
import aiohttp
from config.trading_config import TradingConfig

# Проверка дневника трейдинга python utils/diary_viewer.py


class TelegramNotifier:
    """Класс для отправки уведомлений в Telegram"""

    def __init__(self, token: str, chat_id: str, log_dir: str = "logs/telegram"):
        """
        Инициализация уведомляющего бота Telegram

        Args:
            token: Токен Telegram бота
            chat_id: ID чата для отправки сообщений
            log_dir: Директория для логов
        """
        self.token = token
        self.chat_id = chat_id
        self.log_dir = log_dir
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.logger = logging.getLogger(__name__)
        os.makedirs(self.log_dir, exist_ok=True)

    async def send_message(self, message: str, parse_mode: str = 'HTML') -> bool:
        """
        Асинхронная отправка сообщения в Telegram

        Args:
            message: Текст сообщения
            parse_mode: Режим форматирования (HTML/Markdown)

        Returns:
            bool: Успешность отправки
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/sendMessage"
                payload = {
                    'chat_id': self.chat_id,
                    'text': message,
                    'parse_mode': parse_mode
                }

                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        self.logger.info("Message sent successfully")
                        return True
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Failed to send message: {error_text}")
                        await self._log_error("send_message", error_text, message)
                        return False

        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            await self._log_error("send_message", str(e), message)
            return False

    async def send_trade_notification(self, trade_data: Dict[str, Any]) -> bool:
        """
        Отправка уведомления о торговой операции

        Args:
            trade_data: Данные о сделке

        Returns:
            bool: Успешность отправки
        """
        try:
            message = self._format_trade_message(trade_data)
            return await self.send_message(message)
        except Exception as e:
            self.logger.error(f"Error sending trade notification: {e}")
            await self._log_error("trade_notification", str(e), str(trade_data))
            return False

    async def send_error_notification(self,
                                      error: Exception,
                                      additional_info: Optional[Dict] = None) -> bool:
        """
        Отправка уведомления об ошибке

        Args:
            error: Объект исключения
            additional_info: Дополнительная информация

        Returns:
            bool: Успешность отправки
        """
        try:
            message = self._format_error_message(error, additional_info)
            return await self.send_message(message, parse_mode='Markdown')
        except Exception as e:
            self.logger.error(f"Error sending error notification: {e}")
            await self._log_error("error_notification", str(e), str(error))
            return False

    async def send_strategy_notification(self,
                                         strategy_data: Dict[str, Any]) -> bool:
        """
        Отправка уведомления о сигнале стратегии

        Args:
            strategy_data: Данные стратегии

        Returns:
            bool: Успешность отправки
        """
        try:
            message = self._format_strategy_message(strategy_data)
            return await self.send_message(message)
        except Exception as e:
            self.logger.error(f"Error sending strategy notification: {e}")
            await self._log_error("strategy_notification", str(e), str(strategy_data))
            return False

    def _format_trade_message(self, trade_data: Dict[str, Any]) -> str:
        """Форматирование сообщения о торговой операции"""
        message = (
            f"🔔 <b>Торговая операция</b>\n\n"
            f"📊 Символ: {trade_data.get('symbol', 'N/A')}\n"
            f"📈 Тип: {trade_data.get('type', 'N/A')}\n"
            f"💰 Цена входа: {trade_data.get('entry_price', 'N/A')}\n"
            f"📉 Размер позиции: {trade_data.get('size', 'N/A')}\n"
        )

        if 'take_profit' in trade_data:
            message += f"🎯 Take Profit: {trade_data['take_profit']}\n"
        if 'stop_loss' in trade_data:
            message += f"🛑 Stop Loss: {trade_data['stop_loss']}\n"
        if 'pnl' in trade_data:
            message += f"💵 P&L: {trade_data['pnl']}\n"

        return message

    def _format_error_message(self,
                              error: Exception,
                              additional_info: Optional[Dict] = None) -> str:
        """Форматирование сообщения об ошибке"""
        message = (
            f"⚠️ *Ошибка*\n\n"
            f"Тип: `{type(error).__name__}`\n"
            f"Сообщение: `{str(error)}`\n"
        )

        if additional_info:
            message += "\n*Дополнительная информация:*\n"
            for key, value in additional_info.items():
                message += f"`{key}`: {value}\n"

        return message

    def _format_strategy_message(self, strategy_data: Dict[str, Any]) -> str:
        """Форматирование сообщения о сигнале стратегии"""
        message = (
            f"🤖 <b>Сигнал стратегии</b>\n\n"
            f"📊 Символ: {strategy_data.get('symbol', 'N/A')}\n"
            f"📈 Сигнал: {strategy_data.get('signal', 'N/A')}\n"
            f"💪 Сила сигнала: {strategy_data.get('strength', 'N/A')}\n"
        )

        if 'indicators' in strategy_data:
            message += "\n📊 <b>Индикаторы:</b>\n"
            for indicator, value in strategy_data['indicators'].items():
                message += f"{indicator}: {value}\n"

        return message

    async def _log_error(self,
                         error_type: str,
                         error_message: str,
                         additional_data: str) -> None:
        """
        Логирование ошибки в файл

        Args:
            error_type: Тип ошибки
            error_message: Сообщение об ошибке
            additional_data: Дополнительные данные
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(self.log_dir, f"telegram_error_{timestamp}.log")

        try:
            with open(log_file, "w", encoding='utf-8') as f:
                f.write(
                    f"Timestamp: {timestamp}\n"
                    f"Error Type: {error_type}\n"
                    f"Error Message: {error_message}\n"
                    f"Additional Data: {additional_data}\n"
                )
            self.logger.info(f"Error logged to {log_file}")
        except Exception as e:
            self.logger.error(f"Error writing to log file: {e}")


# Пример использования:
"""
async def main():
    notifier = TelegramNotifier(
        token=TradingConfig.TELEGRAM_TOKEN,
        chat_id=TradingConfig.TELEGRAM_CHAT_ID
    )

    # Отправка уведомления о сделке
    await notifier.send_trade_notification({
        'symbol': 'ETHUSDT',
        'type': 'LONG',
        'entry_price': 2000,
        'size': 0.1,
        'take_profit': 2100,
        'stop_loss': 1950
    })

    # Отправка уведомления об ошибке
    try:
        raise ValueError("Test error")
    except Exception as e:
        await notifier.send_error_notification(e, {'additional': 'info'})

if __name__ == "__main__":
    asyncio.run(main())
"""