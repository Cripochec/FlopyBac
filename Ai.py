import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Извлекаем данные
def load_data_from_json(dataset):
    with open(dataset, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


file_path = 'dataset.json'
data = load_data_from_json(file_path)


def calculate_common_interests(pair_record):
    interests_human1 = set(pair_record['human1']['groups'])
    interests_human2 = set(pair_record['human2']['groups'])
    common_interests = interests_human1.intersection(interests_human2)
    return common_interests


def calculate_common_personal_preferences(pair_record):
    personal_human1 = pair_record['human1']['personal']
    personal_human2 = pair_record['human2']['personal']

    common_personal_preferences_count = sum(
        1 for pref in personal_human1.values() if pref != "" and pref in personal_human2.values())
    return common_personal_preferences_count


def check_occupation_similarity(pair_record):
    occupation_human1 = pair_record['human1']['occupation']
    occupation_human2 = pair_record['human2']['occupation']

    if occupation_human1 == occupation_human2:
        return True
    else:
        return False


# Подготовка данных для обучения
features = []
labels = []

for key, pair_record in data.items():
    # Извлекаем признаки
    common_interests_count = len(calculate_common_interests(pair_record))
    common_personal_preferences_count = calculate_common_personal_preferences(pair_record)
    occupation_similarity = check_occupation_similarity(pair_record)

    # Извлекаем метку
    label = 1 if pair_record['match'] else 0

    # Добавляем признаки и метку в списки
    features.append([common_interests_count, common_personal_preferences_count, occupation_similarity])
    labels.append(label)

# Преобразуем списки в массивы numpy
X = np.array(features)
y = np.array(labels)

# Разделяем данные на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Инициализируем и обучаем модель логистической регрессии
model = LogisticRegression()
model.fit(X_train, y_train)

# Предсказываем метки для тестовой выборки
y_pred = model.predict(X_test)

# Оцениваем производительность модели
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)