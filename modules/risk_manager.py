import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from config.trading_config import TradingConfig

from trading_bot.modules import data_fetcher


class RiskManager:
    """Менеджер рисков для торгового бота"""

    def __init__(self):
        """Инициализация менеджера рисков"""
        self.logger = logging.getLogger(__name__)
        self.config = TradingConfig.RISK_MANAGEMENT

        # Инициализация метрик
        self.reset_daily_metrics()

        # Отслеживание позиций
        self.positions = {}
        self.max_drawdown = 0.0
        self.peak_balance = 0.0

        # Настройки экстренного стопа
        self.emergency_stop = False
        self.emergency_reason = ""

        self.logger.info("RiskManager initialized successfully")

    def reset_daily_metrics(self):
        """Сброс дневной статистики"""
        try:
            self.daily_loss = 0.0
            self.daily_profit = 0.0
            self.daily_trades = 0
            self.daily_winning_trades = 0
            self.daily_losing_trades = 0
            self.last_reset = datetime.now()

            self.logger.info("Daily metrics reset")

        except Exception as e:
            self.logger.error(f"Error resetting daily metrics: {e}")

    def validate_position(self, symbol: str, signal: Dict[str, Any]) -> bool:
        """Комплексная валидация позиции перед открытием"""
        try:
            # Проверка экстренного стопа
            if self.emergency_stop:
                self.logger.warning(f"Emergency stop active: {self.emergency_reason}")
                return False

            # НОВОЕ: Проверка волатильности рынка
            if not self.check_market_volatility(symbol, data_fetcher):
                self.logger.warning(f"Market too volatile for {symbol}")
                return False

            # Проверка времени торговли
            if not self.is_trading_hours():
                self.logger.info("Outside trading hours")
                return False

            # Проверка дневных лимитов
            if not self._check_daily_limits():
                return False

            # Проверка максимального количества позиций
            if not self._check_position_limits():
                return False

            # Проверка риск/прибыль соотношения
            if not self._check_risk_reward_ratio(signal):
                return False

            # Проверка размера позиции
            if not self._validate_position_size(symbol, signal):
                return False

            # Проверка корреляции с существующими позициями
            if not self._check_correlation(symbol, signal):
                return False

            # Проверка просадки
            if not self._check_drawdown_limits():
                return False

            self.logger.info(f"Position validation passed for {symbol}")
            return True

        except Exception as e:
            self.logger.error(f"Error validating position for {symbol}: {e}")
            return False

    def calculate_position_size(self, account_balance: float, entry_price: float,
                                stop_loss: float, symbol: str) -> float:
        """Расчет размера позиции на основе риска"""
        try:
            if account_balance <= 0 or entry_price <= 0:
                self.logger.warning("Invalid account balance or entry price")
                return 0.0

            # Базовый риск на сделку
            risk_amount = account_balance * self.config['risk_per_trade']

            # Расчет расстояния до стоп-лосса
            price_difference = abs(entry_price - stop_loss)
            if price_difference < 0.00000001:
                self.logger.warning(f"Stop-loss too close to entry price for {symbol}")
                return 0.0

            # Базовый размер позиции
            base_size = risk_amount / price_difference

            # Применение настроек символа
            symbol_config = TradingConfig.TRADING_PAIRS.get(symbol, {})
            min_position = symbol_config.get('min_position', 0.001)
            max_position = symbol_config.get('max_position', 10.0)

            # Ограничение размера позиции
            position_size = max(min_position, min(base_size, max_position))

            # Проверка максимальной стоимости позиции
            max_value = self.config['position_sizing'].get('max_position_value', 1000)
            position_value = position_size * entry_price

            if position_value > max_value:
                position_size = max_value / entry_price

            # Корректировка на основе текущих убытков
            position_size = self._adjust_size_for_drawdown(position_size)

            # Применение плеча
            leverage = symbol_config.get('leverage', 1)
            max_leverage = self.config.get('max_leverage', 5)
            effective_leverage = min(leverage, max_leverage)

            # Финальная корректировка
            final_size = round(position_size, 8)

            self.logger.info(
                f"Position size calculated for {symbol}: {final_size} "
                f"(risk: ${risk_amount:.2f}, leverage: {effective_leverage}x)"
            )

            return final_size

        except Exception as e:
            self.logger.error(f"Error calculating position size for {symbol}: {e}")
            return 0.0

    def update_position_metrics(self, symbol: str, pnl: float, is_closed: bool = False):
        """Обновление метрик позиции"""
        try:
            # Обновление дневной статистики
            if is_closed:
                self.daily_trades += 1
                if pnl > 0:
                    self.daily_profit += pnl
                    self.daily_winning_trades += 1
                else:
                    self.daily_loss += abs(pnl)
                    self.daily_losing_trades += 1

                self.logger.info(f"Position closed for {symbol}: PnL = ${pnl:.2f}")

            # Проверка экстренных условий
            self._check_emergency_conditions()

        except Exception as e:
            self.logger.error(f"Error updating position metrics: {e}")

    def calculate_trailing_stop(self, direction: str, current_price: float,
                                entry_price: float, current_stop: float,
                                atr: float = None) -> float:
        """Расчет трейлинг-стопа"""
        try:
            if atr is None:
                # Простой трейлинг-стоп на основе процента
                trailing_percent = 0.02  # 2%

                if direction == 'BUY':
                    new_stop = current_price * (1 - trailing_percent)
                    return max(new_stop, current_stop)
                else:  # SELL
                    new_stop = current_price * (1 + trailing_percent)
                    return min(new_stop, current_stop)
            else:
                # Трейлинг-стоп на основе ATR
                atr_multiplier = 2.0

                if direction == 'BUY':
                    new_stop = current_price - (atr * atr_multiplier)
                    return max(new_stop, current_stop)
                else:  # SELL
                    new_stop = current_price + (atr * atr_multiplier)
                    return min(new_stop, current_stop)

        except Exception as e:
            self.logger.error(f"Error calculating trailing stop: {e}")
            return current_stop

    def is_trading_hours(self) -> bool:
        """Проверка торговых часов"""
        try:
            current_time = datetime.now().time()
            start_time = datetime.strptime(TradingConfig.TRADING_HOURS['start'], '%H:%M').time()
            end_time = datetime.strptime(TradingConfig.TRADING_HOURS['end'], '%H:%M').time()

            if start_time <= end_time:
                return start_time <= current_time <= end_time
            else:  # Переход через полночь
                return current_time >= start_time or current_time <= end_time

        except Exception as e:
            self.logger.error(f"Error checking trading hours: {e}")
            return True  # По умолчанию разрешаем торговлю

    def get_risk_metrics(self) -> Dict[str, Any]:
        """Получение метрик риска"""
        try:
            win_rate = 0.0
            if self.daily_trades > 0:
                win_rate = (self.daily_winning_trades / self.daily_trades) * 100

            net_pnl = self.daily_profit - self.daily_loss

            return {
                'daily_trades': self.daily_trades,
                'daily_profit': round(self.daily_profit, 2),
                'daily_loss': round(self.daily_loss, 2),
                'net_pnl': round(net_pnl, 2),
                'win_rate': round(win_rate, 2),
                'max_drawdown': round(self.max_drawdown, 2),
                'emergency_stop': self.emergency_stop,
                'active_positions': len(self.positions),
                'last_reset': self.last_reset.isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error getting risk metrics: {e}")
            return {}

    def _check_daily_limits(self) -> bool:
        """Проверка дневных лимитов"""
        # Проверка максимальных дневных убытков
        if self.daily_loss >= self.config['max_daily_loss']:
            self.logger.warning(f"Daily loss limit reached: {self.daily_loss}")
            return False

        # Проверка максимального количества сделок в день
        max_daily_trades = self.config.get('max_daily_trades', 10)
        if self.daily_trades >= max_daily_trades:
            self.logger.warning(f"Daily trades limit reached: {self.daily_trades}")
            return False

        return True

    def _check_position_limits(self) -> bool:
        """Проверка лимитов позиций"""
        max_positions = self.config.get('max_positions', 3)
        if len(self.positions) >= max_positions:
            self.logger.warning(f"Maximum positions limit reached: {len(self.positions)}")
            return False
        return True

    def _check_risk_reward_ratio(self, signal: Dict[str, Any]) -> bool:
        """Проверка соотношения риск/прибыль"""
        min_ratio = self.config.get('min_risk_reward', 1.5)

        entry_price = signal.get('entry_price', 0)
        stop_loss = signal.get('stop_loss', 0)
        take_profit = signal.get('take_profit', 0)

        if entry_price <= 0 or stop_loss <= 0 or take_profit <= 0:
            return True  # Пропускаем проверку если данные неполные

        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)

        if risk <= 0:
            return False

        ratio = reward / risk

        if ratio < min_ratio:
            self.logger.warning(f"Risk/reward ratio too low: {ratio:.2f} < {min_ratio}")
            return False

        return True

    def _validate_position_size(self, symbol: str, signal: Dict[str, Any]) -> bool:
        """Валидация размера позиции"""
        size = signal.get('size', 0)
        symbol_config = TradingConfig.TRADING_PAIRS.get(symbol, {})

        min_position = symbol_config.get('min_position', 0)
        max_position = symbol_config.get('max_position', float('inf'))

        if size < min_position:
            self.logger.warning(f"Position size too small for {symbol}: {size} < {min_position}")
            return False

        if size > max_position:
            self.logger.warning(f"Position size too large for {symbol}: {size} > {max_position}")
            return False

        return True

    def _check_correlation(self, symbol: str, signal: Dict[str, Any]) -> bool:
        """Проверка корреляции с существующими позициями"""
        # Простая проверка - не открываем противоположные позиции по одному символу
        if symbol in self.positions:
            existing_direction = self.positions[symbol].get('direction')
            new_direction = signal.get('direction')

            if existing_direction != new_direction:
                self.logger.warning(f"Conflicting position direction for {symbol}")
                return False

        return True

    def _check_drawdown_limits(self) -> bool:
        """Проверка лимитов просадки"""
        max_drawdown_limit = self.config.get('drawdown_limit', 0.15)

        if self.max_drawdown > max_drawdown_limit:
            self.logger.warning(f"Maximum drawdown exceeded: {self.max_drawdown}")
            self._trigger_emergency_stop("Maximum drawdown exceeded")
            return False

        return True

    def _adjust_size_for_drawdown(self, base_size: float) -> float:
        """Корректировка размера позиции на основе просадки"""
        if self.max_drawdown <= 0:
            return base_size

        # Уменьшаем размер позиции при увеличении просадки
        drawdown_factor = max(0.5, 1 - (self.max_drawdown * 2))
        return base_size * drawdown_factor

    def _check_emergency_conditions(self):
        """Проверка экстренных условий"""
        # Проверка критической просадки
        emergency_loss_limit = self.config.get('emergency_stop_loss', 0.10)
        if self.daily_loss > emergency_loss_limit:
            self._trigger_emergency_stop(f"Emergency loss limit exceeded: {self.daily_loss}")

        # Проверка серии убыточных сделок
        if self.daily_losing_trades >= 5 and self.daily_winning_trades == 0:
            self._trigger_emergency_stop("Too many consecutive losing trades")

    def _trigger_emergency_stop(self, reason: str):
        """Активация экстренного стопа"""
        self.emergency_stop = True
        self.emergency_reason = reason
        self.logger.critical(f"EMERGENCY STOP TRIGGERED: {reason}")

    def reset_emergency_stop(self):
        """Сброс экстренного стопа (только вручную)"""
        self.emergency_stop = False
        self.emergency_reason = ""
        self.logger.info("Emergency stop reset manually")

    def should_reset_daily_metrics(self) -> bool:
        """Проверка необходимости сброса дневных метрик"""
        now = datetime.now()
        return now.date() > self.last_reset.date()