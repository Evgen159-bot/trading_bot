#!/usr/bin/env python3
"""
Исправленный скрипт для настройки торгового бота (2025)
Создает все необходимые директории, файлы конфигурации и проверяет зависимости
"""

import os
import sys
import subprocess
import platform
import logging
from pathlib import Path
import shutil


class BotSetup:
    """Класс для настройки торгового бота"""

    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.errors = []
        self.warnings = []
        self.project_root = Path.cwd()

    def setup_logging(self):
        """Настройка логирования для setup"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )

    def print_header(self):
        """Печать заголовка"""
        print("\n" + "=" * 70)
        print("🚀 BYBIT TRADING BOT SETUP (2025)")
        print("=" * 70)
        print(f"🖥️  Platform: {platform.system()} {platform.release()}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        print(f"📁 Project Root: {self.project_root}")
        print("=" * 70)

    def check_python_version(self):
        """Проверка версии Python"""
        print("\n📋 Checking Python version...")

        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.errors.append("Python 3.8+ required")
            print("❌ Python 3.8+ is required!")
            return False

        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True

    def fix_data_directory_issue(self):
        """Исправление проблемы с директорией data"""
        print("\n🔧 Fixing data directory issue...")

        data_path = self.project_root / 'data'

        try:
            # Проверяем, есть ли файл data вместо папки
            if data_path.exists() and data_path.is_file():
                print(f"⚠️  Found file 'data' instead of directory, removing...")
                data_path.unlink()
                print("✅ File 'data' removed")

            # Создаем директорию data
            data_path.mkdir(exist_ok=True)
            print("✅ Directory 'data' created")

            return True

        except Exception as e:
            self.errors.append(f"Failed to fix data directory: {e}")
            print(f"❌ Failed to fix data directory: {e}")
            return False

    def create_directories(self):
        """Создание всех необходимых директорий согласно структуре проекта"""
        print("\n📁 Creating directories...")

        # Сначала исправляем проблему с data
        self.fix_data_directory_issue()

        directories = [
            'config',
            'logs',
            'logs/strategies',
            'logs/telegram',
            'logs/trades',
            'logs/validation',
            'logs/trading_diary',
            'modules',
            'strategies',
            'tests',
            'utils',
            'data/diary',
            'data/performance',
            'data/validation',
            'data/backtest',
            'exports',
            'temp'
        ]

        created_count = 0
        for directory in directories:
            try:
                dir_path = self.project_root / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ {directory}")
                created_count += 1
            except Exception as e:
                self.errors.append(f"Failed to create {directory}: {e}")
                print(f"❌ {directory}: {e}")

        print(f"\n📊 Created/verified {created_count}/{len(directories)} directories")
        return len(self.errors) == 0

    def create_config_files(self):
        """Создание файлов конфигурации"""
        print("\n⚙️  Creating configuration files...")

        # Основной конфиг
        config_file = self.project_root / 'config' / 'config.env'
        if not config_file.exists():
            try:
                config_content = """# ByBit API Configuration
# ВАЖНО: Замените на ваши реальные API ключи!
BYBIT_API_KEY=your_api_key_here
BYBIT_API_SECRET=your_api_secret_here
BYBIT_TESTNET=True

# Bot Configuration
CYCLE_INTERVAL=60
MAX_POSITIONS=4
RISK_PER_TRADE=0.005

# Logging Level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Telegram Notifications (опционально)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
TELEGRAM_ENABLED=False

# Email Notifications (опционально)
SMTP_SERVER=
SMTP_PORT=587
EMAIL_ADDRESS=
EMAIL_PASSWORD=
EMAIL_ENABLED=False

# Database (опционально)
DATABASE_ENABLED=False
DATABASE_PATH=data/trading_bot.db

# Performance Settings
SAVE_PERFORMANCE_DATA=True
PERFORMANCE_SAVE_INTERVAL=300

# Strategy Settings
STRATEGY_VALIDATION_ENABLED=True
MIN_SIGNAL_CONFIDENCE=0.6
"""
                config_file.write_text(config_content, encoding='utf-8')
                print("✅ config/config.env created")
            except Exception as e:
                self.errors.append(f"Failed to create config.env: {e}")
                print(f"❌ config/config.env: {e}")
        else:
            print("✅ config/config.env already exists")

        # .gitignore
        gitignore_file = self.project_root / '.gitignore'
        if not gitignore_file.exists():
            try:
                gitignore_content = """# Trading Bot .gitignore

# Configuration files with sensitive data
config/config.env
.env
*.env

# Logs
logs/
*.log

# Data files
data/
performance_data/
exports/
temp/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Jupyter Notebooks
.ipynb_checkpoints

# pytest
.pytest_cache/
.coverage

# mypy
.mypy_cache/

# CSV files
*.csv
"""
                gitignore_file.write_text(gitignore_content, encoding='utf-8')
                print("✅ .gitignore created")
            except Exception as e:
                self.warnings.append(f"Failed to create .gitignore: {e}")

    def create_init_files(self):
        """Создание __init__.py файлов для всех пакетов"""
        print("\n📝 Creating __init__.py files...")

        init_dirs = ['config', 'modules', 'strategies', 'tests', 'utils']

        for dir_name in init_dirs:
            try:
                init_file = self.project_root / dir_name / '__init__.py'
                if not init_file.exists():
                    init_file.write_text(f"# {dir_name.title()} package\n", encoding='utf-8')
                    print(f"✅ {dir_name}/__init__.py created")
                else:
                    print(f"✅ {dir_name}/__init__.py already exists")
            except Exception as e:
                self.warnings.append(f"Failed to create {dir_name}/__init__.py: {e}")

    def create_startup_scripts(self):
        """Создание скриптов запуска"""
        print("\n🚀 Creating startup scripts...")

        # Windows batch файл
        if platform.system() == "Windows":
            bat_content = """@echo off
chcp 65001 >nul
echo Starting ByBit Trading Bot (2025)...
echo.

REM Проверка виртуального окружения
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Активация виртуального окружения
call .venv\\Scripts\\activate.bat

REM Обновление pip
echo Updating pip...
python -m pip install --upgrade pip

REM Установка зависимостей
echo Installing dependencies...
pip install -r requirements.txt

REM Проверка конфигурации
echo Checking configuration...
python user_config.py

REM Запуск бота
echo Starting bot...
python main.py

pause
"""
            try:
                bat_file = self.project_root / 'start_bot.bat'
                bat_file.write_text(bat_content, encoding='utf-8')
                print("✅ start_bot.bat created")
            except Exception as e:
                self.warnings.append(f"Failed to create start_bot.bat: {e}")

        # Unix shell script
        else:
            sh_content = """#!/bin/bash
echo "Starting ByBit Trading Bot (2025)..."
echo

# Проверка виртуального окружения
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Активация виртуального окружения
source .venv/bin/activate

# Обновление pip
echo "Updating pip..."
python -m pip install --upgrade pip

# Установка зависимостей
echo "Installing dependencies..."
pip install -r requirements.txt

# Проверка конфигурации
echo "Checking configuration..."
python user_config.py

# Запуск бота
echo "Starting bot..."
python main.py
"""
            try:
                script_file = self.project_root / 'start_bot.sh'
                script_file.write_text(sh_content, encoding='utf-8')
                try:
                    script_file.chmod(0o755)  # Делаем исполняемым
                except AttributeError:
                    print("⚠️  chmod not available, you may need to run: chmod +x start_bot.sh")
                print("✅ start_bot.sh created")
            except Exception as e:
                self.warnings.append(f"Failed to create start_bot.sh: {e}")

    def check_and_install_dependencies(self):
        """Проверка и установка зависимостей"""
        print("\n📦 Checking dependencies...")

        requirements_file = self.project_root / 'requirements.txt'
        if not requirements_file.exists():
            print("⚠️  requirements.txt not found, creating default...")
            self.create_requirements_file()

        try:
            # Проверяем pip
            subprocess.run([sys.executable, '-m', 'pip', '--version'],
                           check=True, capture_output=True)
            print("✅ pip is available")

            # Предлагаем установить зависимости
            response = input("\n🤔 Install dependencies now? (y/n): ").lower().strip()
            if response in ['y', 'yes', 'да', 'д', '']:
                print("📥 Installing dependencies...")

                # Обновляем pip
                print("🔄 Updating pip...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
                               capture_output=True, text=True, encoding='utf-8', errors='ignore')

                # Устанавливаем зависимости с правильной кодировкой
                print("📦 Installing packages...")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
                ], capture_output=True, text=True, encoding='utf-8', errors='ignore')

                if result.returncode == 0:
                    print("✅ Dependencies installed successfully")
                    return True
                else:
                    error_msg = result.stderr if result.stderr else "Unknown error"
                    self.errors.append(f"Failed to install dependencies: {error_msg}")
                    print(f"❌ Failed to install dependencies")
                    print(f"Error: {error_msg}")

                    # Пробуем установить по одному
                    print("🔄 Trying to install packages individually...")
                    self.install_packages_individually()
                    return False
            else:
                print("⏭️  Skipping dependency installation")
                print("💡 Run: pip install -r requirements.txt")
                return True

        except subprocess.CalledProcessError as e:
            self.errors.append(f"pip not available: {e}")
            print(f"❌ pip not available: {e}")
            return False

    def install_packages_individually(self):
        """Установка пакетов по одному"""
        packages = [
            'pandas>=2.1.4',
            'numpy>=1.26.2',
            'pybit>=5.6.0',
            'python-dotenv>=1.0.0',
            'ta>=0.11.0',
            'requests>=2.31.0',
            'colorlog>=6.8.0',
            'aiohttp>=3.9.1',
            'tqdm>=4.66.1',
            'rich>=13.7.0'
        ]

        for package in packages:
            try:
                print(f"📦 Installing {package}...")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package
                ], capture_output=True, text=True, encoding='utf-8', errors='ignore')

                if result.returncode == 0:
                    print(f"✅ {package} installed")
                else:
                    print(f"❌ Failed to install {package}")

            except Exception as e:
                print(f"❌ Error installing {package}: {e}")

    def create_requirements_file(self):
        """Создание файла requirements.txt"""
        requirements_content = """# Trading Bot Requirements (2025) - Проверенные версии

# Core dependencies (ОБЯЗАТЕЛЬНЫЕ)
pandas>=2.1.4
numpy>=1.26.2
pybit>=5.6.0
python-dotenv>=1.0.0

# Technical Analysis (КРИТИЧЕСКИ ВАЖНО)
ta>=0.11.0

# HTTP requests and async
requests>=2.31.0
aiohttp>=3.9.1

# Logging and utilities
colorlog>=6.8.0
tqdm>=4.66.1

# Rich console output
rich>=13.7.0

# Optional dependencies for advanced features
matplotlib>=3.8.2
plotly>=5.17.0

# For notifications (optional)
python-telegram-bot>=20.7

# For testing
pytest>=7.4.3
pytest-asyncio>=0.21.1
"""
        try:
            requirements_file = self.project_root / 'requirements.txt'
            requirements_file.write_text(requirements_content, encoding='utf-8')
            print("✅ requirements.txt created")
        except Exception as e:
            self.warnings.append(f"Failed to create requirements.txt: {e}")

    def run_tests(self):
        """Запуск базовых тестов"""
        print("\n🧪 Running basic tests...")

        try:
            # Тест импорта основных модулей
            test_imports = [
                ('pandas', 'pandas'),
                ('numpy', 'numpy'),
                ('pybit', 'pybit'),
                ('ta', 'ta'),
                ('requests', 'requests'),
                ('dotenv', 'python_dotenv')
            ]

            failed_imports = []
            for display_name, import_name in test_imports:
                try:
                    __import__(import_name)
                    print(f"✅ {display_name}")
                except ImportError:
                    failed_imports.append(display_name)
                    print(f"❌ {display_name}")

            if failed_imports:
                self.warnings.append(f"Missing modules: {', '.join(failed_imports)}")
                print(f"⚠️  Missing modules: {', '.join(failed_imports)}")
                print("💡 Try running: pip install -r requirements.txt")
                return False
            else:
                print("✅ All critical modules available")
                return True

        except Exception as e:
            self.warnings.append(f"Test error: {e}")
            return False

    def check_project_structure(self):
        """Проверка структуры проекта"""
        print("\n🔍 Checking project structure...")

        required_files = [
            'main.py',
            'user_config.py',
            'config_loader.py',
            'modules/data_fetcher.py',
            'modules/market_analyzer.py',
            'modules/order_manager.py',
            'modules/position_manager.py',
            'modules/risk_manager.py',
            'modules/performance_tracker.py',
            'modules/trading_diary.py',
            'strategies/base_strategy.py',
            'strategies/custom_strategy.py',
            'strategies/strategy_factory.py',
            'utils/diary_viewer.py',
            'utils/strategy_debug_tool.py',
            'utils/log_analyzer.py',
            'utils/volume_optimizer.py',
            'utils/simple_log_check.py'
        ]

        missing_files = []
        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                missing_files.append(file_path)
                print(f"❌ {file_path}")
            else:
                print(f"✅ {file_path}")

        if missing_files:
            self.warnings.append(f"Missing files: {', '.join(missing_files)}")
            print(f"\n⚠️  Missing {len(missing_files)} required files")
            return False
        else:
            print("\n✅ All required files present")
            return True

    def create_pycharm_config(self):
        """Создание конфигурации для PyCharm"""
        print("\n🔧 Creating PyCharm configuration...")

        try:
            idea_dir = self.project_root / '.idea'
            idea_dir.mkdir(exist_ok=True)

            # modules.xml
            modules_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectModuleManager">
    <modules>
      <module fileurl="file://$PROJECT_DIR$/.idea/trading_bot.iml" filepath="$PROJECT_DIR$/.idea/trading_bot.iml" />
    </modules>
  </component>
</project>"""
            (idea_dir / 'modules.xml').write_text(modules_xml, encoding='utf-8')

            # trading_bot.iml
            iml_content = """<?xml version="1.0" encoding="UTF-8"?>
<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager">
    <content url="file://$MODULE_DIR$">
      <sourceFolder url="file://$MODULE_DIR$" isTestSource="false" />
      <excludeFolder url="file://$MODULE_DIR$/.venv" />
      <excludeFolder url="file://$MODULE_DIR$/venv" />
      <excludeFolder url="file://$MODULE_DIR$/logs" />
      <excludeFolder url="file://$MODULE_DIR$/data" />
      <excludeFolder url="file://$MODULE_DIR$/exports" />
      <excludeFolder url="file://$MODULE_DIR$/temp" />
    </content>
    <orderEntry type="inheritedJdk" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
</module>"""
            (idea_dir / 'trading_bot.iml').write_text(iml_content, encoding='utf-8')

            print("✅ PyCharm configuration created")

        except Exception as e:
            self.warnings.append(f"Failed to create PyCharm config: {e}")

    def print_summary(self):
        """Печать итогового отчета"""
        print("\n" + "=" * 70)
        print("📊 SETUP SUMMARY")
        print("=" * 70)

        if not self.errors:
            print("🎉 Setup completed successfully!")
            print("\n✅ Next steps:")
            print("1. Edit user_config.py with your ByBit API keys")
            print("2. Review trading parameters")
            print("3. Run the bot: python main.py")

            if platform.system() == "Windows":
                print("   Or double-click: start_bot.bat")
            else:
                print("   Or run: ./start_bot.sh")

            print("\n🔧 New diagnostic tools (2025):")
            print("   python utils/strategy_debug_tool.py ETHUSDT  # Detailed debugging")
            print("   python utils/log_analyzer.py                # Log analysis")
            print("   python utils/volume_optimizer.py            # Volume optimization")
            print("   python utils/simple_log_check.py            # Quick check")
            print("   python check_results.py                     # Results analysis")

        else:
            print("⚠️  Setup completed with errors:")
            for error in self.errors:
                print(f"   ❌ {error}")

        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   ⚠️  {warning}")

        print("\n📚 Useful commands:")
        print("   - python main.py                    # Запуск бота")
        print("   - python utils/diary_viewer.py      # Просмотр дневника")
        print("   - python user_config.py             # Проверка конфигурации")
        print("   - python utils/simple_log_check.py  # Быстрая проверка")

        print("\n🆘 Support:")
        print("   - Check logs/ directory for detailed logs")
        print("   - Ensure Python 3.8+ is installed")
        print("   - Verify internet connection for API access")
        print("   - Use TESTNET=True for safe testing")

        print("\n" + "=" * 70)

    def run_setup(self):
        """Запуск полной настройки"""
        self.print_header()

        # Проверки
        if not self.check_python_version():
            return False

        # Создание структуры
        self.create_directories()
        self.create_init_files()
        self.create_config_files()
        self.create_startup_scripts()
        self.create_pycharm_config()

        # Проверка структуры проекта
        self.check_project_structure()

        # Зависимости и тесты
        self.check_and_install_dependencies()
        self.run_tests()

        # Итоги
        self.print_summary()

        return len(self.errors) == 0


def main():
    """Главная функция"""
    try:
        setup = BotSetup()
        success = setup.run_setup()

        if success:
            print("\n👋 Setup finished successfully!")
            print("🚀 You can now run: python main.py")
            sys.exit(0)
        else:
            print("\n💥 Setup finished with errors!")
            print("🔧 Please fix the errors above and run setup again")

            # Дополнительные инструкции для Windows
            if platform.system() == "Windows":
                print("\n💡 Quick fix for missing modules:")
                print("   pip install ta python-dotenv pandas numpy pybit")

            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Critical setup error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()