# Task 4: Spring Batch ETL для TradeWare

## 🚀 Быстрый старт (Ubuntu)

```bash
cd complete
chmod +x *.sh
./run-demo.sh
```

Готово! Приложение запущено и данные обработаны.

Проверить результаты: `./check-results.sh`

---

## Описание решения

Реализовано POC приложение на Spring Batch для пакетной обработки данных о складских остатках.

### Что делает приложение:
1. **Читает** CSV файл с данными о товарах (`product-data.csv`)
2. **Обогащает** данные информацией о программе лояльности из БД (`loyality_data`)
3. **Записывает** обработанные данные в таблицу `products`

### Архитектура:
- **Job**: `importProductJob` - основная задача
- **Step**: обработка chunk'ами по 3 записи
- **Reader**: читает CSV
- **Processor**: обновляет данные из таблицы loyality_data
- **Writer**: batch-вставка в PostgreSQL

## Результаты

- ✅ [ADR.md](ADR.md) - обоснование выбора Spring Batch с анализом альтернатив
- ✅ [architecture-c4.puml](architecture-c4.puml) - C4 диаграмма системного уровня
- ✅ [spring-batch-components.puml](spring-batch-components.puml) - детальная схема компонентов Spring Batch
- ✅ [HOW_IT_WORKS.md](HOW_IT_WORKS.md) - визуализация работы ETL процесса шаг за шагом
- ✅ [DEMO.md](DEMO.md) - инструкция для создания скриншотов/видео демонстрации
- ✅ Рабочее приложение в папке [../complete](../complete)
  - Скрипты для запуска: `run-demo.sh`, `check-results.sh`, `cleanup.sh`
  - [README в complete/](../complete/README.md) с подробными инструкциями

## Быстрый старт (Ubuntu)

### Требования:
- Docker
- Docker Compose

### Запуск:

```bash
cd task-4/complete

# Запустить БД и приложение
docker-compose up --build

# После первого запуска создать таблицы (в другом терминале):
docker exec -i msa-project-5-postgresdb-1 psql -U postgres -d productsdb < src/main/resources/schema-all.sql

# Заполнить справочник лояльности:
docker exec -i msa-project-5-postgresdb-1 psql -U postgres -d productsdb -c "COPY loyality_data FROM '/tmp/loyality_data.csv' DELIMITER ',' CSV;"

# Или вручную:
docker exec -it msa-project-5-postgresdb-1 psql -U postgres -d productsdb
# Затем в psql:
# \i /path/to/schema-all.sql
# Вставить данные из loyality_data.csv

# Перезапустить приложение для повторной обработки:
docker-compose restart app
```

### Альтернативный запуск (если есть Java 17):

```bash
cd task-4/complete

# Запустить только БД
docker-compose up -d postgresdb

# Создать таблицы
docker exec -i msa-project-5-postgresdb-1 psql -U postgres -d productsdb < src/main/resources/schema-all.sql

# Запустить приложение локально
./gradlew bootRun
```

## Проверка результатов

### Просмотр логов приложения:
```bash
docker logs -f msa-project-5-app-1
```

Ожидаемый вывод:
```
Transforming (Product[productId=1, productSku=20001, ...]) into (Product[...])
Job completed with status: COMPLETED
Found 5 products in database
Product{productId=1, productSku=20001, productName='hammer', productData='Loyality_on'}
...
```

### Проверка данных в БД:
```bash
docker exec -it msa-project-5-postgresdb-1 psql -U postgres -d productsdb

# В psql:
SELECT * FROM products;
SELECT * FROM loyality_data;
```

Ожидаемый результат:
- Таблица `products` содержит 5 записей
- Поле `productData` обновлено значениями из `loyality_data` (там где был match по SKU)

## Структура проекта

```
complete/
├── docker-compose.yml          # Оркестрация PostgreSQL + App
├── Dockerfile                  # Образ приложения
├── .env                       # Параметры подключения к БД
├── build.gradle               # Зависимости проекта
└── src/main/
    ├── java/.../batchprocessing/
    │   ├── BatchConfiguration.java           # Конфигурация Job/Step
    │   ├── ProductItemProcessor.java         # Логика обогащения
    │   ├── Product.java                      # Record для товара
    │   ├── Loyality.java                     # Record для лояльности
    │   ├── BatchProcessingApplication.java   # Main
    │   └── JobCompletionNotificationListener.java
    └── resources/
        ├── application.properties    # Настройки Spring/БД
        ├── schema-all.sql           # DDL для таблиц
        ├── product-data.csv         # Входные данные
        └── loyality_data.csv        # Справочник лояльности
```

## Демонстрация работы

### Шаг 1: Исходные данные

**product-data.csv:**
```csv
1,20001,hammer,45,Loyality_off
2,30001,sink,20,Loyality_off
...
```

**loyality_data (таблица в БД):**
```
productSku | loyalityData
20001      | Loyality_on
30001      | Loyality_on
...
```

### Шаг 2: Обработка

Spring Batch:
1. Читает каждую строку из CSV
2. Processor ищет loyalityData по productSku
3. Если найдено - обновляет productData
4. Writer сохраняет в products

### Шаг 3: Результат

**products (таблица в БД):**
```
productId | productSku | productName | productData
1         | 20001      | hammer      | Loyality_on  ✅ (обновлено!)
2         | 30001      | sink        | Loyality_on  ✅ (обновлено!)
3         | 40001      | roof_shell  | Loyality_on  ✅ (обновлено!)
...
```

## Ключевые особенности реализации

### 1. Chunk-based Processing
```java
.<Product, Product>chunk(3, transactionManager)
```
- Читает 3 записи
- Обрабатывает их
- Записывает одним batch-запросом
- Commit транзакции

### 2. Обогащение данных
```java
String sql = "SELECT * FROM loyality_data WHERE productSku=" + productSku;
jdbcTemplate.query(sql, ...)
```
- Для каждого товара запрашивает программу лояльности
- Обновляет productData

### 3. Batch Insert
```java
.sql("INSERT INTO products (productId, productSku, ...) VALUES (...)")
.beanMapped()
```
- Вставка всех записей chunk'а одним запросом

### 4. Мониторинг через JobRepository
Spring Batch автоматически:
- Сохраняет историю запусков в BATCH_* таблицах
- Логирует статус выполнения
- Позволяет перезапустить failed jobs

## Возможные улучшения

Для production:
1. **Увеличить chunk size** до 100-1000 (сейчас 3 для демонстрации)
2. **Добавить validation** входных данных
3. **Реализовать retry** при ошибках БД
4. **Добавить skip logic** для некорректных записей
5. **Интеграция с GCS** для чтения файлов из облака
6. **REST API** для запуска jobs по требованию
7. **Spring Boot Actuator** для метрик
8. **Partitioning** для параллельной обработки больших файлов

## Альтернативы Spring Batch

См. [ADR.md](ADR.md):
- Apache Airflow (Python, оркестрация)
- Apache NiFi (визуальный дизайнер)
- Custom Java code (полный контроль)

Spring Batch выбран для простоты, готовых решений и интеграции с Java-стеком.
