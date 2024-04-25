import sqlite3

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

    # Создание таблицы "пол"
    cur.execute('''CREATE TABLE IF NOT EXISTS gender (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    )''')
    cur.execute("DELETE FROM gender")
    try:
        info = [("не выбрано",), ("мужской",), ("женский",)]
        cur.executemany("INSERT INTO gender (name) VALUES (?)", info)
    except sqlite3.IntegrityError:
        print("Ошибка: Дубликаты значений в таблице 'gender'.")

    # Создание таблицы "цель"
    cur.execute('''CREATE TABLE IF NOT EXISTS goal (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    )''')
    cur.execute("DELETE FROM goal")
    try:
        info = [("Дружба",), ("Свидания",), ("Отношения",), ("Без конкретики",)]
        cur.executemany("INSERT INTO goal (name) VALUES (?)", info)
    except sqlite3.IntegrityError:
        print("Ошибка: Дубликаты значений в таблице 'goal'.")

    # Создание таблицы "знаки зодиака"
    cur.execute('''CREATE TABLE IF NOT EXISTS zodiac_sign (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    )''')
    cur.execute("DELETE FROM zodiac_sign")
    try:
        info = [
            ("Овен",), ("Телец",), ("Близнецы",), ("Рак",), ("Лев",), ("Дева",), ("Весы",), ("Скорпион",), ("Стрелец",),
            ("Козерог",), ("Водолей",), ("Рыбы",), ("Не выбрано",)]
        cur.executemany("INSERT INTO zodiac_sign (name) VALUES (?)", info)
    except sqlite3.IntegrityError:
        print("Ошибка: Дубликаты значений в таблице 'zodiac_signс'.")

    # Создание таблицы "образование"
    cur.execute('''CREATE TABLE IF NOT EXISTS education (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    )''')
    cur.execute("DELETE FROM education")
    try:
        info = [("Среднее",), ("Не законченное высшее",), ("Высшее",), ("Несколько высших",), ("Не выбрано",)]
        cur.executemany("INSERT INTO education (name) VALUES (?)", info)
    except sqlite3.IntegrityError:
        print("Ошибка: Дубликаты значений в таблице 'education'.")

    # Создание таблицы "дети"
    cur.execute('''CREATE TABLE IF NOT EXISTS children (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    )''')
    cur.execute("DELETE FROM children")
    try:
        info = [("Нет и не планирую",), ("Нет, но хотелось бы",), ("Уже есть",), ("Не выбрано",)]
        cur.executemany("INSERT INTO children (name) VALUES (?)", info)
    except sqlite3.IntegrityError:
        print("Ошибка: Дубликаты значений в таблице 'children'.")

    # Создание таблицы "курение"
    cur.execute('''CREATE TABLE IF NOT EXISTS smoking (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    )''')
    cur.execute("DELETE FROM smoking")
    try:
        info = [("Негативно",), ("Нейтрально",), ("Положительно",), ("Не выбрано",)]
        cur.executemany("INSERT INTO smoking (name) VALUES (?)", info)
    except sqlite3.IntegrityError:
        print("Ошибка: Дубликаты значений в таблице 'smoking'.")

    # Создание таблицы "алкоголь"
    cur.execute('''CREATE TABLE IF NOT EXISTS alcohol (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    )''')
    cur.execute("DELETE FROM alcohol")
    try:
        info = [("Негативно",), ("Нейтрально",), ("Положительно",), ("Не выбрано",)]
        cur.executemany("INSERT INTO alcohol (name) VALUES (?)", info)
    except sqlite3.IntegrityError:
        print("Ошибка: Дубликаты значений в таблице 'alcohol'.")

    # Создание таблицы "о себе" с внешним ключом на таблицу "person"
    cur.execute('''CREATE TABLE IF NOT EXISTS about_me (
                            id INTEGER PRIMARY KEY,
                            id_person INTEGER,
                            description TEXT,
                            record_status BOOLEAN,
                            FOREIGN KEY (id_person) REFERENCES person(id)
                        )''')

    # Создание таблицы "фото" с внешним ключом на таблицу "about_me"
    cur.execute('''CREATE TABLE IF NOT EXISTS photo (
                            id_photo INTEGER PRIMARY KEY,
                            id_person INTEGER,
                            photo TEXT,
                            main BOOLEAN,
                            FOREIGN KEY (id_person) REFERENCES person(id)
                        )''')

    # Создание таблицы "person_info" с внешними ключоми
    cur.execute('''CREATE TABLE IF NOT EXISTS person_info (
                            id INTEGER PRIMARY KEY,
                            id_person INTEGER,
                            name TEXT,
                            age INTEGER,
                            id_gender INTEGER,
                            id_goal INTEGER,
                            city TEXT,
                            id_zodiac_sign INTEGER,
                            height TEXT,
                            id_education INTEGER,
                            id_children INTEGER,
                            id_smoking INTEGER,
                            id_alcohol INTEGER,
                            verification BOOLEAN,
                            FOREIGN KEY (id_person) REFERENCES person(id),
                            FOREIGN KEY (id_gender) REFERENCES gender(id),
                            FOREIGN KEY (id_goal) REFERENCES goal(id),
                            FOREIGN KEY (id_zodiac_sign) REFERENCES zodiac_sign(id),
                            FOREIGN KEY (id_education) REFERENCES education(id),
                            FOREIGN KEY (id_children) REFERENCES children(id),
                            FOREIGN KEY (id_smoking) REFERENCES smoking(id),
                            FOREIGN KEY (id_alcohol) REFERENCES alcohol(id)
                        )''')

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


def drop_all_tables():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Удаление всех таблиц
    cur.execute("DROP TABLE IF EXISTS person")
    cur.execute("DROP TABLE IF EXISTS gender")
    cur.execute("DROP TABLE IF EXISTS goal")
    cur.execute("DROP TABLE IF EXISTS zodiac_sign")
    cur.execute("DROP TABLE IF EXISTS education")
    cur.execute("DROP TABLE IF EXISTS children")
    cur.execute("DROP TABLE IF EXISTS smoking")
    cur.execute("DROP TABLE IF EXISTS alcohol")
    cur.execute("DROP TABLE IF EXISTS about_me")
    cur.execute("DROP TABLE IF EXISTS photo")
    cur.execute("DROP TABLE IF EXISTS info")

    conn.commit()
    conn.close()


def add_new_person(email, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # SQL-запрос на добавление записи
        cur.execute(f'INSERT INTO person (email, password) VALUES ("{email}", "{password}")')

        user_id = cur.lastrowid

        conn.commit()
        conn.close()

        return {"status": True, "user_id": user_id}

    except Exception as ex:
        print(ex)
        conn.close()
        return {"status": False}


def check_person_data_base(email, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, password FROM person WHERE email=?", (email,))
        user_info = cur.fetchone()

        if user_info and password == user_info[1]:
            user_id = user_info[0]
            conn.close()
            return {"status": True, "user_id": user_id}
        else:
            conn.close()
            return {"status": False}

    except Exception as ex:
        print(ex)
        conn.close()
        return {"status": False}


def check_email(email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        cur.execute('SELECT COUNT(*) FROM person WHERE email = ?', (email,))
        count = cur.fetchone()[0]

        conn.close()

        if count == 0:
            return True
        else:
            return False

    except Exception as ex:
        print(ex)
        conn.close()
        return False


def set_person_info_data_base(id_person, name, age, gender, goal, city, zodiac_sign, height, education, children,
                              smoking, alcohol, verification):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        # Получение id_gender из таблицы gender
        cur.execute('''SELECT id FROM gender WHERE name = ?''', (gender,))
        gender_row = cur.fetchone()
        if gender_row:
            id_gender = gender_row[0]
        else:
            raise ValueError("Пол {} не найден в таблице gender".format(gender))

        # Получение id_goal из таблицы goal
        cur.execute('''SELECT id FROM goal WHERE name = ?''', (goal,))
        goal_row = cur.fetchone()
        if goal_row:
            id_goal = goal_row[0]
        else:
            raise ValueError("Цель {} не найдена в таблице goal".format(goal))

        # Получение id_zodiac_sign из таблицы zodiac_sign
        cur.execute('''SELECT id FROM zodiac_sign WHERE name = ?''', (zodiac_sign,))
        zodiac_sign_row = cur.fetchone()
        if zodiac_sign_row:
            id_zodiac_sign = zodiac_sign_row[0]
        else:
            raise ValueError("Знак зодиака {} не найден в таблице zodiac_sign".format(zodiac_sign))

        # Получение id_education из таблицы education
        cur.execute('''SELECT id FROM education WHERE name = ?''', (education,))
        education_row = cur.fetchone()
        if education_row:
            id_education = education_row[0]
        else:
            raise ValueError("Уровень образования {} не найден в таблице education".format(education))

        # Получение id_children из таблицы children
        cur.execute('''SELECT id FROM children WHERE name = ?''', (children,))
        children_row = cur.fetchone()
        if children_row:
            id_children = children_row[0]
        else:
            raise ValueError("Дети {} не найдены в таблице children".format(children))

        # Получение id_smoking из таблицы smoking
        cur.execute('''SELECT id FROM smoking WHERE name = ?''', (smoking,))
        smoking_row = cur.fetchone()
        if smoking_row:
            id_smoking = smoking_row[0]
        else:
            raise ValueError("Привычки к курению {} не найдены в таблице smoking".format(smoking))

        # Получение id_alcohol из таблицы alcohol
        cur.execute('''SELECT id FROM alcohol WHERE name = ?''', (alcohol,))
        alcohol_row = cur.fetchone()
        if alcohol_row:
            id_alcohol = alcohol_row[0]
        else:
            raise ValueError("Привычки к алкоголю {} не найдены в таблице alcohol".format(alcohol))

        # Вставка данных в таблицу person_info
        cur.execute('''REPLACE INTO person_info (id_person, name, age, id_gender, id_goal, city, id_zodiac_sign, height, 
                            id_education, id_children, id_smoking, id_alcohol, verification) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (id_person, name, age, id_gender, id_goal, city, id_zodiac_sign, height, id_education,
                     id_children, id_smoking, id_alcohol, verification))

        conn.commit()
        conn.close()
        return True

    except Exception as ex:
        print("Ошибка при вставке данных в таблицу 'person_info':", ex)
        conn.close()
        return False


def get_person_info_data_base(id_person):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        cur.execute('''SELECT pi.id_person, pi.name, pi.age, g.name AS name_gender, 
                              goal.name AS name_goal, pi.city, zs.name AS name_zodiac_sign, 
                              pi.height, e.name AS name_education, 
                              c.name AS name_children, s.name AS name_smoking, 
                              a.name AS name_alcohol, pi.verification
                       FROM person_info AS pi
                       LEFT JOIN gender AS g ON pi.id_gender = g.id
                       LEFT JOIN goal ON pi.id_goal = goal.id
                       LEFT JOIN zodiac_sign AS zs ON pi.id_zodiac_sign = zs.id
                       LEFT JOIN education AS e ON pi.id_education = e.id
                       LEFT JOIN children AS c ON pi.id_children = c.id
                       LEFT JOIN smoking AS s ON pi.id_smoking = s.id
                       LEFT JOIN alcohol AS a ON pi.id_alcohol = a.id
                       WHERE pi.id_person = ?''', (id_person,))
        person_info = cur.fetchone()

        if person_info:
            # Парсинг полученных данных
            name = person_info[1]
            age = person_info[2]
            name_gender = person_info[3]
            name_goal = person_info[4]
            city = person_info[5]
            name_zodiac_sign = person_info[6]
            height = person_info[7]
            name_education = person_info[8]
            name_children = person_info[9]
            name_smoking = person_info[10]
            name_alcohol = person_info[11]
            verification = person_info[12]

            # Возвращение полученных данных
            return {
                "status": True,
                "name": name,
                "age": age,
                "gender": name_gender,
                "goal": name_goal,
                "city": city,
                "zodiac_sign": name_zodiac_sign,
                "height": height,
                "education": name_education,
                "children": name_children,
                "smoking": name_smoking,
                "alcohol": name_alcohol,
                "verification": verification
            }
        else:
            return {"status": False}

    except Exception as ex:
        print("Ошибка при получении данных из таблицы 'person_info':", ex)
        return {"status": False}

    finally:
        conn.close()
