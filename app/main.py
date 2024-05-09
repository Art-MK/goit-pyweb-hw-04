from flask import Flask, render_template, request
import socket
import threading
import json
from datetime import datetime
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# HTTP Сервер
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    # Обробка POST-запиту
    if request.method == 'POST':
        # Отримання даних з форми
        username = request.form['username']
        message = request.form['message']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # Формування словника з даними
        data = {
            timestamp: {
                'username': username,
                'message': message
            }
        }
        # Відправлення даних на сокет
        send_to_socket(data)
    return render_template('message.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

def send_to_socket(data):
    # Відправлення даних на сокет
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(data).encode(), ('localhost', 5000))

# Сокет Сервер
def socket_server():
    # Створення сокету та приймання даних
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('localhost', 5000))
        while True:
            data, addr = s.recvfrom(1024)
            data = json.loads(data.decode())
            # Збереження даних у файл
            save_to_json(data)

def save_to_json(data):
    file_path = os.path.join(app.root_path, 'storage', 'data.json')
    existing_data = {}

    # Перевірка існування та розміру файлу перед завантаженням
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)

    # Оновлення даних
    existing_data.update(data)

    # Запис даних у файл
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=2)

if __name__ == '__main__':
    # Перевірка наявності каталогу `storage`, якщо не існує - створити
    storage_dir = os.path.join(app.root_path, 'storage')
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)

    # Запуск HTTP Сервера
    http_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 3000})
    http_thread.daemon = True
    http_thread.start()

    # Запуск Сокет Сервера
    socket_thread = threading.Thread(target=socket_server)
    socket_thread.daemon = True
    socket_thread.start()

    http_thread.join()
