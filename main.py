import sqlite3
from flask import Flask, render_template, request, redirect, g, flash, abort
from contextlib import closing

app = Flask(__name__, static_url_path='/static')

DATABASE = 'flask.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    cur = c.execute("SELECT id, title, text FROM entries ORDER BY ID DESC LIMIT 10")
    entries = [dict(id=row[0], title=row[1], text=row[2]) for row in cur.fetchall()]
    return render_template('index.html', entries=entries)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/login/', methods=['POST', 'GET'])
def login():
    user = request.form.get('username')
    password = request.form.get('password')
    if user == 'ali' and password == 'admin':
        return redirect('/manager', code=302)
    elif not user == 'ali' and not password == 'admin':
        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/manager/', methods=['POST', 'GET'])
def manager():
    try:
        pidd = request.form.get('pidd')
        t = request.form.get('title')
        p = request.form.get('post')
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        rows = [pidd, t, p]
        c.execute("INSERT INTO entries (id, title, text) values (?,?,?)", (pidd, t, p))
        conn.commit()
        flash('New entry was successfully posted')
        conn.close()
        return render_template('manager.html')
    except:
        return render_template('manager.html')

@app.route('/posts/')
def posts():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    cur = c.execute("SELECT id, title, text FROM entries ORDER BY ID DESC LIMIT 10")
    entries = [dict(id=row[0], title=row[1], text=row[2]) for row in cur.fetchall()]
    return render_template('posts.html', entries=entries)

@app.route('/posts/<int:post_id>')
def post_list(post_id=None):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    cur = c.execute("SELECT id, title, text FROM entries WHERE ID=%s"%post_id)
    entries = [dict(id=row[0], title=row[1], text=row[2]) for row in cur.fetchall()]
    return render_template('post_list.html', entries=entries)

@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


app.run(port=80, use_reloader=True, debug=True)

