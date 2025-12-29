# Task 5: Мониторинг, оповещение и логирование

## Реализованные компоненты

### Мониторинг метрик
- Prometheus для сбора метрик
- Grafana для визуализации
- Spring Boot Actuator + Micrometer для экспорта метрик

### Логирование
- ELK стек (Elasticsearch, Logstash, Kibana)
- Filebeat для сбора логов из Docker контейнеров
- Logback с Logstash Encoder для JSON формата логов

### Оповещения
- Grafana Alerting для оповещений по метрикам

## Метрики

### Кастомные метрики Spring Batch
- `batch.items.processed` - количество обработанных элементов
- `batch.job.completed` - количество успешно завершенных заданий
- `batch.job.failed` - количество провалившихся заданий

### Системные метрики
- CPU Usage
- Memory Usage
- HTTP Requests
- Job Duration

## Оповещения

1. **Batch Job Failed** - критическое оповещение при провале задания
2. **High CPU Usage** - предупреждение при загрузке CPU выше 80%

## Архитектура

См. `architecture-c4.puml` для диаграммы архитектуры с компонентами мониторинга и логирования.

## Обоснование решений

См. `monitoring-logging-decisions.md` для подробного обоснования выбранных решений.

