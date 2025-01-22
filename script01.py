
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