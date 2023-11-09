import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging import getLogger

logger = getLogger("notification-service")

class EmailSender():
    def __init__(self, smtp_username, smtp_password, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

        try:
            self.server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            self.server.starttls()
            self.server.login(smtp_username, smtp_password)

        except:
            logger.info("соединение с сервером не установленно")


    def send_message(self, subject, message, recipient_email):
        try:
            # Создайте объект сообщения
            msg = MIMEMultipart()
            msg["From"] = self.smtp_username
            msg["To"] = recipient_email
            msg["Subject"] = subject

            # Добавьте текст сообщения
            msg.attach(MIMEText(message, "plain"))

            # Отправьте сообщение
            self.server.sendmail(self.smtp_username, recipient_email, msg.as_string())

            # Завершите соединение
            self.server.quit()

            logger.info("Сообщение отправлено успешно.")

        except:
            logger.info("Сообщение не было отправленно")


