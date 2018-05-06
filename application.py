from flask import Flask, render_template, session
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, _app_ctx_stack
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology
import time

app = Flask(__name__)
app.config['DATABASE'] = 'tmp/application.db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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

@app.route("/")
@login_required
def index():
    return render_template("adviser_home.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = get_db().execute("SELECT * FROM user WHERE username = ?",
                          (request.form.get("username"),)).fetchone()

        # Ensure username is registered
        if len(rows) == 0:
            return apology("Sorry, we couldn't find you. To access LessonThread, please register.")

        # Ensure password is correct
        if not check_password_hash(rows["pw_hash"], request.form.get("password")):
            return apology("Sorry, wrong password!")

        # Remember which user has logged in
        session["user_id"] = rows["id"]
        print(session["user_id"])

        # run a check for adviser
        adviser_check = get_db().execute("SELECT * FROM adviser WHERE user_id = ?",
                            (rows["id"],)).fetchone()

        # set session user type to adviser in order to show the adviser side of the site only
        if not adviser_check is None:
            session["user_adviser"] = "true"
            return render_template("adviser_home.html")

        # run a check for teacher
        teacher_check = get_db().execute("SELECT * FROM teacher WHERE user_id = ?",
                            (rows["id"],)).fetchone()

        # session["user_type"] = "teacher"
        if not teacher_check is None:
            session["user_teacher"] = "true"
            return render_template("teacher_home.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        datetime = time.asctime(time.localtime(time.time()))

        # ensure username was unique
        emailcheck = get_db().execute("SELECT * FROM user WHERE email = ?",
                        (request.form.get("email"),)).fetchall()

        if len(emailcheck) > 0:
            print("its the emailcheck apology!")
            return apology("Email entered already registered")

        # ensure username was unique
        rows = get_db().execute("SELECT * FROM user WHERE username = ?",
                        (request.form.get("username"),)).fetchall()

        if len(rows) > 0:
            return apology("Username already registered")

        # save password
        passwordhash = generate_password_hash(request.form.get("password"))

        # Insert username and hash of password into database (and auotgened ID)
        get_db().execute("INSERT INTO user (email, username, pw_hash, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                   (request.form.get("email"), request.form.get("username"), passwordhash, datetime, datetime,))
        get_db().commit()

        # add adviser/teacher information
        user_id = get_db().execute("SELECT id FROM user WHERE username = ?", (request.form.get("username"),)).fetchall()

        # log them on
        rows = get_db().execute("SELECT * FROM user WHERE username = ?", (request.form.get("username"),)).fetchall()
        session["user_id"] = rows[0]["id"]

        newuser = get_db().execute("SELECT * FROM user WHERE username = ?", (request.form.get("username"),)).fetchall()

        # register advisers
        if request.form.get("user_type") == "adviser":
            get_db().execute("INSERT INTO adviser (user_id, created_at, updated_at) VALUES (?, ?, ?)",
                    (user_id[0][0], datetime, datetime,))
            get_db().commit()
            session["user_type"] = "adviser"
            print("adviser check")
            return render_template("adviser_home.html")


        elif request.form.get("user_type") == "teacher":
            get_db().execute("INSERT INTO teacher (user_id, created_at, updated_at) VALUES (?, ?, ?)",
                    (user_id[0][0], datetime, datetime,))
            get_db().commit()
            session["user_type"] = "teacher"
            print("teacher check")
            return render_template("teacher_home.html")
        else:
            return apology("Sorry, there was a problem registering you. Please try again.")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/addclass", methods=["GET", "POST"])
def addclass():
    if request.method == "POST":


    else:
        return render_template("addclass.html")
