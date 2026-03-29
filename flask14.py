from flask import Flask, request,redirect,render_template
import pymysql

app = Flask(__name__)

def create_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd=""
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS flask14")
    conn.commit()
    conn.close()

def connector():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="flask14"
    )

def init_db():
    conn = connector()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT NOT NULL,
              title TEXT NOT NULL,
              quest TEXT NOT NULL,
              answer TEXT NOT NULL
              )""")
    conn.commit()
    conn.close()

@app.route('/',methods=["GET","POST"])
def home():
    conn = connector()
    c = conn.cursor()
    if request.method == "POST":
        nickname = request.form["nickname"]
        title = request.form["title"]
        quest = request.form["quest"]
        answer = request.form["answer"]
        c.execute("INSERT INTO posts (nickname, title, quest, answer) VALUES (%s,%s,%s,%s)",(nickname,title,quest,answer))
        conn.commit()
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()
    conn.close()
    return render_template('flask14_index.html',posts=posts)

@app.route('/quests/<int:post_id>')
def quests(post_id):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
    post = c.fetchone()
    c.close()
    return render_template('flask14_detail.html',post=post)

@app.route('/answer',methods=["POST"])
def answer():
    not_answer = ""
    post_id = request.form["post_id"]
    answer = request.form["answer"]
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
    post = c.fetchone()
    if answer == post[4]:
        c.execute("DELETE FROM posts WHERE id = %s",(post_id,))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        conn.close()
        return redirect(f'/quests/{post_id}')

create_db()
init_db()

app.run(host="0.0.0.0",port=5000,debug=True)