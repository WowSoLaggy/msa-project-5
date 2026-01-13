#!/bin/bash

# Скрипт для сборки Docker образа и загрузки в Minikube

echo "Сборка Docker образа..."
docker build -t shipments-export:latest .

echo "Загрузка образа в Minikube..."
minikube image load shipments-export:latest

echo "✓ Готово! Образ загружен в Minikube"
echo "Теперь можно применять манифесты Kubernetes:"
echo "  kubectl apply -f k8s/postgres-deployment.yaml"
echo "  kubectl apply -f k8s/cronjob.yaml"
