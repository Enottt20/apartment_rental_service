# User service
Сервис включает в себя:

1. **POST /groups/**
   - Создает новую группу.

2. **GET /groups/**
   - Получает все группы.

3. **GET /groups/{GroupID}**
   - Получает группу по идентификатору.

4. **PUT /groups/{GroupID}**
   - Обновляет группу по идентификатору.

5. **DELETE /groups/{GroupID}**
   - Удаляет группу по идентификатору.


# Запуск
Script: `source run.sh`\
Uvicorn: `uvicorn app:app --port 8003 --reload`

# Building from Dockerfile
```bash
docker build -t "user-service:1.0" .
```