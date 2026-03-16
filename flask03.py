from flask import Flask

app = Flask(__name__)

@app.route('/') # 그냥 들어왔을때
def home():
    return "홈 페이지"

@app.route('/users/<string:usname>') # 경로를 추가
def userName(usname):
    return "<strong>Hello,</strong>"+usname

app.run(host="0.0.0.0", port=5000)