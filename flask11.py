from flask import Flask, render_template, request, redirect, session
import pymysql
app = Flask(__name__)
app.secret_key = "123"

def create_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd=""
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS flask11")
    conn.commit()
    conn.close()

def func_sql():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="flask11"
    )
def init_db():
    conn = func_sql()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(50),
            contents TEXT)
              """)
    conn.commit()
    conn.close()

@app.route('/', methods=["GET","POST"])
def home():
    conn = func_sql()
    c = conn.cursor()
    if request.method == "POST":
        title = request.form["title"]
        contents = request.form["contents"]
        c.execute("INSERT INTO posts (title, contents) VALUES (%s, %s)", (title, contents))
        conn.commit()
    c.execute("SELECT * FROM posts ORDER BY id DESC") # 글 번호 내림차순으로 가져오기
    posts = c.fetchall()
    conn.close()
    return render_template("flask11.html",posts=posts)

create_db()
init_db()

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)