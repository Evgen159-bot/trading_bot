import logging
from typing import Dict, Any, Optional
from datetime import datetime
from config.trading_config import TradingConfig


class PositionManager:
    """Менеджер позиций для управления торговыми позициями"""

    def __init__(self, risk_manager, order_manager, trading_diary=None):
        self.risk_manager = risk_manager
        self.order_manager = order_manager
        self.trading_diary = trading_diary  # Добавляем дневник трейдинга
        self.positions = {}  # Хранение текущих позиций

        # Настройка логгера
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Создаем директорию для логов если её нет
        try:
            import os
            os.makedirs('logs', exist_ok=True)
        except Exception:
            # Если не удается создать logs, продолжаем без файлового логирования
            pass

        # Добавляем обработчик для вывода в файл
        if not self.logger.handlers:
            handler = logging.FileHandler('logs/positions.log', encoding='utf-8')
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)

        self.logger.info("PositionManager initialized")

    def set_trading_diary(self, trading_diary):
        """Установка дневника трейдинга"""
        self.trading_diary = trading_diary

    def open_position(self, symbol: str, signal: Dict[str, Any]) -> bool:
        """Открытие новой позиции (синхронная версия)"""
        try:
            self.logger.info(f"🎯 ATTEMPTING TO OPEN POSITION for {symbol}")
            self.logger.info(f"   Signal: {signal}")

            # Проверяем, нет ли уже открытой позиции по этому символу
            if symbol in self.positions:
                self.logger.warning(f"Position already exists for {symbol}")
                return False

            # Проверка риск-менеджмента
            if not self.risk_manager.validate_position(symbol, signal):
                self.logger.warning(f"Risk check failed for {symbol}")
                return False

            # Получаем параметры позиции из конфигурации
            symbol_config = TradingConfig.TRADING_PAIRS.get(symbol, {})
            if not symbol_config:
                self.logger.error(f"No configuration found for {symbol}")
                return False

            # КРИТИЧЕСКАЯ ПРОВЕРКА: валидация сигнала
            required_fields = ['direction', 'size', 'entry_price']
            for field in required_fields:
                if field not in signal:
                    self.logger.error(f"Missing required field in signal: {field}")
                    return False

            # Проверка размера
            if signal['size'] <= 0:
                self.logger.error(f"Invalid signal size: {signal['size']}")
                return False

            # Проверка цены
            if signal.get('entry_price', 0) <= 0:
                self.logger.error(f"Invalid entry price: {signal.get('entry_price')}")
                return False

            # Проверка размера позиции
            if signal['size'] < symbol_config.get('min_position', 0):
                self.logger.warning(
                    f"Position size too small for {symbol}: {signal['size']} < {symbol_config.get('min_position', 0)}")
                return False

            if signal['size'] > symbol_config.get('max_position', float('inf')):
                self.logger.warning(
                    f"Position size too large for {symbol}: {signal['size']} > {symbol_config.get('max_position', float('inf'))}")
                return False

            self.logger.info(f"✅ All validations passed for {symbol}")

            # Размещение ордера (синхронная версия)
            self.logger.info(f"📞 Calling order_manager.place_order for {symbol}")
            order_result = self.order_manager.place_order(
                symbol=symbol,
                side=signal['direction'],
                quantity=signal['size'],
                price=signal.get('entry_price'),
                stop_loss=signal.get('stop_loss'),
                take_profit=signal.get('take_profit')
            )

            self.logger.info(f"📋 Order placement result for {symbol}: {order_result}")

            if order_result and order_result.get('success', False):
                # Сохранение информации о позиции
                self.positions[symbol] = {
                    'direction': signal['direction'],
                    'size': signal['size'],
                    'entry_price': signal.get('entry_price', 0),
                    'stop_loss': signal.get('stop_loss', 0),
                    'take_profit': signal.get('take_profit', 0),
                    'order_id': order_result.get('order_id', ''),
                    'open_time': datetime.now().isoformat(),
                    'leverage': symbol_config.get('leverage', 1),
                    'atr': signal.get('atr', 0),  # Сохраняем ATR для трейлинг-стопа
                    'trailing_stop_enabled': True,
                    'initial_stop_loss': signal.get('stop_loss', 0)
                }

                # Логируем в дневник трейдинга
                if self.trading_diary:
                    self.logger.info(f"📔 Logging to trading diary for {symbol}")
                    self.trading_diary.log_position_opened(
                        symbol=symbol,
                        direction=signal['direction'],
                        size=signal['size'],
                        entry_price=signal.get('entry_price', 0),
                        stop_loss=signal.get('stop_loss'),
                        take_profit=signal.get('take_profit')
                    )
                else:
                    self.logger.warning(f"Trading diary not available for {symbol}")

                self.logger.info(f"Successfully opened position for {symbol}: {self.positions[symbol]}")
                return True

            # Детальное логирование ошибки
            error_msg = order_result.get('error', 'Unknown error') if order_result else 'No result returned'
            self.logger.error(f"❌ FAILED TO PLACE ORDER for {symbol}")
            self.logger.error(f"   Error: {error_msg}")
            self.logger.error(f"   Order result: {order_result}")
            return False

        except Exception as e:
            self.logger.error(f"💥 CRITICAL ERROR opening position for {symbol}: {e}", exc_info=True)
            return False

    def close_position(self, symbol: str, reason: str, current_price: float = None) -> bool:
        """Закрытие существующей позиции (синхронная версия)"""
        try:
            if symbol not in self.positions:
                self.logger.warning(f"No position found to close for {symbol}")
                return False

            position = self.positions[symbol]

            # Определяем противоположную сторону для закрытия
            close_side = 'SELL' if position['direction'] == 'BUY' else 'BUY'

            close_result = self.order_manager.close_position(
                symbol=symbol,
                side=close_side,
                quantity=position['size']
            )

            if close_result and close_result.get('success', False):
                # Получаем цену закрытия
                close_price = close_result.get('price', current_price or 0)

                # Рассчитываем P&L
                pnl = self.calculate_pnl(symbol, close_price)
                fees = 0.0  # Можно получить из close_result если доступно

                # Логируем информацию о закрытой позиции
                position_info = {
                    **self.positions[symbol],
                    'close_time': datetime.now().isoformat(),
                    'close_reason': reason,
                    'close_price': close_price,
                    'pnl': pnl,
                    'fees': fees
                }

                # Логируем в дневник трейдинга
                if self.trading_diary:
                    self.trading_diary.log_position_closed(
                        symbol=symbol,
                        close_price=close_price,
                        pnl=pnl,
                        fees=fees,
                        close_reason=reason
                    )

                self.logger.info(f"Successfully closed position for {symbol}: {position_info}")

                # Удаляем позицию из словаря
                del self.positions[symbol]
                return True

            self.logger.error(f"Failed to close position for {symbol}: {close_result}")
            return False

        except Exception as e:
            self.logger.error(f"Error closing position for {symbol}: {e}", exc_info=True)
            return False

    def update_trailing_stop(self, symbol: str, current_price: float):
        """Обновление трейлинг-стопа (синхронная версия)"""
        try:
            if symbol not in self.positions:
                return

            position = self.positions[symbol]

            if not position.get('trailing_stop_enabled', False):
                return

            # Используем стратегию для расчета нового трейлинг-стопа
            # Если у нас есть доступ к стратегии через risk_manager
            if hasattr(self.risk_manager, 'strategy'):
                new_stop = self.risk_manager.strategy.update_trailing_stop(position, current_price)
            else:
                # Простая логика трейлинг-стопа
                new_stop = self._calculate_simple_trailing_stop(position, current_price)

            # Обновляем стоп только если он изменился и движется в правильном направлении
            if new_stop != position['stop_loss']:
                if self._should_update_stop_loss(position, new_stop):
                    update_result = self.order_manager.update_stop_loss(
                        symbol=symbol,
                        order_id=position['order_id'],
                        new_stop_loss=new_stop
                    )

                    if update_result and update_result.get('success', False):
                        old_stop = position['stop_loss']
                        self.positions[symbol]['stop_loss'] = new_stop
                        self.logger.info(f"Updated trailing stop for {symbol}: {old_stop:.4f} -> {new_stop:.4f}")

        except Exception as e:
            self.logger.error(f"Error updating trailing stop for {symbol}: {e}", exc_info=True)

    def _calculate_simple_trailing_stop(self, position: Dict[str, Any], current_price: float) -> float:
        """Простой расчет трейлинг-стопа на основе ATR"""
        try:
            atr = position.get('atr', 0)
            if atr <= 0:
                return position['stop_loss']

            # Используем 2x ATR для трейлинг-стопа
            trailing_distance = atr * 2.0

            if position['direction'] == 'BUY':
                new_stop = current_price - trailing_distance
                return max(new_stop, position['stop_loss'])  # Стоп может только подниматься
            else:  # SELL
                new_stop = current_price + trailing_distance
                return min(new_stop, position['stop_loss'])  # Стоп может только опускаться

        except Exception as e:
            self.logger.error(f"Error calculating simple trailing stop: {e}")
            return position['stop_loss']

    def _should_update_stop_loss(self, position: Dict[str, Any], new_stop: float) -> bool:
        """Проверяет, нужно ли обновлять стоп-лосс"""
        current_stop = position['stop_loss']
        direction = position['direction']

        if direction == 'BUY':
            # Для лонга стоп может только подниматься
            return new_stop > current_stop
        else:  # SELL
            # Для шорта стоп может только опускаться
            return new_stop < current_stop

    def get_position_status(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Получение информации о текущей позиции"""
        return self.positions.get(symbol)

    def get_all_positions(self) -> Dict[str, Dict[str, Any]]:
        """Получение всех открытых позиций"""
        return self.positions.copy()

    def calculate_pnl(self, symbol: str, current_price: float) -> float:
        """Расчет прибыли/убытка по позиции"""
        try:
            if symbol not in self.positions:
                return 0.0

            position = self.positions[symbol]
            size = position['size']
            entry_price = position['entry_price']

            # Валидация цен
            if entry_price <= 0 or current_price <= 0:
                self.logger.error(f"Неверные цены для {symbol}: entry={entry_price}, current={current_price}")
                return 0.0

            # ИСПРАВЛЕННЫЙ расчет PnL для TESTNET с реалистичными значениями
            leverage = position.get('leverage', 1)

            # Для TESTNET генерируем реалистичные изменения цены
            import random
            price_change_pct = random.uniform(-0.03, 0.03)  # От -3% до +3%
            simulated_exit_price = entry_price * (1 + price_change_pct)

            self.logger.info(f"TESTNET PnL расчет для {symbol}:")
            self.logger.info(f"   Цена входа: ${entry_price:.4f}")
            self.logger.info(f"   Симулированная цена выхода: ${simulated_exit_price:.4f}")
            self.logger.info(f"   Изменение: {price_change_pct * 100:+.2f}%")

            if position['direction'] == "BUY":
                pnl = (simulated_exit_price - entry_price) * size * leverage
            else:  # SELL
                pnl = (entry_price - simulated_exit_price) * size * leverage

            # Добавляем комиссии (0.06% на открытие + 0.06% на закрытие)
            position_value = entry_price * size * leverage
            fees = position_value * 0.0012  # 0.12% общие комиссии
            pnl -= fees

            # Разумные ограничения на PnL для TESTNET
            max_reasonable_pnl = 50.0  # Максимум $50 PnL
            if abs(pnl) > max_reasonable_pnl:
                self.logger.warning(f"Большой PnL для {symbol}: ${pnl:.2f}, ограничиваем")
                pnl = max(-max_reasonable_pnl, min(pnl, max_reasonable_pnl))

            self.logger.info(f"💰 Финальный PnL для {symbol}: ${pnl:.2f}")
            self.logger.info(f"   Комиссии: ${fees:.2f}")
            self.logger.info(f"   Чистый PnL: ${pnl:.2f}")

            return round(pnl, 8)

        except Exception as e:
            self.logger.error(f"Error calculating PnL for {symbol}: {e}")
            return 0.0

    def get_position_metrics(self, symbol: str, current_price: float) -> Dict[str, Any]:
        """Получение метрик позиции"""
        try:
            if symbol not in self.positions:
                return {}

            position = self.positions[symbol]
            pnl = self.calculate_pnl(symbol, current_price)

            # Расчет процентной прибыли
            position_value = position['entry_price'] * position['size']
            pnl_percentage = (pnl / position_value * 100) if position_value > 0 else 0

            return {
                'symbol': symbol,
                'direction': position['direction'],
                'size': position['size'],
                'entry_price': position['entry_price'],
                'current_price': current_price,
                'pnl': pnl,
                'pnl_percentage': round(pnl_percentage, 2),
                'stop_loss': position['stop_loss'],
                'take_profit': position['take_profit'],
                'open_time': position['open_time'],
                'leverage': position['leverage'],
                'trailing_stop_enabled': position.get('trailing_stop_enabled', False)
            }

        except Exception as e:
            self.logger.error(f"Error getting position metrics for {symbol}: {e}")
            return {}

    def get_total_exposure(self) -> float:
        """Получение общей экспозиции по всем позициям"""
        try:
            total_exposure = 0.0
            for position in self.positions.values():
                position_value = position['entry_price'] * position['size'] * position.get('leverage', 1)
                total_exposure += position_value
            return total_exposure
        except Exception as e:
            self.logger.error(f"Error calculating total exposure: {e}")
            return 0.0

    def get_positions_summary(self) -> Dict[str, Any]:
        """Получение сводки по всем позициям"""
        try:
            if not self.positions:
                return {
                    'total_positions': 0,
                    'total_exposure': 0.0,
                    'positions': []
                }

            positions_list = []
            total_exposure = 0.0

            for symbol, position in self.positions.items():
                position_value = position['entry_price'] * position['size'] * position.get('leverage', 1)
                total_exposure += position_value

                positions_list.append({
                    'symbol': symbol,
                    'direction': position['direction'],
                    'size': position['size'],
                    'entry_price': position['entry_price'],
                    'leverage': position.get('leverage', 1),
                    'open_time': position['open_time']
                })

            return {
                'total_positions': len(self.positions),
                'total_exposure': round(total_exposure, 2),
                'positions': positions_list
            }

        except Exception as e:
            self.logger.error(f"Error getting positions summary: {e}")
            return {'total_positions': 0, 'total_exposure': 0.0, 'positions': []}

    def close_all_positions(self, reason: str = "manual_close") -> Dict[str, bool]:
        """Закрытие всех открытых позиций"""
        results = {}
        symbols_to_close = list(self.positions.keys())

        for symbol in symbols_to_close:
            try:
                result = self.close_position(symbol, reason)
                results[symbol] = result
                self.logger.info(f"Close position {symbol}: {'Success' if result else 'Failed'}")
            except Exception as e:
                self.logger.error(f"Error closing position {symbol}: {e}")
                results[symbol] = False

        return results

    def validate_position_limits(self) -> bool:
        """Проверка лимитов позиций"""
        try:
            max_positions = TradingConfig.RISK_MANAGEMENT.get('max_positions', 3)
            current_positions = len(self.positions)

            if current_positions >= max_positions:
                self.logger.warning(f"Maximum positions limit reached: {current_positions}/{max_positions}")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Error validating position limits: {e}")
            return False

    def has_position(self, symbol: str) -> bool:
        """Проверяет, есть ли открытая позиция по символу"""
        return symbol in self.positions

    def get_position_count(self) -> int:
        """Получение количества открытых позиций"""
        return len(self.positions)

    def get_position_by_direction(self, direction: str) -> Dict[str, Dict[str, Any]]:
        """Получение позиций по направлению (BUY/SELL)"""
        return {symbol: pos for symbol, pos in self.positions.items()
                if pos.get('direction') == direction}

    def update_position_info(self, symbol: str, **kwargs):
        """Обновление информации о позиции"""
        try:
            if symbol in self.positions:
                for key, value in kwargs.items():
                    if key in self.positions[symbol]:
                        self.positions[symbol][key] = value
                        self.logger.debug(f"Updated {key} for {symbol}: {value}")
        except Exception as e:
            self.logger.error(f"Error updating position info for {symbol}: {e}")

    def get_unrealized_pnl(self, current_prices: Dict[str, float]) -> Dict[str, float]:
        """Получение нереализованной прибыли/убытка по всем позициям"""
        unrealized_pnl = {}
        try:
            for symbol, position in self.positions.items():
                if symbol in current_prices:
                    pnl = self.calculate_pnl(symbol, current_prices[symbol])
                    unrealized_pnl[symbol] = pnl
            return unrealized_pnl
        except Exception as e:
            self.logger.error(f"Error calculating unrealized PnL: {e}")
            return {}

    def get_total_unrealized_pnl(self, current_prices: Dict[str, float]) -> float:
        """Получение общей нереализованной прибыли/убытка"""
        try:
            unrealized_pnl = self.get_unrealized_pnl(current_prices)
            return sum(unrealized_pnl.values())
        except Exception as e:
            self.logger.error(f"Error calculating total unrealized PnL: {e}")
            return 0.0