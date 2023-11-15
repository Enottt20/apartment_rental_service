import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging import getLogger

logger = getLogger("notification-service")

class EmailSender():
    def __init__(self, smtp_username, smtp_password, is_smtp_ssl, smtp_server="smtp.gmail.com", smtp_port=587):
        self.__smtp_username = smtp_username
        self.__smtp_password = smtp_password
        self.__is_smtp_ssl = is_smtp_ssl
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        self.server = None

    def connect_to_server(self):
        try:
            if self.__is_smtp_ssl:
                self.server = smtplib.SMTP_SSL(self.__smtp_server, self.__smtp_port)
            else:
                self.server = smtplib.SMTP(self.__smtp_server, self.__smtp_port)
                self.server.starttls()

            self.server.login(self.__smtp_username, self.__smtp_password)
            logger.info(f"Подключение к серверу успешно")
            return True

        except Exception as e:
            logger.error(f"Ошибка при подключении к серверу: {e}")

    def disconnect_from_server(self):
        if self.server:
            self.server.quit()
            logger.info("Отключение от сервера выполнено.")

    def send_message(self, subject, message, recipient_email):
        try:
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
