from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=["GET","POST"])
def home():
    
    total_result = 0
    avg_result = 0 
    max_result = 0
    min_result = 0
    
    if request.method == "POST":
        num1 = int(request.form['number01']) # !!!!!!!! HTML에서 값 가져오기@@@@@@@@@@@@@@
        num2 = int(request.form['number02']) # !!!!!!!! HTML에서 값 가져오기@@@@@@@@@@@@@@
        num3 = int(request.form['number03']) # !!!!!!!! HTML에서 값 가져오기@@@@@@@@@@@ 정수값으로 반환해야함
        
        total_result = num1+num2+num3
        avg_result = round((num1+num2+num3)/ 3) #라운드 함수, 반올림
        max_result = max(num1,num2,num3)
        min_result = min(num1,num2,num3)
    #elif request.method=="GET":
    #    return "homeP" HTML에서 GET메서드를 못가져옴, 곧 수정예정??

    return render_template("avg.html", avg_result=avg_result,max_result=max_result,min_result=min_result,total_result=total_result)
app.run(host="0.0.0.0",port=5000)
