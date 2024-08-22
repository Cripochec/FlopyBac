import json
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump

file_path = 'dataset.json'


# Извлечение данных
def load_data_from_json(dataset):
    with open(dataset, 'r', encoding='utf-8') as file:
        read_dataset = json.load(file)
    return read_dataset


# Вычисления общих интересов
def calculate_common_interests(pair_records):
    interests_human1 = set(pair_records['human1']['groups'])
    interests_human2 = set(pair_records['human2']['groups'])
    common_interests = interests_human1.intersection(interests_human2)
    return common_interests


# Вычисления общих личных предпочтений
def calculate_common_personal_preferences(pair_records):
    personal_human1 = pair_records['human1']['personal']
    personal_human2 = pair_records['human2']['personal']
    common_personal_preferences = sum(
        1 for pref in personal_human1.values() if pref != "" and pref in personal_human2.values())
    return common_personal_preferences


# Проверки сходства профессий
def check_occupation_similarity(pair_records):
    occupation_human1 = pair_records['human1']['occupation']
    occupation_human2 = pair_records['human2']['occupation']
    return occupation_human1 == occupation_human2


data = load_data_from_json(file_path)


# Подготовка данных для обучения
features = []
labels = []

for key, pair_record in data.items():
    common_interests_count = len(calculate_common_interests(pair_record))
    common_personal_preferences_count = calculate_common_personal_preferences(pair_record)
    occupation_similarity = check_occupation_similarity(pair_record)
    label = 1 if pair_record['match'] else 0
    features.append([common_interests_count, common_personal_preferences_count, occupation_similarity])
    labels.append(label)

X = np.array(features)
y = np.array(labels)

# Инициализация модели логистической регрессии с учетом несбалансированных классов
model = LogisticRegression(class_weight='balanced')

# Кросс-валидация
cv_scores = cross_val_score(model, X, y, cv=5)
print("Cross-validated scores:", cv_scores)
print("Mean CV score:", cv_scores.mean())

# Поиск лучших параметров с помощью GridSearchCV
param_grid = {
    'C': [0.1, 1, 10, 100],
    'solver': ['liblinear', 'saga']
}

grid_search = GridSearchCV(LogisticRegression(), param_grid, cv=5)
grid_search.fit(X, y)

print("Best parameters found:", grid_search.best_params_)
print("Best cross-validation score:", grid_search.best_score_)

best_model = grid_search.best_estimator_

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели на обучающих данных
best_model.fit(X_train, y_train)

# Предсказание на тестовых данных
y_pred = best_model.predict(X_test)

# Оценка качества модели
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy with best model:", accuracy)
print(classification_report(y_test, y_pred, zero_division=1))

# Сохранение обученной модели
dump(best_model, 'best_model.joblib')
