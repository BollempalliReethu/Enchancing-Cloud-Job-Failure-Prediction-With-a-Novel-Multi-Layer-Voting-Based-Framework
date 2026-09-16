from flask import Flask, render_template, request
import numpy as np
import sqlite3

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_features = [float(x) for x in request.form.values()]
        X = [np.array(input_features)]

        # Temporary prediction logic without model/scaler
        avg_value = np.mean(X)

        if avg_value > 0:
            pred_class = 1
            pred_class_result = "Failed"
            confidence = 0.91
        else:
            pred_class = 0
            pred_class_result = "Not Failed"
            confidence = 0.95

        return render_template(
            "result.html",
            pred_class=pred_class,
            pred_class_result=pred_class_result,
            confidence=confidence
        )

    except Exception as e:
        return render_template(
            "result.html",
            pred_class="Error",
            pred_class_result=str(e),
            confidence=0
        )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = request.form.get('user', '')
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    number = request.form.get('mobile', '')
    password = request.form.get('password', '')

    con = sqlite3.connect('signup.db')
    cur = con.cursor()

    cur.execute("SELECT 1 FROM info WHERE user = ?", (username,))
    if cur.fetchone():
        con.close()
        return render_template("signup.html", message="Username already exists.")

    cur.execute(
        "INSERT INTO info (user, name, email, mobile, password) VALUES (?, ?, ?, ?, ?)",
        (username, name, email, number, password)
    )

    con.commit()
    con.close()

    return render_template("signin.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")

    mail1 = request.form.get('user', '')
    password1 = request.form.get('password', '')

    con = sqlite3.connect('signup.db')
    cur = con.cursor()

    cur.execute(
        "SELECT user, password FROM info WHERE user = ? AND password = ?",
        (mail1, password1)
    )

    data = cur.fetchone()
    con.close()

    if data is None:
        return render_template("signin.html", message="Invalid username or password.")

    return render_template("home.html")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/prediction')
def prediction():
    return render_template('predict.html')


@app.route('/graphs')
def graphs():
    return render_template('graphs.html')


@app.route('/logon')
def logon():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('signin.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)