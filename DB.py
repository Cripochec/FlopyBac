import uuid

import pymysql
import logging
import ast
from API_YandexCloud import upload_photo_to_s3, get_photo_url, delete_photo_from_s3

# Подключение к MySQL
DB_HOST = "192.168.1.6"
DB_PORT = 3306
DB_USER = "gen_user"
DB_PASSWORD = "Z;26w3wm>RVl8n"
DB_NAME = "default_db"  # Замени на название твоей базы

# Настройка логирования
logging.basicConfig(
    filename='LOGGING.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)


def log_error(route_name, error):
    logging.error(f'SERVER, DB_MySQL.py({route_name}): {error}')


def get_connection():
    """Функция для получения соединения с базой данных."""
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


def create_database():
    """Создание базы данных (если у тебя есть права)"""
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
        conn.close()
    except Exception as e:
        log_error("create_database", e)


def create_tables():
    """Создание всех таблиц"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS person (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                email VARCHAR(255) NOT NULL UNIQUE,
                                password TEXT NOT NULL,
                                incognito TINYINT(1) NOT NULL DEFAULT 0
                            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS about_me (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                id_person INT,
                                description TEXT,
                                FOREIGN KEY (id_person) REFERENCES person(id) ON DELETE CASCADE
                            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS photo (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                id_person INT,
                                photo_name TEXT,
                                photo_url TEXT,
                                dominating INT,
                                FOREIGN KEY (id_person) REFERENCES person(id) ON DELETE CASCADE
                            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS person_info (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                id_person INT,
                                name VARCHAR(255),
                                age INT,
                                id_gender INT,
                                id_target INT,
                                city VARCHAR(255),
                                height VARCHAR(50),
                                id_zodiac_sign INT,
                                id_education INT,
                                id_children INT,
                                id_smoking INT,
                                id_alcohol INT,
                                fullness INT,
                                FOREIGN KEY (id_person) REFERENCES person(id) ON DELETE CASCADE
                            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS black_list (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                id_person INT NOT NULL,
                                id_block INT NOT NULL,
                                FOREIGN KEY (id_person) REFERENCES person(id) ON DELETE CASCADE,
                                FOREIGN KEY (id_block) REFERENCES person(id) ON DELETE CASCADE,
                                UNIQUE (id_person, id_block)
                            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS notification (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                id_person INT UNIQUE,
                                like_notif TINYINT(1) NOT NULL DEFAULT 1,
                                match_notif TINYINT(1) NOT NULL DEFAULT 1,
                                chat_notif TINYINT(1) NOT NULL DEFAULT 1,
                                FOREIGN KEY (id_person) REFERENCES person(id) ON DELETE CASCADE
                            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS likes (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                id_person INT NOT NULL,
                                id_liked INT NOT NULL,
                                FOREIGN KEY (id_person) REFERENCES person(id) ON DELETE CASCADE,
                                FOREIGN KEY (id_liked) REFERENCES person(id) ON DELETE CASCADE,
                                UNIQUE (id_person, id_liked)
                            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS dislikes (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                id_person INT NOT NULL,
                                id_disliked INT NOT NULL,
                                FOREIGN KEY (id_person) REFERENCES person(id) ON DELETE CASCADE,
                                FOREIGN KEY (id_disliked) REFERENCES person(id) ON DELETE CASCADE,
                                UNIQUE (id_person, id_disliked)
                            )''')

        conn.commit()
        conn.close()
    except Exception as e:
        log_error("create_tables", e)


def drop_all_tables():
    """Удаление всех таблиц"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")  # Отключаем проверки ключей перед удалением
            cursor.execute("DROP TABLE IF EXISTS dislikes")
            cursor.execute("DROP TABLE IF EXISTS likes")
            cursor.execute("DROP TABLE IF EXISTS notification")
            cursor.execute("DROP TABLE IF EXISTS black_list")
            cursor.execute("DROP TABLE IF EXISTS person_info")
            cursor.execute("DROP TABLE IF EXISTS photo")
            cursor.execute("DROP TABLE IF EXISTS about_me")
            cursor.execute("DROP TABLE IF EXISTS person")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")  # Включаем обратно
        conn.commit()
        conn.close()
    except Exception as e:
        log_error("drop_all_tables", e)


# Добавление в таблицу person нового пользователя
def add_new_person(email, password):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('INSERT INTO person (email, password) VALUES (%s, %s)', (email, password))
        user_id = cur.lastrowid
        conn.commit()

        return {"status": 0, "id_person": user_id}

    except Exception as e:
        log_error("add_new_person", e)
        return {"status": 1}

    finally:
        if conn:
            conn.close()


# Вход в приложение
def check_person_data_base(email, password):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, password FROM person WHERE email=%s", (email,))
        user_info = cur.fetchone()

        if user_info:
            user_id, stored_password = user_info
            if password == stored_password:
                return {"status": 0, "user_id": user_id}
            else:
                return {"status": 2}  # Пароль не совпадает
        else:
            return {"status": 1}  # Email не найден

    except Exception as e:
        log_error("check_person_data_base", e)
        return {"status": 3}  # Ошибка сервера

    finally:
        if conn:
            conn.close()


# Удаление пользователя из бд
def delete_user_data(id_person):
    try:
        conn = get_connection()
        cur = conn.cursor()

        tables = ["person", "about_me", "photo", "person_info", "black_list", "notification", "likes", "dislikes"]

        for table in tables:
            cur.execute(f'DELETE FROM {table} WHERE id_person = %s', (id_person,))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        log_error("delete_user_data", e)
        return False

    finally:
        if conn:
            conn.close()


# Вхождение email в общую таблицу
def check_email(email):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT COUNT(*) FROM person WHERE email = %s', (email,))
        count = cur.fetchone()[0]

        return 1 if count > 0 else 0

    except Exception as e:
        log_error("check_email", e)
        return 2

    finally:
        if conn:
            conn.close()


# Обновление пароля пользователя
def update_password(email, new_password):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('UPDATE person SET password = %s WHERE email = %s', (new_password, email))

        if cur.rowcount == 0:
            log_error("update_password", "Email not found")
            return 1  # Email не найден

        conn.commit()
        return 0

    except Exception as e:
        log_error("update_password", e)
        return {"status": 2, "error": str(e)}

    finally:
        if conn:
            conn.close()


# Сохранение записей о себе пользователя
def save_about_me(about_me, id_person):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Удалить старые записи
        cur.execute('DELETE FROM about_me WHERE id_person = %s', (id_person,))

        # Очистка данных
        about_me = about_me.replace(',""', '')
        about_me_list = ast.literal_eval(about_me)

        # Добавить новые записи
        for description in about_me_list:
            cur.execute('INSERT INTO about_me (id_person, description) VALUES (%s, %s)', (id_person, description))

        conn.commit()
        return True

    except Exception as e:
        log_error("save_about_me", e)
        return False

    finally:
        if conn:
            conn.close()


# Сохранение данных о пользователе
def save_person_info(id_person, name, age, id_gender, id_target, city, height,
                     id_zodiac_sign, id_education, id_children, id_smoking, id_alcohol, fullness):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Удалить старую информацию
        cur.execute('DELETE FROM person_info WHERE id_person = %s', (id_person,))

        # Добавить новую запись
        cur.execute('''INSERT INTO person_info 
            (id_person, name, age, id_gender, id_target, city, height, id_zodiac_sign, 
             id_education, id_children, id_smoking, id_alcohol, fullness) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (id_person, name, age, id_gender, id_target, city, height, id_zodiac_sign,
                     id_education, id_children, id_smoking, id_alcohol, fullness))

        conn.commit()
        return True

    except Exception as e:
        log_error("save_person_info", e)
        return False

    finally:
        if conn:
            conn.close()


# Получение всех записей "О себе" определённого пользователя
def get_about_me_descriptions(id_person):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT description FROM about_me WHERE id_person = %s', (id_person,))
        descriptions = cur.fetchall()

        return [description[0] for description in descriptions]

    except Exception as e:
        log_error("get_about_me_descriptions", e)
        return []

    finally:
        if conn:
            conn.close()


# Получение всех данных о определённого пользователя
def get_person_info(id_person):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM person_info WHERE id_person = %s", (id_person,))
        person_info = cur.fetchone()
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
        return None
    except Exception as e:
        log_error("get_person_info", e)
        return None
    finally:
        cur.close()
        conn.close()


# Обновление данных о фото пользователя
def update_person_photos(id_person, new_photos):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT photo_name, photo_url FROM photo WHERE id_person = %s", (id_person,))
        current_photos = cur.fetchall()
        new_photo_urls = [photo['url'] for photo in new_photos]
        for current_photo_name, current_photo_url in current_photos:
            if current_photo_url not in new_photo_urls:
                delete_photo_from_s3(current_photo_name)
                cur.execute("DELETE FROM photo WHERE photo_name = %s AND id_person = %s", (current_photo_name, id_person))
        for new_photo in new_photos:
            cur.execute("SELECT photo_url FROM photo WHERE id_person = %s AND photo_url = %s", (id_person, new_photo['url']))
            if cur.fetchone():
                cur.execute("UPDATE photo SET dominating = %s WHERE photo_url = %s AND id_person = %s", (new_photo['dominating'], new_photo['url'], id_person))
        conn.commit()
        return True
    except Exception as e:
        log_error("update_person_photos", e)
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def set_notification_person(id_person, like=1, match=1, chat=1):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('''INSERT INTO notification (id_person, like, match, chat)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE like=%s, match=%s, chat=%s''',
                    (id_person, like, match, chat, like, match, chat))
        conn.commit()
        return True
    except Exception as e:
        log_error("set_notification_person", e)
        return False
    finally:
        cur.close()
        conn.close()


# Функция для получения списка пользователей по критериям
def get_filtered_persons(min_age, max_age, gender, target, limit=10):
    try:
        conn = get_connection()
        cur = conn.cursor()

        if gender == 0:
            query = '''
                SELECT id_person, name, age, city, height, id_zodiac_sign,
                       id_education, id_children, id_smoking, id_alcohol
                FROM person_info
                WHERE age BETWEEN %s AND %s
                  AND id_target = %s
                LIMIT %s
            '''
            params = (min_age, max_age, target, limit)
        else:
            query = '''
                SELECT id_person, name, age, city, height, id_zodiac_sign,
                       id_education, id_children, id_smoking, id_alcohol
                FROM person_info
                WHERE age BETWEEN %s AND %s
                  AND id_gender = %s
                  AND id_target = %s
                LIMIT %s
            '''
            params = (min_age, max_age, gender, target, limit)

        cur.execute(query, params)
        persons = cur.fetchall()
        return persons

    except Exception as e:
        log_error("get_filtered_persons", e)
        return False

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


# Добавление данных о фото пользователя
def add_person_photos(id_person, photos, files):
    try:
        conn = get_connection()
        cur = conn.cursor()
        file_index = 0

        for photo_meta in photos:
            if "file_path" in photo_meta:
                if file_index >= len(files):
                    raise ValueError("Количество файлов меньше, чем ожидается по метаданным.")

                photo_data = files[file_index]
                file_index += 1
                photo_name = str(uuid.uuid4()) + ".jpg"
                upload_photo_to_s3(photo_data["content"], photo_name)
                photo_url = get_photo_url(photo_name)

                cur.execute(
                    '''INSERT INTO photo (id_person, photo_name, photo_url, dominating)
                       VALUES (%s, %s, %s, %s)''',
                    (id_person, photo_name, photo_url, photo_meta["dominating"])
                )

        conn.commit()
        return True

    except Exception as e:
        log_error("add_person_photos", e)
        conn.rollback()
        return False

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


# Удаление фото пользователя
def dell_person_photos_in_s3(id_person):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT photo_name FROM photo WHERE id_person = %s', (id_person,))
        current_photos = cur.fetchall()

        for current_photo in current_photos:
            delete_photo_from_s3(current_photo[0])

        conn.commit()
        return True

    except Exception as e:
        log_error("dell_person_photos_in_s3", e)
        conn.rollback()
        return False

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


# Получение фотографий из базы данных по id_person
def get_photo(id_person):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT photo_url, dominating FROM photo WHERE id_person = %s', (id_person,))
        photos = cur.fetchall()
        photo_list = [{"photo_url": photo[0], "dominating": photo[1]} for photo in photos]
        return photo_list

    except Exception as e:
        log_error("get_photo", e)
        return []

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


# Замена статуса инкогнито у пользователя
def update_incognito_status(id_person, incognito_status):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('UPDATE person SET incognito = %s WHERE id = %s', (incognito_status, id_person))
        conn.commit()
        return True

    except Exception as e:
        log_error("update_incognito_status", e)
        return False

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


def get_incognito_status(user_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT incognito FROM person WHERE id = %s', (user_id,))
        result = cur.fetchone()
        return result[0] if result else None

    except Exception as e:
        log_error("get_incognito_status", e)
        return None

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


# Функция для добавления записи в таблицу black_list
def add_to_black_list(id_person, id_block):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO black_list (id_person, id_block) VALUES (%s, %s)', (id_person, id_block))
        conn.commit()
        return True

    except Exception as e:
        log_error("add_to_black_list", e)
        return False

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


# Функция для удаления записи из таблицы black_list
def remove_from_black_list(id_person, id_block):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM black_list WHERE id_person = %s AND id_block = %s', (id_person, id_block))
        conn.commit()
        return True

    except Exception as e:
        log_error("remove_from_black_list", e)
        return False

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


# Функция для получения всех заблокированных пользователей
def get_all_blocked_users(id_person):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT p.id_person, p.name, p.age, ph.photo_url
            FROM black_list bl
            JOIN person_info p ON bl.id_block = p.id_person
            LEFT JOIN photo ph ON p.id_person = ph.id_person AND ph.dominating = 0
            WHERE bl.id_person = %s''', (id_person,))
        blocked_users = cur.fetchall()
        return [{"id": user[0], "name": user[1], "age": user[2], "photo_url": user[3]} for user in blocked_users]

    except Exception as e:
        log_error("get_all_blocked_users", e)
        return None

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


def get_notification_person(id_person):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Выполняем запрос для получения данных по id_person
        cur.execute("SELECT * FROM notification WHERE id_person = %s", (id_person,))
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
        cur.close()
        conn.close()
