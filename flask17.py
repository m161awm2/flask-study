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
    c.execute("CREATE DATABASE IF NOT EXISTS flask17")
    conn.commit()
    conn.close()
def connector():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="flask17"
    )
def init_db():
    conn = connector()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
              nickname VARCHAR(50) NOT NULL,
              password TEXT NOT NULL
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT,
              title TEXT NOT NULL,
              content TEXT NOT NULL
              )
              """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    user = session.get("user")
    return render_template("17_index.html",posts=posts,user=user)

@app.route('/register_go')
def register_go():
    return render_template("register.html")
@app.route('/register',methods=["POST"])
def register():
    conn = connector()
    c = conn.cursor()
    nickname = request.form["nickname"]
    password = request.form["password"]
    c.execute("SELECT * FROM users WHERE nickname = %s",(nickname,))
    isExists = c.fetchone()
    if isExists:
        stop_register = "해당 닉네임은 이미 존재합니다."
        return render_template('register.html',stop_register=stop_register)
    c.execute("INSERT INTO users (nickname,password) VALUES (%s,%s)",(nickname,password))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/login_go')
def login_go():
    return render_template('login.html')
@app.route('/login',methods=["POST"])
def login():
    nickname = request.form["nickname"]
    password = request.form["password"]
    conn=connector()
    c=conn.cursor()
    c.execute("SELECT * FROM users WHERE nickname = %s AND password = %s",(nickname,password))
    loging = c.fetchone()
    if not loging:
        fail_login = "닉네임과 비밀번호가 맞는지 다시 확인하세요!"
        return render_template('login.html',fail_login=fail_login)
    session["user"] = nickname
    return redirect('/')

@app.route('/write_go')
def write_go():
    return render_template('write.html')
@app.route('/write',methods=["POST"])
def write():
    print("폼 데이터:", request.form)
    nickname = session.get("user")
    if not nickname:
        return "로그인좀해라"
    title = request.form["title"]
    content = request.form["contents"]
    conn=connector()
    c = conn.cursor()
    c.execute("INSERT INTO posts (nickname,title,content) VALUES (%s,%s,%s)",(nickname,title,content))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/post/<int:post_id>',methods=["GET","POST"])
def detail(post_id):
    conn=connector()
    c=conn.cursor()
    if request.method == "POST":
        nickname = session.get("user")
        c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
        delete_post = c.fetchone()
        if delete_post[1] == nickname:
            c.execute("DELETE FROM posts WHERE id = %s",(post_id,))
            conn.commit()
            return redirect('/')
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
    post = c.fetchone()
    conn.close()
    return render_template('17_detail.html',post=post)

create_db()
init_db()

app.run(host="0.0.0.0",port=5000,debug=True)