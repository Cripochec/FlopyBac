import requests


def register():
    # URL сервера, куда вы будете отправлять данные
    url = 'http://127.0.0.1:5000/register_data'

    # Данные для отправки на сервер (замените на свои)
    data = {'email': 'danil_biryukov_2003@mail.ru', 'password': '123'}

    # Отправляем POST запрос на сервер
    response = requests.post(url, json=data)

    # Печатаем ответ от сервера
    print(response.text)


def register_code():
    # URL сервера, куда вы будете отправлять данные
    url = 'http://127.0.0.1:5000/register_data'

    # Данные для отправки на сервер (замените на свои)
    data = {'email': 'danil_biryukov_2003@mail.ru', 'password': '123'}

    # Отправляем POST запрос на сервер
    response = requests.post(url, json=data)

    # Печатаем ответ от сервера
    print(response.text)

register()
