import requests

# URL сервера, куда вы будете отправлять данные
url = 'http://127.0.0.1:5000/process_data'

# Данные для отправки на сервер (замените на свои)
data = {'email': 'example@example.com', 'password': 'mypassword'}

# Отправляем POST запрос на сервер
response = requests.post(url, json=data)

# Печатаем ответ от сервера
print(response.text)
