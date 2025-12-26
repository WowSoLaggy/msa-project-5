# Задание 3. Реализация Distributed Scheduling с k8s CronJob

## Описание решения

Реализовано простое решение для ежедневной выгрузки данных из PostgreSQL в CSV файлы с использованием Kubernetes CronJob.

### Архитектура
- **База данных**: PostgreSQL с таблицей `shipments` (перевозки)
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

## Изменение расписания

Откройте файл `k8s/cronjob.yaml` и измените параметр `schedule`:

```yaml
spec:
  schedule: "0 20 * * *"  # Каждый день в 20:00
```

Формат Cron:
- `*/5 * * * *` - каждые 5 минут
- `0 * * * *` - каждый час
- `0 20 * * *` - каждый день в 20:00
- `0 20 * * 1` - каждый понедельник в 20:00

После изменения примените манифест:
```bash
kubectl apply -f k8s/cronjob.yaml
```

## Подключение к PostgreSQL

Для проверки данных в БД:

```bash
# Получить имя pod'а PostgreSQL
kubectl get pods -l app=postgres

# Подключиться к БД
kubectl exec -it <postgres-pod-name> -- psql -U postgres -d logistics

# SQL запросы:
SELECT * FROM shipments;
\q  # выход
```

## Очистка ресурсов

```bash
# Удаление CronJob
kubectl delete -f k8s/cronjob-test.yaml
kubectl delete -f k8s/cronjob.yaml

# Удаление PostgreSQL
kubectl delete -f k8s/postgres-deployment.yaml

# Остановка Minikube
minikube stop
```

## Скриншоты для отчета

Для документации нужно сделать скриншоты:

1. **Список CronJob:**
   ```bash
   kubectl get cronjobs
   ```

2. **Список Jobs:**
   ```bash
   kubectl get jobs
   ```

3. **Список Pod'ов:**
   ```bash
   kubectl get pods
   ```

4. **Логи выполнения:**
   ```bash
   kubectl logs <pod-name>
   ```

5. **Описание CronJob:**
   ```bash
   kubectl describe cronjob shipments-export-test
   ```

## Детали реализации

### Python скрипт (export_data.py)
- Подключается к PostgreSQL
- Выполняет SQL запрос `SELECT * FROM shipments`
- Сохраняет результат в CSV с временной меткой
- Параметры подключения настраиваются через переменные окружения

### Dockerfile
- Базовый образ: `python:3.11-slim`
- Установка библиотеки `psycopg2-binary` для работы с PostgreSQL
- Копирование скрипта экспорта

### Kubernetes CronJob
- Расписание: каждый день в 20:00 (можно настроить)
- Политика параллелизма: `Forbid` (не запускать новую job если предыдущая ещё выполняется)
- История: хранит 3 успешных и 3 неудачных запуска
- Restart policy: `OnFailure`

## Возможные улучшения

Для продакшена можно добавить:
1. **PersistentVolumeClaim** вместо `emptyDir` для сохранения CSV файлов
2. **Secrets** для хранения паролей БД
3. **ConfigMap** для конфигурации параметров экспорта
4. **Monitoring** и алерты при ошибках экспорта
5. Экспорт всех таблиц (shipments, shipment_events, drivers, vehicles, clients)
6. Загрузку CSV в S3/MinIO/другое хранилище
7. Сжатие CSV файлов (gzip)
8. Параллельный экспорт больших таблиц

## Вопросы и поддержка

При возникновении проблем проверьте:
- Запущен ли Minikube: `minikube status`
- Загружен ли образ: `minikube image ls | grep shipments`
- Логи PostgreSQL: `kubectl logs <postgres-pod>`
- События: `kubectl get events --sort-by='.lastTimestamp'`
