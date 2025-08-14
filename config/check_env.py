import os
from dotenv import load_dotenv

# Путь к файлу .env
env_file_path = 'config/config.env'

# 1. Проверка, существует ли файл .env
if os.path.exists(env_file_path):
    print(f"File '{env_file_path}' exists.")

    # 2. Чтение и печать содержимого файла .env
    try:
        with open(env_file_path, 'r') as file:
            for line in file:
                print(line.strip())  # Печать каждой строки, удаляя пробелы
    except Exception as e:
        print(f"Error reading file '{env_file_path}': {e}")

    # 3. Загрузка переменных окружения из файла .env
    load_dotenv(dotenv_path=env_file_path)
    print(f"Environment variables loaded from '{env_file_path}'.")
else:
    print(f"File '{env_file_path}' does not exist.")

# 4. Проверка и печать значений переменных окружения
env_vars = ['BYBIT_API_KEY', 'BYBIT_API_SECRET']
for var in env_vars:
    try:
        value = os.environ[var]
        print(f"Environment variable '{var}': {value}")
    except KeyError:
        print(f"Environment variable '{var}' is not set.")