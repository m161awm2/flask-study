from flask import Flask, redirect, request, render_template
import pymysql

app = Flask(__name__)

def make_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd=""
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS test")
    conn.commit()
    conn.close()

def connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test"
    )

def init_db():
    conn = connection()
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nickname TEXT,
                title TEXT,
                contents TEXT,
                password TEXT
            )
        """)
    conn.commit()
    conn.close()

@app.route('/',methods=["GET","POST"])
def home():
    conn = connection()
    c = conn.cursor()
    if request.method == "POST":
        nickname = request.form["nickname"]
        title = request.form["title"]
        contents = request.form["contents"]
        password = request.form["password"]
        c.execute("INSERT INTO posts (nickname, title, contents, password) VALUES (%s,%s,%s,%s)",(nickname, title, contents, password))
        conn.commit()
    
    c.execute("SELECT * FROM posts")
    post = c.fetchall()
    conn.close()
    
    return render_template("flask12_index.html", posts=post)

@app.route('/detail/<int:post_id>')
def detail(post_id):
    conn = connection()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = c.fetchone()
    conn.close()
    return render_template("flask12_detail.html", post=post)

@app.route('/delete/<int:post_id>', methods=["POST"]) 
def delete(post_id):
    conn = connection()
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id = %s AND password = %s", (post_id, request.form["password"])) 
    conn.commit()
    conn.close()
    return redirect('/')

make_db()
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)