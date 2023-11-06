import json
import multiprocessing

from fastapi import FastAPI, Depends
import config, email_sender
import typing
import logging
import broker, schemas, notification_forms
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

email_send = email_sender.EmailSender(cfg.EMAIL_LOGIN, cfg.EMAIL_PASSWORD, cfg.SMTP_SERVER, cfg.SMTP_PORT)

def send_email_message(body, message: Message):
    data = json.loads(body)

    reservation_data = schemas.ReservationNotification(**data)

    notification = notification_forms.reservation_notification_message(reservation_data)

    email_send.send_message('Apartment rental', notification, reservation_data.email)




consumer.add_callback(send_email_message)


def run_consumer():
    consumer.run()

@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(consumer.run())

if __name__ == "__main__":
    consumer_process = multiprocessing.Process(target=run_consumer)
    consumer_process.start()

    uvicorn.run(app, host="0.0.0.0", port=5006)