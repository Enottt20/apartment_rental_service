## Сервис может запускаться из коробки
В docker-compose установленны значения по умолчанию. Однако все же рекомендую создать файл .env и настроить свои параметры.

Для создания файла конфигурации достаточно переименовать example.env в .env

## Настоятельно рекомендую использовать свои данные почты в файлах конфигурации
Я добавил тестовую почту. Не думаю что она продержиться долго. Так же если будете использовать свою почту не забудьте поменять параметры сервера, порта и ssl
```ini
EMAIL_PASSWORD=pfxgsdpenvktcvtv
EMAIL_LOGIN=yantestsss22@yandex.ru
SMTP_PORT=587
SMTP_SERVER=smtp.yandex.com
IS_SMPT_SSL=False
```

## Запуск в docker-compose
Для запуска нужно прописать данную комманду в директории Deploy предварительно запустив docker
```ini
docker compose up -d
```