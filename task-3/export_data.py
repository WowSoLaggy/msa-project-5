#!/usr/bin/env python3
"""
Простой скрипт для экспорта данных из PostgreSQL в CSV
"""
import os
import psycopg2
import csv
from datetime import datetime

def export_shipments_to_csv():
    """Экспортирует данные таблицы shipments в CSV файл"""
    
    # Параметры подключения к БД из переменных окружения
    db_host = os.getenv('DB_HOST', 'postgres')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'logistics')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    
    # Путь для сохранения CSV
    output_dir = os.getenv('OUTPUT_DIR', '/data')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"{output_dir}/shipments_{timestamp}.csv"
    
    try:
        # Подключение к БД
        print(f"Подключение к БД {db_host}:{db_port}/{db_name}...")
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()
        
        # Выполнение запроса
        print("Выполнение SQL запроса...")
        cursor.execute("SELECT * FROM shipments")
        
        # Получение данных
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        
        print(f"Найдено {len(rows)} записей")
        
        # Создание директории если не существует
        os.makedirs(output_dir, exist_ok=True)
        
        # Запись в CSV
        print(f"Запись данных в {output_file}...")
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)  # Заголовки
            writer.writerows(rows)  # Данные
        
        print(f"✓ Экспорт успешно завершён: {output_file}")
        print(f"✓ Экспортировано записей: {len(rows)}")
        
        # Закрытие соединения
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Ошибка при экспорте данных: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("Запуск экспорта данных перевозок")
    print("=" * 50)
    success = export_shipments_to_csv()
    exit(0 if success else 1)
