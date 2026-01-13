# Задание 1: Решение для пакетной обработки данных

## Выбор технологического решения: Apache Airflow

### Обоснование выбора

**Apache Airflow** выбран, потому что:

#### 1. Готовые интеграции
- **BigQuery**: `apache-airflow-providers-google`
- **Redshift**: `apache-airflow-providers-amazon` 
- **Kafka**: `apache-airflow-providers-apache-kafka`
- **Spark**: `apache-airflow-providers-apache-spark`

Все устанавливаются через pip.

#### 2. Поддержка нужного функционала

- **Ветвление пайплайна**: `BranchPythonOperator`
- **Условия**: `trigger_rule`, условия в Python
- **Event-triggers**: Sensors, API triggers
- **Retry**: встроенный с экспоненциальной задержкой
- **Fallback**: `on_failure_callback`
- **Email**: встроенные уведомления

#### 3. Развертывание в облаке

- **AWS**: MWAA
- **GCP**: Cloud Composer
- **Azure**: развертывание в AKS
- **Kubernetes**: Helm charts

#### 4. Масштабирование

Для обработки больших объемов данных (~1 млн записей):
- **LocalExecutor** - простые задачи
- **CeleryExecutor** - распределенная обработка
- **KubernetesExecutor** - динамическое масштабирование

---

## POC (Proof of Concept)

### Что демонстрирует POC

1. Чтение данных из CSV файла
2. Трансформация данных
3. Ветвление пайплайна по условию
4. Retry-политика с экспоненциальной задержкой
5. Email-уведомления

### Архитектура POC

```
┌─────────────────────┐
│  read_csv_job       │  ← Чтение CSV данных
└──────────┬──────────┘
           │
           v
┌─────────────────────────┐
│  transform_data_job     │  ← Трансформация (bonus_money)
└──────────┬──────────────┘
           │
           v
┌───────────────────────────────┐
│  analyze_with_condition_job   │  ← Условное ветвление (random)
└────────┬──────────────────┬───┘
         │                  │
         v                  v
┌────────────────┐   ┌────────────────┐
│ email_success  │   │  email_fail    │  ← Email уведомления
└────────┬───────┘   └────────┬───────┘
         │                    │
         └──────────┬─────────┘
                    v
           ┌─────────────────┐
           │  finalize_job   │  ← Финализация
           └─────────────────┘
```

### Инструкция по запуску

1. **Скопируйте файлы проекта**
2. **Запустите Docker Compose**:
   ```bash
   cd task-1
   docker-compose up -d
   ```

3. **Дождитесь инициализации** (~30 сек)

4. **Откройте Airflow UI**:
   - URL: http://localhost:8080
   - Login: `airflow`
   - Password: `airflow`

5. **Откройте MailHog** (для просмотра email):
   - URL: http://localhost:8025

6. **Активируйте и запустите DAG** `task1_dag`

### Как работает

#### 1. Ветвление
На основе случайного условия (имитация реальной логики):
- 50% → `email_success`
- 50% → `email_fail`

#### 2. Retry
```python
default_args = {
    'retries': 2,
    'retry_delay': timedelta(seconds=10),
    'retry_exponential_backoff': True,
}
```
При ошибке задача перезапускается до 2 раз с увеличивающейся задержкой.

#### 3. Email
```python
default_args = {
    'email': ['admin@example.com'],
    'email_on_failure': True,
    'email_on_retry': True,
}
```
Используется `EmailOperator` для уведомлений. Все письма видны в MailHog (http://localhost:8025)

#### 4. Обработка данных
- Чтение CSV
- Трансформация: `bonus_money = money * 2`
- Условное ветвление
- Финализация

---

## Выводы

Apache Airflow подходит для задачи:
- Готовые интеграции с BigQuery, Redshift, Kafka, Spark
- Ветвление, условия, event-triggers
- Retry, fallback, email из коробки
- Можно развернуть в облаке (AWS, GCP)
- Масштабируется до миллионов записей