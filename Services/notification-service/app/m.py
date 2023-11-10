import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging import getLogger
import config


logger = getLogger("notification-service")
cfg: config.Config = config.load_config()

class EmailSender():
    def __init__(self, smtp_username, smtp_password, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

        try:
            self.server = smtplib.SMTP(smtp_server, smtp_port)
            self.server.starttls()
            self.server.login(smtp_username, smtp_password)
            print('соединение с сервером установленно')
            logger.info("соединение с сервером установленно")

        except:
            print('соединение с сервером не установленно')
            logger.error("соединение с сервером не установленно")


    def send_message(self, subject, message, recipient_email):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_username
            msg["To"] = recipient_email
            msg["Subject"] = subject

            msg.attach(MIMEText(message, "plain"))

            self.server.sendmail(self.smtp_username, recipient_email, msg.as_string())

            self.server.quit()

            logger.info("Сообщение отправлено успешно.")
            print('Сообщение отправлено успешно.')
        except:
            logger.error("Сообщение не было отправленно")
            print('Сообщение не было отправленно')


m = EmailSender('gigabooster@yandex.ru', 'gjfddhdgre22', 'smtp.yandex.ru', 587)
m.send_message('t', 't', 'levkin03@mail.ru')