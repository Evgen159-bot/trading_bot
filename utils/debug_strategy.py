#!/usr/bin/env python3
"""
Утилита для отладки стратегий и диагностики проблем
"""

import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Добавляем корневую папку в путь
sys.path.append(str(Path(__file__).parent.parent))

from config_loader import load_user_configuration
from modules.data_fetcher import DataFetcher
from modules.market_analyzer import MarketAnalyzer
from modules.risk_manager import RiskManager
from modules.order_manager import OrderManager
from modules.position_manager import PositionManager
from pybit.unified_trading import HTTP


class StrategyDebugger:
    """Отладчик стратегий"""

    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)

    def setup_logging(self):
        """Настройка детального логирования"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('debug_strategy.log', encoding='utf-8')
            ]
        )

    def debug_strategy_execution(self, symbol: str = 'ETHUSDT'):
        """Отладка выполнения стратегии"""
        try:
            print(f"🔍 ОТЛАДКА СТРАТЕГИИ ДЛЯ {symbol}")
            print("=" * 50)

            # Загружаем конфигурацию
            config_loader = load_user_configuration()

            # Создаем компоненты
            data_fetcher = DataFetcher()
            market_analyzer = MarketAnalyzer(data_fetcher)

            # Создаем полный набор компонентов для тестирования
            api_client = HTTP(
                testnet=True,  # Всегда используем testnet для отладки
                api_key="test_key",
                api_secret="test_secret"
            )

            risk_manager = RiskManager()
            order_manager = OrderManager(api_client)
            position_manager = PositionManager(risk_manager, order_manager)

            # Создаем стратегию
            strategy = config_loader.create_strategy(market_analyzer, position_manager)
            if not strategy:
                print("❌ Не удалось создать стратегию")
                return

            print(f"✅ Стратегия создана: {strategy.name}")

            # Получаем данные
            print(f"\n📊 Получение данных для {symbol}...")
            end_time = datetime.now()
            start_time = end_time - timedelta(days=1)

            df = data_fetcher.get_kline(
                symbol=symbol,
                interval='5',
                start_time=int(start_time.timestamp()),
                end_time=int(end_time.timestamp())
            )

            if df is None or len(df) == 0:
                print(f"❌ Нет данных для {symbol}")
                return

            print(f"✅ Получено {len(df)} свечей")
            print(f"📈 Цена: ${df['close'].iloc[-1]:.4f}")
            print(f"📊 Объем: {df['volume'].iloc[-1]:,.0f}")

            # Тестируем генерацию сигнала
            print(f"\n🎯 Тестирование генерации сигнала...")

            market_data = {
                'df': df,
                'symbol': symbol,
                'account_balance': 1000.0,
                'timestamp': datetime.now()
            }

            # Выполняем стратегию
            result = strategy.execute(symbol, market_data)

            if result:
                print(f"✅ Сигнал сгенерирован!")
                print(f"   Действие: {result.get('action', 'UNKNOWN')}")
                print(f"   Направление: {result.get('direction', 'UNKNOWN')}")
                print(f"   Уверенность: {result.get('confidence', 0):.1%}")
                print(f"   Причины: {result.get('reasons', 'N/A')}")
            else:
                print("⚠️ Сигнал не сгенерирован")

                # Детальная диагностика
                print("\n🔍 ДЕТАЛЬНАЯ ДИАГНОСТИКА:")
                self._detailed_signal_analysis(strategy, df, symbol)

        except Exception as e:
            print(f"❌ Ошибка отладки: {e}")
            self.logger.error(f"Debug error: {e}", exc_info=True)

    def _detailed_signal_analysis(self, strategy, df, symbol):
        """Детальный анализ почему не генерируется сигнал"""
        try:
            print("\n📊 Анализ индикаторов:")

            # Проверяем расчет индикаторов для Custom Strategy
            if hasattr(strategy, 'generate_signals'):
                indicators = strategy.generate_signals(df)

                if indicators:
                    print(f"✅ Индикаторы рассчитаны: {len(indicators)} значений")

                    # Показываем ключевые индикаторы
                    rsi = indicators.get('rsi', 0)
                    macd = indicators.get('macd', 0)
                    macd_signal = indicators.get('macd_signal', 0)
                    volume_ratio = indicators.get('volume_ratio', 0)
                    ema_fast = indicators.get('ema_fast', 0)
                    ema_slow = indicators.get('ema_slow', 0)

                    print(f"   RSI: {rsi:.1f}")
                    print(f"   MACD: {macd:.6f} vs Signal: {macd_signal:.6f}")
                    print(f"   Volume Ratio: {volume_ratio:.2f}")
                    print(f"   EMA Fast: {ema_fast:.2f}, Slow: {ema_slow:.2f}")

                    # Проверяем условия входа для Custom Strategy
                    if hasattr(strategy, '_check_long_entry_conditions'):
                        try:
                            long_valid, long_score, long_reasons = strategy._check_long_entry_conditions(indicators)
                            print(
                                f"   Long условия: {long_score:.1f} выполнено (нужно {strategy.MIN_CONDITIONS_REQUIRED})")
                            print(f"   Long валидность: {'✅ Да' if long_valid else '❌ Нет'}")
                            print(f"   Long причины: {long_reasons}")
                        except Exception as e:
                            print(f"   Long условия: ❌ Ошибка проверки - {e}")

                    if hasattr(strategy, '_check_short_entry_conditions'):
                        try:
                            short_valid, short_score, short_reasons = strategy._check_short_entry_conditions(indicators)
                            print(
                                f"   Short условия: {short_score:.1f} выполнено (нужно {strategy.MIN_CONDITIONS_REQUIRED})")
                            print(f"   Short валидность: {'✅ Да' if short_valid else '❌ Нет'}")
                            print(f"   Short причины: {short_reasons}")
                        except Exception as e:
                            print(f"   Short условия: ❌ Ошибка проверки - {e}")

                    # Проверяем cooldown
                    if hasattr(strategy, '_is_signal_cooldown_active'):
                        cooldown_active = strategy._is_signal_cooldown_active()
                        print(f"   Signal Cooldown: {'🔴 Активен' if cooldown_active else '✅ Неактивен'}")

                else:
                    print("❌ Не удалось рассчитать индикаторы")
            else:
                print("⚠️ Метод generate_signals не найден в стратегии")

        except Exception as e:
            print(f"❌ Ошибка детального анализа: {e}")
            import traceback
            traceback.print_exc()

    def test_all_pairs(self):
        """Тестирование всех торговых пар"""
        try:
            from user_config import UserConfig

            print("🔍 ТЕСТИРОВАНИЕ ВСЕХ ТОРГОВЫХ ПАР")
            print("=" * 60)

            enabled_pairs = UserConfig.get_enabled_pairs()

            for symbol in enabled_pairs:
                print(f"\n📊 Тестирование {symbol}:")
                self.debug_strategy_execution(symbol)
                print("-" * 30)

        except Exception as e:
            print(f"❌ Ошибка тестирования пар: {e}")

    def analyze_market_conditions(self):
        """Анализ текущих рыночных условий"""
        try:
            print("📈 АНАЛИЗ РЫНОЧНЫХ УСЛОВИЙ")
            print("=" * 40)

            from user_config import UserConfig
            data_fetcher = DataFetcher()

            enabled_pairs = UserConfig.get_enabled_pairs()

            for symbol in enabled_pairs:
                try:
                    price = data_fetcher.get_current_price(symbol)
                    print(f"{symbol}: ${price:.4f}" if price else f"{symbol}: ❌ Нет данных")
                except Exception as e:
                    print(f"{symbol}: ❌ Ошибка - {e}")

        except Exception as e:
            print(f"❌ Ошибка анализа рынка: {e}")


def main():
    """Главная функция отладки"""
    debugger = StrategyDebugger()

    if len(sys.argv) > 1:
        if sys.argv[1] == '--all':
            debugger.test_all_pairs()
        elif sys.argv[1] == '--market':
            debugger.analyze_market_conditions()
        elif sys.argv[1].startswith('--symbol='):
            symbol = sys.argv[1].split('=')[1]
            debugger.debug_strategy_execution(symbol)
        else:
            print("Использование:")
            print("  python utils/debug_strategy.py --all                # Тест всех пар")
            print("  python utils/debug_strategy.py --market             # Анализ рынка")
            print("  python utils/debug_strategy.py --symbol=ETHUSDT     # Тест конкретной пары")
    else:
        # По умолчанию тестируем ETHUSDT
        debugger.debug_strategy_execution('ETHUSDT')


if __name__ == "__main__":
    main()