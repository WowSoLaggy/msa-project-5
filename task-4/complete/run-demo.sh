#!/bin/bash
# Скрипт для первого запуска Spring Batch приложения

set -e

echo "=== Запуск Spring Batch Demo ==="
echo ""

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker и повторите попытку."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose и повторите попытку."
    exit 1
fi

echo "✅ Docker и Docker Compose найдены"
echo ""

# Переход в директорию complete
cd "$(dirname "$0")"
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Файл docker-compose.yml не найден. Запустите скрипт из директории complete/"
    exit 1
fi

echo "📦 Остановка старых контейнеров (если есть)..."
docker-compose down -v 2>/dev/null || true

echo ""
echo "🚀 Запуск PostgreSQL..."
docker-compose up -d postgresdb

echo ""
echo "⏳ Ожидание готовности PostgreSQL (15 секунд)..."
sleep 15

echo ""
echo "📋 Создание таблиц в БД..."
docker exec -i $(docker ps -qf "name=postgresdb") psql -U postgres -d productsdb < src/main/resources/schema-all.sql

echo ""
echo "📊 Загрузка справочных данных (loyality_data)..."
docker cp src/main/resources/loyality_data.csv $(docker ps -qf "name=postgresdb"):/tmp/loyality_data.csv
docker exec -i $(docker ps -qf "name=postgresdb") psql -U postgres -d productsdb -c "COPY loyality_data FROM '/tmp/loyality_data.csv' DELIMITER ',' CSV;"

echo ""
echo "🔨 Сборка и запуск Spring Batch приложения..."
docker-compose up --build app

echo ""
echo "✅ Готово! Проверьте логи выше."
echo ""
echo "Для проверки данных в БД выполните:"
echo "  docker exec -it \$(docker ps -qf 'name=postgresdb') psql -U postgres -d productsdb"
echo "  SELECT * FROM products;"
