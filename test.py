from flask import Flask, render_template, request
app = Flask(__name__, static_folder='static')


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")
