import random
import sqlite3
import ast
import uuid
import logging
import os

from API_YandexCloud import upload_photo_to_s3, get_photo_url, delete_photo_from_s3

DB_NAME = 'database.db'

# Настройка логирования
logging.basicConfig(
    filename='LOGGING.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)


def log_error(route_name, error):
    logging.error(f' SERVER, DB_SQLite.py({route_name}): {error}')


def create_data_base():
    try:
        # Подключение к базе данных SQLite
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        # Создание таблицы "person"
        cur.execute('''CREATE TABLE IF NOT EXISTS person (
                            id INTEGER PRIMARY KEY,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            incognito INTEGER NOT NULL DEFAULT 0
                        )''')

        # Создание таблицы "о себе" с внешним ключом на таблицу "person"
        cur.execute('''CREATE TABLE IF NOT EXISTS about_me (
                                id INTEGER PRIMARY KEY,
                                id_person INTEGER,
                                description TEXT,
                                FOREIGN KEY (id_person) REFERENCES person(id)
                            )''')

        # Создание таблицы "фото" с внешним ключом на таблицу "person"
        cur.execute('''CREATE TABLE IF NOT EXISTS photo (
                                id INTEGER PRIMARY KEY,
                                id_person INTEGER,
                                photo_name TEXT,
                                photo_url TEXT,
                                dominating INTEGER,
                                FOREIGN KEY (id_person) REFERENCES person(id)
                            )''')

        # Создание таблицы "person_info" с внешними ключами
        cur.execute('''CREATE TABLE IF NOT EXISTS person_info (
                                id INTEGER PRIMARY KEY,
                                id_person INTEGER,
                                name TEXT,
                                age INTEGER,
                                id_gender INTEGER,
                                id_target INTEGER,
                                city TEXT,
                                height TEXT,
                                id_zodiac_sign INTEGER,
                                id_education INTEGER,
                                id_children INTEGER,
                                id_smoking INTEGER,
                                id_alcohol INTEGER,
                                fullness INTEGER,
                                FOREIGN KEY (id_person) REFERENCES person(id)
                            )''')

        # Создание таблицы "black_list"
        cur.execute('''CREATE TABLE IF NOT EXISTS black_list (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    id_person INTEGER NOT NULL,
                                    id_block INTEGER NOT NULL,
                                    FOREIGN KEY (id_person) REFERENCES person(id),
                                    FOREIGN KEY (id_block) REFERENCES person(id),
                                    UNIQUE (id_person, id_block)
                                )''')

        # Создание таблицы "notification" с внешними ключами
        cur.execute('''CREATE TABLE IF NOT EXISTS notification (
                                    id INTEGER PRIMARY KEY,
                                    id_person INTEGER UNIQUE,
                                    like INTEGER NOT NULL DEFAULT 1,
                                    match INTEGER NOT NULL DEFAULT 1,
                                    chat INTEGER NOT NULL DEFAULT 1,
                                    FOREIGN KEY (id_person) REFERENCES person(id)
                                )''')

        # Создание таблицы "likes"
        cur.execute('''CREATE TABLE IF NOT EXISTS likes (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    id_person INTEGER NOT NULL,
                                    id_liked INTEGER NOT NULL,
                                    FOREIGN KEY (id_person) REFERENCES person(id),
                                    FOREIGN KEY (id_liked) REFERENCES person(id),
                                    UNIQUE (id_person, id_liked)
                                )''')

        # Создание таблицы "dislikes"
        cur.execute('''CREATE TABLE IF NOT EXISTS dislikes (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    id_person INTEGER NOT NULL,
                                    id_disliked INTEGER NOT NULL,
                                    FOREIGN KEY (id_person) REFERENCES person(id),
                                    FOREIGN KEY (id_disliked) REFERENCES person(id),
                                    UNIQUE (id_person, id_disliked)
                                )''')

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()
    except Exception as e:
        log_error("create_data_base", e)


def drop_all_tables():
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        # Удаление всех таблиц
        cur.execute("DROP TABLE IF EXISTS person")
        cur.execute("DROP TABLE IF EXISTS about_me")
        cur.execute("DROP TABLE IF EXISTS photo")
        cur.execute("DROP TABLE IF EXISTS person_info")
        cur.execute("DROP TABLE IF EXISTS black_list")
        cur.execute("DROP TABLE IF EXISTS notification")
        cur.execute("DROP TABLE IF EXISTS likes")
        cur.execute("DROP TABLE IF EXISTS dislikes")

        conn.commit()
        conn.close()
    except Exception as e:
        log_error("drop_all_tables", e)


# Удаление пользователя из бд
def delete_user_data(id_person):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # Удаление данных из таблицы "person"
        cur.execute('DELETE FROM person WHERE id = ?', (id_person,))

        # Удаление данных из таблицы "about_me"
        cur.execute('DELETE FROM about_me WHERE id_person = ?', (id_person,))

        # Удаление данных из таблицы "photo"
        cur.execute('DELETE FROM photo WHERE id_person = ?', (id_person,))

        # Удаление данных из таблицы "person_info"
        cur.execute('DELETE FROM person_info WHERE id_person = ?', (id_person,))

        # Удаление данных из таблицы "black_list"
        cur.execute('DELETE FROM black_list WHERE id_person = ?', (id_person,))

        # Удаление данных из таблицы "notification"
        cur.execute('DELETE FROM notification WHERE id_person = ?', (id_person,))

        # Удаление данных из таблицы "likes"
        cur.execute('DELETE FROM likes WHERE id_person = ?', (id_person,))

        # Удаление данных из таблицы "dislikes"
        cur.execute('DELETE FROM dislikes WHERE id_person = ?', (id_person,))

        # Сохранение изменений
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        log_error("delete_user_data", e)
        return False

    finally:
        if conn:
            conn.close()


# Вход в приложение
def check_person_data_base(email, password):
    # status:
    # 0 - успешно
    # 1 - email не найден
    # 2 - password не совпадает
    # 3 - ошибка сервера
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, password FROM person WHERE email=?", (email,))
        user_info = cur.fetchone()

        if user_info:
            user_id, stored_password = user_info
            if password == stored_password:
                return {"status": 0, "user_id": user_id}
            else:
                return {"status": 2}
        else:
            return {"status": 1}
    except Exception as e:
        log_error("check_person_data_base", e)
        return {"status": 3}
    finally:
        conn.close()


# Вхождение email в общую таблицу
def check_email(email):
    # return
    # 0 - Не входит
    # 1 - Входит
    # 2 - Ошибка
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        cur.execute('SELECT COUNT(*) FROM person WHERE email = ?', (email,))
        count = cur.fetchone()[0]

        if count == 0:
            return 0
        else:
            return 1

    except Exception as e:
        log_error("check_email", e)
        return 2
    finally:
        conn.close()


# Добавление в таблицу person нового пользователя
def add_new_person(email, password):
    # return
    # 0 - Удачно
    # 1 - Ошибка

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # SQL-запрос на добавление записи
        cur.execute('INSERT INTO person (email, password) VALUES (?, ?)', (email, password))
        user_id = cur.lastrowid
        conn.commit()

        return {"status": 0, "id_person": user_id}

    except Exception as e:
        log_error("add_new_person", e)
        return {"status": 1}
    finally:
        conn.close()


# Обновление пароля пользователя
def update_password(email, new_password):
    # return
    # 0 - Удачно
    # 1 - Ошибка (например, если email не найден)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # Обновляем пароль пользователя с указанным email
        cur.execute('UPDATE person SET password = ? WHERE email = ?', (new_password, email))

        if cur.rowcount == 0:  # Если email не найден
            log_error("update_password", "Email not found")
            return 1

        conn.commit()
        return 0

    except Exception as e:
        log_error("update_password", e)
        return {"status": 2, "error": str(e)}

    finally:
        conn.close()


# Сохранение записей о себе пользователя
def save_about_me(about_me, id_person):
    # return
    # true - Удачно
    # false - Ошибка

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # Удалить все записи с таким же id_person
        cur.execute('DELETE FROM about_me WHERE id_person = ?', (id_person,))

        about_me = about_me.replace(',""', '')
        # Преобразование строки в список
        about_me_list = ast.literal_eval(about_me)

        # Добавить новые записи
        for description in about_me_list:
            cur.execute('INSERT INTO about_me (id_person, description) VALUES (?, ?)', (id_person, description))

        # Сохранить изменения в базе данных
        conn.commit()

        return True

    except Exception as e:
        log_error("save_about_me", e)
        return False

    finally:
        conn.close()


# Сохранение данных о пользователе
def save_person_info(id_person, name, age, id_gender, id_target, city, height,
                     id_zodiac_sign, id_education, id_children, id_smoking, id_alcohol, fullness):
    # return
    # true - Удачно
    # false - Ошибка

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # Удалить все записи с таким же id_person
        cur.execute('DELETE FROM person_info WHERE id_person = ?', (id_person,))

        # Добавить новую запись
        cur.execute('''INSERT INTO person_info (id_person, name, age, id_gender, id_target, city, id_zodiac_sign, 
        height, id_education, id_children, id_smoking, id_alcohol, fullness) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?)''',
                    (id_person, name, age, id_gender, id_target, city, id_zodiac_sign, height, id_education,
                     id_children, id_smoking, id_alcohol, fullness))

        # Сохранить изменения в базе данных
        conn.commit()

        return True

    except Exception as e:
        log_error("save_person_info", e)
        return False

    finally:
        conn.close()


# Получение всех записей "О себе" определённого пользователя
def get_about_me_descriptions(id_person):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # SQL-запрос для выборки всех description по заданному id_person
        cur.execute('SELECT description FROM about_me WHERE id_person = ?', (id_person,))
        descriptions = cur.fetchall()

        # Преобразование списка кортежей в список строк
        description_list = [description[0] for description in descriptions]
        return description_list

    except Exception as e:
        log_error("get_about_me_descriptions", e)
        return []

    finally:
        conn.close()


# Получение всех данных о определённого пользователя
def get_person_info(id_person):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # SQL-запрос для выборки всех данных по заданному id_person
        cur.execute('''SELECT * FROM person_info WHERE id_person = ?''', (id_person,))
        person_info = cur.fetchone()

        # Если информация найдена, возвращаем её как словарь
        if person_info:
            info_dict = {
                "name": person_info[2],
                "age": person_info[3],
                "id_gender": person_info[4],
                "id_target": person_info[5],
                "city": person_info[6],
                "height": person_info[7],
                "id_zodiac_sign": person_info[8],
                "id_education": person_info[9],
                "id_children": person_info[10],
                "id_smoking": person_info[11],
                "id_alcohol": person_info[12],
                "fullness": person_info[13]
            }
            return info_dict
        else:
            return None

    except Exception as e:
        log_error("get_person_info", e)
        return None

    finally:
        conn.close()


# Обновление данных о фото пользователя
def update_person_photos(id_person, new_photos):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # Получаем старые данные о фотографиях из базы данных
        cur.execute('SELECT photo_name, photo_url FROM photo WHERE id_person = ?', (id_person,))
        current_photos = cur.fetchall()  # Список старых данных (photo_name, photo_url)

        # Создаем список новых url фотографий для дальнейшего сравнения
        new_photo_url = [photo['url'] for photo in new_photos]

        # Сравниваем старые фотографии с новыми:
        for current_photo in current_photos:
            current_photo_name, current_photo_url = current_photo

            if current_photo_url not in new_photo_url:
                # Если фото из старых данных нет в новых, удаляем его
                delete_photo_from_s3(current_photo_name)  # Удаляем фото из хранилища
                cur.execute('DELETE FROM photo WHERE photo_name = ? AND id_person = ?',
                            (current_photo_name, id_person))

        # Обновляем или добавляем новые фотографии
        for new_photo in new_photos:
            new_photo_url = new_photo['url']
            new_dominating = new_photo['dominating']

            # Проверяем, существует ли уже такая фотография
            cur.execute('SELECT photo_url FROM photo WHERE id_person = ? AND photo_url = ?',
                        (id_person, new_photo_url))
            existing_photo = cur.fetchone()

            if existing_photo:
                # Если фото существует, обновляем его доминирование
                cur.execute('UPDATE photo SET dominating = ? WHERE photo_url = ? AND id_person = ?',
                            (new_dominating, new_photo_url, id_person))

        # Сохраняем изменения в базе данных
        conn.commit()
        return True

    except Exception as e:
        log_error("update_person_photos", e)
        conn.rollback()
        return False
    finally:
        conn.close()


# Добавление данных о фото пользователя
def add_person_photos(id_person, photos, files):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        file_index = 0  # Индекс для списка файлов

        # Обрабатываем каждый элемент из списка метаданных
        for photo_meta in photos:
            # Проверяем, есть ли файл для загрузки
            if "file_path" in photo_meta:
                # Убедимся, что файл для текущего "file_path" доступен
                if file_index >= len(files):
                    raise ValueError("Количество файлов меньше, чем ожидается по метаданным.")

                photo_data = files[file_index]  # {"filename": ..., "content": ...}
                file_index += 1  # Переходим к следующему файлу
                photo_name = str(uuid.uuid4()) + ".jpg"

                # Загружаем фото в S3 (Передаем только content)
                upload_photo_to_s3(photo_data["content"], photo_name)

                # Формируем URL фотографии
                photo_url = get_photo_url(photo_name)

                # Сохраняем данные о фото в базу
                cur.execute(
                    '''INSERT INTO photo (id_person, photo_name, photo_url, dominating)
                       VALUES (?, ?, ?, ?)''',
                    (id_person, photo_name, photo_url, photo_meta["dominating"])
                )

        # Сохраняем изменения
        conn.commit()
        return True

    except Exception as e:
        log_error("add_person_photos", e)
        conn.rollback()
        return False

    finally:
        conn.close()


# Удаление фото пользователя
def dell_person_photos_in_s3(id_person):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # Получаем старые данные о фотографиях из базы данных
        cur.execute('SELECT photo_name FROM photo WHERE id_person = ?', (id_person,))
        current_photos = cur.fetchall()  # Список старых данных (photo_name)

        # Сравниваем старые фотографии с новыми:
        for current_photo in current_photos:
            current_photo_name = current_photo
            delete_photo_from_s3(current_photo_name)  # Удаляем фото из хранилища

        # Сохраняем изменения в базе данных
        conn.commit()
        return True

    except Exception as e:
        log_error("dell_person_photos_in_s3", e)
        conn.rollback()
        return False
    finally:
        conn.close()


# Получение фотографий из базы данных по id_person
def get_photo(id_person):
    # return
    # photo_list - Удачно
    # [] - Ошибка

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # SQL-запрос для выборки всех фотографий по заданному id_person
        cur.execute('SELECT photo_url, dominating FROM photo WHERE id_person = ?', (id_person,))
        photos = cur.fetchall()

        # Преобразование результата в список словарей
        photo_list = [{"photo_url": photo[0], "dominating": photo[1]} for photo in photos]
        return photo_list

    except Exception as e:
        log_error("get_photo", e)
        return []

    finally:
        conn.close()


# Замена статуса инкогнито у пользователя
def update_incognito_status(id_person, incognito_status):
    # return
    # true - Удачно
    # false - Ошибка
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        # SQL запрос для обновления поля incognito
        cur.execute('''UPDATE person
                       SET incognito = ?
                       WHERE id = ?''', (incognito_status, id_person))
        conn.commit()
        return True

    except Exception as e:
        log_error("update_incognito_status", e)
        return False

    finally:
        conn.close()


def get_incognito_status(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        # SQL запрос для обновления поля incognito
        cur.execute('''SELECT incognito FROM person WHERE id = ?''', (user_id,))
        result = cur.fetchone()
        return result[0]

    except Exception as e:
        log_error("get_incognito_status", e)
        return None

    finally:
        conn.close()


# Функция для добавления записи в таблицу black_list
def add_to_black_list(id_person, id_block):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('INSERT INTO black_list (id_person, id_block) VALUES (?, ?)', (id_person, id_block))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        log_error("add_to_black_list", e)
        return False


# Функция для удаления записи из таблицы black_list
def remove_from_black_list(id_person, id_block):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('DELETE FROM black_list WHERE id_person = ? AND id_block = ?', (id_person, id_block))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        log_error("remove_from_black_list", e)
        return False


# Функция для получения всех заблокированных пользователей
def get_all_blocked_users(id_person):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        # Запрос с JOIN для получения данных о заблокированных пользователях
        cur.execute('''
            SELECT 
                p.id_person AS blocked_id, 
                p.name, 
                p.age, 
                ph.photo_url
            FROM black_list bl
            JOIN person_info p ON bl.id_block = p.id_person
            LEFT JOIN photo ph ON p.id_person = ph.id_person AND ph.dominating = 0
            WHERE bl.id_person = ?
        ''', (id_person,))

        blocked_users = cur.fetchall()
        conn.close()

        # Форматируем результат в удобный список словарей
        result = [
            {
                "id": user[0],
                "name": user[1],
                "age": user[2],
                "photo_url": user[3]
            }
            for user in blocked_users
        ]

        return result

    except Exception as e:
        log_error("get_all_blocked_users", e)
        return None


def get_notification_person(id_person):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        # Выполняем запрос для получения данных по id_person
        cur.execute("SELECT * FROM notification WHERE id_person = ?", (id_person,))
        result = cur.fetchone()

        if result:
            return {
                "like": result[2],
                "match": result[3],
                "chat": result[4],
            }
        else:
            return None

    except Exception as e:
        log_error("get_notification_person", e)
        return None

    finally:
        conn.close()


def set_notification_person(id_person, like=1, match=1, chat=1):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        # SQL-запрос с ON CONFLICT DO UPDATE
        cur.execute('''
            INSERT INTO notification (id_person, like, match, chat)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id_person) DO UPDATE SET
                like=excluded.like,
                match=excluded.match,
                chat=excluded.chat
        ''', (id_person, like, match, chat))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        log_error("set_notification_person", e)
        return False


# Функция для получения списка пользователей по критериям
def get_filtered_persons(min_age, max_age, gender, target, limit=10):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        # Формируем SQL-запрос в зависимости от значения gender
        if gender == 0:
            query = '''
                SELECT person_info.id_person, person_info.name, person_info.age, person_info.city, person_info.height, person_info.id_zodiac_sign,
                       person_info.id_education, person_info.id_children, person_info.id_smoking, person_info.id_alcohol
                FROM person_info
                WHERE person_info.age BETWEEN ? AND ?
                  AND person_info.id_target = ?
                LIMIT ?
            '''
            params = (min_age, max_age, target, limit)
        else:
            query = '''
                SELECT person_info.id_person, person_info.name, person_info.age, person_info.city, person_info.height, person_info.id_zodiac_sign,
                       person_info.id_education, person_info.id_children, person_info.id_smoking, person_info.id_alcohol
                FROM person_info
                WHERE person_info.age BETWEEN ? AND ?
                  AND person_info.id_gender = ?
                  AND person_info.id_target = ?
                LIMIT ?
            '''
            params = (min_age, max_age, gender, target, limit)

        cur.execute(query, params)
        persons = cur.fetchall()
        return persons

    except Exception as e:
        log_error("get_filtered_persons", e)
        return False

    finally:
        conn.close()
