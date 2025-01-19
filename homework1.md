## 作业1

#### 写在前面

```python
from flask import Flask,jsonify,request

app=Flask(__name__)

@app.route('/mul',methods=['POST'])
def mul():
    data=request.get_json()
    a,b=data.get('a'),data.get('b')
    if a is not None and b is not None:
        try:
            result = float(a) * float(b)
            res = f'{result:g}'
            return jsonify({"res": res}), 200
        except ValueError:
            return jsonify({"error": "Invalid input. Please provide valid numbers."}), 400
    else:
        return jsonify({"error": "Please provide both 'a' and 'b' in the JSON data."}), 400

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8000)
```





#### 非json

如果不使用`json`格式，我会这么写

```python
from flask import Flask,request

app=Flask(__name__)

@app.route('/mul',methods=['POST'])
def multiply():
    a,b=request.form.get('a'),request.form.get('b')
    res=f'{float(a)*float(b):g}'
    return f'{res}'

if __name__=='__main__':
	app.run(host='0.0.0.0',port=8000)
```

运行返回的两个地址:

-   本地:http://127.0.0.1:8000
-   公网:http://192.168.1.6:8000 

```bash
curl -X POST -d "a=66&b=2" http://127.0.0.1:8000/mul
```

```bash
curl -X POST -d "a=66&b=2" http://192.168.1.6:8000/mul
```

都会返回相同132

**到此存在几个问题(局限)**

要测试公网的是否可用,用POST请求我就不会了,只能改成GET请求.接着在手机浏览器上面输入

```
192.168.1.6:8000/mul?a=66&b=2
```

得到的确实是132,但是接着问AI说公网不指WiFi,但是手机上改成移动数据就转不出来,问了怎么改但是还没学会,这是问题之一

#### json

json的话改在哪:输入、接受和返回

*   接受:先用`request.get_json()`把json格式的数据提取出来,再分别提取a,b

*   返回:json化--->jsonify

*   输入:暂且只考虑curl上的命令作修改,即添加头部Content-Type，指定为json格式

` curl -X POST -H "Content-Type: application/json" -d "{\"a\":66,\"b\":2}" http://127.0.0.1:8000/multiply`

```python
from flask import Flask,jsonify,request

app=Flask(__name__)

@app.route('/mul',methods=['POST'])
def mul():
    data=request.get_json()
    a,b=data.get('a'),data.get('b')
    res=f'{float(a)*float(b):g}'
    return jsonify({"res": res}), 200

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8000)
```

