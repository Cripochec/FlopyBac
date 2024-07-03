from flask import Flask, request, jsonify
import threading
from smtp import key_generation, send_email
from DB_SQLite import (create_data_base, add_new_person, check_email, check_person_data_base, save_about_me,
                       save_person_info, get_about_me_descriptions, get_person_info)

app = Flask(__name__)


# Вход в приложение
@app.route('/entry_person', methods=['POST'])
def entry_person():
    # Получаем данные из запроса
    data = request.get_json()

    email = data['email']
    password = data['password']

    info = check_person_data_base(email, password)

    # status:
    # 0 - успешно
    # 1 - email не найден
    # 2 - password не совпадает
    # 3 - ошибка сервера

    if info['status'] == 0:
        return jsonify({"status": info['status'], "id_person": info['user_id']})
    else:
        return jsonify({"status": info['status']})


# Регистрация, проверка email нового пользователя и отправка разового кода
@app.route('/register_person', methods=['POST'])
def register_person():
    # Получаем данные из запроса
    data = request.get_json()

    email = data['email']

    status = check_email(email)

    # status:
    # 0 - успешно
    # 1 - email занят
    # 3 - ошибка сервера

    if status == 0:
        code = key_generation()
        # Вызываем функцию send_email в отдельном потоке
        email_thread = threading.Thread(target=send_email, args=(email, "Код регистрации", "Разовый код: " + str(code)))
        email_thread.start()

        return jsonify({"status": 0, "code": code})
    elif status == 1:
        return jsonify({"status": 1})
    else:
        return jsonify({"status": 3})


# Добавление нового пользователя
@app.route('/add_new_person_route', methods=['POST'])
def add_new_person_route():
    # Получаем данные из запроса
    data = request.get_json()

    email = data['email']
    password = data['password']

    info = add_new_person(email, password)

    # status:
    # 0 - успешно
    # 1 - ошибка сервера

    if info['status'] == 0:
        return jsonify({"status": 0, "id_person": info['id_person']})
    else:
        return jsonify({"status": 1})


# Добавление информации о пользователи
@app.route('/save_persons_info', methods=['POST'])
def save_persons_info():
    # Получаем данные из запроса
    data = request.get_json()

    id_person = data['id_person']
    name = data['name']
    age = data['age']
    id_gender = data['id_gender']
    id_target = data['id_target']
    about_me = data['about_me']
    city = data['city']
    height = data['height']
    id_zodiac_sign = data['id_zodiac_sign']
    id_education = data['id_education']
    id_children = data['id_children']
    id_smoking = data['id_smoking']
    id_alcohol = data['id_alcohol']

    about_me_status = save_about_me(about_me, id_person)

    info_status = save_person_info(id_person, name, age, id_gender, id_target, city, height, id_zodiac_sign,
                                   id_education, id_children, id_smoking, id_alcohol)
    if info_status:
        if about_me_status:
            return jsonify({"status": 0})
        else:
            return jsonify({"status": 1})
    else:
        return jsonify({"status": 1})


# Добавление информации о пользователи
@app.route('/pars_persons_info', methods=['POST'])
def pars_persons_info():
    # Получаем данные из запроса
    data = request.get_json()

    id_person = data['id_person']

    about_me_list = get_about_me_descriptions(id_person)
    info_dict = get_person_info(id_person)

    if info_dict is not None and about_me_list is not None:
        return jsonify({"status": 0, "name": info_dict['name'], "age": info_dict['age'],
                        "id_gender": info_dict['id_gender'], "id_target": info_dict['id_target'],
                        "about_me": about_me_list, "city": info_dict['city'], "height": info_dict['height'],
                        "id_zodiac_sign": info_dict['id_zodiac_sign'], "id_education": info_dict['id_education'],
                        "id_children": info_dict['id_children'], "id_smoking": info_dict['id_smoking'],
                        "id_alcohol": info_dict['id_alcohol']})
    else:
        return jsonify({"status": 1})


# @app.route('/get_persons_info', methods=['POST'])
# def get_persons_info():
#     # Получаем данные из запроса
#     data = request.get_json()
#
#     id_person = data['id_person']
#
#     info = get_person_info_data_base(id_person)
#     if info['status']:
#         return jsonify({"status": True, "name": info['name'], "age": info['age'], "gender": info['gender'],
#                         "goal": info['goal'], "city": info['city'], "zodiac_sign": info['zodiac_sign'],
#                         "height": info['height'], "education": info['education'], "children": info['children'],
#                         "smoking": info['smoking'], "alcohol": info['alcohol'], "verification": info['verification']})
#     else:
#         return jsonify({"status": False})


if __name__ == '__main__':
    create_data_base()
    # Запускаем сервер на всех доступных интерфейсах (0.0.0.0) и указываем порт 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
