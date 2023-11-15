# Инструкция по установке и запуску сервиса уведомлений

Этот сервис делает рассылки на почту пользователям
заказавших аренду

Для начала работы нужно добавить данные о своей почте
в env как в example.env

Необходимо что бы почта поддерживала SMTP. 
Пример настройки почты gmail -
https://youtu.be/g_j6ILT-X0k?si=50YQ8Gg328tIczLZ&t=24

Данные конфигураций для яндекса -

```ini
EMAIL_PASSWORD=pass
EMAIL_LOGIN=example@yandex.ru
SMTP_PORT=587
SMTP_SERVER=smtp.yandex.com
IS_SMPT_SSL=False
```

Для гугла - 
```ini
EMAIL_PASSWORD=pass
EMAIL_LOGIN=example@gmail.ru
SMTP_PORT=587
SMTP_SERVER=smtp.gmail.com
IS_SMPT_SSL=False
```

Сервис так же может работать без почты. Будет просто писать логи

# Запуск тестов
```bash
python -m unittest
```

Для запуска нужно перейти в Deploy:
```bash
docker-compose up -d
```