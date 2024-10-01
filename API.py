import os

from flask import Flask, request, jsonify
import threading
import datetime

from smtp import key_generation, send_email
from DB_SQLite import (create_data_base, add_new_person, check_email, check_person_data_base, save_about_me,
                       save_person_info, get_about_me_descriptions, get_person_info, drop_all_tables, get_photo,
                       save_photo, swap_dominating, delete_photo_and_update_dominating, get_filtered_persons)

app = Flask(__name__)


# Обновление репозитория на сервере
@app.route('/git_update_hook', methods=['POST'])
def git_update():
    try:
        os.system('/root/FlopyBac/git_update_hook.sh')
        return 'Updated', 200
    except Exception as e:
        return f'no updated error:{e}', 400


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

    photo_list = get_photo(id_person)
    about_me_list = get_about_me_descriptions(id_person)
    info_dict = get_person_info(id_person)

    if info_dict is not None and about_me_list is not None and photo_list is not None:
        response_data = {"status": 0, "name": info_dict['name'], "age": info_dict['age'],
                         "id_gender": info_dict['id_gender'], "id_target": info_dict['id_target'],
                         "about_me": about_me_list, "city": info_dict['city'], "height": info_dict['height'],
                         "id_zodiac_sign": info_dict['id_zodiac_sign'], "id_education": info_dict['id_education'],
                         "id_children": info_dict['id_children'], "id_smoking": info_dict['id_smoking'],
                         "id_alcohol": info_dict['id_alcohol']}

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


# Сохранение новой фотографии пользователя
@app.route('/save_persons_photo', methods=['POST'])
def save_persons_photo():
    id_person = request.form.get('id_person')
    dominating = request.form.get('dominating')

    # Получаем файл
    photo_file = request.files.get('photo')

    if not photo_file:
        return jsonify({"status": 1})

    # Чтение файла
    photo_data = photo_file.read()

    # Обработка и сохранение файла
    if save_photo(id_person, photo_data, dominating):
        return jsonify({"status": 0})
    else:
        return jsonify({"status": 1})


# Маршрут для получения информации о пользователях
@app.route('/pars_persons_list', methods=['POST'])
def pars_persons_list():
    # Получаем данные из запроса
    data = request.get_json()
    min_age = data.get('min_age')
    max_age = data.get('max_age')
    gender = data.get('id_gender')
    target = data.get('id_target')

    # Получаем список пользователей по критериям
    persons_list = get_filtered_persons(min_age, max_age, gender, target)

    response_list = []

    # Формируем ответ для каждого пользователя
    for person in persons_list:
        (id_person, name, age, id_gender, id_target, city, height, id_zodiac_sign,
         id_education, id_children, id_smoking, id_alcohol) = person

        # Используем вашу функцию для получения описаний
        about_me_list = get_about_me_descriptions(id_person)

        response_data = {
            "id_person": id_person,
            "name": name,
            "age": age,
            "id_gender": id_gender,
            "id_target": id_target,
            "about_me": about_me_list,
            "city": city,
            "height": height,
            "id_zodiac_sign": id_zodiac_sign,
            "id_education": id_education,
            "id_children": id_children,
            "id_smoking": id_smoking,
            "id_alcohol": id_alcohol
        }

        response_list.append(response_data)

    # Возвращаем список пользователей в ответе
    return jsonify({"status": 0, "persons": response_list})


if __name__ == '__main__':
    # drop_all_tables()
    create_data_base()
    # Запускаем сервер на всех доступных интерфейсах (0.0.0.0) и указываем порт 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
