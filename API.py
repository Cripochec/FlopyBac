from flask import Flask, request, jsonify
import threading
from smtp import key_generation, send_email
from DB_SQLite import (create_data_base, add_new_person, check_email, check_person_data_base, save_about_me,
                       save_person_info, get_about_me_descriptions, get_person_info, drop_all_tables, get_photo,
                       save_photo, swap_dominating, delete_photo_and_update_dominating)

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


# Отправка информации о пользователи
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


# Отправка фотографий пользователя
@app.route('/pars_persons_photo', methods=['POST'])
def pars_persons_photo():
    # Получаем данные из запроса
    data = request.get_json()

    id_person = data['id_person']

    photo_list = get_photo(id_person)

    if photo_list is not None:
        response_data = {"status": 0}

        photo_list = sorted(photo_list, key=lambda x: x['dominating'])

        # Добавляем фото данные в ответ
        for i, photo in enumerate(photo_list, start=1):
            response_data[f"photo{i}_url"] = photo['photo_url']

        # Добавляем пустые значения для фото если их меньше 4
        for i in range(len(photo_list) + 1, 5):
            response_data[f"photo{i}_url"] = 'None'

        return jsonify(response_data)
    else:
        return jsonify({"status": 1})


# Сделать фото главным
@app.route('/make_main_photo', methods=['POST'])
def make_main_photo():
    # Получаем данные из запроса
    data = request.get_json()

    id_person = data['id_person']
    photo_url = data['photo_url']

    if swap_dominating(id_person, photo_url):
        return jsonify({"status": 0})
    else:
        return jsonify({"status": 1})


# Удалтиь фото
@app.route('/delete_photo', methods=['POST'])
def delete_photo():
    # Получаем данные из запроса
    data = request.get_json()

    id_person = data['id_person']
    photo_url = data['photo_url']

    if delete_photo_and_update_dominating(id_person, photo_url):
        return jsonify({"status": 0})
    else:
        return jsonify({"status": 1})

# Отправка фотографий пользователя
# @app.route('/save_persons_photo', methods=['POST'])
# def save_persons_photo():
#     # Получаем данные из запроса
#     data = request.get_json()
#
#     id_person = data['id_person']
#     name_photo = data['name_photo']
#     photo = data['photo']
#     dominating = data['dominating']
#
#     save_photo(id_person, name_photo, dominating)
#     upload_photo_to_s3(photo)
#
#     photo_list = get_photo(id_person)
#
#     if photo_list is not None:
#         return jsonify({"status": 0, "photo_list": photo_list})
#     else:
#         return jsonify({"status": 1})


if __name__ == '__main__':
    # drop_all_tables()
    create_data_base()
    # Запускаем сервер на всех доступных интерфейсах (0.0.0.0) и указываем порт 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
