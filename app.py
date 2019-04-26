import os
import psycopg2
from flask import Flask, render_template, session, redirect, request, url_for
app = Flask(__name__)

conn = psycopg2.connect(host="localhost",database="slutspurt", user="postgres", password="docker")
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
def home():
    return render_template('index_{}.html'.format(session['lang']))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('/')
    elif request.method == 'GET':
        return render_template('login_{}.html'.format(session['lang']))

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()