# Task 5: Мониторинг, оповещение и логирование

## Описание

Данный проект демонстрирует комплексное решение для мониторинга, логирования и оповещений для Spring Batch приложения с использованием современного стека инструментов.

## Реализованные компоненты

### 1. Мониторинг метрик
- **Prometheus** - сбор и хранение метрик
- **Grafana** - визуализация метрик через дашборды
- **Spring Boot Actuator + Micrometer** - экспорт метрик из приложения

### 2. Логирование
- **ELK стек** (Elasticsearch, Logstash, Kibana) - централизованное логирование
- **Filebeat** - сбор логов из Docker контейнеров
- **Logback с Logstash Encoder** - структурированные логи в JSON формате

### 3. Оповещения
- **Prometheus Alerting** - правила оповещений
- **Grafana Alerting** - визуализация и управление алертами

## Метрики

### Кастомные метрики Spring Batch
- `batch.items.processed` - количество обработанных элементов
- `batch.job.completed` - количество успешно завершенных заданий
- `batch.job.failed` - количество провалившихся заданий

### Системные метрики
- `process_cpu_usage` - использование CPU
- `jvm_memory_used_bytes` - использование памяти JVM
- `http_server_requests_seconds_count` - количество HTTP запросов
- `spring_batch_job_duration_seconds` - длительность выполнения заданий

## Оповещения

Настроены следующие алерты в Prometheus:

1. **BatchJobFailed** (критическое)
   - Условие: `batch_job_failed_total{job="batch-processing"} > 0`
   - Описание: Оповещение при провале batch задания

2. **HighCPUUsage** (предупреждение)
   - Условие: `process_cpu_usage{job="batch-processing"} * 100 > 80`
   - Описание: Оповещение при загрузке CPU выше 80% в течение 1 минуты

## Запуск проекта

### Шаги запуска

1. **Сборка Docker образов:**
   ```powershell
   cd c:\Projects\msa-project-5\task-5\results
   docker compose build
   ```

2. **Запуск всех сервисов:**
   ```powershell
   docker compose up -d
   ```

3. **Проверка статуса сервисов:**
   ```powershell
   docker compose ps
   ```

### Доступ к компонентам

После запуска доступны следующие интерфейсы:

| Сервис | URL | Описание |
|--------|-----|----------|
| Spring Batch App | http://localhost:8080 | Batch приложение |
| Actuator Metrics | http://localhost:8080/actuator/prometheus | Метрики в формате Prometheus |
| Prometheus | http://localhost:9090 | UI Prometheus |
| Grafana | http://localhost:3000 | Дашборды (admin/admin) |
| Kibana | http://localhost:5601 | Просмотр логов |
| Elasticsearch | http://localhost:9200 | API Elasticsearch |

### Проверка работы

1. **Проверка метрик в Prometheus:**
   - Откройте http://localhost:9090
   - Перейдите в Status → Targets
   - Убедитесь, что `batch-processing` в состоянии UP

2. **Просмотр дашборда в Grafana:**
   - Откройте http://localhost:3000
   - Войдите (admin/admin)
   - Перейдите в Dashboards → batch-processing-dashboard
   - Вы увидите графики CPU, Memory, Batch метрики

3. **Проверка алертов в Prometheus:**
   - Откройте http://localhost:9090/alerts
   - Просмотрите настроенные правила оповещений

4. **Просмотр логов в Kibana:**
   - Откройте http://localhost:5601
   - Перейдите в Management → Stack Management → Index Patterns
   - Создайте index pattern: `filebeat-*`
   - Перейдите в Discover для просмотра логов

### Остановка сервисов

```powershell
docker compose down
```

Для удаления всех данных (volumes):
```powershell
docker compose down -v
```

## Документация

- **[architecture-c4.puml](architecture-c4.puml)** - C4-диаграмма архитектуры с компонентами мониторинга и логирования
- **[metrics.md](metrics.md)** - Подробное описание и обоснование выбранных метрик
- **[monitoring-logging-decisions.md](monitoring-logging-decisions.md)** - Обоснование технических решений по мониторингу, логированию и оповещениям
