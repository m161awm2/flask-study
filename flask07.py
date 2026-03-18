from flask import Flask, request, render_template
import time

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return render_template("score_calculator.html")

@app.route('/result', methods=["POST"])
def result():
        score = int(request.form["point"])
        if score >= 90:
            result = 'A'
        elif score >= 80:
            result = 'B'
        elif score >= 70:
            result = 'C'
        elif score >= 60:
            result = 'D'
        else:
            return render_template("kick.html")
         
        return render_template("result.html", score=score, result=result)
if "__main__" == __name__:
    app.run(host="0.0.0.0", port=5000)
