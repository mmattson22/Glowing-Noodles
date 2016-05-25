from flask import Flask, render_template, session, request
from flask import redirect, url_for

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def home():
    return render_template("home.html")

@app.route('/about', methods = ['GET','POST'])
def about():
    return render_template("about.html")

@app.route('/found', methods = ['GET','POST'])
def found():
    return render_template("found.html")


if __name__ == '__main__':
        app.secret_key = "hello"
        app.debug = True
        app.threaded = True
        app.run(host='0.0.0.0', port=8000)
else:
        app.secret_key = "hello"
        app.debug = True
