from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Загрузка модели
model = joblib.load('best_model.joblib')


@app.route('/predict', methods=['POST'])
def predict():
    # Получаем данные из запроса
    data = request.json

    # Преобразуем данные в массив numpy
    features = np.array([[
        len(data['common_interests']),
        data['common_personal_preferences'],
        data['occupation_similarity']
    ]])

    # Предсказываем
    prediction = model.predict(features)

    # Формируем ответ
    result = {'prediction': int(prediction[0])}

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
