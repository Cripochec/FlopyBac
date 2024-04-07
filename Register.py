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
    # Запускаем сервер на всех доступных интерфейсах (0.0.0.0) и указываем порт 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
