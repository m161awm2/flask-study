from flask import Flask, request,redirect,render_template,session
import pymysql
import datetime

app = Flask(__name__)
app.secret_key = "편향된방송국들을대체할m161News"

def create_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd=""
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS flask19")
    conn.commit()
    conn.close()

def connector():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="flask19"
    )

def init_db():
    conn = connector()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS articles(
              id INT AUTO_INCREMENT PRIMARY KEY,
              name TEXT,
              article_title TEXT,
              article_content TEXT
              )  
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS reporter(
              reporter_name VARCHAR(50),
              reporter_password TEXT
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS comments(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT,
              comment_content TEXT,
              comment_id INT
              )
              """)
    conn.commit()
    conn.close()

@app.route('/')
def news_home():
    name = session.get("user")  
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM articles ORDER BY id DESC")
    aritlcles = c.fetchall()
    conn.close()
    return render_template("news_index.html",articles=aritlcles,name=name)

@app.route('/write',methods=["GET","POST"])
def write_try():
    name = session.get("user")
    if not name:
        return "해당 기능은 로그인 후 사용 가능합니다."
    if request.method == "GET":
        return render_template("news_write.html")
    article_title = request.form["article_title"]
    article_content = request.form["article_content"]
    check_at = article_title.replace(" ",""); check_ac = article_content.replace(" ","")
    if not check_ac or not check_at:
        return "값을 입력하세요!"
    conn = connector()
    c = conn.cursor()
    c.execute("INSERT INTO articles (name,article_title, article_content) VALUES (%s,%s,%s)",(name,article_title,article_content))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("news_register.html")
    conn = connector()
    c = conn.cursor()
    reporter_name = request.form["reporter_name"]
    reporter_password = request.form["reporter_password"]
    c.execute("SELECT * FROM reporter WHERE reporter_name = %s",(reporter_name,))
    is_exists = c.fetchone()
    if is_exists:
        return "해당 이름은 이미 존재합니다"
    c.execute("INSERT INTO reporter (reporter_name,reporter_password) VALUES (%s,%s)",(reporter_name,reporter_password))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('news_login.html')
    conn = connector()
    c = conn.cursor()
    reporter_name = request.form["reporter_name"]
    reporter_password = request.form["reporter_password"]
    c.execute("SELECT * FROM reporter WHERE reporter_name = %s AND reporter_password = %s",(reporter_name,reporter_password))
    is_login = c.fetchone()
    conn.close()
    if not is_login:
        login_fail = "로그인에 실패하였습니다.\n이름과 비밀번호를 다시 확인하십시오."
        return render_template('news_login.html',login_fail=login_fail)
    session["user"] = reporter_name
    return redirect('/')

@app.route('/news_detail/<int:news_id>',methods=["GET","POST"])
def news_detail(news_id):
    conn = connector()
    c = conn.cursor()
    if request.method == "POST":
        nickname = session.get("user")
        if not nickname:
            return "꺼져"
        comment_content = request.form["comment_content"]
        # 코멘트 id를 news_id의 값과 같게해서 댓글을 구별하게 함 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        c.execute("INSERT INTO comments (nickname,comment_content,comment_id) VALUES (%s,%s,%s)",(nickname,comment_content,news_id)) 
        conn.commit()
        
    c.execute("SELECT * FROM articles WHERE id = %s",(news_id,))
    article = c.fetchone()
    c.execute("SELECT * FROM comments WHERE comment_id = %s",(news_id,)) 
    comments = c.fetchall()
    conn.close()
    return render_template('news_detail.html',article=article,comments=comments)
create_db()
init_db()

app.run(host="localhost",port=6767,debug=True)