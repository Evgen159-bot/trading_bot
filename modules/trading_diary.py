import logging
import os
import json
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
from pathlib import Path


class TradingDiary:
    """Дневник трейдинга для отслеживания ежедневной торговой активности"""

    def __init__(self):
        """Инициализация дневника трейдинга"""
        self.logger = logging.getLogger(__name__)

        # Создаем директорию для дневника
        self.diary_dir = Path("data/diary")
        self.diary_dir.mkdir(parents=True, exist_ok=True)

        # Текущий торговый день
        self.current_date = date.today()
        self.session_start_time = datetime.now()
        self.session_start_balance = 0.0
        self.current_balance = 0.0

        # Данные текущего дня
        self.daily_data = {
            'date': self.current_date.isoformat(),
            'session_start': self.session_start_time.isoformat(),
            'start_balance': 0.0,
            'current_balance': 0.0,
            'positions': [],
            'trades': [],
            'daily_stats': {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_pnl': 0.0,
                'total_fees': 0.0,
                'max_profit': 0.0,
                'max_loss': 0.0,
                'win_rate': 0.0,
                'profit_factor': 0.0
            },
            'session_end': None,
            'end_balance': 0.0,
            'daily_return': 0.0,
            'daily_return_pct': 0.0
        }

        # Загружаем данные текущего дня если они есть
        self._load_daily_data()

        self.logger.info("TradingDiary initialized successfully")

    def start_trading_session(self, initial_balance: float) -> None:
        """Начало торговой сессии"""
        try:
            self.session_start_balance = initial_balance
            self.current_balance = initial_balance

            # Проверяем, новый ли это день
            if self.current_date != date.today():
                self._save_daily_data()  # Сохраняем предыдущий день
                self._start_new_day()

            self.daily_data['start_balance'] = initial_balance
            self.daily_data['current_balance'] = initial_balance
            self.daily_data['session_start'] = datetime.now().isoformat()

            self.logger.info(f"Trading session started with balance: ${initial_balance:.2f}")
            print(f"\n📅 Торговая сессия начата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
            print(f"💰 Начальный баланс: ${initial_balance:.2f}")

        except Exception as e:
            self.logger.error(f"Error starting trading session: {e}")

    def log_position_opened(self, symbol: str, direction: str, size: float,
                            entry_price: float, stop_loss: float = None,
                            take_profit: float = None) -> None:
        """Логирование открытия позиции"""
        try:
            position = {
                'id': len(self.daily_data['positions']) + 1,
                'symbol': symbol,
                'direction': direction,
                'size': size,
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'open_time': datetime.now().isoformat(),
                'status': 'OPEN',
                'close_time': None,
                'close_price': None,
                'pnl': 0.0,
                'fees': 0.0,
                'close_reason': None
            }

            self.daily_data['positions'].append(position)

            self.logger.info(f"Position opened: {symbol} {direction} {size} @ {entry_price}")
            print(f"\n📈 Позиция открыта:")
            print(f"   🎯 {symbol} | {direction} | Размер: {size}")
            print(f"   💵 Цена входа: ${entry_price:.4f}")
            if stop_loss:
                print(f"   🛑 Стоп-лосс: ${stop_loss:.4f}")
            if take_profit:
                print(f"   🎯 Тейк-профит: ${take_profit:.4f}")

            self._save_daily_data()

        except Exception as e:
            self.logger.error(f"Error logging position opened: {e}")

    def log_position_closed(self, symbol: str, close_price: float, pnl: float,
                            fees: float = 0.0, close_reason: str = "manual") -> None:
        """Логирование закрытия позиции"""
        try:
            # Находим открытую позицию
            position = None
            for pos in self.daily_data['positions']:
                if pos['symbol'] == symbol and pos['status'] == 'OPEN':
                    position = pos
                    break

            if not position:
                self.logger.warning(f"No open position found for {symbol}")
                return

            # Обновляем позицию
            position['status'] = 'CLOSED'
            position['close_time'] = datetime.now().isoformat()
            position['close_price'] = close_price
            position['pnl'] = pnl
            position['fees'] = fees
            position['close_reason'] = close_reason

            # Создаем запись о сделке
            trade = {
                'id': len(self.daily_data['trades']) + 1,
                'symbol': symbol,
                'direction': position['direction'],
                'size': position['size'],
                'entry_price': position['entry_price'],
                'exit_price': close_price,
                'pnl': pnl,
                'fees': fees,
                'net_pnl': pnl - fees,
                'open_time': position['open_time'],
                'close_time': position['close_time'],
                'duration': self._calculate_duration(position['open_time'], position['close_time']),
                'close_reason': close_reason,
                'roi_pct': (pnl / (position['entry_price'] * position['size']) * 100) if position['entry_price'] *
                                                                                         position['size'] > 0 else 0
            }

            self.daily_data['trades'].append(trade)

            # Обновляем баланс
            self.current_balance += (pnl - fees)
            self.daily_data['current_balance'] = self.current_balance

            # Обновляем статистику
            self._update_daily_stats(trade)

            # Выводим информацию
            profit_emoji = "💚" if pnl > 0 else "❤️"
            print(f"\n📉 Позиция закрыта:")
            print(f"   🎯 {symbol} | {position['direction']}")
            print(f"   💵 Цена выхода: ${close_price:.4f}")
            print(f"   {profit_emoji} P&L: ${pnl:.2f} (комиссия: ${fees:.2f})")
            print(f"   📊 ROI: {trade['roi_pct']:.2f}%")
            print(f"   ⏱️ Длительность: {trade['duration']}")
            print(f"   💰 Текущий баланс: ${self.current_balance:.2f}")

            self._save_daily_data()

        except Exception as e:
            self.logger.error(f"Error logging position closed: {e}")

    def end_trading_session(self) -> Dict[str, Any]:
        """Завершение торговой сессии"""
        try:
            end_time = datetime.now()
            self.daily_data['session_end'] = end_time.isoformat()
            self.daily_data['end_balance'] = self.current_balance
            self.daily_data['daily_return'] = self.current_balance - self.session_start_balance
            self.daily_data['daily_return_pct'] = (
                (self.current_balance - self.session_start_balance) / self.session_start_balance * 100
                if self.session_start_balance > 0 else 0
            )

            # Сохраняем данные
            self._save_daily_data()

            # Генерируем отчет
            report = self._generate_daily_report()

            self.logger.info("Trading session ended")
            return report

        except Exception as e:
            self.logger.error(f"Error ending trading session: {e}")
            return {}

    def _update_daily_stats(self, trade: Dict[str, Any]) -> None:
        """Обновление дневной статистики"""
        try:
            stats = self.daily_data['daily_stats']
            net_pnl = trade['net_pnl']

            stats['total_trades'] += 1
            stats['total_pnl'] += net_pnl
            stats['total_fees'] += trade['fees']

            if net_pnl > 0:
                stats['winning_trades'] += 1
                stats['max_profit'] = max(stats['max_profit'], net_pnl)
            else:
                stats['losing_trades'] += 1
                stats['max_loss'] = min(stats['max_loss'], net_pnl)

            # Обновляем производные метрики
            if stats['total_trades'] > 0:
                stats['win_rate'] = (stats['winning_trades'] / stats['total_trades']) * 100

            if stats['losing_trades'] > 0 and stats['max_loss'] < 0:
                total_wins = sum(t['net_pnl'] for t in self.daily_data['trades'] if t['net_pnl'] > 0)
                total_losses = abs(sum(t['net_pnl'] for t in self.daily_data['trades'] if t['net_pnl'] < 0))
                stats['profit_factor'] = total_wins / total_losses if total_losses > 0 else float('inf')

        except Exception as e:
            self.logger.error(f"Error updating daily stats: {e}")

    def _calculate_duration(self, start_time: str, end_time: str) -> str:
        """Расчет длительности позиции"""
        try:
            start = datetime.fromisoformat(start_time)
            end = datetime.fromisoformat(end_time)
            duration = end - start

            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60

            if duration.days > 0:
                return f"{duration.days}д {hours}ч {minutes}м"
            elif hours > 0:
                return f"{hours}ч {minutes}м"
            else:
                return f"{minutes}м"

        except Exception as e:
            self.logger.error(f"Error calculating duration: {e}")
            return "N/A"

    def _generate_daily_report(self) -> Dict[str, Any]:
        """Генерация дневного отчета"""
        try:
            stats = self.daily_data['daily_stats']

            print("\n" + "=" * 60)
            print("📊 ДНЕВНОЙ ОТЧЕТ ТРЕЙДИНГА")
            print("=" * 60)
            print(f"📅 Дата: {self.current_date.strftime('%d.%m.%Y')}")
            print(
                f"⏰ Время сессии: {datetime.fromisoformat(self.daily_data['session_start']).strftime('%H:%M')} - {datetime.now().strftime('%H:%M')}")
            print("-" * 60)

            # Баланс
            print("💰 БАЛАНС:")
            print(f"   Начальный: ${self.daily_data['start_balance']:.2f}")
            print(f"   Конечный:  ${self.daily_data['end_balance']:.2f}")

            daily_return = self.daily_data['daily_return']
            return_pct = self.daily_data['daily_return_pct']
            return_emoji = "📈" if daily_return >= 0 else "📉"

            print(f"   {return_emoji} Изменение: ${daily_return:.2f} ({return_pct:+.2f}%)")
            print("-" * 60)

            # Статистика сделок
            print("📋 СТАТИСТИКА СДЕЛОК:")
            print(f"   Всего сделок: {stats['total_trades']}")
            print(f"   Прибыльных: {stats['winning_trades']} ({stats['win_rate']:.1f}%)")
            print(f"   Убыточных: {stats['losing_trades']}")
            print(f"   Общий P&L: ${stats['total_pnl']:.2f}")
            print(f"   Комиссии: ${stats['total_fees']:.2f}")

            if stats['total_trades'] > 0:
                print(f"   Лучшая сделка: ${stats['max_profit']:.2f}")
                print(f"   Худшая сделка: ${stats['max_loss']:.2f}")
                if stats['profit_factor'] != float('inf'):
                    print(f"   Profit Factor: {stats['profit_factor']:.2f}")

            print("-" * 60)

            # Детали сделок
            if self.daily_data['trades']:
                print("📈 ДЕТАЛИ СДЕЛОК:")
                for i, trade in enumerate(self.daily_data['trades'], 1):
                    pnl_emoji = "💚" if trade['net_pnl'] > 0 else "❤️"
                    print(f"   {i}. {trade['symbol']} {trade['direction']} | "
                          f"{pnl_emoji} ${trade['net_pnl']:.2f} | "
                          f"ROI: {trade['roi_pct']:+.2f}% | "
                          f"{trade['duration']}")

            print("=" * 60)

            return {
                'date': self.current_date.isoformat(),
                'daily_return': daily_return,
                'daily_return_pct': return_pct,
                'stats': stats,
                'trades_count': len(self.daily_data['trades'])
            }

        except Exception as e:
            self.logger.error(f"Error generating daily report: {e}")
            return {}

    def _save_daily_data(self) -> None:
        """Сохранение данных дня"""
        try:
            filename = f"diary_{self.current_date.isoformat()}.json"
            filepath = self.diary_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.daily_data, f, indent=2, ensure_ascii=False, default=str)

        except Exception as e:
            self.logger.error(f"Error saving daily data: {e}")

    def _load_daily_data(self) -> None:
        """Загрузка данных текущего дня"""
        try:
            filename = f"diary_{self.current_date.isoformat()}.json"
            filepath = self.diary_dir / filename

            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    self.daily_data.update(loaded_data)

                # Восстанавливаем текущий баланс
                self.current_balance = self.daily_data.get('current_balance', 0.0)
                self.session_start_balance = self.daily_data.get('start_balance', 0.0)

                self.logger.info(f"Loaded daily data for {self.current_date}")

        except Exception as e:
            self.logger.error(f"Error loading daily data: {e}")

    def _start_new_day(self) -> None:
        """Начало нового торгового дня"""
        self.current_date = date.today()
        self.session_start_time = datetime.now()

        # Сброс данных дня
        self.daily_data = {
            'date': self.current_date.isoformat(),
            'session_start': self.session_start_time.isoformat(),
            'start_balance': 0.0,
            'current_balance': 0.0,
            'positions': [],
            'trades': [],
            'daily_stats': {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_pnl': 0.0,
                'total_fees': 0.0,
                'max_profit': 0.0,
                'max_loss': 0.0,
                'win_rate': 0.0,
                'profit_factor': 0.0
            },
            'session_end': None,
            'end_balance': 0.0,
            'daily_return': 0.0,
            'daily_return_pct': 0.0
        }

        self.logger.info(f"Started new trading day: {self.current_date}")

    def get_weekly_summary(self) -> Dict[str, Any]:
        """Получение недельной сводки"""
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=7)

            weekly_data = []
            total_return = 0.0
            total_trades = 0

            current_date = start_date
            while current_date <= end_date:
                filename = f"diary_{current_date.isoformat()}.json"
                filepath = self.diary_dir / filename

                if filepath.exists():
                    with open(filepath, 'r', encoding='utf-8') as f:
                        day_data = json.load(f)
                        weekly_data.append(day_data)
                        total_return += day_data.get('daily_return', 0.0)
                        total_trades += day_data.get('daily_stats', {}).get('total_trades', 0)

                current_date += timedelta(days=1)

            return {
                'period': f"{start_date.isoformat()} - {end_date.isoformat()}",
                'total_return': total_return,
                'total_trades': total_trades,
                'trading_days': len(weekly_data),
                'daily_data': weekly_data
            }

        except Exception as e:
            self.logger.error(f"Error generating weekly summary: {e}")
            return {}

    def get_current_day_status(self) -> Dict[str, Any]:
        """Получение статуса текущего дня"""
        try:
            return {
                'date': self.current_date.isoformat(),
                'session_active': self.daily_data.get('session_end') is None,
                'start_balance': self.daily_data.get('start_balance', 0.0),
                'current_balance': self.current_balance,
                'daily_return': self.current_balance - self.daily_data.get('start_balance', 0.0),
                'open_positions': len([p for p in self.daily_data['positions'] if p['status'] == 'OPEN']),
                'completed_trades': len(self.daily_data['trades']),
                'daily_stats': self.daily_data['daily_stats']
            }

        except Exception as e:
            self.logger.error(f"Error getting current day status: {e}")
            return {}

    def export_diary_to_csv(self, days: int = 30) -> str:
        """Экспорт дневника в CSV файл"""
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=days)

            diary_records = []

            current_date = start_date
            while current_date <= end_date:
                filename = f"diary_{current_date.isoformat()}.json"
                filepath = self.diary_dir / filename

                if filepath.exists():
                    with open(filepath, 'r', encoding='utf-8') as f:
                        day_data = json.load(f)

                        record = {
                            'date': day_data['date'],
                            'start_balance': day_data.get('start_balance', 0.0),
                            'end_balance': day_data.get('end_balance', 0.0),
                            'daily_return': day_data.get('daily_return', 0.0),
                            'daily_return_pct': day_data.get('daily_return_pct', 0.0),
                            'total_trades': day_data.get('daily_stats', {}).get('total_trades', 0),
                            'winning_trades': day_data.get('daily_stats', {}).get('winning_trades', 0),
                            'win_rate': day_data.get('daily_stats', {}).get('win_rate', 0.0),
                            'total_pnl': day_data.get('daily_stats', {}).get('total_pnl', 0.0),
                            'total_fees': day_data.get('daily_stats', {}).get('total_fees', 0.0)
                        }
                        diary_records.append(record)

                current_date += timedelta(days=1)

            if diary_records:
                df = pd.DataFrame(diary_records)
                export_file = f"trading_diary_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                export_path = self.diary_dir / export_file
                df.to_csv(export_path, index=False, encoding='utf-8')

                self.logger.info(f"Diary exported to {export_path}")
                return str(export_path)

            return ""

        except Exception as e:
            self.logger.error(f"Error exporting diary to CSV: {e}")
            return ""