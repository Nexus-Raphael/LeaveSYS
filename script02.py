from flask import Flask, request, session, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'no_matter_what'


def get_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='nexus'
    )
    return connection


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)  # 把数据库里面的东西用字典表示
    cursor.execute('SELECT * FROM winefac WHERE username=%s AND password=%s', (username, password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user:
        session['username'] = username
        return jsonify({'message': 'login successfully.'}), 200
    else:
        return jsonify({'message': 'login FAILED.'}), 401


@app.route('/user_info', methods=['GET'])
def user_info():
    username = session.get('username')
    if username:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM winefac WHERE username=%s', (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        if user:
            return jsonify({
                'id': user['id'],
                'username': user['username'],
                'true_name': user['nameT'],
                'wine_name': user['nameW'],
                'status': user['status'],
                'life': user['life']
            })
        else:
            return jsonify({'message': 'NOT FOUND'}), 404
    else:
        return jsonify({'message': 'PLEASE login'}), 401


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)