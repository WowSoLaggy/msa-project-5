# Spring Batch Demo - Быстрый старт

## Самый простой способ запуска (Ubuntu)

### 1. Убедитесь что установлен Docker
```bash
docker --version
docker-compose --version
```

### 2. Дайте права на выполнение скриптам
```bash
chmod +x *.sh
```

### 3. Запустите демо
```bash
./run-demo.sh
```

Скрипт автоматически:
- ✅ Запустит PostgreSQL
- ✅ Создаст таблицы
- ✅ Загрузит справочные данные
- ✅ Соберет и запустит Spring Batch приложение

### 4. Проверьте результаты
```bash
./check-results.sh
```

### 5. Очистка (опционально)
```bash
./cleanup.sh
```

## Что происходит внутри?

1. **Читается CSV**: [product-data.csv](src/main/resources/product-data.csv)
   ```
   1,20001,hammer,45,Loyality_off
   2,30001,sink,20,Loyality_off
   ...
   ```

2. **Обогащение данными** из таблицы `loyality_data`:
   ```
   productSku=20001 → Loyality_on
   ```

3. **Результат в таблице** `products`:
   ```
   productId=1, productSku=20001, productData=Loyality_on ✅
   ```

## Ручной запуск (без скриптов)

```bash
# 1. Запуск БД
docker-compose up -d postgresdb
sleep 15

# 2. Создание таблиц
docker exec -i $(docker ps -qf "name=postgresdb") psql -U postgres -d productsdb < src/main/resources/schema-all.sql

# 3. Загрузка данных loyality
docker cp src/main/resources/loyality_data.csv $(docker ps -qf "name=postgresdb"):/tmp/
docker exec -i $(docker ps -qf "name=postgresdb") psql -U postgres -d productsdb -c "COPY loyality_data FROM '/tmp/loyality_data.csv' DELIMITER ',' CSV;"

# 4. Запуск приложения
docker-compose up --build app
```

## Проверка вручную

```bash
# Подключиться к БД
docker exec -it $(docker ps -qf "name=postgresdb") psql -U postgres -d productsdb

# В psql выполнить:
SELECT * FROM products;
SELECT * FROM loyality_data;
\q
```

## Структура проекта

```
complete/
├── run-demo.sh              ⭐ Главный скрипт
├── check-results.sh         📊 Проверка результатов
├── cleanup.sh              🧹 Очистка
├── docker-compose.yml      🐳 PostgreSQL + App
├── Dockerfile              📦 Сборка Java приложения
├── .env                    🔐 Переменные окружения
└── src/main/
    ├── java/.../batchprocessing/
    │   ├── BatchConfiguration.java    # Job/Step конфигурация
    │   ├── ProductItemProcessor.java  # ETL логика
    │   └── ...
    └── resources/
        ├── application.properties     # Spring настройки
        ├── schema-all.sql            # DDL
        ├── product-data.csv          # Входные данные
        └── loyality_data.csv         # Справочник
```

## FAQ

**Q: Приложение падает с ошибкой "relation products does not exist"**  
A: Таблицы не созданы. Запустите `./run-demo.sh` или создайте вручную через schema-all.sql

**Q: Как повторно запустить обработку?**  
A: `docker-compose restart app`

**Q: Как изменить chunk size?**  
A: Отредактируйте [BatchConfiguration.java](src/main/java/com/example/batchprocessing/BatchConfiguration.java), строка `chunk(3, ...)` → `chunk(100, ...)`

**Q: Как добавить свои данные?**  
A: Отредактируйте [product-data.csv](src/main/resources/product-data.csv), пересоберите: `docker-compose up --build app`

**Q: Где посмотреть историю запусков?**  
A: 
```sql
SELECT * FROM batch_job_execution;
SELECT * FROM batch_step_execution;
```

## Дальше

- 📖 [../results/README.md](../results/README.md) - полная документация
- 📝 [../results/ADR.md](../results/ADR.md) - обоснование архитектурных решений
- 🎨 [../results/architecture-c4.puml](../results/architecture-c4.puml) - диаграммы
