import sqlite3

conn = sqlite3.connect("community.db")
c = conn.cursor()

c.execute("SELECT * FROM posts")
print(c.fetchall())
