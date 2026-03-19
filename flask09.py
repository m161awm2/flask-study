import sqlite3  # sqlite DB 쓰려고 불러옴
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("community.db")  # community.db 파일 연결(없으면 생성)
    c = conn.cursor()  # SQL 실행 도구 만들기
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (  -- posts 테이블이 없으면 생성
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 글 번호(자동 증가)
            nickname TEXT NOT NULL,  -- 닉네임
            contents TEXT NOT NULL  -- 글 내용
        )
    """)
    conn.commit()  # 저장
    conn.close()  # DB 닫기

@app.route("/", methods=["GET", "POST"])
def home():
    conn = sqlite3.connect("community.db")  # DB 연결
    c = conn.cursor()  # SQL 실행 도구

    if request.method == "POST":
        nickname = request.form["nickName"]
        contents = request.form["contents"]

        c.execute(
            "INSERT INTO posts (nickname, contents) VALUES (?, ?)",  # 글 추가
            (nickname, contents)
        )
        conn.commit()  # 추가한 내용 저장
        conn.close()  # DB 닫기
        return redirect("/")

    c.execute("SELECT * FROM posts ORDER BY id DESC")  # 글 전체 조회(최신글 먼저)
    posts = c.fetchall()  # 조회한 결과 전부 가져오기
    conn.close()  # DB 닫기

    return render_template("community_index.html", posts=posts)

@app.route("/delete_all", methods=["POST"])
def delete_all():
    conn = sqlite3.connect("community.db")  # DB 연결
    c = conn.cursor()  # SQL 실행 도구
    c.execute("DELETE FROM posts")  # posts 테이블의 글 전부 삭제
    conn.commit()  # 삭제 내용 저장
    conn.close()  # DB 닫기
    return redirect("/")

init_db()  # 처음 실행할 때 테이블 준비
app.run(host="0.0.0.0", port=5000)