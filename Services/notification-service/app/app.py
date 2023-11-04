import json
import multiprocessing

from fastapi import FastAPI, Depends
from . import config
import typing
import logging
from . import broker, schemas, notification_forms
import uvicorn
import asyncio
from kombu import Message


# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

# load config
cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json()}'
)


app = FastAPI(
    title='Notification service'
)

consumer = broker.Consumer(str(cfg.RABBITMQ_DSN), str(cfg.QUEUE_NAME))


def fo(body, message: Message):
    ss = json.loads(body)

    # Создаем объект ReservationNotification
    reservation_data = schemas.ReservationNotification(**ss)

    # Далее можно использовать объект reservation_data для обработки данных
    n = notification_forms.reservation_notification_message(reservation_data)
    print(n)


consumer.add_callback(fo)

def run_consumer():
    consumer.run()

@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(consumer.run())

if __name__ == "__main__":
    # Запускаем ваш сервис в отдельном процессе
    consumer_process = multiprocessing.Process(target=run_consumer)
    consumer_process.start()

    # Запускаем FastAPI приложение
    uvicorn.run(app, host="0.0.0.0", port=8000)