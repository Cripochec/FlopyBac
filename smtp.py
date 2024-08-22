from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import smtplib


smtp_server = 'smtp.yandex.ru'
smtp_port = 587
smtp_username = 'Fikys203@yandex.ru'
smtp_password = 'mmzudkqlfejbgsvk'


def start_smtp_server():
    try:
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.set_debuglevel(1)  # Enable debug output
        server.starttls()
        print("Logging in...")
        server.login(smtp_username, smtp_password)
        print("Connected and logged in.")
        return server
    except Exception as ex:
        print(f"ERROR: {ex}")
        return None


def send_email(to_email, subject, message):
    try:
        server = start_smtp_server()
        if server is not None:
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(f'<div style="text-align: center;">{message}</div>', 'html'))
            server.sendmail(smtp_username, to_email, msg.as_string())
            server.quit()
            return 0
        else:
            print("ERROR: No connection to SMTP server.")
            return 1
    except Exception as ex:
        print(f"ERROR: {ex}")
        return 2


def key_generation():
    code = random.randint(100000, 999999)
    print(f"Generated code: {code}")
    return code
