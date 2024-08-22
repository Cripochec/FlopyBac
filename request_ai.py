import requests


def ai():
    url = 'http://127.0.0.1:5000/predict'
    data = {
        'person': {
            "id": 1,
            "games": "",
            "music": "",
            "occupation": "university",
            "personal": {
                "alcohol": "",
                "smoking": "",
                "inspired_by": "",
                "people_main": "",
                "life_main": ""
            },
            "groups": [
                "Танцевальная музыка",
                "Онлайн-игра",
                "Видеоигра",
                "Электроника",
                "Электронная музыка"
            ]
        },
        'people_list': [
            {
                "id": 2,
                "games": "",
                "music": "",
                "occupation": "university",
                "personal": {
                    "alcohol": "",
                    "smoking": "",
                    "inspired_by": "",
                    "people_main": "",
                    "life_main": ""
                },
                "groups": [
                    "Городское сообщество",
                    "Родители и дети",
                    "Беременность, роды",
                    "Беременность, роды",
                    "Анимация"
                ]
            },
            {
                "id": 3,
                "games": "",
                "music": "",
                "occupation": "work",
                "personal": {
                    "alcohol": "",
                    "smoking": "",
                    "inspired_by": "",
                    "people_main": "",
                    "life_main": ""
                },
                "groups": [
                    "Интернет-СМИ",
                    "Фитнес",
                    "Блогер",
                    "Блогер",
                    "Молодёжное движение"
                ]
            }
        ]
    }

    response = requests.post(url, json=data)
    matches = response.json()
    print("Found matches (IDs):", matches)


ai()
