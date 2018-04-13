<<<<<<< HEAD
from flask import Flask, render_template
=======
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, _app_ctx_stack

>>>>>>> 784463ccf5a927f66938a1239513f65cd6f6e357
app = Flask(__name__)
app.config['DATABASE'] = 'tmp/application.db'

def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    if not os.path.exists('tmp/application.db'):
        os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok = True)
    init_db()
    print('Initialized the database')

@app.route('/')
<<<<<<< HEAD
def studentClass():
    return render_template("studentClass.html")
=======
def index():
    return 'Hello, World!'
>>>>>>> 784463ccf5a927f66938a1239513f65cd6f6e357
