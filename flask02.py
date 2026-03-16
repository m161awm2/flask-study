from flask import Flask, render_template

def addNum(a,b):
    return str(a+b) # 브라우저에 보내는게 무조건 str타입이여야함 그래서 str로 묶음
    
app = Flask(__name__) 

num1, num2 = int(input("정수 2개 입력")), int(input())

@app.route("/")
def home():
    return ("<h1>더하기 프로그램</h1><br>"
    "더한 값은... : " + addNum(num1,num2))

app.run(host="0.0.0.0",port=5000)