import json
import numpy as np
from joblib import load

# Загрузка обученной модели
model = load('best_model.joblib')

# Функция для загрузки данных из json
def load_people_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Функция для предсказания пар
def predict_matches(person, people_list):
    matches = []
    for potential_match in people_list:
        common_interests_count = len(set(person['groups']).intersection(set(potential_match['groups'])))
        common_personal_preferences_count = sum(
            1 for pref in person['personal'].values() if pref != "" and pref in potential_match['personal'].values()
        )
        occupation_similarity = person['occupation'] == potential_match['occupation']
        features = np.array([[common_interests_count, common_personal_preferences_count, occupation_similarity]])
        match_probability = model.predict_proba(features)[0][1]
        if match_probability > 0.5:  # порог вероятности для совпадения
            matches.append(potential_match['id'])
    return matches

# Пример использования
person = {
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
}

people_list = [
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

matches = predict_matches(person, people_list)
print("Found matches:", matches)
