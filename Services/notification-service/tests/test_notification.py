import imaplib
import unittest
from app.email_sender import EmailSender
import app.config as config

cfg: config.Config = config.load_config()

class TestEmailSender(unittest.TestCase):
    def setUp(self):
        # Инициализация объекта EmailSender для тестов
        self.email_sender = EmailSender(
            smtp_username=cfg.EMAIL_LOGIN,
            smtp_password=cfg.EMAIL_PASSWORD,
            is_smtp_ssl=cfg.IS_SMPT_SSL,
            smtp_server=cfg.SMTP_SERVER,
            smtp_port=cfg.SMTP_PORT
        )

        # она реально существует
        self.recipient_email = 'recipient@example.com'

    def test_connect_to_server(self):
        result = self.email_sender.connect_to_server()
        self.assertTrue(result)
        self.assertIsNotNone(self.email_sender.server)
        self.email_sender.disconnect_from_server()

    def test_connect_to_server_failure(self):
        email_sender = EmailSender(
            smtp_username='test',
            smtp_password='test',
            is_smtp_ssl='test',
            smtp_server='test',
            smtp_port=111
        )
        result = email_sender.connect_to_server()
        self.assertFalse(result)
        self.assertIsNone(email_sender.server)
        email_sender.disconnect_from_server()

    def test_send_message(self):
        subject = "Test Subject"
        message = "Test Message"
        recipient_email = self.recipient_email

        self.email_sender.connect_to_server()
        result = self.email_sender.send_message(subject, message, recipient_email)
        self.assertTrue(result)
        self.email_sender.disconnect_from_server()

    def test_send_message_failure(self):
        subject = "Test Subject"
        message = "Test Message"
        recipient_email = "invalid_email"

        self.email_sender.connect_to_server()
        result = self.email_sender.send_message(subject, message, recipient_email)
        self.assertFalse(result)
        self.email_sender.disconnect_from_server()


if __name__ == '__main__':
    unittest.main()
