import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random


# Настройки SMTP-сервера
smtp_server = 'smtp.yandex.ru'
smtp_port = 587
smtp_username = 'Fikys203@yandex.ru'
smtp_password = 'mmzudkqlfejbgsvk'

# TO_EMAIL = "danil_biryukov_2003@mail.ru"
# TO_EMAIL = "ticholazroman@mail.ru"
TO_EMAIL = "artsport03@gmail.com"


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
            # Добавляем текст письма
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            # Отправляем письмо
            server.sendmail(smtp_username, to_email, msg.as_string())
            print("good!")
            server.quit()
        else:
            print("no connection")
    except Exception as ex:
        print(f"bad( ERROR:{ex}")


def key_generation():
    code = random.randint(1000, 9999)
    return code

for i in range(10):
    send_email(TO_EMAIL, "Тест", "Привет! Это тестовое сообщение.")

