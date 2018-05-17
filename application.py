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
    if session["user_adviser"] == "true":
        return redirect("/adviser_home")

    else:
        return redirect("/teacher_home")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    session["user_adviser"] = 'false'
    session["user_teacher"] = 'false'

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = get_db().execute("SELECT * FROM user WHERE username = ?",
                          (request.form.get("username"),)).fetchone()

        # Ensure username is registered
        if rows is None:
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
            return redirect("/teacher_home")

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
        get_db().execute("INSERT INTO user (email, username, pw_hash, created_at, updated_at, firstname, lastname) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (request.form.get("email"), request.form.get("username"), passwordhash, datetime, datetime, request.form.get("firstname"), request.form.get("lastname"),))
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
            session["user_adviser"] = "true"
            print("adviser check")
            return render_template("adviser_home.html")


        elif request.form.get("user_type") == "teacher":
            get_db().execute("INSERT INTO teacher (user_id, created_at, updated_at) VALUES (?, ?, ?)",
                    (user_id[0][0], datetime, datetime,))
            get_db().commit()
            session["user_teacher"] = "true"
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
@login_required
def addclass():
    if request.method == "POST":
        datetime = time.asctime(time.localtime(time.time()))

        get_db().execute("INSERT INTO class (class_title, department, credits, created_at, updated_at, req_count) VALUES (?, ?, ?, ?, ?, ?)",
                   (request.form.get("classtitle"), request.form.get("department"), request.form.get("credit"), datetime, datetime, 0,))
        get_db().commit()

        return redirect("/addclass")
    else:
        # get classes for the side list
        flclasses = get_db().execute("SELECT class_title FROM class WHERE department = ? ORDER BY class_title ASC", ("foreignlanguage",)).fetchall()
        humclasses = get_db().execute("SELECT class_title FROM class WHERE department = ?  ORDER BY class_title ASC", ("humanities",)).fetchall()
        mathclasses = get_db().execute("SELECT class_title FROM class WHERE department = ?  ORDER BY class_title ASC", ("math",)).fetchall()
        sciclasses = get_db().execute("SELECT class_title FROM class WHERE department = ?  ORDER BY class_title ASC", ("science",)).fetchall()
        ssclasses = get_db().execute("SELECT class_title FROM class WHERE department = ?  ORDER BY class_title ASC", ("socialstudies",)).fetchall()
        techclasses = get_db().execute("SELECT class_title FROM class WHERE department = ?  ORDER BY class_title ASC", ("technology",)).fetchall()

        return render_template("addclass.html", flclasses=flclasses, humclasses=humclasses, mathclasses=mathclasses, sciclasses=sciclasses, ssclasses=ssclasses, techclasses=techclasses)

@app.route("/deleteclass", methods=["GET", "POST"])
@login_required
def deleteclass():
    if request.method == "POST":

        get_db().execute("DELETE FROM class WHERE class_title = ?",
                   (request.form.get("classtitle"),))
        get_db().commit()

        return redirect("/deleteclass")
    else:
        # get classes for the side list
        flclasses = get_db().execute("SELECT class_title FROM class WHERE department = ? ORDER BY class_title ASC", ("foreignlanguage",)).fetchall()
        humclasses = get_db().execute("SELECT class_title FROM class WHERE department = ?  ORDER BY class_title ASC", ("humanities",)).fetchall()
        mathclasses = get_db().execute("SELECT class_title FROM class WHERE department = ?  ORDER BY class_title ASC", ("math",)).fetchall()
        sciclasses = get_db().execute("SELECT class_title FROM class WHERE department = ?  ORDER BY class_title ASC", ("science",)).fetchall()
        ssclasses = get_db().execute("SELECT class_title FROM class WHERE department = ?  ORDER BY class_title ASC", ("socialstudies",)).fetchall()
        techclasses = get_db().execute("SELECT class_title FROM class WHERE department = ?  ORDER BY class_title ASC", ("technology",)).fetchall()


        classes = get_db().execute("SELECT class_title FROM class").fetchall()

        return render_template("deleteclass.html", classes=classes, flclasses=flclasses, humclasses=humclasses, mathclasses=mathclasses, sciclasses=sciclasses, ssclasses=ssclasses, techclasses=techclasses)

@app.route("/enrollstudent", methods=["GET", "POST"])
@login_required
def enrollstudent():
    if request.method == "POST":
        datetime = time.asctime(time.localtime(time.time()))

        get_db().execute("INSERT INTO student (lastname, firstname, grade, enrollment_date, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (request.form.get("lastname"), request.form.get("firstname"), request.form.get("grade"), request.form.get("enrolldate"), datetime, datetime,))
        get_db().commit()

        return redirect("/enrollstudent")
    else:
        students = get_db().execute("SELECT lastname, firstname, grade FROM student ORDER BY lastname ASC")

        return render_template("enrollstudent.html", students=students)

@app.route("/assignclass", methods=["GET", "POST"])
@login_required
def assignclass():
    if request.method == "POST":
        datetime = time.asctime(time.localtime(time.time()))

        get_db().execute("INSERT INTO studentClass (student_id, class_id, teacher_id, hours_purchased, start_date, end_date, created_at, updated_at, req_completion_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (request.form.get("studentname"), request.form.get("class"), request.form.get("teacher"), request.form.get("hours"), request.form.get("startdate"), request.form.get("enddate"), datetime, datetime, 0,))
        get_db().commit()

        return redirect("/assignclass")
    else:
        students = get_db().execute("SELECT id, lastname, firstname, grade from student ORDER BY lastname ASC").fetchall()
        stclasses = get_db().execute("SELECT class.id, class.class_title, studentClass.teacher_id, studentClass.class_id, studentClass.student_id FROM class  INNER JOIN studentClass ON class_id=class.id ORDER BY class_title ASC").fetchall()
        classes = get_db().execute("SELECT id, class_title FROM class ORDER BY class_title ASC").fetchall()
        teachers = get_db().execute("SELECT user_id, firstname, lastname, user.id FROM teacher INNER JOIN user ON user.id=teacher.user_id").fetchall()
        return render_template("assignclass.html", students=students, classes=classes, teachers=teachers, stclasses=stclasses)

@app.route("/requirements", methods=["GET", "POST"])
@login_required
def requirements():
    if request.method == "POST":
        datetime = time.asctime(time.localtime(time.time()))

        # get the id of the class selected
        class_id = get_db().execute("SELECT id FROM class WHERE class_title = ?", (request.form.get("class_title"),)).fetchall()

        # update req_count
        req_grab = get_db().execute("SELECT req_count FROM class WHERE class_title = ?", (request.form.get("class_title"),)).fetchall()

        if req_grab[0][0] is None:
            req_count = 1
        else:
            req_count = req_grab[0][0] + 1

        get_db().execute("UPDATE class SET req_count = ? WHERE class_title = ?", (req_count, request.form.get("class_title"),))
        get_db().commit()

        # enter the new requirements into the min_req table
        get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                    (class_id[0][0], request.form.get("new_req_title"), request.form.get("new_req_body"), datetime, datetime,))
        get_db().commit()

        return redirect("/requirements")
    else:
        # get classes for the side list
        flclasses = get_db().execute("SELECT class_title, id FROM class WHERE department = ? ORDER BY class_title ASC", ("foreignlanguage",)).fetchall()
        humclasses = get_db().execute("SELECT class_title, id FROM class WHERE department = ?  ORDER BY class_title ASC", ("humanities",)).fetchall()
        mathclasses = get_db().execute("SELECT class_title, id FROM class WHERE department = ?  ORDER BY class_title ASC", ("math",)).fetchall()
        sciclasses = get_db().execute("SELECT class_title, id FROM class WHERE department = ?  ORDER BY class_title ASC", ("science",)).fetchall()
        ssclasses = get_db().execute("SELECT class_title, id FROM class WHERE department = ?  ORDER BY class_title ASC", ("socialstudies",)).fetchall()
        techclasses = get_db().execute("SELECT class_title, id FROM class WHERE department = ?  ORDER BY class_title ASC", ("technology",)).fetchall()

        classes = get_db().execute("SELECT class_title FROM class").fetchall()

        # get min reqs to populate req lists in new_req_body
        min_req = get_db().execute("SELECT class_id, req_title, req_description FROM min_req ORDER BY req_title ASC").fetchall()

        return render_template("requirements.html", min_req=min_req, classes=classes, flclasses=flclasses, humclasses=humclasses, mathclasses=mathclasses, sciclasses=sciclasses, ssclasses=ssclasses, techclasses=techclasses)

@app.route("/teacher_home", methods=["GET", "POST"])
@login_required
def teacher_home():
    if request.method == "POST":

        student_id = request.form.get("student_id")
        class_id = request.form.get("class_id")

        return render_template("student_tracker.html", student_id = student_id, class_id = class_id)

    else:
        # assign user id for signed in user
        teacherId = session["user_id"]

        # get list of student classes assigned to the teacher who is logged in
        teacher_classes = get_db().execute("SELECT studentClass.class_id, studentClass.teacher_id, studentClass.student_id, studentClass.req_completion_count, class.class_title, class.req_count, student.firstname, student.lastname, student.grade FROM studentClass INNER JOIN class ON class.id = studentClass.class_id INNER JOIN student ON student.id = studentClass.student_id").fetchall()

        # get name of teacher for welcome page
        teacher_info = get_db().execute("SELECT firstname, lastname FROM user WHERE id = ?", (teacherId,)).fetchall()



        return render_template("teacher_home.html", teacher_info = teacher_info, teacher_classes = teacher_classes, teacherId = teacherId)

@app.route("/student_tracker", methods=["GET", "POST"])
@login_required
def student_tracker():
    if request.method == "POST":

        student_id = request.form.get("student_id")
        class_id = request.form.get("class_id")

        print(student_id)
        print(class_id)

        return render_template("student_tracker.html", student_id = student_id, class_id = class_id)

    else:

        return render_template("student_tracker", student_id = student_id, class_id = class_id)
