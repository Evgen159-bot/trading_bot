import logging
import time
import pandas as pd
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from pybit.unified_trading import HTTP
from config.trading_config import TradingConfig


class DataFetcher:
    def __init__(self, client: HTTP = None):
        self.logger = logging.getLogger(__name__)
        self.retry_count = TradingConfig.MAX_RETRIES
        self.retry_delay = TradingConfig.RETRY_DELAY
        self.rate_limit_delay = 1.0  # Задержка между запросами для избежания rate limit

        if client is None:
            self.client = HTTP(
                testnet=TradingConfig.TESTNET,
                api_key=TradingConfig.API_KEY,
                api_secret=TradingConfig.API_SECRET,
                recv_window=TradingConfig.RECV_WINDOW
            )
        else:
            self.client = client

        self.testnet = TradingConfig.TESTNET
        self.last_request_time = 0

        try:
            self.logger.info("Initializing ByBit client...")
            self._test_connection()
        except Exception as e:
            self.logger.error(f"Failed to initialize DataFetcher: {str(e)}")
            raise

    def _rate_limit_check(self):
        """Проверка rate limit - добавляем задержку между запросами"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def _test_connection(self):
        """Тестирование подключения к ByBit"""
        try:
            self._rate_limit_check()
            response = self.client.get_tickers(category="linear", symbol="BTCUSDT")

            if response.get('retCode') == 0:
                self.logger.info("Successfully connected to ByBit.")
            else:
                error_msg = response.get('retMsg', 'Unknown error')
                raise Exception(f"Connection test failed: {error_msg}")

        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            raise

    def get_kline(self, symbol: str, interval: str, start_time: int, end_time: int) -> Optional[pd.DataFrame]:
        """
        Получение данных свечей и возврат в виде pandas DataFrame

        :param symbol: Торговая пара (например, 'ETHUSDT')
        :param interval: Интервал ('1', '5', '15', '30', '60', '240', 'D')
        :param start_time: Время начала в timestamp (секунды)
        :param end_time: Время окончания в timestamp (секунды)
        :return: DataFrame с колонками [open, high, low, close, volume] или None
        """
        # Валидация интервала
        valid_intervals = ['1', '3', '5', '15', '30', '60', '120', '240', '360', '720', 'D', 'M', 'W']
        if interval not in valid_intervals:
            self.logger.error(f"Invalid interval: {interval}. Valid intervals: {valid_intervals}")
            return None

        # Конвертация в миллисекунды для ByBit API
        start_ms = int(start_time * 1000) if start_time < 1e12 else int(start_time)
        end_ms = int(end_time * 1000) if end_time < 1e12 else int(end_time)

        for attempt in range(self.retry_count):
            try:
                self.logger.info(
                    f"Attempt {attempt + 1}/{self.retry_count}: Fetching kline for {symbol} "
                    f"with interval {interval}, start: {start_ms}, end: {end_ms}"
                )

                self._rate_limit_check()

                response = self.client.get_kline(
                    category="linear",
                    symbol=symbol,
                    interval=interval,
                    start=str(start_ms),
                    end=str(end_ms),
                    limit=200
                )

                if response.get('retCode') == 0 and response.get('result', {}).get('list'):
                    klines = response['result']['list']

                    if not klines:
                        self.logger.warning(f"No kline data returned for {symbol}")
                        return None

                    # Преобразование в DataFrame
                    df_data = []
                    for kline in klines:
                        try:
                            df_data.append({
                                'timestamp': datetime.fromtimestamp(int(kline[0]) / 1000, tz=timezone.utc),
                                'open': float(kline[1]),
                                'high': float(kline[2]),
                                'low': float(kline[3]),
                                'close': float(kline[4]),
                                'volume': float(kline[5])
                            })
                        except (ValueError, IndexError) as e:
                            self.logger.warning(f"Error parsing kline data: {e}")
                            continue

                    if not df_data:
                        self.logger.warning(f"No valid kline data for {symbol}")
                        return None

                    df = pd.DataFrame(df_data)
                    df = df.sort_values('timestamp').reset_index(drop=True)

                    self.logger.info(f"Successfully fetched {len(df)} klines for {symbol}")
                    return df

                else:
                    error_msg = response.get('retMsg', 'Unknown error')
                    self.logger.warning(f"Attempt {attempt + 1} failed for {symbol}: {error_msg}")

                    # Если ошибка rate limit, увеличиваем задержку
                    if 'rate limit' in error_msg.lower():
                        time.sleep(self.retry_delay * 2)
                    else:
                        time.sleep(self.retry_delay)

            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} error in get_kline for {symbol}: {e}")
                time.sleep(self.retry_delay)

        self.logger.error(f"All {self.retry_count} attempts failed for {symbol}")
        return None

    def get_current_price(self, symbol: str) -> Optional[float]:
        """Получение текущей цены символа"""
        for attempt in range(self.retry_count):
            try:
                self._rate_limit_check()

                response = self.client.get_tickers(category="linear", symbol=symbol)

                if response.get('retCode') == 0 and response.get('result', {}).get('list'):
                    price = float(response['result']['list'][0]['lastPrice'])
                    self.logger.debug(f"Current price for {symbol}: {price}")
                    return price
                else:
                    error_msg = response.get('retMsg', 'Unknown error')
                    self.logger.warning(f"Failed to get price for {symbol}: {error_msg}")

            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} error getting price for {symbol}: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)

        self.logger.error(f"Failed to get current price for {symbol} after {self.retry_count} attempts")
        return None

    def get_account_balance(self, coin: str = "USDT") -> Optional[float]:
        """Получение баланса аккаунта"""
        for attempt in range(self.retry_count):
            try:
                self._rate_limit_check()

                response = self.client.get_wallet_balance(accountType="UNIFIED", coin=coin)

                if response.get('retCode') == 0 and response.get('result', {}).get('list'):
                    wallet_list = response['result']['list']

                    if wallet_list and wallet_list[0].get('coin'):
                        for asset in wallet_list[0]['coin']:
                            if asset.get('coin') == coin:
                                balance = float(asset.get('walletBalance', 0))
                                self.logger.debug(f"Account balance ({coin}): {balance}")
                                return balance

                    self.logger.warning(f"Coin {coin} not found in wallet")
                    # Для TESTNET возвращаем фиксированный баланс
                    if self.testnet:
                        return 1000.0
                    return 0.0
                else:
                    error_msg = response.get('retMsg', 'Unknown error')
                    self.logger.warning(f"Failed to get balance: {error_msg}")

                    # Для TESTNET возвращаем фиксированный баланс при ошибках
                    if self.testnet:
                        self.logger.info("TESTNET: Returning fixed balance $1000")
                        return 1000.0

                    # Если это testnet и нет баланса, возвращаем тестовый баланс
                    if self.testnet and 'insufficient' in error_msg.lower():
                        self.logger.info("Testnet detected with no balance, returning default test balance")
                        return 1000.0

            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} error getting balance: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)

        self.logger.error(f"Failed to get account balance after {self.retry_count} attempts")
        # Для TESTNET всегда возвращаем фиксированный баланс
        if self.testnet:
            self.logger.warning("TESTNET: Returning fallback balance $1000")
            return 1000.0
        return None
        if self.testnet:
            self.logger.warning("Returning default testnet balance due to API issues")
            return 1000.0
        return 0.0

    def get_position_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Получение информации о позиции"""
        for attempt in range(self.retry_count):
            try:
                self._rate_limit_check()

                response = self.client.get_positions(category="linear", symbol=symbol)

                if response.get('retCode') == 0 and response.get('result', {}).get('list'):
                    positions = response['result']['list']

                    for position in positions:
                        if position.get('symbol') == symbol and float(position.get('size', 0)) > 0:
                            return {
                                'symbol': position.get('symbol'),
                                'side': position.get('side'),
                                'size': float(position.get('size', 0)),
                                'entry_price': float(position.get('avgPrice', 0)),
                                'mark_price': float(position.get('markPrice', 0)),
                                'unrealized_pnl': float(position.get('unrealisedPnl', 0)),
                                'leverage': float(position.get('leverage', 1))
                            }

                    # Позиция не найдена или размер = 0
                    return None
                else:
                    error_msg = response.get('retMsg', 'Unknown error')
                    self.logger.warning(f"Failed to get position info for {symbol}: {error_msg}")

            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} error getting position for {symbol}: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)

        self.logger.error(f"Failed to get position info for {symbol} after {self.retry_count} attempts")
        return None

    def get_order_book(self, symbol: str, limit: int = 25) -> Optional[Dict[str, Any]]:
        """Получение стакана заявок"""
        try:
            self._rate_limit_check()

            response = self.client.get_orderbook(category="linear", symbol=symbol, limit=limit)

            if response.get('retCode') == 0 and response.get('result'):
                orderbook = response['result']
                return {
                    'symbol': symbol,
                    'bids': [[float(bid[0]), float(bid[1])] for bid in orderbook.get('b', [])],
                    'asks': [[float(ask[0]), float(ask[1])] for ask in orderbook.get('a', [])],
                    'timestamp': datetime.now(timezone.utc)
                }
            else:
                error_msg = response.get('retMsg', 'Unknown error')
                self.logger.warning(f"Failed to get orderbook for {symbol}: {error_msg}")
                return None

        except Exception as e:
            self.logger.error(f"Error getting orderbook for {symbol}: {e}")
            return None

    def get_server_time(self) -> Optional[datetime]:
        """Получение времени сервера"""
        try:
            self._rate_limit_check()

            response = self.client.get_server_time()

            if response.get('retCode') == 0:
                server_time_ms = int(response['result']['timeSecond']) * 1000
                return datetime.fromtimestamp(server_time_ms / 1000, tz=timezone.utc)
            else:
                error_msg = response.get('retMsg', 'Unknown error')
                self.logger.warning(f"Failed to get server time: {error_msg}")
                return None

        except Exception as e:
            self.logger.error(f"Error getting server time: {e}")
            return None

    def health_check(self) -> bool:
        """Проверка здоровья соединения"""
        try:
            server_time = self.get_server_time()
            if server_time:
                self.logger.info("DataFetcher health check: OK")
                return True
            else:
                self.logger.warning("DataFetcher health check: FAILED")
                return False
        except Exception as e:
            self.logger.error(f"DataFetcher health check error: {e}")
            return False