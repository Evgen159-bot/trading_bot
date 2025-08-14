import logging
import os
import sys
import time
import signal
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

# Импорт основной конфигурации
from config_loader import load_user_configuration
from config.trading_config import TradingConfig

# Импорт модулей
from modules.data_fetcher import DataFetcher
from modules.market_analyzer import MarketAnalyzer
from modules.risk_manager import RiskManager
from modules.order_manager import OrderManager
from modules.position_manager import PositionManager
from modules.performance_tracker import PerformanceTracker
from modules.trading_diary import TradingDiary
from strategies.strategy_validator import StrategyValidator
from pybit.unified_trading import HTTP


class TradingBot:
    """Основной класс торгового бота"""

    def __init__(self):
        try:
            # Загрузка пользовательской конфигурации
            print("🚀 Инициализация торгового бота...")
            self.config_loader = load_user_configuration()

            self.logger = self._setup_logging()
            self.logger.info("Initializing trading bot...")

            self._validate_config()
            self.init_components()

            self.is_running = False
            self.cycle_count = 0
            self.last_heartbeat = datetime.now()

            # Настройка обработчиков сигналов для корректного завершения
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)

            self.logger.info("Trading bot initialized successfully")

        except Exception as e:
            self.logger.error(f"Error initializing trading bot: {e}", exc_info=True)
            raise

    def _setup_logging(self) -> logging.Logger:
        """Настройка системы логирования"""
        logger = logging.getLogger("trading_bot")
        logger.setLevel(logging.INFO)

        # Очищаем существующие обработчики
        logger.handlers.clear()

        # Создаем директорию для логов
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        # Файл лога с датой
        log_file = os.path.join(log_dir, f"trading_{datetime.now().strftime('%Y%m%d')}.log")

        # Форматтер
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Файловый обработчик
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        # Консольный обработчик
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

        return logger

    def _signal_handler(self, signum, frame):
        """Обработчик сигналов для корректного завершения"""
        self.logger.info(f"Received signal {signum}. Initiating graceful shutdown...")
        self.stop()

    def _validate_config(self):
        """Валидация конфигурации"""
        if not TradingConfig.API_KEY or not TradingConfig.API_SECRET:
            raise ValueError("API keys not configured")
        if not TradingConfig.TRADING_PAIRS:
            raise ValueError("No trading pairs configured")
        if TradingConfig.CYCLE_INTERVAL < 5:
            raise ValueError("Cycle interval too short (minimum 5 seconds)")

        self.logger.info("Configuration validated successfully")

    def init_components(self):
        """Инициализация всех компонентов бота"""
        try:
            self.logger.info("Initializing components...")

            # Инициализация API клиента
            self.api_client = HTTP(
                testnet=TradingConfig.TESTNET,
                api_key=TradingConfig.API_KEY,
                api_secret=TradingConfig.API_SECRET
            )

            # Инициализация компонентов в правильном порядке
            self.data_fetcher = DataFetcher(client=self.api_client)
            self.logger.info("DataFetcher initialized")

            self.market_analyzer = MarketAnalyzer(self.data_fetcher)
            self.logger.info("MarketAnalyzer initialized")

            self.risk_manager = RiskManager()
            self.logger.info("RiskManager initialized")

            self.order_manager = OrderManager(self.api_client)
            self.logger.info("OrderManager initialized")

            self.position_manager = PositionManager(self.risk_manager, self.order_manager)
            self.logger.info("PositionManager initialized")

            # Создаем стратегию на основе пользовательского выбора
            self.strategy = self.config_loader.create_strategy(self.market_analyzer, self.position_manager)
            if self.strategy is None:
                raise Exception("Failed to create trading strategy")
            self.logger.info(f"Strategy initialized: {self.strategy.name}")

            # Инициализация валидатора стратегий
            self.strategy_validator = StrategyValidator()
            self.logger.info("StrategyValidator initialized")

            # Валидация стратегии при запуске
            self._validate_strategy_on_startup()

            self.performance_tracker = PerformanceTracker()
            self.logger.info("PerformanceTracker initialized")

            # Инициализация дневника трейдинга
            self.trading_diary = TradingDiary()

            # Передаем дневник в position_manager
            self.position_manager.set_trading_diary(self.trading_diary)
            self.logger.info("TradingDiary initialized")

            self.logger.info("All components initialized successfully")

        except Exception as e:
            self.logger.error(f"Error initializing components: {e}", exc_info=True)
            raise

    def _validate_strategy_on_startup(self):
        """Валидация стратегии при запуске бота"""
        try:
            self.logger.info("Validating trading strategy...")

            # Создаем тестовые данные для валидации
            test_data = self._create_test_data_for_validation()

            if test_data:
                # Запускаем валидацию
                validation_result = self.strategy_validator.validate_strategy(
                    strategy=self.strategy,
                    test_data=test_data,
                    strict_mode=False,  # Не строгий режим при запуске
                    performance_test=True
                )

                # Логируем результаты
                if validation_result['is_valid']:
                    self.logger.info(f"Strategy validation PASSED. Score: {validation_result['score']:.1f}/100")
                    print(f"✅ Strategy validation PASSED (Score: {validation_result['score']:.1f}/100)")
                else:
                    self.logger.warning(f"Strategy validation FAILED. Score: {validation_result['score']:.1f}/100")
                    print(f"⚠️  Strategy validation FAILED (Score: {validation_result['score']:.1f}/100)")

                    # Показываем ошибки
                    if validation_result['errors']:
                        print("❌ Errors found:")
                        for error in validation_result['errors']:
                            print(f"   - {error}")

                    # Показываем рекомендации
                    if validation_result['recommendations']:
                        print("💡 Recommendations:")
                        for rec in validation_result['recommendations']:
                            print(f"   - {rec}")

                # Сохраняем результат валидации
                self.last_validation_result = validation_result

            else:
                self.logger.warning("Could not create test data for strategy validation")
                print("⚠️  Strategy validation skipped - no test data available")

        except Exception as e:
            self.logger.error(f"Error during strategy validation: {e}")
            print(f"❌ Strategy validation error: {e}")

    def _create_test_data_for_validation(self) -> dict:
        """Создание тестовых данных для валидации стратегии"""
        try:
            # Берем первую доступную торговую пару для тестирования
            test_symbol = list(TradingConfig.TRADING_PAIRS.keys())[0]

            # Получаем тестовые данные
            test_market_data = self.get_market_data(test_symbol, 10000.0)  # Тестовый баланс

            if test_market_data and test_market_data.get('df') is not None:
                return {
                    'df': test_market_data['df'],
                    'symbol': test_symbol,
                    'account_balance': 10000.0
                }

            return None

        except Exception as e:
            self.logger.error(f"Error creating test data: {e}")
            return None

    def start(self):
        """Запуск торгового бота"""
        try:
            self.is_running = True
            self.logger.info("Starting trading bot...")
            print("\n🤖 Bot is running...")
            print("Press Ctrl+C to stop the bot gracefully")

            while self.is_running:
                try:
                    cycle_start = datetime.now()
                    self.cycle_count += 1

                    print(f"\n📊 Starting trading cycle #{self.cycle_count}...")
                    self.trading_cycle()

                    cycle_duration = (datetime.now() - cycle_start).total_seconds()
                    print(f"✅ Trading cycle #{self.cycle_count} completed in {cycle_duration:.2f}s")

                    # Обновляем heartbeat
                    self.last_heartbeat = datetime.now()

                    # Пауза между циклами
                    if self.is_running:
                        time.sleep(TradingConfig.CYCLE_INTERVAL)

                except KeyboardInterrupt:
                    self.logger.info("Keyboard interrupt received")
                    break
                except Exception as e:
                    self.logger.error(f"Error in trading cycle #{self.cycle_count}: {e}", exc_info=True)
                    print(f"❌ Error in cycle: {e}")
                    time.sleep(60)  # Пауза при ошибке

        except Exception as e:
            self.logger.error(f"Critical error in bot execution: {e}", exc_info=True)
            raise
        finally:
            self.stop()

    def trading_cycle(self):
        """Основной торговый цикл"""
        cycle_start = datetime.now()
        self.logger.info(f"Trading cycle started at {cycle_start.strftime('%H:%M:%S')}")
        self.logger.info(f"Available trading pairs: {list(TradingConfig.TRADING_PAIRS.keys())}")
        print(f"\n🕐 Trading cycle started at {cycle_start.strftime('%H:%M:%S')}")
        print(f"📈 Available trading pairs: {list(TradingConfig.TRADING_PAIRS.keys())}")

        # Получаем баланс один раз в начале цикла
        try:
            account_balance = self.data_fetcher.get_account_balance()

            # Проверяем минимальный баланс
            balance_info = self.config_loader.get_balance_info()
            self.logger.info(
                f"Account balance: ${account_balance:.2f}, Min threshold: ${balance_info['min_balance_threshold']:.2f}")

            if account_balance < balance_info['min_balance_threshold']:
                self.logger.critical(
                    f"Balance too low: ${account_balance:.2f} < ${balance_info['min_balance_threshold']:.2f}")
                print(f"🚨 КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ: Баланс слишком низкий!")
                print(f"   Текущий: ${account_balance:.2f}")
                print(f"   Минимальный: ${balance_info['min_balance_threshold']:.2f}")
                return

            print(f"💰 Account balance: ${account_balance:.2f}")

            # Начинаем торговую сессию в дневнике
            self.trading_diary.start_trading_session(account_balance)
        except Exception as e:
            self.logger.error(f"Error getting account balance: {e}")
            print(f"❌ Error getting balance: {e}")
            account_balance = 0.0

        successful_pairs = 0

        for symbol in TradingConfig.TRADING_PAIRS:
            try:
                self.logger.info(f"Processing {symbol}...")
                print(f"\n🔍 Processing {symbol}...")

                # Получаем рыночные данные
                market_data = self.get_market_data(symbol, account_balance)
                if not market_data:
                    self.logger.warning(f"No market data for {symbol}")
                    print(f"⚠️  No market data for {symbol}")
                    continue

                # Выполняем стратегию
                self.logger.info(f"Executing strategy for {symbol}")
                result = self.strategy.execute(symbol, market_data)

                if result:
                    self.logger.info(f"Strategy result for {symbol}: {result['action']}")
                    print(f"📋 Strategy result for {symbol}: {result['action']}")

                    # Логируем в дневник
                    self._log_to_diary(symbol, result)

                    # Обновляем статистику стратегии
                    if hasattr(self.strategy, 'update_stats') and result.get('pnl'):
                        self.strategy.update_stats(result)

                    self.update_performance(result)
                else:
                    self.logger.debug(f"No action for {symbol}")
                    print(f"⏸️  No action for {symbol}")

                # Обновляем позиции
                self.update_positions(symbol)
                successful_pairs += 1

                # Небольшая пауза между парами
                time.sleep(1)

            except Exception as e:
                self.logger.error(f"Error processing {symbol}: {e}", exc_info=True)
                print(f"❌ Error processing {symbol}: {e}")

        cycle_duration = (datetime.now() - cycle_start).total_seconds()
        self.logger.info(
            f"Processed {successful_pairs}/{len(TradingConfig.TRADING_PAIRS)} pairs in {cycle_duration:.2f}s")
        print(f"\n✅ Processed {successful_pairs}/{len(TradingConfig.TRADING_PAIRS)} pairs in {cycle_duration:.2f}s")

    def _log_to_diary(self, symbol: str, result: Dict[str, Any]) -> None:
        """Логирование результатов в дневник трейдинга"""
        try:
            action = result.get('action')

            if action == 'OPEN':
                # Логируем открытие позиции
                self.trading_diary.log_position_opened(
                    symbol=symbol,
                    direction=result.get('direction', 'UNKNOWN'),
                    size=result.get('size', 0.0),
                    entry_price=result.get('entry_price', 0.0),
                    stop_loss=result.get('stop_loss'),
                    take_profit=result.get('take_profit')
                )
            elif action == 'CLOSE':
                # Логируем закрытие позиции
                self.trading_diary.log_position_closed(
                    symbol=symbol,
                    close_price=result.get('exit_price', result.get('current_price', 0.0)),
                    pnl=result.get('pnl', 0.0),
                    fees=result.get('fees', 0.0),
                    close_reason=result.get('reason', 'strategy_signal')
                )

        except Exception as e:
            self.logger.error(f"Error logging to diary: {e}")

    def get_market_data(self, symbol: str, account_balance: float = None) -> Optional[Dict[str, Any]]:
        """Получение рыночных данных для символа"""
        try:
            # Рассчитываем временные рамки
            end_time = datetime.now()
            start_time = end_time - timedelta(days=1)

            # Получаем данные свечей
            df = self.data_fetcher.get_kline(
                symbol=symbol,
                interval=TradingConfig.TIMEFRAMES['primary'],
                start_time=int(start_time.timestamp()),
                end_time=int(end_time.timestamp())
            )

            if df is None or len(df) == 0:
                self.logger.warning(f"No kline data for {symbol}")
                return None

            # Получаем баланс если не передан
            if account_balance is None:
                account_balance = self.data_fetcher.get_account_balance()
                if account_balance is None:
                    account_balance = 0.0

            return {
                "df": df,
                "symbol": symbol,
                "account_balance": account_balance,
                "timestamp": datetime.now()
            }

        except Exception as e:
            self.logger.error(f"Error getting market data for {symbol}: {e}", exc_info=True)
            return None

    def update_positions(self, symbol: str):
        """Обновление позиций и трейлинг-стопов"""
        try:
            position = self.position_manager.get_position_status(symbol)
            if position:
                current_price = self.data_fetcher.get_current_price(symbol)
                if current_price is not None:
                    old_stop = position.get('stop_loss', 0)
                    self.position_manager.update_trailing_stop(symbol, current_price)

                    # Логируем изменения трейлинг-стопа
                    new_position = self.position_manager.get_position_status(symbol)
                    if new_position and new_position.get('stop_loss', 0) != old_stop:
                        self.logger.info(
                            f"Trailing stop updated for {symbol}: {old_stop:.4f} -> {new_position['stop_loss']:.4f}")

        except Exception as e:
            self.logger.error(f"Error updating positions for {symbol}: {e}", exc_info=True)

    def update_performance(self, result: Dict[str, Any]):
        """Обновление статистики производительности"""
        try:
            if result.get("action") == "CLOSE":
                self.performance_tracker.log_trade(result)
                self.logger.info(f"Trade logged: {result}")

        except Exception as e:
            self.logger.error(f"Error updating performance: {e}", exc_info=True)

    def get_bot_status(self) -> Dict[str, Any]:
        """Получение статуса бота"""
        return {
            "is_running": self.is_running,
            "cycle_count": self.cycle_count,
            "last_heartbeat": self.last_heartbeat,
            "uptime": datetime.now() - self.last_heartbeat if self.last_heartbeat else None,
            "trading_pairs": list(TradingConfig.TRADING_PAIRS.keys()),
            "strategy_name": self.strategy.name if hasattr(self.strategy, 'name') else "MultiIndicatorStrategy",
            "last_validation": getattr(self, 'last_validation_result', None)
        }

    def run_strategy_validation(self, strict_mode: bool = True) -> dict:
        """Запуск валидации стратегии по требованию"""
        try:
            self.logger.info("Running on-demand strategy validation...")

            test_data = self._create_test_data_for_validation()
            if not test_data:
                return {'error': 'Could not create test data'}

            validation_result = self.strategy_validator.validate_strategy(
                strategy=self.strategy,
                test_data=test_data,
                strict_mode=strict_mode,
                performance_test=True
            )

            self.last_validation_result = validation_result
            return validation_result

        except Exception as e:
            self.logger.error(f"Error running strategy validation: {e}")
            return {'error': str(e)}

    def get_strategy_performance(self) -> dict:
        """Получение статистики производительности стратегии"""
        try:
            if hasattr(self.strategy, 'get_performance_summary'):
                return self.strategy.get_performance_summary()
            else:
                return {'error': 'Strategy does not support performance tracking'}
        except Exception as e:
            self.logger.error(f"Error getting strategy performance: {e}")
            return {'error': str(e)}

    def stop(self):
        """Остановка торгового бота"""
        try:
            if not self.is_running:
                return

            self.is_running = False
            self.logger.info("Stopping trading bot...")
            print("\n🛑 Stopping trading bot...")

            # Закрываем все открытые позиции
            print("📤 Closing all open positions...")
            closed_positions = 0

            for symbol in TradingConfig.TRADING_PAIRS:
                try:
                    position = self.position_manager.get_position_status(symbol)
                    if position:
                        self.logger.info(f"Closing position for {symbol}")
                        self.position_manager.close_position(symbol, "bot_shutdown")
                        closed_positions += 1
                        print(f"✅ Closed position for {symbol}")
                except Exception as e:
                    self.logger.error(f"Error closing position for {symbol}: {e}")
                    print(f"❌ Error closing position for {symbol}: {e}")

            if closed_positions > 0:
                print(f"📊 Closed {closed_positions} positions")
            else:
                print("📊 No open positions to close")

            # Сохраняем данные производительности
            try:
                self.performance_tracker.save_performance_data()

                # Завершаем торговую сессию в дневнике
                daily_report = self.trading_diary.end_trading_session()

                print("💾 Performance data saved")
                print("📔 Trading diary updated")
            except Exception as e:
                self.logger.error(f"Error saving performance data: {e}")
                print(f"❌ Error saving performance data: {e}")

            print("🏁 Trading bot stopped successfully")
            self.logger.info("Trading bot stopped successfully")

        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}", exc_info=True)
            print(f"❌ Error stopping bot: {e}")

    def show_daily_status(self) -> None:
        """Показать статус текущего дня"""
        try:
            status = self.trading_diary.get_current_day_status()

            print("\n" + "=" * 50)
            print("📔 СТАТУС ТОРГОВОГО ДНЯ")
            print("=" * 50)
            print(f"📅 Дата: {status['date']}")
            print(f"💰 Начальный баланс: ${status['start_balance']:.2f}")
            print(f"💰 Текущий баланс: ${status['current_balance']:.2f}")

            daily_return = status['daily_return']
            return_emoji = "📈" if daily_return >= 0 else "📉"
            print(f"{return_emoji} Изменение за день: ${daily_return:.2f}")

            print(f"📊 Открытых позиций: {status['open_positions']}")
            print(f"✅ Завершенных сделок: {status['completed_trades']}")

            stats = status['daily_stats']
            if stats['total_trades'] > 0:
                print(f"🎯 Win Rate: {stats['win_rate']:.1f}%")
                print(f"💵 Общий P&L: ${stats['total_pnl']:.2f}")

            print("=" * 50)

        except Exception as e:
            self.logger.error(f"Error showing daily status: {e}")

    def export_diary(self, days: int = 30) -> None:
        """Экспорт дневника в CSV"""
        try:
            export_path = self.trading_diary.export_diary_to_csv(days)
            if export_path:
                print(f"📊 Дневник экспортирован: {export_path}")
            else:
                print("❌ Ошибка экспорта дневника")

        except Exception as e:
            self.logger.error(f"Error exporting diary: {e}")


def main():
    """Главная функция запуска бота"""
    bot = None
    try:
        print("\n" + "=" * 50)
        print("🚀 BYBIT TRADING BOT STARTING")
        print("=" * 50)

        bot = TradingBot()
        bot.start()

    except KeyboardInterrupt:
        print("\n⚠️  Shutdown signal received")

    except Exception as e:
        print(f"\n💥 Critical error: {e}")
        import traceback
        print(traceback.format_exc())

    finally:
        if bot:
            print("\n🔄 Initiating shutdown sequence...")
            bot.stop()
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()