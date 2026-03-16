from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
        return '로긴 홈피'

@app.route('/login', methods=['GET', 'POST']) # 메서드와 겟, 포스트는 절대절대 바꾸면 안됨
def login():
        if request.method=='GET': # html에서 얘 정보좀 줘라라고 요청할때 얘가 먼저 실행되고 
            return "로그인 화면열기"
        elif request.method=='POST': # 이건 아이디 비밀번호를 서버로 제출하는 거라 POST.
            return "로그인 시도 처리"
        else:
                return "알수없음?"
    
app.run(host="0.0.0.0", port=5000)