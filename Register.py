from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/process_data', methods=['POST'])
def process_data():
    # Получаем данные из запроса
    data = request.get_json()

    # Проверяем, что в запросе есть email и пароль
    if 'email' in data and 'password' in data:
        email = data['email']
        password = data['password']

        # Возвращаем "good" в формате JSON
        return jsonify({"message": "good"})
    else:
        # Если не все данные были предоставлены, возвращаем ошибку
        return jsonify({"error": "Необходимо предоставить email и пароль"}), 400


if __name__ == '__main__':
    # Запускаем сервер на порту 5000 (можете выбрать другой порт)
    app.run(debug=True, port=5000)
