from flask import Flask, redirect,request,render_template,session
import pymysql

app = Flask(__name__)
app.secret_key = "flask16화이팅!"
def create_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd=""
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS flask16")
    conn.commit()
    conn.close()

def connector():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="flask16"
    )

def init_db():
    conn = connector()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nickname TEXT,              
                title TEXT NOT NULL,
                content TEXT NOT NULL
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS users(
                nickname VARCHAR(50) UNIQUE,
                password TEXT NOT NULL
              )""")
    c.execute("""CREATE TABLE IF NOT EXISTS likes(
                id INT NOT NULL,
                nickname TEXT
              )
              """)
    conn.commit()
    conn.close()

@app.route('/',methods=["GET","POST"])
def home():
    conn = connector()
    c = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        
        c.execute("INSERT INTO posts (nickname,title,content) VALUES (%s,%s,%s)",(session.get("user"),title,content))
        conn.commit()
        
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    
    conn.close()

    user = session.get("user")

    return render_template('flask16.html',posts=posts,user=user)

@app.route('/register_go')
def register_go():
    return render_template('flask16_register.html')
@app.route('/register',methods=["POST"])
def register():
    text_exists = ""
    nickname = request.form["nickname"]
    password = request.form["password"]
    conn=connector()
    c=conn.cursor()
    c.execute("SELECT * FROM users WHERE nickname = %s",(nickname,))
    is_exists = c.fetchone()
    if is_exists:
        text_exists = "이미 해당 닉네임이 존재합니다."
        return render_template('flask16_register.html',text_exists=text_exists)
    c.execute("INSERT INTO users (nickname,password) VALUES (%s,%s)",(nickname,password))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/login_go')
def login_go():
    return render_template('flask16_login.html')
@app.route('/login',methods=["POST"])
def login():
    nickname = request.form["nickname"]
    password = request.form["password"]
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE nickname = %s",(nickname,))
    post = c.fetchone()
    if post[1] == password:
        session["user"] = nickname
        return redirect('/')
    return "닉네임이나 비밀번호가 옳지 않습니다!"

@app.route('/post_go')
def post_go():
    return render_template('flask16_post.html')
@app.route('/post/<int:post_id>',methods=["GET","POST"])
def post(post_id):
    conn = connector()
    c = conn.cursor()
    if request.method=="POST":
        current_user = session.get("user")
        if not current_user:
            return "로그인이 필요한 메서드입니다."
        c.execute("SELECT * FROM likes WHERE id = %s AND nickname = %s",(post_id,current_user)) #좋아요 테이블에서 현재 유저가 해당 게시글에 좋아요를 눌렀는지 확인 (검사)
        is_liked = c.fetchone()
        if is_liked:
            return "하트를 또 누를수는 없읍니다."
        c.execute("INSERT INTO likes (id,nickname) VALUES (%s,%s)",(post_id,current_user)) #좋아요 테이블에 현재 유저가 해당 게시글에 좋아요를 눌렀다고 기록 (삽입)
        conn.commit()
        
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
    post = c.fetchone()
    c.execute("SELECT * FROM likes WHERE id = %s",(post_id,)) 
    like_users = c.fetchall()  
    conn.commit()
    conn.close()
    return render_template('flask16_post.html',post=post,like_users=like_users)

create_db()
init_db()
app.run(host="0.0.0.0",port=5050,debug=True)