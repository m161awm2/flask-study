from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def home():
    result = None # 아니 뭔 미리 NOne 이라고 정의해야함? 뭔 이딴 모듈이 다있음???????????????????????????
    if request.method == "POST":
        num1 = int(request.form['number01']) # !!!!!!!! HTML에서 값 가져오기@@@@@@@@@@@@@@
        
        num2 = int(request.form['number02']) # !!!!!!!! HTML에서 값 가져오기@@@@@@@@@@@@@@

        num3 = int(request.form['number02']) # !!!!!!!! HTML에서 값 가져오기@@@@@@@@@@@
        
        result =( num1+num2+num3)/ 3

    return render_template("avg.html", result=result)
app.run(host="0.0.0.0",port=5000)