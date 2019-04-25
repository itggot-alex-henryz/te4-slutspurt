import os
import psycopg2
from flask import Flask, render_template, session, redirect, request
app = Flask(__name__)

conn = psycopg2.connect(host="localhost",database="fruitdb", user="postgres", password="docker")
cur = conn.cursor()

@app.before_first_request
def before_first_request():
    session['lang'] = "swe"

@app.route('/switch', methods=['POST'])
def language_switch():
    if session['lang'] == "swe":
        session['lang'] = "eng"
    elif session['lang'] == "eng":
        session['lang'] = "swe"
    return redirect("/")

@app.route('/')
def index():
    return render_template("index_{}.html".format(session['lang']))

@app.route('/fruits')
def fruits():
    cur.execute("SELECT * FROM fruits")
    fruitlist = cur.fetchall()
    return render_template("fruits_{}.html".format(session['lang']), fruits=fruitlist)

@app.route('/fruit/<name>')
def fruit(name=None):
    cur.execute("SELECT * FROM fruits WHERE name='{}'".format(name))
    fruitdata = cur.fetchone()
    print(fruitdata)
    return  render_template("fruit_{}.html".format(session['lang']), fruit=fruitdata)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()