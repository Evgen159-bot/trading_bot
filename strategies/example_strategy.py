"""
Пример пользовательской стратегии
"""
from strategies.base_strategy import BaseStrategy
import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime


class ExampleStrategy(BaseStrategy):
    """Пример простой стратегии"""

    def __init__(self):
        super().__init__(name="ExampleStrategy")

    def generate_signal(self, data: pd.DataFrame, symbol: str = None) -> Optional[Dict[str, Any]]:
        """Генерация сигнала"""
        if data.empty or len(data) < 20:
            return None

        # Простая логика: покупаем если цена выше SMA20
        sma20 = data['close'].rolling(20).mean().iloc[-1]
        current_price = data['close'].iloc[-1]

        if current_price > sma20:
            return {
                'action': 'BUY',
                'entry_price': current_price,
                'timestamp': datetime.now(),
                'confidence': 0.7
            }

        return None

    def execute(self, symbol: str, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Выполнение стратегии"""
        df = market_data.get('df')
        if df is None:
            return None

        signal = self.generate_signal(df, symbol)
        return signal
