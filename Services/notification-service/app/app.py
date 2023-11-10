import json
import config, email_sender
import logging
import broker, schemas, notification_forms
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

consumer = broker.Consumer(str(cfg.RABBITMQ_DSN), str(cfg.QUEUE_NAME))

email_send = email_sender.EmailSender(cfg.EMAIL_LOGIN, cfg.EMAIL_PASSWORD, cfg.IS_SMPT_SSL, cfg.SMTP_SERVER, cfg.SMTP_PORT)

def send_email_message(body, message: Message):
    data = json.loads(body)

    reservation_data = schemas.ReservationNotification(**data)

    notification = notification_forms.reservation_notification_message(reservation_data)

    email_send.send_message('Apartment rental', notification, reservation_data.email)


consumer.add_callback(send_email_message)

def main():
    consumer.run()

if __name__ == "__main__":
    main()