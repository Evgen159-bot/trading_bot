import logging
import os
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy


class StrategyValidator:
    """Класс для валидации торговых стратегий"""

    def __init__(self):
        self.logger = self._setup_logger()
        self.validation_history: List[Dict] = []

        # Критерии валидации
        self.validation_criteria = {
            'min_data_points': 100,
            'max_signal_age': 60,  # секунд
            'min_win_rate': 0.0,  # минимальный win rate для прохождения
            'max_drawdown': 0.5,  # максимальная просадка 50%
            'min_profit_factor': 0.0,
            'required_methods': [
                'generate_signal', 'validate_signal', 'calculate_position_size',
                'should_close_position', 'execute'
            ],
            'required_attributes': ['name', 'logger', 'stats', 'config']
        }

        self.logger.info("StrategyValidator initialized")

    def _setup_logger(self) -> logging.Logger:
        """Настройка логгера"""
        logger = logging.getLogger("strategy_validator")
        logger.setLevel(logging.INFO)

        # Очищаем существующие обработчики
        logger.handlers.clear()

        # Создаем директорию для логов
        log_dir = "logs/validation"
        os.makedirs(log_dir, exist_ok=True)

        # Файловый обработчик
        log_file = os.path.join(log_dir, f"validation_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(file_handler)

        return logger

    def validate_strategy(self,
                          strategy: BaseStrategy,
                          test_data: Dict[str, Any],
                          strict_mode: bool = True,
                          performance_test: bool = False) -> Dict[str, Any]:
        """
        Комплексная валидация торговой стратегии

        Args:
            strategy: Объект торговой стратегии
            test_data: Тестовые данные для валидации
            strict_mode: Строгий режим проверки
            performance_test: Включить тест производительности

        Returns:
            Dict с результатами валидации
        """
        validation_result = {
            'strategy_name': strategy.name,
            'timestamp': datetime.now(),
            'is_valid': True,
            'score': 0.0,  # Общий балл валидации (0-100)
            'errors': [],
            'warnings': [],
            'recommendations': [],
            'test_results': {},
            'performance_metrics': {}
        }

        try:
            self.logger.info(f"Starting validation for strategy: {strategy.name}")

            # 1. Проверка базовой структуры (20 баллов)
            structure_score = self._validate_structure(strategy, validation_result)
            validation_result['score'] += structure_score

            # 2. Проверка входных данных (15 баллов)
            data_score = self._validate_input_data(test_data, validation_result)
            validation_result['score'] += data_score

            # 3. Проверка генерации сигналов (25 баллов)
            signal_score = self._validate_signal_generation(strategy, test_data, validation_result)
            validation_result['score'] += signal_score

            # 4. Проверка управления рисками (20 баллов)
            risk_score = self._validate_risk_management(strategy, test_data, validation_result)
            validation_result['score'] += risk_score

            # 5. Проверка исполнения (20 баллов)
            execution_score = self._validate_execution(strategy, test_data, validation_result)
            validation_result['score'] += execution_score

            # 6. Тест производительности (бонус)
            if performance_test:
                perf_score = self._validate_performance(strategy, test_data, validation_result)
                validation_result['score'] += perf_score

            # Финальная оценка
            validation_result['score'] = min(100.0, validation_result['score'])

            # В строгом режиме любая ошибка делает стратегию невалидной
            if strict_mode and validation_result['errors']:
                validation_result['is_valid'] = False
            elif validation_result['score'] < 60:  # Минимальный проходной балл
                validation_result['is_valid'] = False
                validation_result['errors'].append("Overall validation score too low")

            # Генерация рекомендаций
            self._generate_recommendations(validation_result)

            # Сохранение результатов
            self.validation_history.append(validation_result)

            self.logger.info(f"Validation completed for {strategy.name}: "
                             f"Score={validation_result['score']:.1f}, "
                             f"Valid={validation_result['is_valid']}")

            return validation_result

        except Exception as e:
            self.logger.exception(f"Critical error during strategy validation: {e}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Critical validation error: {str(e)}")
            return validation_result

    def _validate_structure(self, strategy: BaseStrategy, result: Dict) -> float:
        """Проверка структуры стратегии (20 баллов)"""
        score = 0.0
        max_score = 20.0

        try:
            # Проверка методов (10 баллов)
            method_score = 0
            for method in self.validation_criteria['required_methods']:
                if hasattr(strategy, method) and callable(getattr(strategy, method)):
                    method_score += 2
                else:
                    result['errors'].append(f"Missing or invalid method: {method}")
            score += min(10, method_score)

            # Проверка атрибутов (5 баллов)
            attr_score = 0
            for attr in self.validation_criteria['required_attributes']:
                if hasattr(strategy, attr):
                    attr_score += 1.25
                else:
                    result['warnings'].append(f"Missing recommended attribute: {attr}")
            score += min(5, attr_score)

            # Проверка наследования (5 баллов)
            if isinstance(strategy, BaseStrategy):
                score += 5
            else:
                result['errors'].append("Strategy does not inherit from BaseStrategy")

            result['test_results']['structure_score'] = score

        except Exception as e:
            result['errors'].append(f"Structure validation error: {str(e)}")

        return score

    def _validate_input_data(self, data: Dict, result: Dict) -> float:
        """Проверка входных данных (15 баллов)"""
        score = 0.0
        max_score = 15.0

        try:
            required_fields = ['df', 'symbol', 'account_balance']

            # Проверка наличия полей (5 баллов)
            field_score = 0
            for field in required_fields:
                if field in data:
                    field_score += 5 / 3
                else:
                    result['errors'].append(f"Missing required data field: {field}")
            score += min(5, field_score)

            # Проверка качества данных (10 баллов)
            if 'df' in data:
                df = data['df']
                if isinstance(df, pd.DataFrame):
                    if len(df) >= self.validation_criteria['min_data_points']:
                        score += 5
                    else:
                        result['warnings'].append(f"Dataset might be too small: {len(df)} rows")
                        score += 2

                    # Проверка колонок
                    required_cols = ['open', 'high', 'low', 'close', 'volume']
                    if all(col in df.columns for col in required_cols):
                        score += 3
                    else:
                        missing_cols = [col for col in required_cols if col not in df.columns]
                        result['warnings'].append(f"Missing columns: {missing_cols}")

                    # Проверка на NaN
                    if not df.isnull().any().any():
                        score += 2
                    else:
                        result['warnings'].append("Data contains NaN values")
                else:
                    result['errors'].append("'df' is not a pandas DataFrame")

            # Проверка баланса
            if 'account_balance' in data:
                balance = data['account_balance']
                if isinstance(balance, (int, float)) and balance > 0:
                    score += 0  # Уже учтено в field_score
                else:
                    result['errors'].append("Invalid account balance")

            result['test_results']['data_score'] = score

        except Exception as e:
            result['errors'].append(f"Data validation error: {str(e)}")

        return score

    def _validate_signal_generation(self, strategy: BaseStrategy, data: Dict, result: Dict) -> float:
        """Проверка генерации сигналов (25 баллов)"""
        score = 0.0
        max_score = 25.0

        try:
            # Тест генерации сигнала (15 баллов)
            if 'df' in data:
                signal = strategy.generate_signal(data['df'], data.get('symbol'))

                if signal is not None:
                    score += 5  # Сигнал сгенерирован

                    # Проверка структуры сигнала (10 баллов)
                    required_signal_fields = ['action', 'entry_price', 'timestamp']
                    field_score = 0
                    for field in required_signal_fields:
                        if field in signal:
                            field_score += 10 / 3
                        else:
                            result['errors'].append(f"Missing signal field: {field}")
                    score += min(10, field_score)

                    # Проверка валидности сигнала (10 баллов)
                    if strategy.validate_signal(signal):
                        score += 10
                        result['test_results']['signal_valid'] = True
                    else:
                        result['errors'].append("Generated signal failed validation")
                        result['test_results']['signal_valid'] = False
                else:
                    result['warnings'].append("No signal generated (may be normal)")
                    score += 5  # Частичный балл за отсутствие ошибок

            result['test_results']['signal_score'] = score

        except Exception as e:
            result['errors'].append(f"Signal generation error: {str(e)}")

        return score

    def _validate_risk_management(self, strategy: BaseStrategy, data: Dict, result: Dict) -> float:
        """Проверка управления рисками (20 баллов)"""
        score = 0.0
        max_score = 20.0

        try:
            # Создаем тестовые сигналы
            test_signals = [
                {
                    'action': 'BUY',
                    'entry_price': 100.0,
                    'stop_loss': 95.0,
                    'take_profit': 110.0,
                    'timestamp': datetime.now()
                },
                {
                    'action': 'SELL',
                    'entry_price': 100.0,
                    'stop_loss': 105.0,
                    'take_profit': 90.0,
                    'timestamp': datetime.now()
                }
            ]

            balance = data.get('account_balance', 10000)
            symbol = data.get('symbol', 'TESTUSDT')

            for i, test_signal in enumerate(test_signals):
                try:
                    # Тест расчета размера позиции (10 баллов за каждый сигнал)
                    position_size = strategy.calculate_position_size(test_signal, balance, symbol)

                    if position_size > 0:
                        score += 5

                        # Проверка разумности размера
                        position_value = position_size * test_signal['entry_price']
                        if position_value <= balance:
                            score += 5
                        else:
                            result['errors'].append(f"Position size exceeds balance for signal {i + 1}")
                    else:
                        result['warnings'].append(f"Zero position size for signal {i + 1}")

                except Exception as e:
                    result['errors'].append(f"Position size calculation error for signal {i + 1}: {str(e)}")

            result['test_results']['risk_score'] = score

        except Exception as e:
            result['errors'].append(f"Risk management validation error: {str(e)}")

        return score

    def _validate_execution(self, strategy: BaseStrategy, data: Dict, result: Dict) -> float:
        """Проверка исполнения стратегии (20 баллов)"""
        score = 0.0
        max_score = 20.0

        try:
            symbol = data.get('symbol', 'TESTUSDT')
            market_data = {
                'df': data.get('df'),
                'symbol': symbol,
                'account_balance': data.get('account_balance', 10000),
                'timestamp': datetime.now()
            }

            # Тест выполнения стратегии (20 баллов)
            execution_result = strategy.execute(symbol, market_data)

            if execution_result is not None:
                score += 10  # Стратегия выполнилась

                # Проверка структуры результата (10 баллов)
                if isinstance(execution_result, dict):
                    score += 5

                    if 'action' in execution_result:
                        score += 5
                    else:
                        result['warnings'].append("Execution result missing 'action' field")
                else:
                    result['warnings'].append("Execution result is not a dictionary")
            else:
                score += 5  # Частичный балл за отсутствие ошибок
                result['warnings'].append("Strategy execution returned None")

            result['test_results']['execution_score'] = score

        except Exception as e:
            result['errors'].append(f"Execution validation error: {str(e)}")

        return score

    def _validate_performance(self, strategy: BaseStrategy, data: Dict, result: Dict) -> float:
        """Тест производительности (бонус до 10 баллов)"""
        score = 0.0

        try:
            # Симуляция множественных выполнений
            execution_times = []
            successful_executions = 0

            for i in range(10):
                try:
                    start_time = datetime.now()
                    strategy.execute(data.get('symbol', 'TEST'), data)
                    end_time = datetime.now()

                    execution_time = (end_time - start_time).total_seconds()
                    execution_times.append(execution_time)
                    successful_executions += 1

                except Exception:
                    pass

            if execution_times:
                avg_time = np.mean(execution_times)
                result['performance_metrics'] = {
                    'avg_execution_time': avg_time,
                    'max_execution_time': max(execution_times),
                    'min_execution_time': min(execution_times),
                    'success_rate': successful_executions / 10
                }

                # Бонусные баллы за производительность
                if avg_time < 0.1:  # Менее 100мс
                    score += 5
                elif avg_time < 0.5:  # Менее 500мс
                    score += 3
                elif avg_time < 1.0:  # Менее 1с
                    score += 1

                if successful_executions == 10:
                    score += 5
                elif successful_executions >= 8:
                    score += 3
                elif successful_executions >= 6:
                    score += 1

            result['test_results']['performance_score'] = score

        except Exception as e:
            result['warnings'].append(f"Performance test error: {str(e)}")

        return score

    def _generate_recommendations(self, result: Dict) -> None:
        """Генерация рекомендаций по улучшению"""
        try:
            score = result['score']
            recommendations = []

            if score < 60:
                recommendations.append("Strategy needs significant improvements to pass validation")
            elif score < 80:
                recommendations.append("Strategy is functional but has room for improvement")
            else:
                recommendations.append("Strategy shows good quality and reliability")

            # Специфичные рекомендации
            if result['test_results'].get('signal_score', 0) < 15:
                recommendations.append("Improve signal generation logic and validation")

            if result['test_results'].get('risk_score', 0) < 15:
                recommendations.append("Enhance risk management calculations")

            if result['test_results'].get('execution_score', 0) < 15:
                recommendations.append("Review strategy execution logic")

            if len(result['errors']) > 0:
                recommendations.append("Fix all reported errors before deployment")

            if len(result['warnings']) > 3:
                recommendations.append("Address warnings to improve strategy robustness")

            result['recommendations'] = recommendations

        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")

    def validate_multiple_strategies(self, strategies: List[BaseStrategy],
                                     test_data: Dict[str, Any]) -> Dict[str, Dict]:
        """Валидация нескольких стратегий"""
        results = {}

        for strategy in strategies:
            try:
                result = self.validate_strategy(strategy, test_data)
                results[strategy.name] = result
            except Exception as e:
                self.logger.error(f"Error validating strategy {strategy.name}: {e}")
                results[strategy.name] = {
                    'is_valid': False,
                    'error': str(e)
                }

        return results

    def get_validation_report(self, strategy_name: str = None) -> Dict[str, Any]:
        """Получение отчета по валидации"""
        try:
            if strategy_name:
                # Отчет по конкретной стратегии
                validations = [v for v in self.validation_history if v['strategy_name'] == strategy_name]
                if validations:
                    return validations[-1]  # Последняя валидация
                else:
                    return {'error': f'No validation found for strategy: {strategy_name}'}
            else:
                # Общий отчет
                if not self.validation_history:
                    return {'message': 'No validations performed yet'}

                total_validations = len(self.validation_history)
                passed_validations = len([v for v in self.validation_history if v['is_valid']])
                avg_score = np.mean([v['score'] for v in self.validation_history])

                return {
                    'total_validations': total_validations,
                    'passed_validations': passed_validations,
                    'pass_rate': (passed_validations / total_validations) * 100,
                    'average_score': round(avg_score, 2),
                    'last_validation': self.validation_history[-1]['timestamp'].isoformat()
                }

        except Exception as e:
            self.logger.error(f"Error generating validation report: {e}")
            return {'error': str(e)}

    def get_validation_history(self) -> List[Dict]:
        """Получение истории валидации"""
        return self.validation_history

    def get_last_validation(self) -> Optional[Dict]:
        """Получение результатов последней валидации"""
        return self.validation_history[-1] if self.validation_history else None

    def clear_validation_history(self) -> None:
        """Очистка истории валидации"""
        self.validation_history.clear()
        self.logger.info("Validation history cleared")

    def export_validation_results(self, filename: str = None) -> str:
        """Экспорт результатов валидации в файл"""
        try:
            if not filename:
                filename = f"validation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            import json

            # Подготовка данных для экспорта
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'total_validations': len(self.validation_history),
                'validation_criteria': self.validation_criteria,
                'validations': []
            }

            for validation in self.validation_history:
                # Конвертируем datetime объекты в строки
                validation_copy = validation.copy()
                if 'timestamp' in validation_copy:
                    validation_copy['timestamp'] = validation_copy['timestamp'].isoformat()
                export_data['validations'].append(validation_copy)

            # Создаем директорию если её нет
            os.makedirs('data/validation', exist_ok=True)
            filepath = os.path.join('data/validation', filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Validation results exported to {filepath}")
            return filepath

        except Exception as e:
            self.logger.error(f"Error exporting validation results: {e}")
            return ""