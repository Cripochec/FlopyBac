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
                                FOREIGN KEY (id_person) REFERENCES person(id)
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

        conn.commit()
        conn.close()
    except Exception as e:
        log_error("drop_all_tables", e)


# Удаление пользователя из бд
def delete_user_data(id_person):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # Удаление данных из таблицы "about_me"
        cur.execute('DELETE FROM about_me WHERE id_person = ?', (id_person,))

        # Удаление данных из таблицы "photo"
        cur.execute('DELETE FROM photo WHERE id_person = ?', (id_person,))

        # Удаление данных из таблицы "person_info"
        cur.execute('DELETE FROM person_info WHERE id_person = ?', (id_person,))

        # Удаление данных из таблицы "person"
        cur.execute('DELETE FROM person WHERE id = ?', (id_person,))

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
                     id_zodiac_sign, id_education, id_children, id_smoking, id_alcohol):
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
         height, id_education, id_children, id_smoking, id_alcohol) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (id_person, name, age, id_gender, id_target, city, id_zodiac_sign, height, id_education,
                     id_children, id_smoking, id_alcohol))

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
                "id_alcohol": person_info[12]
            }
            return info_dict
        else:
            return None

    except Exception as e:
        log_error("get_person_info", e)
        return None

    finally:
        conn.close()


# Добавление фотографии в базу данных
def save_photo(id_person, photo, dominating):
    # return
    # true - Удачно
    # false - Ошибка

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # Генерация уникального имени фотографии
        photo_name = str(uuid.uuid4()) + ".jpg"  # Уникальное имя для фото

        upload_photo_to_s3(photo, photo_name)

        photo_url = get_photo_url(photo_name)

        # Добавление записи в таблицу photo
        cur.execute('''INSERT INTO photo (id_person, photo_name, photo_url, dominating) 
                               VALUES (?, ?, ?, ?)''',
                    (id_person, photo_name, photo_url, dominating))
        # Сохранить изменения в базе данных
        conn.commit()

        return True

    except Exception as e:
        log_error("save_photo", e)
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


# Удаление фотографии из базы данных
def delete_photo_and_update_dominating(id_person, photo_url):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # Получаем значение dominating для удаляемой фотографии
        cur.execute('SELECT dominating, photo_name FROM photo WHERE id_person = ? AND photo_url = ?',
                    (id_person, photo_url))
        row = cur.fetchone()

        if row:
            dominating_to_remove = row[0]
            photo_name = row[1]

            # Удаляем фотографию из базы данных
            cur.execute('DELETE FROM photo WHERE id_person = ? AND photo_url = ?', (id_person, photo_url))

            # Обновляем значения dominating для оставшихся фотографий
            cur.execute('''UPDATE photo 
                           SET dominating = dominating - 1 
                           WHERE id_person = ? AND dominating > ?''', (id_person, dominating_to_remove))

            # Удаляем фотографию из объектного хранилища
            delete_photo_from_s3(photo_name)

            conn.commit()
            return True

        return False

    except Exception as e:
        log_error("delete_photo_and_update_dominating", e)
        return False

    finally:
        conn.close()


# Замена доминация у фотографии на главную
def swap_dominating(id_person, photo_url_to_1):
    # return
    # true - Удачно
    # false - Ошибка

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # Получаем значение dominating для заданной фотографии
        cur.execute('SELECT dominating FROM photo WHERE id_person = ? AND photo_url = ?', (id_person, photo_url_to_1))
        row_to_1 = cur.fetchone()

        if row_to_1:
            dominating_to_1 = row_to_1[0]

            # Получаем значение dominating для фотографии, у которой значение dominating равно 1
            cur.execute('SELECT photo_url FROM photo WHERE id_person = ? AND dominating = 1', (id_person,))
            row_with_1 = cur.fetchone()

            if row_with_1:
                photo_url_with_1 = row_with_1[0]

                # Обновляем значение dominating для фотографии с dominating 1 на старое значение заданной фотографии
                cur.execute('UPDATE photo SET dominating = ? WHERE id_person = ? AND photo_url = ?',
                            (dominating_to_1, id_person, photo_url_with_1))

            # Обновляем значение dominating для заданной фотографии на 1
            cur.execute('UPDATE photo SET dominating = 1 WHERE id_person = ? AND photo_url = ?',
                        (id_person, photo_url_to_1))

            conn.commit()
            return True

        return False

    except Exception as e:
        log_error("swap_dominating", e)
        return False

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


# Функция для получения списка пользователей по критериям
def get_filtered_persons(min_age, max_age, gender, target, limit=10):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        # SQL-запрос с фильтрацией по возрасту, полу и цели
        cur.execute('''
            SELECT person_info.id_person, person_info.name, person_info.age, person_info.id_gender, 
                   person_info.id_target, person_info.city, person_info.height, person_info.id_zodiac_sign,
                   person_info.id_education, person_info.id_children, person_info.id_smoking, person_info.id_alcohol
            FROM person_info
            WHERE person_info.age BETWEEN ? AND ?
              AND person_info.id_gender = ?
              AND person_info.id_target = ?
            LIMIT ?
        ''', (min_age, max_age, gender, target, limit))

        persons = cur.fetchall()
        return persons

    except Exception as e:
        log_error("get_filtered_persons", e)
        return False

    finally:
        conn.close()


# drop_all_tables()
# create_data_base()


# # Список возможных городов России
# cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань", "Нижний Новгород", "Челябинск",
#           "Самара", "Ростов-на-Дону", "Омск"]
#
# # Список имён
# names_male = ["Иван", "Алексей", "Максим", "Сергей", "Владимир", "Дмитрий", "Егор", "Андрей", "Николай", "Константин",
#               "Роман", "Олег", "Артем"]
# names_female = ["Анна", "Мария", "Екатерина", "София", "Дарья", "Ольга", "Юлия", "Ирина", "Наталья", "Елена", "Алиса",
#                 "Виктория", "Вероника"]
#
# # Список ягод
# berries = ["клубнику", "малину", "чернику", "ежевику", "клюкву", "вишню"]
#
# conn = sqlite3.connect(DB_NAME)
# cur = conn.cursor()
#
# # Генерация 26 аккаунтов
# for i in range(26):
#     # Генерация email
#     email = f"user{i + 1}@example.com"
#     password = "12345678"
#
#     # Вставка данных в таблицу person
#     cur.execute("INSERT INTO person (email, password) VALUES (?, ?)", (email, password))
#     person_id = cur.lastrowid
#
#     # Выбор пола и имени
#     if i < 13:  # Первая половина мужчины
#         name = random.choice(names_male)
#         gender = 1
#     else:  # Вторая половина женщины
#         name = random.choice(names_female)
#         gender = 2
#
#     # Генерация остальной информации
#     age = random.randint(18, 60)
#     target = random.randint(0, 3)
#     city = random.choice(cities)
#     height = str(random.randint(160, 190)) + " см"
#     zodiac_sign = random.randint(0, 11)
#     education = random.randint(0, 3)
#     children = random.randint(0, 2)
#     smoking = random.randint(0, 2)
#     alcohol = random.randint(0, 2)
#
#     # Вставка данных в таблицу person_info
#     cur.execute('''INSERT INTO person_info (
#                         id_person, name, age, id_gender, id_target, city, height, id_zodiac_sign, id_education, id_children, id_smoking, id_alcohol
#                     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
#                 (
#                 person_id, name, age, gender, target, city, height, zodiac_sign, education, children, smoking, alcohol))
#
#     # Генерация "о себе"
#     description = f"Я люблю {random.choice(berries)}"
#     cur.execute("INSERT INTO about_me (id_person, description) VALUES (?, ?)", (person_id, description))
#
# # Сохранение изменений
# conn.commit()
#
# # Закрытие соединения
# conn.close()
