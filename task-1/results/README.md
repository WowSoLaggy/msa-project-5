# Задание 1: Решение для пакетной обработки данных

## Выбор технологического решения: Apache Airflow

### Обоснование выбора

**Apache Airflow** - оптимальное решение для требований задачи:

#### 1. Готовые интеграции (провайдеры)
- ✅ **BigQuery**: `apache-airflow-providers-google`
- ✅ **Redshift**: `apache-airflow-providers-amazon` 
- ✅ **Kafka**: `apache-airflow-providers-apache-kafka`
- ✅ **Spark**: `apache-airflow-providers-apache-spark`

Все интеграции устанавливаются через pip и имеют готовые операторы.

#### 2. Поддержка требуемого функционала

| Требование | Поддержка | Реализация |
|------------|-----------|------------|
| Ветвление пайплайна | ✅ Да | `BranchPythonOperator` |
| Условные операторы | ✅ Да | `trigger_rule`, условия в Python |
| Event-triggers | ✅ Да | Sensors, API triggers |
| Retry логика | ✅ Да | Встроенная с экспоненциальной задержкой |
| Fallback logic | ✅ Да | `on_failure_callback` |
| Email уведомления | ✅ Да | Встроенные, настраиваются в DAG |

#### 3. Облачное развертывание

- **AWS**: MWAA (Managed Workflows for Apache Airflow)
- **GCP**: Cloud Composer (полностью управляемый Airflow)
- **Azure**: Самостоятельное развертывание в AKS
- **Kubernetes**: Официальные Helm charts для любого облака

**Преимущества управляемых сервисов:**
- Автоматические обновления
- Встроенный мониторинг
- Масштабирование из коробки
- Интеграция с облачными сервисами

#### 4. Масштабирование

Для обработки ~1 млн записей используются:
- **LocalExecutor** - для простых задач
- **CeleryExecutor** - для распределенной обработки
- **KubernetesExecutor** - для динамического масштабирования

---

## POC (Proof of Concept)

### Демонстрируемая функциональность

1. ✅ Чтение данных из CSV файла (симуляция файлового хранилища)
2. ✅ Анализ данных и ветвление пайплайна по условию
3. ✅ Retry-политика с экспоненциальной задержкой
4. ✅ Email-уведомления при успехе/ошибке

### Архитектура POC

```
┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       v
┌─────────────────┐
│  Read CSV Data  │  ← Чтение данных
└──────┬──────────┘
       │
       v
┌──────────────────┐
│ Analyze & Branch │  ← Условное ветвление
└────┬─────────┬───┘
     │         │
     v         v
┌─────────┐ ┌─────────┐
│ Large   │ │ Small   │  ← Разные стратегии обработки
│ Volume  │ │ Volume  │
└────┬────┘ └────┬────┘
     │           │
     └─────┬─────┘
           v
    ┌─────────────┐
    │   Report    │  ← Генерация отчета
    └──────┬──────┘
           v
    ┌─────────────┐
    │     End     │
    └─────────────┘
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
   - Login: `admin`
   - Password: `admin`

5. **Откройте MailHog** (для просмотра email):
   - URL: http://localhost:8025

6. **Активируйте и запустите DAG** `batch_processing_pipeline_poc`

### Демонстрация функционала

#### 1. Ветвление пайплайна
Если записей > 500 → используется `process_large_volume`  
Если записей ≤ 500 → используется `process_small_volume`

#### 2. Retry политика
```python
default_args = {
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
    'retry_exponential_backoff': True,
}
```
При ошибке таск автоматически перезапускается до 3 раз с увеличивающейся задержкой.

#### 3. Email уведомления
```python
default_args = {
    'email': ['alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'email_on_success': True,
}
```
Все уведомления видны в MailHog (http://localhost:8025)

### Скриншоты

Скриншоты демонстрации находятся в папке `screenshots/`:
1. `01_airflow_dags.png` - список DAG'ов
2. `02_dag_graph.png` - граф пайплайна с ветвлением
3. `03_dag_running.png` - выполнение DAG
4. `04_task_retry.png` - демонстрация retry
5. `05_email_notifications.png` - email в MailHog
6. `06_logs.png` - логи выполнения

---

## Заключение

Apache Airflow полностью покрывает все требования:
- ✅ Готовые интеграции с BigQuery, Redshift, Kafka, Spark
- ✅ Ветвление, условия, event-triggers
- ✅ Retry, fallback, email из коробки
- ✅ Легкий переход в облако через MWAA/Cloud Composer
- ✅ Масштабируется до миллионов записей

**Локальное развертывание готово к production-переносу в облако без изменения кода DAG.**