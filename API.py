from flask import Flask, request, jsonify
from smtp import key_generation, send_email
from DB import add_new_person
app = Flask(__name__)


@app.route('/register_data', methods=['POST'])
def register_data():
    # Получаем данные из запроса
    data = request.get_json()

    email = data['email']
    password = data['password']
    info = add_new_person(email, password)

    if info['status']:
        code = key_generation()
        send_email(email, "Код регистрации", "Разовый код: "+str(code))
        return jsonify({"status": True, "user_id": info['user_id'], "code": code})
    else:
        return jsonify({"status": False})

# для сервера
if __name__ == '__main__':
    # Запускаем сервер на всех доступных интерфейсах (0.0.0.0) и указываем порт 5000
    app.run(debug=True, host='0.0.0.0', port=5000)

# для локалки
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
