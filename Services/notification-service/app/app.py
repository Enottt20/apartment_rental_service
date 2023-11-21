import json
import config, email_sender
import logging
import broker, schemas, notification_forms
from kombu import Message
import threading


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

consumer_apartment_rental = broker.Consumer(str(cfg.RABBITMQ_DSN), cfg.QUEUE_RESERVATION_NAME)
consumer_publish_review = broker.Consumer(str(cfg.RABBITMQ_DSN), cfg.QUEUE_REVIEW_NAME)

email_send = email_sender.EmailSender(cfg.EMAIL_LOGIN, cfg.EMAIL_PASSWORD, cfg.IS_SMPT_SSL, cfg.SMTP_SERVER, cfg.SMTP_PORT)
email_send.connect_to_server()

def send_email_message_apartment_rental(body, message: Message):
    data = json.loads(body)

    reservation_data = schemas.ReservationNotification(**data)

    notification = notification_forms.reservation_notification_message(reservation_data)

    email_send.send_message('Apartment rental', notification, reservation_data.email)

def send_email_message_review(body, message: Message):
    data = json.loads(body)

    review_data = schemas.ReviewNotification(**data)

    notification = notification_forms.review_notification_message(review_data)

    email_send.send_message('Review', notification, review_data.email)




consumer_apartment_rental.add_callback(send_email_message_apartment_rental)
consumer_publish_review.add_callback(send_email_message_review)

def main():
    # Создаем отдельные потоки для каждого потребителя
    thread_apartment_rental = threading.Thread(target=consumer_apartment_rental.run)
    thread_publish_review = threading.Thread(target=consumer_publish_review.run)

    # Запускаем потоки
    thread_apartment_rental.start()
    thread_publish_review.start()

    # Ждем, пока оба потока завершат выполнение
    thread_apartment_rental.join()
    thread_publish_review.join()

if __name__ == "__main__":
    main()