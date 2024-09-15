import sqlite3
import ast
import time
import uuid

from API_YandexCloud import upload_photo_to_s3, get_photo_url, delete_photo_from_s3

DB_NAME = 'database.db'


def create_data_base():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Создание таблицы "person"
    cur.execute('''CREATE TABLE IF NOT EXISTS person (
                        id INTEGER PRIMARY KEY,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
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


def drop_all_tables():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Удаление всех таблиц
    cur.execute("DROP TABLE IF EXISTS person")
    cur.execute("DROP TABLE IF EXISTS about_me")
    cur.execute("DROP TABLE IF EXISTS photo")
    cur.execute("DROP TABLE IF EXISTS person_info")

    conn.commit()
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
    except Exception as ex:
        print(ex)
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

    except Exception as ex:
        print(ex)
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

    except Exception as ex:
        print(ex)
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

    except Exception as ex:
        print(ex)
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

    except Exception as ex:
        print(ex)
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

    except Exception as ex:
        print(ex)
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

    except Exception as ex:
        print(ex)
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
    except Exception as ex:
        print(ex)
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

    except Exception as ex:
        print(ex)
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

    except Exception as ex:
        print(ex)
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

    except Exception as ex:
        print(ex)
        return False

    finally:
        conn.close()
