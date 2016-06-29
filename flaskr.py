# -*- coding:utf-8 -*-


import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing


app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#
# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().execute(f.read())
#         db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    g.db.close()


@app.route('/post', methods=['GET'])
def post():
    return render_template('add.html')


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        g.db.execute('insert into entries (title, text) VALUES (?, ?)', [request.form['title'], request.form['text']])
        g.db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))
    else:
        return redirect(url_for('show_entries'))


@app.route('/show_entries')
def show_entries():
    cur = g.db.execute('select title, text from entries ORDER BY id DESC ')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'wrong username or passwd'
        else:
            session['logged_in'] = True
            flash('you have logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('logout sucess')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(debug=True)


