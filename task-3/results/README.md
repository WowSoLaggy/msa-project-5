# Задание 3. Реализация Distributed Scheduling с k8s CronJob

## Описание решения

Реализовано решение для ежедневной выгрузки данных из PostgreSQL в CSV файлы с использованием Kubernetes CronJob.

### Архитектура
- **База данных**: PostgreSQL с таблицей `shipments`
- **Экспорт**: Python скрипт для экспорта данных в CSV
- **Планировщик**: Kubernetes CronJob (ежедневно в 20:00)

## Структура файлов

```
task-3/
├── export_data.py          # Python скрипт для экспорта данных
├── requirements.txt        # Зависимости Python
├── Dockerfile             # Dockerfile для создания образа
├── .dockerignore          # Исключения для Docker
├── build.sh               # Скрипт сборки
└── k8s/                   # Kubernetes манифесты
    ├── postgres-deployment.yaml  # Деплоймент PostgreSQL (для демо)
    ├── cronjob.yaml             # CronJob (запуск в 20:00)
    └── cronjob-test.yaml        # CronJob для тестирования (каждые 2 мин)
```

## Быстрый старт

### Предварительные требования
- Docker
- Minikube
- kubectl

### 1. Запуск Minikube

```bash
minikube start
```

### 2. Сборка и загрузка Docker образа

```bash
cd task-3
chmod +x build.sh
./build.sh
```

**Или вручную:**
```bash
# Сборка образа
docker build -t shipments-export:latest .

# Загрузка в Minikube
minikube image load shipments-export:latest
```

### 3. Развертывание PostgreSQL

```bash
kubectl apply -f k8s/postgres-deployment.yaml
```

**Проверка:**
```bash
kubectl get pods
kubectl get svc
```

Дождитесь запуска PostgreSQL (статус `Running`).

### 4. Развертывание CronJob

**Для тестирования (запускается каждые 2 минуты):**
```bash
kubectl apply -f k8s/cronjob-test.yaml
```

**Для продакшена (запускается каждый день в 20:00):**
```bash
kubectl apply -f k8s/cronjob.yaml
```

## Проверка работы

### Просмотр CronJob
```bash
kubectl get cronjobs
```

### Просмотр запущенных Job
```bash
kubectl get jobs
```

### Просмотр Pod'ов
```bash
kubectl get pods
```

### Просмотр логов последнего выполнения
```bash
# Найти имя pod'а
kubectl get pods

# Посмотреть логи
kubectl logs <pod-name>
```

Пример успешного выполнения:
```
==================================================
Запуск экспорта данных перевозок
==================================================
Подключение к БД postgres:5432/logistics...
Выполнение SQL запроса...
Найдено 5 записей
Запись данных в /data/shipments_20251226_200001.csv...
✓ Экспорт успешно завершён: /data/shipments_20251226_200001.csv
✓ Экспортировано записей: 5
```

### Просмотр экспортированных файлов
```bash
# Получить имя pod'а
POD_NAME=$(kubectl get pods -l app=shipments-export-test --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1].metadata.name}')

# Просмотреть список файлов
kubectl exec $POD_NAME -- ls -lh /data
```

## Ручной запуск Job для тестирования

```bash
kubectl create job --from=cronjob/shipments-export-test manual-export-1
```
