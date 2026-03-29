from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

def make_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd="Zdzdsmsm44!"
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS flask13")
    conn.commit()
    conn.close()

def connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="Zdzdsmsm44!",
        database="flask13"
    )

def init_db():
    conn = connection()
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS posts(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nickname VARCHAR(30) NOT NULL,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                password VARCHAR(255) NOT NULL,
                time DATETIME DEFAULT CURRENT_TIMESTAMP)
                          """) 
    conn.commit()
    conn.close()

#posts[1]은 nickname, posts[2]는 title, posts[3]은 content, posts[4]는 password, posts[5]는 time이 됨. @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@app.route('/',methods=["GET","POST"])
def home():
    conn = connection()
    c = conn.cursor()
    if request.method == "POST":
        nickname = request.form["nickname"]
        title = request.form["title"]
        content = request.form["content"]
        password = request.form["password"]
        c.execute("INSERT INTO posts (nickname, title, content, password) VALUES (%s,%s,%s,%s)",(nickname, title, content, password))
        conn.commit()
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()
    conn.close()
    return render_template("flask13_index.html",posts=posts)

@app.route('/post/<int:post_id>')
def posts(post_id):
    conn = connection()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
    post = c.fetchone()
    conn.close()
    return render_template("flask13_post.html", post=post)

@app.route('/delete_this', methods=["POST"])
def delete_this():
    post_id = request.form["post_id"]
    password = request.form["password"]
    conn = connection()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,)) # post_id가 같은 게시글을 찾아라
    post = c.fetchone() # flask13_posthtml에서 전달된 post_id의 값을 이용해서 해당 게시글 행의 정보를 찾음 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    if post and post[4] == password: # post[4]는 password 컬럼의 값이 됨. post가 존재하고, 입력된 패스워드와 일치할 때 삭제 실행 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        c.execute("DELETE FROM posts WHERE id = %s",(post_id,)) # post_id가 같은 게시글을 삭제해라
        conn.commit()
    conn.close()
    return redirect('/')

make_db()
init_db()

app.run(host="localhost", port=5000, debug=True)