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
    # return
    # 0 - Письмо отправленно
    # 1 - Письмо не отправленно
    # 2 - Ошибка
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
            server.quit()
            return 0
        else:
            print("ERROR: no connection in smtp server")
            return 1
    except Exception as ex:
        print(f"ERROR: {ex}")
        return 2


def key_generation():
    code = random.randint(100000, 999999)
    print(code)
    return code
