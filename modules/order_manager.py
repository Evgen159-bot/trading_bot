import logging
from typing import Dict, Any, Optional
from datetime import datetime
from config.trading_config import TradingConfig
from pybit.unified_trading import HTTP
import time


class OrderManager:
    """Менеджер ордеров для управления торговыми операциями"""

    def __init__(self, client: HTTP):
        """Инициализация менеджера ордеров"""
        self.client = client
        self.logger = logging.getLogger(__name__)
        self.open_orders = {}  # Исправлено: правильная инициализация словаря
        self.order_history = []  # История ордеров
        self.rate_limit_delay = 1.0  # Задержка между запросами
        self.last_request_time = 0

        # Настройка логирования
        self.logger.setLevel(logging.INFO)

        # Создаем директорию для логов если её нет
        try:
            import os
            os.makedirs('logs', exist_ok=True)
        except Exception:
            # Если не удается создать logs, продолжаем без файлового логирования
            pass

        # Добавляем обработчик для файла если его нет
        if not self.logger.handlers:
            handler = logging.FileHandler('logs/orders.log', encoding='utf-8')
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)

        self.logger.info("OrderManager initialized successfully")

    def _rate_limit_check(self):
        """Проверка rate limit - добавляем задержку между запросами"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def place_order(self, symbol: str, side: str, quantity: float,
                    price: float = None, stop_loss: float = None,
                    take_profit: float = None) -> Optional[Dict[str, Any]]:
        """Размещение нового ордера (синхронная версия)"""
        try:
            self._rate_limit_check()

            # Получаем конфигурацию символа
            symbol_config = TradingConfig.TRADING_PAIRS.get(symbol, {})
            if not symbol_config:
                self.logger.error(f"No configuration found for {symbol}")
                return None

            # Валидация параметров
            if quantity <= 0:
                self.logger.error(f"Invalid quantity: {quantity}")
                return None

            # Округляем количество согласно lot_size
            lot_size = symbol_config.get('lot_size', 0.001)
            quantity = round(quantity / lot_size) * lot_size

            # Определяем тип ордера
            order_type = "Market" if price is None else "Limit"

            # Подготавливаем параметры ордера
            order_params = {
                "category": "linear",
                "symbol": symbol,
                "side": side,
                "orderType": order_type,
                "qty": str(quantity),
                "timeInForce": "GTC" if order_type == "Limit" else "IOC",
                "reduceOnly": False,
                "closeOnTrigger": False
            }

            # Добавляем цену для лимитного ордера
            if price is not None:
                tick_size = symbol_config.get('tick_size', 0.01)
                price = round(price / tick_size) * tick_size
                order_params["price"] = str(price)

            # Добавляем стоп-лосс и тейк-профит если указаны
            if stop_loss is not None:
                order_params["stopLoss"] = str(stop_loss)
            if take_profit is not None:
                order_params["takeProfit"] = str(take_profit)

            self.logger.info(f"Placing order for {symbol}: {side} {quantity} @ {price}")

            # Размещение основного ордера
            response = self.client.place_order(**order_params)

            if response.get('retCode') == 0 and response.get('result'):
                order_id = response['result']['orderId']

                # Сохраняем информацию об ордере
                order_info = {
                    'order_id': order_id,
                    'symbol': symbol,
                    'side': side,
                    'quantity': quantity,
                    'price': price,
                    'order_type': order_type,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'status': 'NEW',
                    'timestamp': datetime.now().isoformat()
                }

                self.open_orders[order_id] = order_info
                self.order_history.append(order_info.copy())

                self.logger.info(f"Order placed successfully: {order_id}")

                return {
                    'success': True,
                    'order_id': order_id,
                    'symbol': symbol,
                    'side': side,
                    'quantity': quantity,
                    'price': price
                }
            else:
                error_msg = response.get('retMsg', 'Unknown error')
                self.logger.error(f"Failed to place order for {symbol}: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }

        except Exception as e:
            self.logger.error(f"Error placing order for {symbol}: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }

    def close_position(self, symbol: str, side: str, quantity: float) -> Optional[Dict[str, Any]]:
        """Закрытие позиции (синхронная версия)"""
        try:
            self._rate_limit_check()

            # Размещаем рыночный ордер для закрытия позиции
            response = self.client.place_order(
                category="linear",
                symbol=symbol,
                side=side,
                orderType="Market",
                qty=str(quantity),
                timeInForce="IOC",
                reduceOnly=True,
                closeOnTrigger=False
            )

            if response.get('retCode') == 0 and response.get('result'):
                order_id = response['result']['orderId']

                self.logger.info(f"Position close order placed for {symbol}: {order_id}")

                return {
                    'success': True,
                    'order_id': order_id,
                    'symbol': symbol,
                    'side': side,
                    'quantity': quantity
                }
            else:
                error_msg = response.get('retMsg', 'Unknown error')
                self.logger.error(f"Failed to close position for {symbol}: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }

        except Exception as e:
            self.logger.error(f"Error closing position for {symbol}: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }

    def update_stop_loss(self, symbol: str, order_id: str, new_stop_loss: float) -> Optional[Dict[str, Any]]:
        """Обновление стоп-лосса (синхронная версия)"""
        try:
            self._rate_limit_check()

            # Получаем конфигурацию символа для округления
            symbol_config = TradingConfig.TRADING_PAIRS.get(symbol, {})
            tick_size = symbol_config.get('tick_size', 0.01)
            new_stop_loss = round(new_stop_loss / tick_size) * tick_size

            response = self.client.amend_order(
                category="linear",
                symbol=symbol,
                orderId=order_id,
                stopLoss=str(new_stop_loss)
            )

            if response.get('retCode') == 0:
                # Обновляем локальную информацию
                if order_id in self.open_orders:
                    self.open_orders[order_id]['stop_loss'] = new_stop_loss

                self.logger.info(f"Stop loss updated for {symbol}: {new_stop_loss}")

                return {
                    'success': True,
                    'order_id': order_id,
                    'new_stop_loss': new_stop_loss
                }
            else:
                error_msg = response.get('retMsg', 'Unknown error')
                self.logger.error(f"Failed to update stop loss for {symbol}: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }

        except Exception as e:
            self.logger.error(f"Error updating stop loss for {symbol}: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }

    def cancel_order(self, symbol: str, order_id: str) -> bool:
        """Отмена ордера"""
        try:
            self._rate_limit_check()

            response = self.client.cancel_order(
                category="linear",
                symbol=symbol,
                orderId=order_id
            )

            if response.get('retCode') == 0:
                # Удаляем из открытых ордеров
                if order_id in self.open_orders:
                    self.open_orders[order_id]['status'] = 'CANCELLED'
                    del self.open_orders[order_id]

                self.logger.info(f"Order cancelled successfully: {order_id}")
                return True
            else:
                error_msg = response.get('retMsg', 'Unknown error')
                self.logger.error(f"Failed to cancel order {order_id}: {error_msg}")
                return False

        except Exception as e:
            self.logger.error(f"Error cancelling order {order_id}: {e}", exc_info=True)
            return False

    def get_order_status(self, symbol: str, order_id: str) -> Optional[Dict[str, Any]]:
        """Получение статуса ордера"""
        try:
            self._rate_limit_check()

            response = self.client.get_open_orders(
                category="linear",
                symbol=symbol,
                orderId=order_id
            )

            if response.get('retCode') == 0 and response.get('result', {}).get('list'):
                order_data = response['result']['list'][0]
                return {
                    'order_id': order_data.get('orderId'),
                    'symbol': order_data.get('symbol'),
                    'side': order_data.get('side'),
                    'quantity': float(order_data.get('qty', 0)),
                    'price': float(order_data.get('price', 0)),
                    'status': order_data.get('orderStatus'),
                    'filled_qty': float(order_data.get('cumExecQty', 0)),
                    'avg_price': float(order_data.get('avgPrice', 0))
                }
            else:
                # Ордер может быть исполнен или отменен
                return None

        except Exception as e:
            self.logger.error(f"Error getting order status for {order_id}: {e}")
            return None

    def get_open_orders(self, symbol: str = None) -> Dict[str, Dict[str, Any]]:
        """Получение всех открытых ордеров"""
        if symbol:
            return {k: v for k, v in self.open_orders.items() if v['symbol'] == symbol}
        return self.open_orders.copy()

    def update_orders_status(self):
        """Обновление статуса всех открытых ордеров"""
        try:
            orders_to_remove = []

            for order_id, order_info in self.open_orders.items():
                try:
                    status = self.get_order_status(order_info['symbol'], order_id)

                    if status is None:
                        # Ордер не найден - возможно исполнен или отменен
                        orders_to_remove.append(order_id)
                    else:
                        # Обновляем статус
                        self.open_orders[order_id]['status'] = status['status']

                        # Если ордер исполнен или отменен, удаляем из открытых
                        if status['status'] in ['Filled', 'Cancelled', 'Rejected']:
                            orders_to_remove.append(order_id)

                except Exception as e:
                    self.logger.error(f"Error updating status for order {order_id}: {e}")

            # Удаляем исполненные/отмененные ордера
            for order_id in orders_to_remove:
                if order_id in self.open_orders:
                    self.logger.info(f"Removing completed order: {order_id}")
                    del self.open_orders[order_id]

        except Exception as e:
            self.logger.error(f"Error updating orders status: {e}")

    def cancel_all_orders(self, symbol: str = None) -> Dict[str, bool]:
        """Отмена всех открытых ордеров"""
        results = {}
        orders_to_cancel = list(self.open_orders.keys())

        if symbol:
            orders_to_cancel = [
                order_id for order_id, order_info in self.open_orders.items()
                if order_info['symbol'] == symbol
            ]

        for order_id in orders_to_cancel:
            try:
                order_info = self.open_orders[order_id]
                result = self.cancel_order(order_info['symbol'], order_id)
                results[order_id] = result

                if result:
                    self.logger.info(f"Cancelled order {order_id}")
                else:
                    self.logger.warning(f"Failed to cancel order {order_id}")

            except Exception as e:
                self.logger.error(f"Error cancelling order {order_id}: {e}")
                results[order_id] = False

        return results

    def get_order_history(self, limit: int = 50) -> list:
        """Получение истории ордеров"""
        return self.order_history[-limit:] if self.order_history else []

    def get_orders_summary(self) -> Dict[str, Any]:
        """Получение сводки по ордерам"""
        try:
            total_orders = len(self.order_history)
            open_orders_count = len(self.open_orders)

            # Подсчет по статусам
            status_counts = {}
            for order in self.order_history:
                status = order.get('status', 'UNKNOWN')
                status_counts[status] = status_counts.get(status, 0) + 1

            return {
                'total_orders': total_orders,
                'open_orders': open_orders_count,
                'status_breakdown': status_counts,
                'last_order_time': self.order_history[-1]['timestamp'] if self.order_history else None
            }

        except Exception as e:
            self.logger.error(f"Error getting orders summary: {e}")
            return {}

    def health_check(self) -> bool:
        """Проверка работоспособности OrderManager"""
        try:
            # Простая проверка - получение информации о балансе
            self._rate_limit_check()
            response = self.client.get_wallet_balance(accountType="UNIFIED")

            if response.get('retCode') == 0:
                self.logger.info("OrderManager health check: OK")
                return True
            else:
                self.logger.warning("OrderManager health check: FAILED")
                return False

        except Exception as e:
            self.logger.error(f"OrderManager health check error: {e}")
            return False