from flask import Flask, request, jsonify
from smtp import key_generation, send_email
from DB import add_new_person, check_email, check_person_data_base
app = Flask(__name__)


# Проверка email нового пользователя и отправка разового кода
@app.route('/entry_email', methods=['POST'])
def entry_email():
    # Получаем данные из запроса
    data = request.get_json()

    email = data['email']

    if check_email(email):
        code = key_generation()
        send_email(email, "Код регистрации", "Разовый код: "+str(code))
        return jsonify({"status": True, "code": code})
    else:
        return jsonify({"status": False})


# Добавление нового пользователя
@app.route('/add_new_person_route', methods=['POST'])
def add_new_person_route():
    # Получаем данные из запроса
    data = request.get_json()

    email = data['email']
    password = data['password']

    info = add_new_person(email, password)
    return jsonify({"status": info['status'], "user_id": info['user_id']})


# Добавление нового пользователя
@app.route('/check_person', methods=['POST'])
def check_person():
    # Получаем данные из запроса
    data = request.get_json()

    email = data['email']
    password = data['password']

    info = check_person_data_base(email, password)
    if info['status']:
        return jsonify({"status": True, "id_person": info['user_id']})
    else:
        return jsonify({"status": False, "id_person": 0})


# для сервера
if __name__ == '__main__':
    # Запускаем сервер на всех доступных интерфейсах (0.0.0.0) и указываем порт 5000
    app.run(debug=True, host='0.0.0.0', port=5000)

# для локалки
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
