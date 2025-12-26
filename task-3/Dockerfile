# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипт экспорта
COPY export_data.py .

# Делаем скрипт исполняемым
RUN chmod +x export_data.py

# Запускаем скрипт при старте контейнера
CMD ["python", "export_data.py"]
