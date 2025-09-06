#!/usr/bin/env python3
"""
Инструмент для детальной отладки стратегий
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


class StrategyDebugTool:
    """Инструмент для детальной отладки стратегий"""

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
                logging.FileHandler('strategy_debug.log', encoding='utf-8')
            ]
        )

    def debug_signal_generation(self, symbol: str = 'ETHUSDT'):
        """Детальная отладка генерации сигналов"""
        try:
            print(f"🔍 ДЕТАЛЬНАЯ ОТЛАДКА СИГНАЛОВ ДЛЯ {symbol}")
            print("=" * 60)

            # Загружаем конфигурацию
            config_loader = load_user_configuration()

            # Создаем компоненты
            data_fetcher = DataFetcher()
            market_analyzer = MarketAnalyzer(data_fetcher)

            # Создаем полный набор компонентов
            api_client = HTTP(
                testnet=True,
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

            # Детальный анализ сигналов
            print(f"\n🎯 ДЕТАЛЬНЫЙ АНАЛИЗ СИГНАЛОВ:")

            if hasattr(strategy, 'generate_signals'):
                signals = strategy.generate_signals(df)

                if signals:
                    print(f"✅ Индикаторы рассчитаны:")
                    print(f"   RSI: {signals.get('rsi', 0):.1f}")
                    print(f"   MACD: {signals.get('macd', 0):.6f}")
                    print(f"   MACD Signal: {signals.get('macd_signal', 0):.6f}")
                    print(f"   EMA Fast: {signals.get('ema_fast', 0):.2f}")
                    print(f"   EMA Slow: {signals.get('ema_slow', 0):.2f}")
                    print(f"   Volume Ratio: {signals.get('volume_ratio', 0):.2f}")
                    print(f"   BB Upper: {signals.get('bb_upper', 0):.2f}")
                    print(f"   BB Lower: {signals.get('bb_lower', 0):.2f}")
                    print(f"   Stoch K: {signals.get('stoch_k', 0):.1f}")
                    print(f"   Stoch D: {signals.get('stoch_d', 0):.1f}")

                    # Проверяем условия входа
                    print(f"\n🔍 АНАЛИЗ УСЛОВИЙ ВХОДА:")

                    if hasattr(strategy, '_check_long_entry_conditions'):
                        long_valid, long_score, long_reasons = strategy._check_long_entry_conditions(signals)
                        print(f"   📈 LONG: {long_score}/{strategy.MIN_CONDITIONS_REQUIRED} условий")
                        print(f"      Валидность: {'✅ ДА' if long_valid else '❌ НЕТ'}")
                        print(f"      Причины: {long_reasons}")

                        # Детальный анализ каждого условия
                        self._analyze_long_conditions_detailed(strategy, signals)

                    if hasattr(strategy, '_check_short_entry_conditions'):
                        short_valid, short_score, short_reasons = strategy._check_short_entry_conditions(signals)
                        print(f"   📉 SHORT: {short_score}/{strategy.MIN_CONDITIONS_REQUIRED} условий")
                        print(f"      Валидность: {'✅ ДА' if short_valid else '❌ НЕТ'}")
                        print(f"      Причины: {short_reasons}")

                        # Детальный анализ каждого условия
                        self._analyze_short_conditions_detailed(strategy, signals)

                    # Проверяем cooldown
                    if hasattr(strategy, '_is_signal_cooldown_active'):
                        cooldown_active = strategy._is_signal_cooldown_active()
                        print(f"\n⏰ Signal Cooldown: {'🔴 АКТИВЕН' if cooldown_active else '✅ НЕАКТИВЕН'}")

                        if cooldown_active and hasattr(strategy, 'last_signal_time'):
                            time_since = (datetime.now() - strategy.last_signal_time).total_seconds()
                            print(f"   Время с последнего сигнала: {time_since:.0f}с")
                            print(f"   Требуется cooldown: {strategy.SIGNAL_COOLDOWN}с")

                    # Рекомендации по улучшению
                    print(f"\n💡 РЕКОМЕНДАЦИИ:")
                    self._provide_optimization_recommendations(strategy, signals, long_valid, short_valid)

                else:
                    print("❌ Не удалось рассчитать индикаторы")
            else:
                print("⚠️ Метод generate_signals не найден в стратегии")

        except Exception as e:
            print(f"❌ Ошибка отладки: {e}")
            import traceback
            traceback.print_exc()

    def _analyze_long_conditions_detailed(self, strategy, signals):
        """Детальный анализ условий для лонга"""
        print(f"\n      📊 ДЕТАЛЬНЫЙ АНАЛИЗ LONG CONDITIONS:")

        # RSI
        if strategy.RSI_ENABLED:
            rsi = signals.get('rsi', 50)
            rsi_prev = signals.get('rsi_prev', 50)
            rsi_condition = rsi < strategy.RSI_OVERSOLD_UPPER or (rsi > rsi_prev and rsi < 50)
            print(f"         RSI: {rsi:.1f} ({'✅' if rsi_condition else '❌'}) - Порог: <{strategy.RSI_OVERSOLD_UPPER}")

        # MACD
        if strategy.MACD_ENABLED:
            macd = signals.get('macd', 0)
            macd_signal = signals.get('macd_signal', 0)
            macd_condition = macd > macd_signal
            print(f"         MACD: {macd:.6f} vs {macd_signal:.6f} ({'✅' if macd_condition else '❌'})")

        # Volume
        if strategy.VOLUME_ENABLED:
            volume_ratio = signals.get('volume_ratio', 0)
            volume_condition = volume_ratio > strategy.MIN_VOLUME_RATIO
            print(
                f"         Volume: {volume_ratio:.2f} ({'✅' if volume_condition else '❌'}) - Порог: >{strategy.MIN_VOLUME_RATIO}")

    def _analyze_short_conditions_detailed(self, strategy, signals):
        """Детальный анализ условий для шорта"""
        print(f"\n      📊 ДЕТАЛЬНЫЙ АНАЛИЗ SHORT CONDITIONS:")

        # RSI
        if strategy.RSI_ENABLED:
            rsi = signals.get('rsi', 50)
            rsi_prev = signals.get('rsi_prev', 50)
            rsi_condition = rsi > strategy.RSI_OVERBOUGHT_LOWER or (rsi < rsi_prev and rsi > 50)
            print(
                f"         RSI: {rsi:.1f} ({'✅' if rsi_condition else '❌'}) - Порог: >{strategy.RSI_OVERBOUGHT_LOWER}")

        # MACD
        if strategy.MACD_ENABLED:
            macd = signals.get('macd', 0)
            macd_signal = signals.get('macd_signal', 0)
            macd_condition = macd < macd_signal
            print(f"         MACD: {macd:.6f} vs {macd_signal:.6f} ({'✅' if macd_condition else '❌'})")

        # Volume
        if strategy.VOLUME_ENABLED:
            volume_ratio = signals.get('volume_ratio', 0)
            volume_condition = volume_ratio > strategy.MIN_VOLUME_RATIO
            print(
                f"         Volume: {volume_ratio:.2f} ({'✅' if volume_condition else '❌'}) - Порог: >{strategy.MIN_VOLUME_RATIO}")

    def _provide_optimization_recommendations(self, strategy, signals, long_valid, short_valid):
        """Рекомендации по оптимизации"""
        if not long_valid and not short_valid:
            print("   🔧 Для увеличения количества сигналов:")
            print("      - Снизьте min_conditions_required до 1")
            print("      - Увеличьте oversold_upper до 50")
            print("      - Снизьте overbought_lower до 50")
            print("      - Снизьте min_ratio до 0.8")

        volume_ratio = signals.get('volume_ratio', 0)
        if volume_ratio < strategy.MIN_VOLUME_RATIO:
            print(f"   📊 Объем слишком низкий: {volume_ratio:.2f} < {strategy.MIN_VOLUME_RATIO}")
            print(f"      Рекомендация: снизить min_ratio до {max(0.5, volume_ratio * 0.8):.1f}")

        rsi = signals.get('rsi', 50)
        if 45 < rsi < 55:
            print(f"   📈 RSI в нейтральной зоне: {rsi:.1f}")
            print("      Рекомендация: расширить диапазоны RSI для нейтральной зоны")


def main():
    """Главная функция отладки"""
    debugger = StrategyDebugTool()

    if len(sys.argv) > 1:
        symbol = sys.argv[1]
        debugger.debug_signal_generation(symbol)
    else:
        # Тестируем все активные пары
        from user_config import UserConfig
        enabled_pairs = UserConfig.get_enabled_pairs()

        for symbol in enabled_pairs:
            debugger.debug_signal_generation(symbol)
            print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()