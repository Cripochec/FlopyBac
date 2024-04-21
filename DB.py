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

    # Сохранение изменений и закрытие соединения
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
