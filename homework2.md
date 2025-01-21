>   作业2

作业核心问题，怎么在输入账号密码登录成功后再显示id、姓名和年龄等内容

答案是使用session记录

```python
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
```

问题:

-   没有表示年龄
-   考虑到早晚会用到数据库,所以去尝试了一下,下面附上建表语句和表内容
-   `app.secret_key = 'no_matter_what'`这一句的必要性任然存疑,也看到过用os生成的安全密钥,是生成了随机字符串?
-   昨天晚上培训时看到写的是@app.post之类的,尝试了但是好像不适用
-   而且培训时的测试接口方法没接触过,不太会用
-   这个用cmd的curl去测会有问题,连起来查询第二分句也返回未登录,下面附上图片
-   重复登录会覆盖,打算多了解一点session再弄登出
-   (买了服务器不会用) (

>   关于数据库

-   建表语句

![](D:\QQ\建表语句.png)

-   表内容

![](D:\QQ\winefac.png)

>   接口测试

![](D:\QQ\binga登录.png)

![](D:\QQ\binga信息.png)

![](D:\QQ\Gin登录.png)

![](D:\QQ\Gin信息.png)

![](D:\QQ\作业2问题.png)