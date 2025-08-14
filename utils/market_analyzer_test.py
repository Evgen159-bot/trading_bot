#!/usr/bin/env python3
"""
Тестирование анализатора рынка и генерации сигналов
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Добавляем корневую папку в путь
sys.path.append(str(Path(__file__).parent.parent))

from modules.data_fetcher import DataFetcher
from modules.market_analyzer import MarketAnalyzer
from user_config import UserConfig


def test_market_analyzer():
    """Тестирование анализатора рынка"""
    try:
        print("🔍 ТЕСТИРОВАНИЕ АНАЛИЗАТОРА РЫНКА")
        print("=" * 50)

        # Инициализация
        data_fetcher = DataFetcher()
        market_analyzer = MarketAnalyzer(data_fetcher)

        enabled_pairs = UserConfig.get_enabled_pairs()

        for symbol in enabled_pairs:
            print(f"\n📊 Анализ {symbol}:")

            # Получаем данные
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
                continue

            print(f"✅ Данные получены: {len(df)} свечей")

            # Рассчитываем индикаторы
            df_with_indicators = market_analyzer.calculate_indicators(df)

            if df_with_indicators is None:
                print(f"❌ Ошибка расчета индикаторов для {symbol}")
                continue

            print(f"✅ Индикаторы рассчитаны")

            # Показываем последние значения
            last_row = df_with_indicators.iloc[-1]

            print(f"   💰 Цена: ${last_row['close']:.4f}")
            print(f"   📊 RSI: {last_row.get('rsi', 0):.1f}")
            print(f"   📈 EMA Fast: ${last_row.get('ema_fast', 0):.4f}")
            print(f"   📈 EMA Slow: ${last_row.get('ema_slow', 0):.4f}")
            print(f"   📊 MACD: {last_row.get('macd', 0):.6f}")
            print(f"   📊 Volume Ratio: {last_row.get('volume_ratio', 0):.2f}")

            # Анализ рыночных условий
            conditions = market_analyzer.analyze_market_conditions(df_with_indicators)

            print(f"   🎯 Тренд: {conditions.get('trend', 'UNKNOWN')}")
            print(f"   📊 Волатильность: {conditions.get('volatility', 'UNKNOWN')}")
            print(f"   📈 Объем: {conditions.get('volume', 'UNKNOWN')}")
            print(f"   💪 Сила тренда: {conditions.get('strength', 0):.2f}")

    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        import traceback
        traceback.print_exc()


def test_signal_generation():
    """Тестирование генерации сигналов"""
    try:
        print("\n🎯 ТЕСТИРОВАНИЕ ГЕНЕРАЦИИ СИГНАЛОВ")
        print("=" * 50)

        from config_loader import load_user_configuration

        # Загружаем конфигурацию
        config_loader = load_user_configuration()

        # Создаем компоненты (без position_manager для тестирования)
        data_fetcher = DataFetcher()
        market_analyzer = MarketAnalyzer(data_fetcher)

        # Создаем стратегию
        strategy = config_loader.create_strategy(market_analyzer, None)

        enabled_pairs = UserConfig.get_enabled_pairs()

        for symbol in enabled_pairs:
            print(f"\n🔍 Тестирование сигналов для {symbol}:")

            # Получаем данные
            end_time = datetime.now()
            start_time = end_time - timedelta(days=1)

            df = data_fetcher.get_kline(
                symbol=symbol,
                interval='5',
                start_time=int(start_time.timestamp()),
                end_time=int(end_time.timestamp())
            )

            if df is None:
                print(f"❌ Нет данных")
                continue

            # Тестируем генерацию сигнала
            signal = strategy.generate_signal(df, symbol)

            if signal:
                print(f"✅ Сигнал: {signal.get('action', 'UNKNOWN')}")
                print(f"   Уверенность: {signal.get('confidence', 0):.1%}")
                print(f"   Причины: {signal.get('reasons', 'N/A')}")
            else:
                print(f"⚠️ Сигнал не сгенерирован")

                # Показываем почему
                if hasattr(strategy, 'MIN_CONFIDENCE'):
                    print(f"   Требуется уверенность: {strategy.MIN_CONFIDENCE:.1%}")

                if hasattr(strategy, 'MIN_CONDITIONS_REQUIRED'):
                    print(f"   Требуется условий: {strategy.MIN_CONDITIONS_REQUIRED}")

    except Exception as e:
        print(f"❌ Ошибка тестирования сигналов: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--signals':
        test_signal_generation()
    else:
        test_market_analyzer()
        test_signal_generation()