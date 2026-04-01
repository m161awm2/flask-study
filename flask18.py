from flask import Flask,request,redirect,render_template,session
import pymysql

app = Flask(__name__)
app.secret_key = "총들일하폭"
def create_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd=""
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS flask18")
    conn.commit()
    conn.close()



def connector():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="flask18"
    )



def init_db():
    conn = connector()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT,
              title TEXT,
              content TEXT
              )""")
    c.execute("""CREATE TABLE IF NOT EXISTS users(
              nickname VARCHAR(50) UNIQUE,
              password TEXT
              )
            """)
    c.execute("""CREATE TABLE IF NOT EXISTS likes(
              like_id INT AUTO_INCREMENT PRIMARY KEY,
              nickname VARCHAR(50),
              post_id INT
              )
              """)
    conn.commit()
    c.close()


@app.route('/')
def home():
    nickname = session.get("user")
    conn=connector()
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    c.close()
    return render_template('18_index.html',posts=posts,nickname=nickname)

@app.route('/go_register')
def go_register():
    return render_template('18_register.html')
@app.route('/register',methods=["POST"])
def register():
    conn = connector()
    c = conn.cursor()
    nickname = request.form["nickname"]
    password = request.form["password"]
    c.execute("SELECT * FROM users WHERE nickname = %s",(nickname,))
    is_exists = c.fetchone()
    if is_exists:
        fail_register = "회원가입에 실패하였습니다."
        return render_template('18_index',fail_register=fail_register)
    c.execute("INSERT INTO users (nickname,password) VALUES (%s,%s)",(nickname,password))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/go_login')
def go_login():
    return render_template('18_login.html')
@app.route('/login',methods=["POST"])
def login():
    conn = connector()
    c = conn.cursor()
    nickname = request.form["nickname"]
    password = request.form["password"]
    c.execute("SELECT * FROM users WHERE nickname = %s AND password = %s",(nickname,password))
    is_login = c.fetchone()
    if is_login:
        session["user"] = nickname
    return redirect('/')

@app.route('/go_write')
def go_write():
    return render_template('18_write.html')
@app.route('/write',methods=["POST"])
def write():
    conn = connector()
    c = conn.cursor()
    nickname = session.get("user")
    title = request.form["title"]
    content = request.form["content"]
    c.execute("INSERT INTO posts (nickname,title,content) VALUES (%s,%s,%s)",(nickname,title,content))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/go_detail')
def go_detail():
    return render_template('detail.html')
@app.route('/detail/<int:post_id>',methods=["GET","POST"])
def detail(post_id):
    conn=connector()
    c=conn.cursor()
    nickname = session.get("user")
    if request.method == "POST":
          if not nickname:
              conn.close()
              return redirect('/go_login')

          c.execute(
              "SELECT * FROM likes WHERE nickname = %s AND post_id = %s",
              (nickname, post_id)
          )
          is_liked = c.fetchone()

          if not is_liked:
              c.execute(
                  "INSERT INTO likes (nickname, post_id) VALUES (%s, %s)",
                  (nickname, post_id)
              )
              conn.commit()
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
    post = c.fetchone()
    c.execute("SELECT * FROM likes WHERE post_id = %s", (post_id,))
    like_users = c.fetchall()
    conn.close()
    return render_template('18_detail.html',post=post,like_users=like_users)


create_db()
init_db()

app.run(host="0.0.0.0",port=5000,debug=True)