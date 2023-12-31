# Apartment service
Сервис для работы с апартаментами. Включает в себя:

1. **GET /apartments/{apartment_id}**
   - Возвращает информацию о квартире по указанному айди.

2. **GET /apartments**
   - Возвращает список квартир с возможностью фильтрации относительно определенных координат.

3. **POST /apartments**
   - Добавляет новую квартиру в базу данных.

4. **PATCH /apartments/{apartment_id}**
   - Обновляет информацию о квартире по айди.

5. **DELETE /apartments/{apartment_id}**
   - Удаляет квартиру из базы данных.

# Инструкция по установке и запуску сервиса

Перед запуском сервиса необходимо установить все зависимости. Для этого выполните следующие шаги:

1. Установите и активируйте виртуальное окружение Python.

2. Выполните команду pip install -r requirements.txt.

3. Требуется установить расширение для postgres - postgis

После установки зависимостей вы можете запустить сервис. Для этого выполните одну из следующих команд:

- uvicorn app:app --port 8002 --reload - запуск сервиса с помощью Uvicorn на порту 8002 с автоматической перезагрузкой при изменении кода.
- ./run.sh - запуск сервиса с помощью скрипта run.sh.

# Запуск тестов
```bash
python -m unittest
```

### Сборкра docker образа
```bash
docker build -t "apartment-service:1.0" .
```

Для запуска нужно перейти в Deploy:
```bash
docker compose up -d
```