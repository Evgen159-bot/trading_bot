import unittest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np
from datetime import datetime
from strategies.multi_indicator_strategy import MultiIndicatorStrategy
from strategies.base_strategy import BaseStrategy
from modules.market_analyzer import MarketAnalyzer
from modules.position_manager import PositionManager


class TestMultiIndicatorStrategy(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения"""
        # Создаем мок-объекты
        self.market_analyzer = Mock(spec=MarketAnalyzer)
        self.position_manager = Mock(spec=PositionManager)

        # Инициализация стратегии
        self.strategy = MultiIndicatorStrategy(
            market_analyzer=self.market_analyzer,
            position_manager=self.position_manager
        )

        # Создаем тестовые данные
        self.test_data = self._generate_test_data()

    def _generate_test_data(self):
        """Генерация тестовых данных"""
        dates = pd.date_range(start='2024-01-01', periods=100, freq='15T')

        df = pd.DataFrame({
            'timestamp': dates,
            'open': np.random.uniform(1000, 2000, 100),
            'high': np.random.uniform(1000, 2000, 100),
            'low': np.random.uniform(1000, 2000, 100),
            'close': np.random.uniform(1000, 2000, 100),
            'volume': np.random.uniform(100000, 1000000, 100)
        })

        # Добавляем индикаторы
        df['ema_8'] = df['close'].ewm(span=8).mean()
        df['ema_21'] = df['close'].ewm(span=21).mean()
        df['ema_50'] = df['close'].ewm(span=50).mean()
        df['rsi'] = self._calculate_test_rsi(df['close'])
        df['macd'] = df['close'].ewm(span=12).mean() - df['close'].ewm(span=26).mean()
        df['volume_sma'] = df['volume'].rolling(window=20).mean()

        return df

    def _calculate_test_rsi(self, prices, period=14):
        """Расчет RSI для тестовых данных"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def test_strategy_initialization(self):
        """Тест инициализации стратегии"""
        self.assertIsInstance(self.strategy, BaseStrategy)
        self.assertEqual(self.strategy.name, "MultiIndicatorStrategy")

    def test_generate_signal_buy(self):
        """Тест генерации сигнала на покупку"""
        # Подготавливаем данные для сигнала покупки
        test_data = self.test_data.copy()
        test_data.loc[test_data.index[-1], 'ema_8'] = 1500
        test_data.loc[test_data.index[-1], 'ema_21'] = 1400
        test_data.loc[test_data.index[-1], 'ema_50'] = 1300
        test_data.loc[test_data.index[-1], 'rsi'] = 35
        test_data.loc[test_data.index[-1], 'macd'] = 10
        test_data.loc[test_data.index[-1], 'volume'] = 800000
        test_data.loc[test_data.index[-1], 'volume_sma'] = 500000

        signal = self.strategy.generate_signal({'df': test_data})

        self.assertIsNotNone(signal)
        self.assertEqual(signal['type'], 'LONG')
        self.assertTrue(0 <= signal['strength'] <= 1)

    def test_generate_signal_sell(self):
        """Тест генерации сигнала на продажу"""
        # Подготавливаем данные для сигнала продажи
        test_data = self.test_data.copy()
        test_data.loc[test_data.index[-1], 'ema_8'] = 1300
        test_data.loc[test_data.index[-1], 'ema_21'] = 1400
        test_data.loc[test_data.index[-1], 'ema_50'] = 1500
        test_data.loc[test_data.index[-1], 'rsi'] = 75
        test_data.loc[test_data.index[-1], 'macd'] = -10
        test_data.loc[test_data.index[-1], 'volume'] = 800000
        test_data.loc[test_data.index[-1], 'volume_sma'] = 500000

        signal = self.strategy.generate_signal({'df': test_data})

        self.assertIsNotNone(signal)
        self.assertEqual(signal['type'], 'SHORT')
        self.assertTrue(0 <= signal['strength'] <= 1)

    def test_validate_signal(self):
        """Тест валидации сигнала"""
        valid_signal = {
            'type': 'LONG',
            'strength': 0.8,
            'price': 1500,
            'timestamp': datetime.now()
        }

        self.assertTrue(self.strategy.validate_signal(valid_signal))

        # Тест с невалидным сигналом
        invalid_signal = {
            'type': 'LONG',
            'strength': 0.3,  # Слишком низкая сила сигнала
            'price': 1500,
            'timestamp': datetime.now()
        }

        self.assertFalse(self.strategy.validate_signal(invalid_signal))

    def test_execute_strategy(self):
        """Тест выполнения стратегии"""
        # Подготовка тестовых данных
        test_data = {
            'df': self.test_data,
            'symbol': 'ETHUSDT',
            'account_balance': 10000
        }

        # Мокаем необходимые методы
        self.market_analyzer.get_market_data.return_value = test_data['df']
        self.position_manager.open_position.return_value = True

        # Выполняем стратегию
        result = self.strategy.execute('ETHUSDT', test_data)

        # Проверяем результат
        if result:
            self.assertIn('action', result)
            if result['action'] == 'OPEN':
                self.assertIn('signal', result)
                self.assertIn('position_size', result)

    def test_calculate_signal_strength(self):
        """Тест расчета силы сигнала"""
        test_row = pd.Series({
            'rsi': 30,
            'macd': 0.02,
            'volume': 800000,
            'volume_sma': 500000
        })

        strength = self.strategy.calculate_signal_strength(test_row)
        self.assertTrue(0 <= strength <= 1)

    def test_error_handling(self):
        """Тест обработки ошибок"""
        # Тест с некорректными данными
        with self.assertRaises(Exception):
            self.strategy.generate_signal({'df': None})

    def tearDown(self):
        """Очистка после тестов"""
        pass


if __name__ == '__main__':
    unittest.main()