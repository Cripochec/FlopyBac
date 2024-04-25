from flask import Flask, request, jsonify
from smtp import key_generation, send_email
from DB import (create_data_base, add_new_person, check_email, check_person_data_base, set_person_info_data_base,
                get_person_info_data_base)
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


# Добавление информации о пользователи
@app.route('/set_persons_info', methods=['POST'])
def set_persons_info():
    # Получаем данные из запроса
    data = request.get_json()

    id_person = data['id_person']
    name = data['name']
    age = data['age']
    gender = data['gender']
    goal = data['goal']
    city = data['city']
    zodiac_sign = data['zodiac_sign']
    height = data['height']
    education = data['education']
    children = data['children']
    smoking = data['smoking']
    alcohol = data['alcohol']
    verification = data['verification']

    if set_person_info_data_base(id_person, name, age, gender, goal, city, zodiac_sign, height, education, children,
                                 smoking, alcohol, verification):
        return jsonify({"status": True})
    else:
        return jsonify({"status": False})


@app.route('/get_persons_info', methods=['POST'])
def get_persons_info():
    # Получаем данные из запроса
    data = request.get_json()

    id_person = data['id_person']

    info = get_person_info_data_base(id_person)
    if info['status']:
        return jsonify({"status": True, "name": info['name'], "age": info['age'], "gender": info['gender'],
                        "goal": info['goal'], "city": info['city'], "zodiac_sign": info['zodiac_sign'],
                        "height": info['height'], "education": info['education'], "children": info['children'],
                        "smoking": info['smoking'], "alcohol": info['alcohol'], "verification": info['verification']})
    else:
        return jsonify({"status": False})


if __name__ == '__main__':
    create_data_base()
    # Запускаем сервер на всех доступных интерфейсах (0.0.0.0) и указываем порт 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
