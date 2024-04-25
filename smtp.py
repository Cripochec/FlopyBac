from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import smtplib

# Настройки SMTP-сервера
smtp_server = 'smtp.yandex.ru'
smtp_port = 587
smtp_username = 'Fikys203@yandex.ru'
smtp_password = 'mmzudkqlfejbgsvk'


def start_smtp_server():
    try:
        # Создаем объект соединения с SMTP-сервером
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        # Авторизация на SMTP-сервере
        server.login(smtp_username, smtp_password)
        return server
    except Exception as ex:
        print(f"ERROR: {ex}")


def send_email(to_email, subject, message):
    try:
        server = start_smtp_server()
        if server is not None:
            # Создаем письмо
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            # Изменения: Используем HTML для форматирования текста
            msg.attach(MIMEText(f'<div style="text-align: center;">{message}</div>', 'html'))
            # Отправляем письмо
            server.sendmail(smtp_username, to_email, msg.as_string())
            print("good!")
            server.quit()
        else:
            print("no connection")
    except Exception as ex:
        print(f"bad( ERROR:{ex}")


def key_generation():
    code = random.randint(100000, 999999)
    return code
