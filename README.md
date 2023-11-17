# Инструкция по запуску процесса поиска уязвимостей

## Анализ исходного кода сервисов
1) Установить bandit:
```sh
pip install bandit
```
2) Запустить проверку в нужной дериктории
```sh
python3 -m bandit -r ./dir
```

## Анализ докер образов
Нужно просто запустить эту команду и вписать название интересующего образа вместо IMAGE_NAME
```sh
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image IMAGE_NAME
```
Если не работает то попробуйте в начале прописать эту команду
```sh
docker pull aquasec/trivy
```