from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "아무문자열이나넣기"

def init_db():
    conn = sqlite3.connect("login.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (  -- posts 테이블이 없으면 생성
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 글 번호(자동 증가)
            nickname TEXT UNIQUE,  -- 닉네임 유니크 (중복안됨)
            password TEXT -- pw
        )
    """)
    conn.commit()
    conn.close()

@app.route('/',methods=["GET"]) 
def home():
    return render_template("flask10.html")

@app.route('/sign_in',methods=["GET"]) # 얘로 html을 열어서 회원가입 하러가는 문으로 가야함
def flask10_sign_in():
    return render_template('flask10_sign_in.html')

@app.route('/login',methods=["GET"]) # 얘로 html을 열어서 로그인 하러가는 문으로 가야함
def flask10_login():
    return render_template('flask10_login.html')

@app.route('/flask10_sign_in',methods=["POST"]) # 회원가입을 처리하는거임 @@@@@@@@@@@@@@@@@
def sign_in(): 
    conn = sqlite3.connect("login.db")
    c= conn.cursor()
    nickname = request.form["nickname"]
    password = request.form["password"]
    c.execute("INSERT INTO posts (nickname, password) VALUES (?,?)",(nickname,password))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/flask10_login',methods=["POST"]) # 로그인을 처리함 @@@@@@@@@@@@@@@@
def login():
    userName = ""
    conn = sqlite3.connect("login.db")
    c= conn.cursor()
    nickname = request.form["nickname"]
    password = request.form["password"]
    c.execute("SELECT * FROM posts WHERE nickname = (?) AND password = (?)",(nickname,password))

    user = c.fetchone()
    if user: #값이 있을때 실행
        print("test 로그인 완료")
        userName = user[1]
        
    else: #없으면 else하고 프린트
        print("로그인 실패")
        
    return render_template('/flask10.html',userName=userName)
init_db()
app.run(host="0.0.0.0",port=5000,debug=True)