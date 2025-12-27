#!/bin/bash
# Скрипт для проверки результатов работы Spring Batch

echo "=== Проверка результатов Spring Batch ==="
echo ""

CONTAINER=$(docker ps -qf "name=postgresdb")

if [ -z "$CONTAINER" ]; then
    echo "❌ PostgreSQL контейнер не запущен."
    echo "Запустите сначала: ./run-demo.sh"
    exit 1
fi

echo "📊 Таблица products:"
echo "-------------------"
docker exec -i $CONTAINER psql -U postgres -d productsdb -c "SELECT * FROM products ORDER BY productId;"

echo ""
echo "📋 Таблица loyality_data:"
echo "-------------------------"
docker exec -i $CONTAINER psql -U postgres -d productsdb -c "SELECT * FROM loyality_data ORDER BY productSku;"

echo ""
echo "📈 История выполнения Jobs (Spring Batch):"
echo "-------------------------------------------"
docker exec -i $CONTAINER psql -U postgres -d productsdb -c "SELECT job_instance_id, job_name, start_time, end_time, status FROM batch_job_execution ORDER BY job_instance_id DESC LIMIT 5;"

echo ""
echo "✅ Проверка завершена!"
