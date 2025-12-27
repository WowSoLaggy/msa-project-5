# Демонстрация работы Spring Batch приложения

## Что нужно показать для сдачи задания

### 1. Успешный запуск приложения

**Команда:**
```bash
cd task-4/complete
./run-demo.sh
```

**Что показать:**
- ✅ Успешный старт PostgreSQL
- ✅ Создание таблиц
- ✅ Загрузка loyality_data
- ✅ Сборка приложения
- ✅ Логи Spring Batch с обработкой данных

**Важные строки в логах:**
```
Transforming (Product[productId=1, productSku=20001, productName=hammer, productAmount=45, productData=Loyality_off]) 
         into (Product[productId=1, productSku=20001, productName=hammer, productAmount=45, productData=Loyality_on])
...
!!! JOB FINISHED! Time to verify the results
Transformed <Product[productId=1, productSku=20001, productName=hammer, productAmount=45, productData=Loyality_on]> in the database.
```

### 2. Результаты в базе данных

**Команда:**
```bash
./check-results.sh
```

**Что показать:**
- ✅ Таблица `products` с обновленными данными
- ✅ Таблица `loyality_data` со справочными данными
- ✅ Таблица `batch_job_execution` с историей запусков (статус COMPLETED)

**Пример вывода:**
```
 productid | productsku | productname | productamount | productdata 
-----------+------------+-------------+---------------+-------------
         1 |      20001 | hammer      |            45 | Loyality_on    ← было Loyality_off!
         2 |      30001 | sink        |            20 | Loyality_on    ← было Loyality_off!
         3 |      40001 | roof_shell  |           256 | Loyality_on    ← уже было Loyality_on
         4 |      50001 | priming     |            67 | Loyality_on    ← было Loyality_off!
         5 |      60001 | clapboard   |           120 | Loyality_on    ← уже было Loyality_on
```

### 3. Сравнение данных до и после

**До обработки (product-data.csv):**
```csv
1,20001,hammer,45,Loyality_off      ← OFF
2,30001,sink,20,Loyality_off        ← OFF
3,40001,roof_shell,256,Loyality_on
4,50001,priming,67,Loyality_off     ← OFF
5,60001,clapboard,120,Loyality_on
```

**Справочник (loyality_data):**
```csv
20001,Loyality_on    ← для hammer
30001,Loyality_on    ← для sink
50001,Loyality_on    ← для priming
60001,Loyality_on    ← для clapboard
```

**После обработки (таблица products):**
```
Все productData обновлены на Loyality_on где был match по productSku! ✅
```

### 4. Архитектурные диаграммы

Показать файлы:
- ✅ [ADR.md](../results/ADR.md) - обоснование выбора Spring Batch
- ✅ [architecture-c4.puml](../results/architecture-c4.puml) - общая архитектура
- ✅ [spring-batch-components.puml](../results/spring-batch-components.puml) - детальная схема

Можно рендерить через:
- PlantUML plugin в VS Code
- https://www.plantuml.com/plantuml/uml/
- IntelliJ IDEA с PlantUML plugin

## Формат демонстрации

### Вариант 1: Скриншоты (минимум)

1. **screenshot-1-run.png**: Вывод команды `./run-demo.sh`
2. **screenshot-2-logs.png**: Логи Spring Batch с transforming
3. **screenshot-3-results.png**: Вывод `./check-results.sh`
4. **screenshot-4-adr.png**: Открытый файл ADR.md
5. **screenshot-5-diagram.png**: Рендер C4 диаграммы

### Вариант 2: Видео (рекомендуется)

Записать экран (2-3 минуты):

1. Показать структуру проекта `tree task-4/`
2. Открыть `product-data.csv` и показать исходные данные
3. Запустить `./run-demo.sh`
4. Дождаться завершения, показать ключевые логи
5. Запустить `./check-results.sh`
6. Показать изменения в данных (было OFF → стало ON)
7. Кратко пролистать ADR.md
8. Показать одну из диаграмм

**Инструменты для записи:**
- Ubuntu: `kazam`, `SimpleScreenRecorder`, `OBS Studio`
- Или записать через Zoom/Teams

## Чеклист для проверки

Перед демонстрацией убедитесь:

- [ ] Docker и Docker Compose установлены
- [ ] Скрипты имеют права на выполнение (`chmod +x *.sh`)
- [ ] Порт 5432 свободен (нет других PostgreSQL)
- [ ] `./run-demo.sh` выполняется без ошибок
- [ ] В логах есть "JOB FINISHED"
- [ ] `./check-results.sh` показывает обновленные данные
- [ ] ADR.md содержит обоснование решения
- [ ] Диаграммы корректно рендерятся

## Типичные проблемы

**Ошибка: "port 5432 already allocated"**
```bash
# Остановить существующий PostgreSQL
sudo systemctl stop postgresql
# Или изменить порт в .env: POSTGRESDB_LOCAL_PORT=5433
```

**Ошибка: "relation products does not exist"**
```bash
# Таблицы не созданы, запустите заново:
./cleanup.sh
./run-demo.sh
```

**Ошибка: "permission denied" при запуске скриптов**
```bash
chmod +x *.sh
```

**Приложение завершается сразу после старта**
```bash
# Это нормально! Spring Batch выполняет job и завершается.
# Проверьте логи:
docker logs msa-project-5-app-1
```

## Пример успешного вывода

```bash
$ ./run-demo.sh
=== Запуск Spring Batch Demo ===

✅ Docker и Docker Compose найдены

📦 Остановка старых контейнеров (если есть)...

🚀 Запуск PostgreSQL...

⏳ Ожидание готовности PostgreSQL (15 секунд)...

📋 Создание таблиц в БД...
CREATE TABLE
CREATE TABLE

📊 Загрузка справочных данных (loyality_data)...
COPY 4

🔨 Сборка и запуск Spring Batch приложения...
[...]
Transforming (Product[productId=1, ...]) into (Product[...])
[...]
!!! JOB FINISHED! Time to verify the results
Transformed <Product[productId=1, productSku=20001, productName=hammer, productAmount=45, productData=Loyality_on]> in the database.

✅ Готово! Проверьте логи выше.
```

```bash
$ ./check-results.sh
=== Проверка результатов Spring Batch ===

📊 Таблица products:
 productid | productsku | productname | productamount | productdata 
-----------+------------+-------------+---------------+-------------
         1 |      20001 | hammer      |            45 | Loyality_on
         2 |      30001 | sink        |            20 | Loyality_on
         3 |      40001 | roof_shell  |           256 | Loyality_on
         4 |      50001 | priming     |            67 | Loyality_on
         5 |      60001 | clapboard   |           120 | Loyality_on

📋 Таблица loyality_data:
 productsku | loyalitydata 
------------+--------------
      20001 | Loyality_on
      30001 | Loyality_on
      50001 | Loyality_on
      60001 | Loyality_on

📈 История выполнения Jobs:
 job_instance_id |    job_name      |         start_time         |          end_time          | status
-----------------+------------------+----------------------------+----------------------------+-----------
               1 | importProductJob | 2025-12-27 10:30:15.123456 | 2025-12-27 10:30:18.654321 | COMPLETED

✅ Проверка завершена!
```
