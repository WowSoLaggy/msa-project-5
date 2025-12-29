# Метрики для мониторинга Spring Batch приложения

## Кастомные метрики

### batch.items.processed
- **Тип:** Counter
- **Описание:** Количество обработанных элементов
- **Использование:** Отслеживание прогресса обработки данных

### batch.job.completed
- **Тип:** Counter
- **Описание:** Количество успешно завершенных заданий
- **Использование:** Мониторинг успешности выполнения заданий

### batch.job.failed
- **Тип:** Counter
- **Описание:** Количество провалившихся заданий
- **Использование:** Обнаружение проблем в работе batch-обработки

## Стандартные метрики Spring Boot Actuator

### Системные метрики
- `process_cpu_usage` - использование CPU
- `jvm_memory_used_bytes` - использование памяти JVM
- `jvm_memory_max_bytes` - максимальная память JVM

### Метрики Spring Batch
- `spring_batch_job_duration_seconds` - длительность выполнения заданий
- `spring_batch_job_active` - активные задания

### HTTP метрики
- `http_server_requests_seconds_count` - количество HTTP запросов
- `http_server_requests_seconds_sum` - суммарное время обработки запросов

## Доступ к метрикам

Метрики доступны через Spring Boot Actuator endpoint:
- Prometheus формат: `http://localhost:8080/actuator/prometheus`
- JSON формат: `http://localhost:8080/actuator/metrics`

