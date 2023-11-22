import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging import getLogger
import threading
import time

logger = getLogger("notification-service")

class EmailSender():
    def __init__(self, smtp_username, smtp_password, is_smtp_ssl, smtp_server="smtp.gmail.com", smtp_port=587):
        self.__smtp_username = smtp_username
        self.__smtp_password = smtp_password
        self.__is_smtp_ssl = is_smtp_ssl
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        self.server = None

        # Запускаем поток для периодического вывода состояния соединения
        self.connection_status_thread = threading.Thread(target=self.log_connection_status_thread)
        self.connection_status_thread.daemon = True
        self.connection_status_thread.start()

    def log_connection_status_thread(self):
        while True:
            time.sleep(10)  # Задержка в секундах между проверками
            self.log_connection_status()

    def log_connection_status(self):
        if self.server:
            try:
                status_code = self.server.noop()[0]
                logger.info(f"Состояние соединения: {status_code}")
            except Exception as e:
                logger.error(f"Ошибка при проверке состояния соединения: {e}")
        else:
            logger.info("Сервер не подключен.")

    def connect_to_server(self):
        try:
            if self.__is_smtp_ssl:
                self.server = smtplib.SMTP_SSL(self.__smtp_server, self.__smtp_port)
            else:
                self.server = smtplib.SMTP(self.__smtp_server, self.__smtp_port)
                self.server.starttls()

            self.server.login(self.__smtp_username, self.__smtp_password)
            logger.info("Подключение к серверу успешно")
            return True

        except Exception as e:
            logger.error(f"Ошибка при подключении к серверу: {e}")
            return False

    def disconnect_from_server(self):
        if self.server:
            self.server.quit()
            logger.info("Отключение от сервера выполнено.")

    def send_message(self, subject, message, recipient_email):
        try:
            if not self.server or not self.server.noop()[0] == 250:
                logger.info("Пытаемся восстановить подключение...")
                self.connect_to_server()

            msg = MIMEMultipart()
            msg["From"] = self.__smtp_username
            msg["To"] = recipient_email
            msg["Subject"] = subject

            msg.attach(MIMEText(message, "plain"))

            self.server.sendmail(self.__smtp_username, recipient_email, msg.as_string())

            logger.info("Сообщение успешно отправлено.")
            return True

        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
            return False
