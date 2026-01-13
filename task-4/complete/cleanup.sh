#!/bin/bash
# Скрипт для очистки и остановки всех контейнеров

echo "=== Очистка Docker контейнеров ==="
echo ""

cd "$(dirname "$0")"

echo "🛑 Остановка контейнеров..."
docker-compose down -v

echo ""
echo "🧹 Удаление образов (опционально)..."
docker rmi batch-processing 2>/dev/null || echo "Образ batch-processing не найден"

echo ""
echo "✅ Очистка завершена!"
echo ""
echo "Для повторного запуска используйте: ./run-demo.sh"
