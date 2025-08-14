@echo off
chcp 65001 >nul
echo Starting ByBit Trading Bot...
echo.

REM Проверка виртуального окружения
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Активация виртуального окружения
call .venv\Scripts\activate.bat

REM Обновление pip
echo Updating pip...
python -m pip install --upgrade pip

REM Установка зависимостей
echo Installing dependencies...
pip install -r requirements.txt

REM Запуск бота
echo Starting bot...
python main.py

pause
