import os
import psycopg2
from flask import Flask, render_template, session, redirect, request, url_for
app = Flask(__name__)

"""
.. module:: app
   :platform: Unix, Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Alex Henryz


"""

@app.before_first_request
def before_first_request():
    """
    Handles everything that is needed before the site is rendered.
    """
    session['lang'] = "swe"
    session['loggedIn'] = False
    session['currentUser'] = None

@app.route('/switch', methods=['POST'])
def language_switch():
    """ 
    Handles the language switching by changing the session['lang'] to other language

    """

    if session['lang'] == "swe":
        session['lang'] = "eng"
    elif session['lang'] == "eng":
        session['lang'] = "swe"
    return redirect("/")

@app.route('/')
def home():
    """
    Renders the initial index page.
    """
    return render_template('index_{}.html'.format(session['lang']))

@app.route('/search', methods=['POST'])
def search():
    """
    Handles the searches in the application.
    """
    try:
        cur.execute("SELECT username, created_on FROM users WHERE username LIKE '{}'".format(request.form['searchbar']))
        data = cur.fetchall()
        print(request.form['searchbar'])
        return render_template("index_{}.html".format(session['lang']), data=data)
    except:
        return redirect('/')

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    """
    GET and POST for both the website rendering and the form submission.
    """
    if request.method == 'POST':
        comment = request.form['comment']
        command = "INSERT INTO comments (username, comment, title) VALUES ('{0}', '{1}', '{2}')".format(session['currentUser'], comment, request.form['title'])
        cur.execute(command)
        return redirect('/comments')
    elif request.method == 'GET':
        return render_template('comment_{}.html'.format(session['lang']))

@app.route('/comments')
def comments():
    """
    Displays all comments that have been made.
    """
    cur.execute("SELECT * FROM comments")
    comments = cur.fetchall()
    return render_template("comments_{}.html".format(session['lang']), comments=comments)

@app.route('/deletecomment', methods=['POST'])
def deleteComment():
    """
    Deletes specific comment.
    """
    cur.execute("DELETE FROM comments WHERE id={}".format(request.form['id']))
    return redirect('/comments')

@app.route('/register', methods=["GET", "POST"])
def register():
    """
    Allows a user to register an account.
    """
    if request.method == 'POST':
        command = "INSERT INTO users (username, password, created_on) VALUES ('{0}', '{1}', CURRENT_TIMESTAMP)".format(request.form['username'], request.form['password'])
        cur.execute(command)
        return redirect('/')
    elif request.method == 'GET':
        return render_template('register_{}.html'.format(session['lang']))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Allows a known user to login.
    This also starts a session with the current logged in user.
    """
    if request.method == 'POST':
        try:
            cur.execute("SELECT * FROM users WHERE username='{}'".format(request.form['username']))
            username = cur.fetchone()
            print(username)
            if username[1] == request.form['username'] and username[2] == request.form['password']:
                session['loggedIn'] = True
                session['currentUser'] = username[1]
                print("Logged in!")
        except:
            return redirect('/login')
        return redirect('/')
    elif request.method == 'GET':
        return render_template('login_{}.html'.format(session['lang']))

@app.route('/logout', methods=['POST'])
def logout():
    """
    Allows a logged in user to logout.
    """
    session.pop('currentUser', None)
    session.pop('loggedIn', False)
    return redirect('/')

if __name__ == '__main__':
    conn = psycopg2.connect(host="localhost",database="slutspurt", user="postgres", password="docker")
    conn.autocommit = True
    cur = conn.cursor()
    app.secret_key = os.urandom(24)
    app.run()