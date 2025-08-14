import logging
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np


class PerformanceTracker:
    """Трекер производительности торгового бота с расширенной аналитикой"""

    def __init__(self):
        """Инициализация трекера производительности"""
        self.logger = logging.getLogger(__name__)

        # Основные данные
        self.trades: List[Dict] = []
        self.equity_curve: List[Dict] = []
        self.daily_stats: Dict = {}

        # Метрики производительности
        self.total_pnl: float = 0.0
        self.start_time = datetime.now()
        self.initial_balance: float = 0.0
        self.current_balance: float = 0.0

        # Статистика сделок
        self.max_drawdown: float = 0.0
        self.max_drawdown_duration: timedelta = timedelta(0)
        self.best_trade: float = 0.0
        self.worst_trade: float = 0.0
        self.consecutive_wins: int = 0
        self.consecutive_losses: int = 0
        self.max_consecutive_wins: int = 0
        self.max_consecutive_losses: int = 0

        # Анализ по символам
        self.symbol_performance: Dict[str, Dict] = {}

        # Настройка директории для сохранения
        self.data_dir = os.path.join("data", "performance")
        try:
            os.makedirs(self.data_dir, exist_ok=True)
        except Exception as e:
            # Если не удается создать в data/performance, создаем в текущей директории
            self.logger.warning(f"Could not create {self.data_dir}: {e}")
            self.data_dir = "performance_data"
            os.makedirs(self.data_dir, exist_ok=True)
            self.logger.info(f"Using alternative directory: {self.data_dir}")

        self.logger.info("PerformanceTracker initialized")

    def set_initial_balance(self, balance: float):
        """Установка начального баланса"""
        self.initial_balance = balance
        self.current_balance = balance
        self.logger.info(f"Initial balance set to: ${balance:.2f}")

    def log_trade(self, trade_data: Dict[str, Any]) -> None:
        """
        Запись информации о сделке

        Args:
            trade_data: Словарь с данными о сделке
        """
        try:
            # Извлекаем данные из trade_data
            symbol = trade_data.get('symbol', 'UNKNOWN')
            entry_price = float(trade_data.get('entry_price', 0))
            exit_price = float(trade_data.get('exit_price', 0))
            size = float(trade_data.get('size', 0))
            direction = trade_data.get('direction', 'UNKNOWN')
            pnl = float(trade_data.get('pnl', 0))
            timestamp = trade_data.get('timestamp', datetime.now())

            # Дополнительные данные
            fees = float(trade_data.get('fees', 0))
            slippage = float(trade_data.get('slippage', 0))
            duration = trade_data.get('duration', timedelta(0))

            # Расчет метрик сделки
            position_value = entry_price * size
            roi = (pnl / position_value * 100) if position_value > 0 else 0
            net_pnl = pnl - fees

            trade = {
                'id': len(self.trades) + 1,
                'symbol': symbol,
                'entry_price': entry_price,
                'exit_price': exit_price,
                'size': size,
                'direction': direction,
                'pnl': pnl,
                'net_pnl': net_pnl,
                'fees': fees,
                'slippage': slippage,
                'roi': roi,
                'position_value': position_value,
                'duration': duration,
                'timestamp': timestamp,
                'entry_time': trade_data.get('entry_time', timestamp),
                'exit_time': trade_data.get('exit_time', timestamp)
            }

            self.trades.append(trade)
            self.total_pnl += net_pnl
            self.current_balance += net_pnl

            # Обновление статистики
            self._update_statistics(trade)
            self._update_equity_curve(trade)
            self._update_symbol_performance(trade)

            self.logger.info(f"Trade logged: {symbol} {direction} PnL: ${net_pnl:.2f}")

        except Exception as e:
            self.logger.error(f"Error logging trade: {e}", exc_info=True)

    def _update_statistics(self, trade: Dict) -> None:
        """Обновление статистических показателей"""
        try:
            pnl = trade['net_pnl']

            # Обновление лучшей/худшей сделки
            self.best_trade = max(self.best_trade, pnl)
            self.worst_trade = min(self.worst_trade, pnl)

            # Обновление серий выигрышных/проигрышных сделок
            if pnl > 0:
                self.consecutive_wins += 1
                self.consecutive_losses = 0
                self.max_consecutive_wins = max(self.max_consecutive_wins, self.consecutive_wins)
            else:
                self.consecutive_losses += 1
                self.consecutive_wins = 0
                self.max_consecutive_losses = max(self.max_consecutive_losses, self.consecutive_losses)

            # Обновление дневной статистики
            date = trade['timestamp'].date()
            if date not in self.daily_stats:
                self.daily_stats[date] = {
                    'pnl': 0.0,
                    'trades': 0,
                    'wins': 0,
                    'losses': 0,
                    'volume': 0.0,
                    'fees': 0.0
                }

            daily = self.daily_stats[date]
            daily['pnl'] += pnl
            daily['trades'] += 1
            daily['volume'] += trade['position_value']
            daily['fees'] += trade['fees']

            if pnl > 0:
                daily['wins'] += 1
            else:
                daily['losses'] += 1

            # Расчет просадки
            self._calculate_drawdown()

        except Exception as e:
            self.logger.error(f"Error updating statistics: {e}")

    def _update_equity_curve(self, trade: Dict) -> None:
        """Обновление кривой эквити"""
        try:
            equity_point = {
                'timestamp': trade['timestamp'],
                'balance': self.current_balance,
                'pnl': trade['net_pnl'],
                'cumulative_pnl': self.total_pnl,
                'trade_id': trade['id']
            }
            self.equity_curve.append(equity_point)

        except Exception as e:
            self.logger.error(f"Error updating equity curve: {e}")

    def _update_symbol_performance(self, trade: Dict) -> None:
        """Обновление статистики по символам"""
        try:
            symbol = trade['symbol']

            if symbol not in self.symbol_performance:
                self.symbol_performance[symbol] = {
                    'trades': 0,
                    'wins': 0,
                    'losses': 0,
                    'total_pnl': 0.0,
                    'volume': 0.0,
                    'best_trade': 0.0,
                    'worst_trade': 0.0
                }

            perf = self.symbol_performance[symbol]
            pnl = trade['net_pnl']

            perf['trades'] += 1
            perf['total_pnl'] += pnl
            perf['volume'] += trade['position_value']
            perf['best_trade'] = max(perf['best_trade'], pnl)
            perf['worst_trade'] = min(perf['worst_trade'], pnl)

            if pnl > 0:
                perf['wins'] += 1
            else:
                perf['losses'] += 1

        except Exception as e:
            self.logger.error(f"Error updating symbol performance: {e}")

    def _calculate_drawdown(self) -> None:
        """Расчет максимальной просадки"""
        try:
            if not self.equity_curve:
                return

            balances = [point['balance'] for point in self.equity_curve]
            peak = np.maximum.accumulate(balances)
            drawdown = (peak - balances) / peak * 100

            max_dd_idx = np.argmax(drawdown)
            self.max_drawdown = float(drawdown[max_dd_idx])

            # Расчет продолжительности просадки
            if max_dd_idx > 0:
                peak_time = None
                for i in range(max_dd_idx, -1, -1):
                    if balances[i] == peak[max_dd_idx]:
                        peak_time = self.equity_curve[i]['timestamp']
                        break

                if peak_time:
                    recovery_time = self.equity_curve[max_dd_idx]['timestamp']
                    self.max_drawdown_duration = recovery_time - peak_time

        except Exception as e:
            self.logger.error(f"Error calculating drawdown: {e}")

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Получение детальных метрик производительности"""
        try:
            if not self.trades:
                return self._get_empty_metrics()

            total_trades = len(self.trades)
            winning_trades = len([t for t in self.trades if t['net_pnl'] > 0])
            losing_trades = total_trades - winning_trades

            # Базовые метрики
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            avg_win = np.mean([t['net_pnl'] for t in self.trades if t['net_pnl'] > 0]) if winning_trades > 0 else 0
            avg_loss = np.mean([t['net_pnl'] for t in self.trades if t['net_pnl'] < 0]) if losing_trades > 0 else 0

            # Коэффициенты
            profit_factor = abs(avg_win * winning_trades / (
                        avg_loss * losing_trades)) if losing_trades > 0 and avg_loss != 0 else float('inf')
            expectancy = (win_rate / 100 * avg_win) + ((100 - win_rate) / 100 * avg_loss)

            # Временные метрики
            trading_duration = datetime.now() - self.start_time
            total_return = ((
                                        self.current_balance - self.initial_balance) / self.initial_balance * 100) if self.initial_balance > 0 else 0

            metrics = {
                # Основные метрики
                'total_pnl': round(self.total_pnl, 2),
                'total_return_pct': round(total_return, 2),
                'current_balance': round(self.current_balance, 2),
                'initial_balance': round(self.initial_balance, 2),

                # Статистика сделок
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': losing_trades,
                'win_rate': round(win_rate, 2),

                # Средние значения
                'avg_pnl': round(self.total_pnl / total_trades, 2) if total_trades > 0 else 0,
                'avg_win': round(avg_win, 2),
                'avg_loss': round(avg_loss, 2),

                # Экстремумы
                'best_trade': round(self.best_trade, 2),
                'worst_trade': round(self.worst_trade, 2),
                'max_drawdown_pct': round(self.max_drawdown, 2),
                'max_drawdown_duration': str(self.max_drawdown_duration),

                # Серии
                'max_consecutive_wins': self.max_consecutive_wins,
                'max_consecutive_losses': self.max_consecutive_losses,
                'current_streak': self.consecutive_wins if self.consecutive_wins > 0 else -self.consecutive_losses,

                # Коэффициенты
                'profit_factor': round(profit_factor, 2) if profit_factor != float('inf') else 'N/A',
                'expectancy': round(expectancy, 2),
                'sharpe_ratio': round(self._calculate_sharpe_ratio(), 2),
                'sortino_ratio': round(self._calculate_sortino_ratio(), 2),

                # Временные метрики
                'trading_duration': str(trading_duration),
                'trades_per_day': round(total_trades / max(trading_duration.days, 1), 2),

                # Дополнительные метрики
                'total_fees': round(sum(t['fees'] for t in self.trades), 2),
                'total_volume': round(sum(t['position_value'] for t in self.trades), 2),
                'avg_trade_duration': str(self._calculate_avg_trade_duration()),

                'last_update': datetime.now().isoformat()
            }

            return metrics

        except Exception as e:
            self.logger.error(f"Error calculating performance metrics: {e}")
            return self._get_empty_metrics()

    def _calculate_sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
        """Расчет коэффициента Шарпа"""
        try:
            if len(self.trades) < 2:
                return 0.0

            returns = pd.Series([t['roi'] for t in self.trades])
            excess_returns = returns - (risk_free_rate / 252)

            if excess_returns.std() == 0:
                return 0.0

            return float(np.sqrt(252) * (excess_returns.mean() / excess_returns.std()))

        except Exception as e:
            self.logger.error(f"Error calculating Sharpe ratio: {e}")
            return 0.0

    def _calculate_sortino_ratio(self, risk_free_rate: float = 0.02) -> float:
        """Расчет коэффициента Сортино"""
        try:
            if len(self.trades) < 2:
                return 0.0

            returns = pd.Series([t['roi'] for t in self.trades])
            excess_returns = returns - (risk_free_rate / 252)
            downside_returns = excess_returns[excess_returns < 0]

            if len(downside_returns) == 0 or downside_returns.std() == 0:
                return 0.0

            return float(np.sqrt(252) * (excess_returns.mean() / downside_returns.std()))

        except Exception as e:
            self.logger.error(f"Error calculating Sortino ratio: {e}")
            return 0.0

    def _calculate_avg_trade_duration(self) -> timedelta:
        """Расчет средней продолжительности сделки"""
        try:
            durations = [t['duration'] for t in self.trades if isinstance(t['duration'], timedelta)]
            if not durations:
                return timedelta(0)

            total_seconds = sum(d.total_seconds() for d in durations)
            avg_seconds = total_seconds / len(durations)
            return timedelta(seconds=avg_seconds)

        except Exception as e:
            self.logger.error(f"Error calculating average trade duration: {e}")
            return timedelta(0)

    def get_daily_report(self) -> pd.DataFrame:
        """Получение ежедневного отчета"""
        try:
            if not self.daily_stats:
                return pd.DataFrame()

            df = pd.DataFrame.from_dict(self.daily_stats, orient='index')
            df['win_rate'] = (df['wins'] / df['trades'] * 100).round(2)
            df['avg_pnl'] = (df['pnl'] / df['trades']).round(2)
            df['profit_factor'] = np.where(
                df['losses'] > 0,
                (df['wins'] * df['pnl']) / (df['losses'] * abs(df['pnl'])),
                np.inf
            )
            df.index.name = 'date'
            return df.sort_index()

        except Exception as e:
            self.logger.error(f"Error generating daily report: {e}")
            return pd.DataFrame()

    def get_symbol_report(self) -> pd.DataFrame:
        """Получение отчета по символам"""
        try:
            if not self.symbol_performance:
                return pd.DataFrame()

            df = pd.DataFrame.from_dict(self.symbol_performance, orient='index')
            df['win_rate'] = (df['wins'] / df['trades'] * 100).round(2)
            df['avg_pnl'] = (df['total_pnl'] / df['trades']).round(2)
            df.index.name = 'symbol'
            return df.sort_values('total_pnl', ascending=False)

        except Exception as e:
            self.logger.error(f"Error generating symbol report: {e}")
            return pd.DataFrame()

    def get_equity_curve_df(self) -> pd.DataFrame:
        """Получение кривой эквити в виде DataFrame"""
        try:
            if not self.equity_curve:
                return pd.DataFrame()

            df = pd.DataFrame(self.equity_curve)
            df.set_index('timestamp', inplace=True)
            return df

        except Exception as e:
            self.logger.error(f"Error generating equity curve DataFrame: {e}")
            return pd.DataFrame()

    def save_performance_data(self, filename_prefix: str = "performance") -> None:
        """Сохранение данных о производительности"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Сохранение сделок
            if self.trades:
                trades_df = pd.DataFrame(self.trades)
                trades_file = os.path.join(self.data_dir, f"{filename_prefix}_trades_{timestamp}.csv")
                trades_df.to_csv(trades_file, index=False)
                self.logger.info(f"Trades data saved to {trades_file}")

            # Сохранение метрик
            metrics = self.get_performance_metrics()
            metrics_file = os.path.join(self.data_dir, f"{filename_prefix}_metrics_{timestamp}.json")
            with open(metrics_file, 'w') as f:
                json.dump(metrics, f, indent=2, default=str)
            self.logger.info(f"Metrics saved to {metrics_file}")

            # Сохранение кривой эквити
            if self.equity_curve:
                equity_df = self.get_equity_curve_df()
                equity_file = os.path.join(self.data_dir, f"{filename_prefix}_equity_{timestamp}.csv")
                equity_df.to_csv(equity_file)
                self.logger.info(f"Equity curve saved to {equity_file}")

            # Сохранение дневного отчета
            daily_df = self.get_daily_report()
            if not daily_df.empty:
                daily_file = os.path.join(self.data_dir, f"{filename_prefix}_daily_{timestamp}.csv")
                daily_df.to_csv(daily_file)
                self.logger.info(f"Daily report saved to {daily_file}")

        except Exception as e:
            self.logger.error(f"Error saving performance data: {e}")

    def load_performance_data(self, trades_file: str) -> bool:
        """Загрузка данных о производительности из файла"""
        try:
            if not os.path.exists(trades_file):
                self.logger.warning(f"File {trades_file} not found")
                return False

            trades_df = pd.read_csv(trades_file)
            trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])

            for _, row in trades_df.iterrows():
                trade_data = row.to_dict()
                self.log_trade(trade_data)

            self.logger.info(f"Loaded {len(trades_df)} trades from {trades_file}")
            return True

        except Exception as e:
            self.logger.error(f"Error loading performance data: {e}")
            return False

    def reset_performance(self) -> None:
        """Сброс всех данных о производительности"""
        try:
            self.trades.clear()
            self.equity_curve.clear()
            self.daily_stats.clear()
            self.symbol_performance.clear()

            self.total_pnl = 0.0
            self.current_balance = self.initial_balance
            self.max_drawdown = 0.0
            self.max_drawdown_duration = timedelta(0)
            self.best_trade = 0.0
            self.worst_trade = 0.0
            self.consecutive_wins = 0
            self.consecutive_losses = 0
            self.max_consecutive_wins = 0
            self.max_consecutive_losses = 0

            self.start_time = datetime.now()
            self.logger.info("Performance data reset")

        except Exception as e:
            self.logger.error(f"Error resetting performance data: {e}")

    def _get_empty_metrics(self) -> Dict[str, Any]:
        """Возвращает пустые метрики при отсутствии сделок"""
        return {
            'total_pnl': 0.0,
            'total_return_pct': 0.0,
            'current_balance': self.current_balance,
            'initial_balance': self.initial_balance,
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0.0,
            'avg_pnl': 0.0,
            'avg_win': 0.0,
            'avg_loss': 0.0,
            'best_trade': 0.0,
            'worst_trade': 0.0,
            'max_drawdown_pct': 0.0,
            'max_drawdown_duration': '0:00:00',
            'max_consecutive_wins': 0,
            'max_consecutive_losses': 0,
            'current_streak': 0,
            'profit_factor': 'N/A',
            'expectancy': 0.0,
            'sharpe_ratio': 0.0,
            'sortino_ratio': 0.0,
            'trading_duration': str(datetime.now() - self.start_time),
            'trades_per_day': 0.0,
            'total_fees': 0.0,
            'total_volume': 0.0,
            'avg_trade_duration': '0:00:00',
            'last_update': datetime.now().isoformat()
        }

    def get_performance_summary(self) -> str:
        """Получение краткой сводки производительности"""
        try:
            metrics = self.get_performance_metrics()

            summary = f"""
📊 PERFORMANCE SUMMARY
{'=' * 50}
💰 Total PnL: ${metrics['total_pnl']} ({metrics['total_return_pct']}%)
📈 Current Balance: ${metrics['current_balance']}
🎯 Win Rate: {metrics['win_rate']}% ({metrics['winning_trades']}/{metrics['total_trades']})
📉 Max Drawdown: {metrics['max_drawdown_pct']}%
⚡ Sharpe Ratio: {metrics['sharpe_ratio']}
🔥 Current Streak: {metrics['current_streak']}
⏱️  Trading Duration: {metrics['trading_duration']}
{'=' * 50}
            """
            return summary.strip()

        except Exception as e:
            self.logger.error(f"Error generating performance summary: {e}")
            return "Error generating summary"