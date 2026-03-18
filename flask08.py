from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return render_template("bmiHome.html")

@app.route('/resultBMI', methods=["POST"])
def result():
    hei = float(request.form["height"])
    wei = float(request.form["weight"])
    height_m = hei / 100
    bmi = round(wei / (height_m * height_m), 2)
    if bmi < 18.5:
        status = "저체중"
    elif bmi < 23:
        status = "정상"
    elif bmi < 25:
        status = "과체중"
    elif bmi < 30:
        status = "비만"
    else:
        status = "고도 비만"
    return render_template("resultBMI.html",bmi=bmi,status=status)

app.run(host="0.0.0.0",port=5000)