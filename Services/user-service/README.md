# User service
Для начала работы нужно переименовать example.env -> .env\
и поменять данные на свои

# Запуск
Script: `source run.sh`\
Uvicorn: `uvicorn app:app --port 8003 --reload`

# Building from Dockerfile
```bash
docker build -t "user-service:1.0" .
```