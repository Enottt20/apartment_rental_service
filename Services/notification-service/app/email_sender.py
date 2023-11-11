import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging import getLogger

logger = getLogger("notification-service")


class EmailSender():
    def __init__(self, smtp_username, smtp_password, is_smtp_ssl, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_username = smtp_username

        try:
            if is_smtp_ssl:
                self.server = smtplib.SMTP_SSL(smtp_server, smtp_port)
                self.server.login(smtp_username, smtp_password)
            else:
                self.server = smtplib.SMTP(smtp_server, smtp_port)
                self.server.starttls()
                self.server.login(smtp_username, smtp_password)

            logger.info("соединение с сервером установленно")

        except:
            logger.error("соединение с сервером не установленно")

    def send_message(self, subject, message, recipient_email):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_username
            msg["To"] = recipient_email
            msg["Subject"] = subject

            msg.attach(MIMEText(message, "plain"))

            self.server.sendmail(self.smtp_username, recipient_email, msg.as_string())

            logger.info("Сообщение отправлено успешно.")
        except:
            logger.error("Сообщение не было отправленно")
