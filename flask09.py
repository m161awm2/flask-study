import sqlite3  # sqlite DB 쓰려고 불러옴
import datetime # 현재시간을 출력하게,
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("community.db")  # community.db 파일 연결(없으면 생성)
    c = conn.cursor()  # SQL 실행 도구 만들기
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (  -- posts 테이블이 없으면 생성
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 글 번호(자동 증가)
            nickname TEXT NOT NULL,  -- 닉네임
            contents TEXT NOT NULL,  -- 글 내용
            password TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)
    conn.commit()  # 저장
    conn.close()  # DB 닫기

@app.route("/", methods=["GET", "POST"])
def home():
    
    is_null = ""
    conn = sqlite3.connect("community.db")  # DB 연결
    c = conn.cursor()  # SQL 실행 도구
    
    if request.method == "POST":
        time = datetime.datetime.now()
        nickname = request.form["nickName"]
        contents = request.form["contents"]
        password = request.form["password"]
        

        if nickname != "" and contents != "" and password != "":
            c.execute(
            "INSERT INTO posts (nickname, contents, password, time) VALUES (?, ?, ?, ?)",  # 글 추가
            (nickname, contents, password, time)
        )
            conn.commit()  # 추가한 내용 저장
            conn.close()  # DB 닫기
            return redirect("/")
        else:
            is_null = "값을 입력하세요!!"
  

    c.execute("SELECT * FROM posts ORDER BY id DESC")  # 글 전체 조회(최신글 먼저)
    posts = c.fetchall()  # 조회한 결과 전부 가져오기
    conn.close()  # DB 닫기

    return render_template("community_index.html", posts=posts, is_null=is_null)

@app.route("/delete_this", methods=["POST"])
def delete_this():
    post_id = request.form["post_id"] # HTML에서 hidden input으로 전달된 글 id 받기

    conn = sqlite3.connect("community.db") # community.db 데이터베이스 연결
    c = conn.cursor() # SQL 실행용 커서 생성
    c.execute("DELETE FROM posts WHERE id = ?", (post_id,)) # posts 테이블에서 id가 일치하는 글 1개만 삭제
    conn.commit() # 삭제 내용을 실제 DB에 반영
    conn.close() # DB 연결 종료

    return redirect("/")

init_db()  # 처음 실행할 때 테이블 준비
app.run(host="0.0.0.0", port=5000, debug=True)