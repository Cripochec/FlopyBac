import os

from flask import Flask, request, jsonify, json
import threading
import logging
import datetime

from smtp import key_generation, send_email
from DB_SQLite import (create_data_base, add_new_person, check_email, check_person_data_base, save_about_me,
                save_person_info, get_about_me_descriptions, get_person_info, drop_all_tables,
                get_filtered_persons,
                update_incognito_status, get_incognito_status, delete_user_data, get_photo,
                add_to_black_list, get_all_blocked_users, remove_from_black_list, get_notification_person,
                set_notification_person, update_password, update_person_photos, add_person_photos,
                dell_person_photos_in_s3)

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(
    filename='LOGGING.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)


@app.route('/')
def home():
    return 'Hello, World!'


def log_error(route_name, error):
    logging.error(f'SERVER, API.py ({route_name}): {error}')


def log_error_cl(module, method, error):
    logging.error(f'CLIENT, {module}({method}): {error}')


# Обновление репозитория на сервере
@app.route('/git_update_hook', methods=['POST'])
def git_update():
    try:
        logging.info('Git update hook triggered')
        os.system('/root/FlopyBac/git_update_hook.sh')
        logging.info('Git update completed successfully')
        return 'Updated', 200
    except Exception as e:
        log_error("/git_update_hook", e)
        return f'no updated error: {e}', 400


# Логгирование ошибок клиентац
@app.route('/log', methods=['POST'])
def log():
    try:
        data = request.get_json()

        module = data['module']
        method = data['method']
        error = data['error']
        log_error_cl(module, method, error)

        return jsonify({"status": 0})

    except Exception as er:
        log_error("/log", er)
        return jsonify({"status": 1})


# Вход в приложение
@app.route('/entry_person', methods=['POST'])
def entry_person():
    try:
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
    except Exception as e:
        log_error("/entry_person", e)


# Регистрация, проверка email нового пользователя и отправка разового кода
@app.route('/register_person', methods=['POST'])
def register_person():
    try:
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
            email_thread = threading.Thread(target=send_email,
                                            args=(email, "Код регистрации", "Разовый код: " + str(code)))
            email_thread.start()

            return jsonify({"status": 0, "code": code})
        elif status == 1:
            return jsonify({"status": 1})
        else:
            return jsonify({"status": 3})
    except Exception as e:
        log_error("/register_person", e)


# Добавление нового пользователя
@app.route('/add_new_person_route', methods=['POST'])
def add_new_person_route():
    try:
        # Получаем данные из запроса
        data = request.get_json()

        email = data['email']
        password = data['password']

        info = add_new_person(email, password)

        # status:
        # 0 - успешно
        # 1 - ошибка сервера

        # + Добавления информации о уведомлениях для пользователя
        if info['status'] == 0 and set_notification_person(info['id_person']):
            return jsonify({"status": 0, "id_person": info['id_person']})
        else:
            return jsonify({"status": 1})
    except Exception as e:
        log_error("/add_new_person_route", e)


# Восстановление пароля, проверка email пользователя и отправка разового кода
@app.route('/resurrect_email', methods=['POST'])
def resurrect_email():
    try:
        # Получаем данные из запроса
        data = request.get_json()

        email = data['email']

        status = check_email(email)

        # status:
        # 0 - email не занят
        # 1 - успешно
        # 3 - ошибка сервера

        if status == 0:
            return jsonify({"status": 0})
        elif status == 1:
            code = key_generation()
            # Вызываем функцию send_email в отдельном потоке
            email_thread = threading.Thread(target=send_email, args=(email, "Восстановление доступа Flopy",
                                                                     "Разовый код: " + str(code)))
            email_thread.start()

            return jsonify({"status": 1, "code": code})
        else:
            return jsonify({"status": 3})
    except Exception as e:
        log_error("/resurrect_email", e)


# Повторная отправка разового кода
@app.route('/one_time_code', methods=['POST'])
def one_time_code():
    try:
        # Получаем данные из запроса
        data = request.get_json()

        email = data['email']

        code = key_generation()
        # Вызываем функцию send_email в отдельном потоке
        email_thread = threading.Thread(target=send_email, args=(email, "Код доступа Flopy",
                                                                 "Разовый код: " + str(code)))
        email_thread.start()

        return jsonify({"code": code})

    except Exception as e:
        log_error("/one_time_code", e)


# Замена пароля пользователя
@app.route('/new_password', methods=['POST'])
def new_password():
    try:
        # Получаем данные из запроса
        data = request.get_json()

        email = data['email']
        password = data['password']

        status = update_password(email, password)

        # status:
        # 0 - успешно
        # 1 - ошибка сервера

        if status == 0:
            return jsonify({"status": 0})
        else:
            return jsonify({"status": 1})
    except Exception as e:
        log_error("/new_password", e)


# Добавление информации о пользователи
@app.route('/save_persons_info', methods=['POST'])
def save_persons_info():
    try:
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
        fullness = data['fullness']

        about_me_status = save_about_me(about_me, id_person)

        info_status = save_person_info(id_person, name, age, id_gender, id_target, city, height, id_zodiac_sign,
                                       id_education, id_children, id_smoking, id_alcohol, fullness)

        if info_status:
            if about_me_status:
                return jsonify({"status": 0})
            else:
                return jsonify({"status": 2})
        else:
            return jsonify({"status": 1})
    except Exception as e:
        log_error("/save_persons_info", e)
        return jsonify({"status": 3})


@app.route('/update_persons_photos', methods=['POST'])
def update_persons_photos():
    try:
        # Получаем данные из формы
        data = request.get_json()
        id_person = data['id_person']
        photos = data['photos']

        # Обновление данных о фотографиях
        if update_person_photos(id_person, photos):
            return jsonify({"status": 0})
        else:
            return jsonify({"status": 1})
    except Exception as e:
        log_error("/update_persons_photos", e)
        return jsonify({"status": 2})


@app.route('/save_persons_photos', methods=['POST'])
def save_persons_photos():
    try:
        # Получаем данные из формы
        photo_data = request.form.get('json')

        # Преобразуем строку JSON в словарь
        photo_data_dict = json.loads(photo_data)
        id_person = photo_data_dict.get("id_person", [])
        photos = photo_data_dict.get("photos", [])

        # Получаем файлы из запроса
        files = [{"filename": file.filename, "content": file.read()} for file in request.files.getlist('photo')]

        # Обновление данных о фотографиях
        if add_person_photos(id_person, photos, files):
            return jsonify({"status": 0})
        else:
            return jsonify({"status": 1})
    except Exception as e:
        log_error("/save_persons_photos", e)  # Логирование ошибки
        return jsonify({"status": 2})


# Отправка информации о пользователи
@app.route('/pars_persons_info', methods=['POST'])
def pars_persons_info():
    try:
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
                             "id_alcohol": info_dict['id_alcohol'], "fullness": info_dict['fullness']}

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
    except Exception as e:
        log_error("/pars_persons_info", e)


# Отправления текущего статуса инкогнито пользователя
@app.route('/get_incognito', methods=['POST'])
def get_incognito():
    try:
        id_person = request.json.get('id_person')

        incognito_status = get_incognito_status(id_person)
        if incognito_status is not None:
            return jsonify({"status": 0, "incognito_status": incognito_status})
        else:
            return jsonify({"status": 1})

    except Exception as e:
        log_error("/get_incognito", e)


# Сохранение нового статуса инкогнито пользователя
@app.route('/set_incognito', methods=['POST'])
def set_incognito():
    try:
        id_person = request.json.get('id_person')
        incognito_status = request.json.get('incognito_status')

        # Обработка и сохранение файла
        if update_incognito_status(id_person, incognito_status):
            return jsonify({"status": 0})
        else:
            return jsonify({"status": 1})
    except Exception as e:
        log_error("/set_incognito", e)


# Удаление аккаунта пользователя
@app.route('/delete_account', methods=['POST'])
def delete_account():
    try:
        id_person = request.json.get('id_person')

        if dell_person_photos_in_s3(id_person) and delete_user_data(id_person):
            return jsonify({"status": 0})
        else:
            return jsonify({"status": 1})

    except Exception as e:
        log_error("/delete_account", e)


# Добавления пользоватля в чёрный список
@app.route('/add_black_list', methods=['POST'])
def add_black_list():
    try:
        id_person = request.json.get('id_person')
        id_block = request.json.get('id_block')

        if add_to_black_list(id_person, id_block):
            return jsonify({"status": 0})
        else:
            return jsonify({"status": 1})

    except Exception as ex:
        log_error("/add_black_list", ex)
        return jsonify({"status": 2})


# Добавления пользоватля в чёрный список
@app.route('/remove_black_list', methods=['POST'])
def remove_black_list():
    try:
        id_person = request.json.get('id_person')
        id_block = request.json.get('id_block')

        if remove_from_black_list(id_person, id_block):
            return jsonify({"status": 0})
        else:
            return jsonify({"status": 1})

    except Exception as ex:
        log_error("/remove_black_list", ex)
        return jsonify({"status": 2})


# Получение чёрного списка пользоватля
@app.route('/get_blocked_users', methods=['POST'])
def get_blocked_users():
    try:
        id_person = request.json.get('id_person')

        block_list = get_all_blocked_users(id_person)
        if block_list is not None:
            return jsonify({"status": 0, "block_list": block_list})
        else:
            return jsonify({"status": 1})

    except Exception as ex:
        log_error("/get_blocked_users", ex)
        return jsonify({"status": 2})


# Отправка данных о рассылки уведомлений для пользователя
@app.route('/get_notification', methods=['POST'])
def get_notification():
    try:
        id_person = request.json.get('id_person')

        notification = get_notification_person(id_person)
        if notification is not None:
            return jsonify({"status": 0, "like": notification['like'],
                            "match": notification['match'], "chat": notification['chat']})
        else:
            return jsonify({"status": 1})

    except Exception as ex:
        log_error("/get_notification", ex)
        return jsonify({"status": 2})


# Получение данных о рассылки уведомлений для пользователя
@app.route('/set_notification', methods=['POST'])
def set_notification():
    try:
        id_person = request.json.get('id_person')
        like = request.json.get('like')
        match = request.json.get('match')
        chat = request.json.get('chat')

        if set_notification_person(id_person, like, match, chat):
            return jsonify({"status": 0})
        else:
            return jsonify({"status": 1})

    except Exception as ex:
        log_error("/set_notification", ex)
        return jsonify({"status": 2})


# Пользователь поставил лайк
# @app.route('/like_person', methods=['POST'])
# def like_person():
# try:
#     id_person = request.json.get('id_person')
#     id_second_person = request.json.get('id_second_person')
#
#     if set_notification_person(id_person, like, match, chat):
#         return jsonify({"status": 0})
#     else:
#         return jsonify({"status": 1})
#
# except Exception as ex:
#     log_error("/set_notification", ex)
#     return jsonify({"status": 2})


# Маршрут для получения информации о пользователях
@app.route('/pars_persons_list', methods=['POST'])
def pars_persons_list():
    try:
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
            (id_person, name, age, city, height, id_zodiac_sign,
             id_education, id_children, id_smoking, id_alcohol) = person

            # Используем вашу функцию для получения описаний
            about_me_list = get_about_me_descriptions(id_person)
            photo_list = get_photo(id_person)

            response_data = {
                "id_person": id_person,
                "name": name,
                "age": age,
                "about_me": about_me_list,
                "city": city,
                "height": height,
                "id_zodiac_sign": id_zodiac_sign,
                "id_education": id_education,
                "id_children": id_children,
                "id_smoking": id_smoking,
                "id_alcohol": id_alcohol
            }

            # Добавляем фото данные в ответ
            for i, photo in enumerate(photo_list, start=1):
                response_data[f"photo{i}_url"] = photo['photo_url']

            # Добавляем пустые значения для фото если их меньше 4
            for i in range(len(photo_list) + 1, 5):
                response_data[f"photo{i}_url"] = 'None'

            response_list.append(response_data)

        # Возвращаем список пользователей в ответе
        return jsonify({"status": 0, "persons": response_list})
    except Exception as e:
        log_error("/pars_persons_list", e)


if __name__ == '__main__':
    try:
        # drop_all_tables()
        create_data_base()
        # Запускаем сервер на всех доступных интерфейсах (0.0.0.0) и указываем порт 5000
        app.run(debug=True, host='0.0.0.0', port=8000)

        with open('LOGGING.log', 'w'):
            pass
        logging.info('Server started successfully')

    except Exception as e:
        log_error("app.run", e)
