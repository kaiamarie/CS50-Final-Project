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
    user_id = get_db().execute("SELECT user_id FROM adviser WHERE user_id = ?", (session["user_id"],)).fetchall()

    if len(user_id) != 0:
        session["user_adviser"] = "true"
        return render_template("adviser_home.html")

    else:
        session["user_adviser"] = "false"
        return redirect("/teacher_home")

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
        if rows is None:
            return apology("Sorry, we couldn't find you. To access LessonThread, please register.")

        # Ensure password is correct
        if not check_password_hash(rows["pw_hash"], request.form.get("password")):
            return apology("Sorry, wrong password!")

        # Remember which user has logged in
        session["user_id"] = rows["id"]


        # run a check for adviser
        adviser_check = get_db().execute("SELECT * FROM adviser WHERE user_id = ?",
                            (rows["id"],)).fetchone()

        # set session user type to adviser in order to show the adviser side of the site only
        if not adviser_check is None:
            session["user_adviser"] = "true"
            return redirect('/')

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
            return render_template("adviser_home.html")


        elif request.form.get("user_type") == "teacher":
            get_db().execute("INSERT INTO teacher (user_id, created_at, updated_at) VALUES (?, ?, ?)",
                    (user_id[0][0], datetime, datetime,))
            get_db().commit()
            session["user_teacher"] = "true"
            return redirect("/teacher_home")
        else:
            return apology("Sorry, there was a problem registering you. Please try again.")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session["user_adviser"] = None
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

        get_db().execute("INSERT INTO student (lastname_s, firstname_s, grade, enrollment_date, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (request.form.get("lastname"), request.form.get("firstname"), request.form.get("grade"), request.form.get("enrolldate"), datetime, datetime,))
        get_db().commit()

        return redirect("/enrollstudent")
    else:
        students = get_db().execute("SELECT lastname_s, firstname_s, grade FROM student ORDER BY lastname_s ASC")

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
        students = get_db().execute("SELECT id, lastname_s, firstname_s, grade from student ORDER BY lastname_s ASC").fetchall()
        stclasses = get_db().execute("SELECT class.id, class.class_title, studentClass.teacher_id, studentClass.class_id, studentClass.student_id, user.lastname, user.firstname FROM class INNER JOIN studentClass ON class_id = class.id INNER JOIN user on studentClass.teacher_id = user.id ORDER BY class_title ASC").fetchall()
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

        session["student_id"] = request.form.get("student_id")
        session["class_id"] = request.form.get("class_id")

        return redirect("/student_tracker")

    else:
        datetime = time.asctime(time.localtime(time.time()))

        # assign user id for signed in user
        teacherId = session["user_id"]
        session["user_adviser"] = 'false'


        # get name of teacher for welcome page
        teacher_info = get_db().execute("SELECT firstname, lastname FROM user WHERE id = ?", (teacherId,)).fetchall()


        student_com_grab = get_db().execute("SELECT req_completion_count, class_id, student_id FROM studentClass WHERE teacher_id = ?", (teacherId,)).fetchall()
        class_req_grab = get_db().execute("SELECT req_count, id FROM class").fetchall()
        print(class_req_grab)

        if not class_req_grab == '':
            for student in student_com_grab:
                for classes in class_req_grab:
                    if student["class_id"] == classes["id"]:
                        class_req = classes[0]
                        if class_req != 0:
                            student_com = student[0]
                            percent = (student_com / class_req) * 100

                            get_db().execute("UPDATE studentClass SET com_percent = ?, updated_at = ? WHERE student_id = ? AND class_id = ?", (percent, datetime, student["student_id"], student["class_id"],))
                            get_db().commit()

        # get list of student classes assigned to the teacher who is logged in
        teacher_classes = get_db().execute("SELECT studentClass.com_percent, studentClass.class_id, studentClass.teacher_id, studentClass.student_id, studentClass.req_completion_count, class.class_title, class.req_count, student.firstname_s, student.lastname_s, student.grade FROM studentClass INNER JOIN class ON class.id = studentClass.class_id INNER JOIN student ON student.id = studentClass.student_id").fetchall()

        # get a list of student classes for network of other classes/teachers a teacher's students have
        #network = get_db().execute("SELECT firstname_s, lastname_s FROM student INNER JOIN ")



        return render_template("teacher_home.html", teacher_info = teacher_info, teacher_classes = teacher_classes, teacherId = teacherId)

@app.route("/student_tracker", methods=["GET", "POST"])
@login_required
def student_tracker():
    if request.method == "POST":

        session["student_id"] = request.form.get("student_id")
        session["class_id"] = request.form.get("class_id")

        return redirect("/student_tracker")
        #return render_template("student_tracker.html", student_id = student_id, class_id = class_id)

    else:
        student_id = session["student_id"]
        class_id = session["class_id"]
        datetime = time.asctime(time.localtime(time.time()))

        get_db().execute("UPDATE min_req SET com_tmp = ?, updated_at = ?", ("0", datetime,))
        get_db().commit()

        student_name = get_db().execute("SELECT id, firstname_s, lastname_s FROM student WHERE id = ?", (student_id,)).fetchall()
        class_title = get_db().execute("SELECT class_title FROM class WHERE id = ?", (class_id,)).fetchall()
        min_req = get_db().execute("SELECT id, req_title, req_description FROM min_req WHERE class_id = ?", (class_id,)).fetchall()

        # assign user id for signed in user
        teacherId = session["user_id"]

        # get list of student classes assigned to the teacher who is logged in
        teacher_classes = get_db().execute("SELECT studentClass.class_id, studentClass.teacher_id, studentClass.student_id, studentClass.req_completion_count, class.class_title, class.req_count, student.firstname_s, student.lastname_s, student.grade FROM studentClass INNER JOIN class ON class.id = studentClass.class_id INNER JOIN student ON student.id = studentClass.student_id").fetchall()

        # get information about completed courses
        com_req = get_db().execute("SELECT min_req_id FROM student_com_req WHERE student_id = ?", (student_id,)).fetchall()

        # get assignments
        assignment = get_db().execute("SELECT id, assignment_name, assignment_info, com_tmp, min_req_id FROM assignment WHERE student_id = ?", (student_id,)).fetchall()

        # get progress percentage
        student_com_grab = get_db().execute("SELECT req_completion_count FROM studentClass WHERE student_id = ? AND class_id = ?", (student_id, class_id,)).fetchall()
        student_com = student_com_grab[0][0]

        class_req_grab = get_db().execute("SELECT req_count FROM class WHERE id = ?", (class_id,)).fetchall()
        class_req = class_req_grab[0][0]

        progress = (student_com / class_req) * 100

        for req in min_req:
            for com in com_req:
                if req["id"] == com["min_req_id"]:
                    get_db().execute("UPDATE min_req SET com_tmp = ?, updated_at = ? WHERE id = ?", ("1", datetime, req["id"],))
                    get_db().commit()

        min_req = get_db().execute("SELECT id, req_title, req_description, com_tmp FROM min_req WHERE class_id = ?", (class_id,)).fetchall()

        return render_template("student_tracker.html", progress = progress, assignment = assignment, com_req = com_req, min_req = min_req, class_title = class_title, student_name = student_name, teacherId = teacherId, teacher_classes = teacher_classes, student_id = student_id, class_id = class_id)

@app.route("/student_req", methods=["POST"])
@login_required
def student_req():
    datetime = time.asctime(time.localtime(time.time()))
    min_req_id = request.form.get("req_id")
    student_id = session["student_id"]
    class_id = session["class_id"]

    get_db().execute("INSERT INTO student_com_req (min_req_id, student_id, created_at, updated_at) VALUES (?, ?, ?, ?)", (min_req_id, student_id, datetime, datetime,))
    get_db().commit()

    # get old count of completed number to add to it
    com_count = get_db().execute("SELECT req_completion_count FROM studentClass WHERE student_id = ? AND class_id = ?", (student_id, class_id,)).fetchall()
    new_count = com_count[0][0] + 1

    # adjust new count in studentClass
    get_db().execute("UPDATE studentClass SET req_completion_count = ?, updated_at = ? WHERE student_id = ? AND class_id = ?", (new_count, datetime, student_id, class_id,))
    get_db().commit()

    return redirect("/student_tracker")

@app.route("/undo_req", methods=["POST"])
@login_required
def undo_req():
    datetime = time.asctime(time.localtime(time.time()))
    min_req_id = request.form.get("req_id")
    student_id = session["student_id"]
    class_id = session["class_id"]

    get_db().execute("DELETE FROM student_com_req WHERE min_req_id = ? AND student_id = ?", (min_req_id, student_id,))
    get_db().commit()

    # get old count of completed number to add to it
    com_count = get_db().execute("SELECT req_completion_count FROM studentClass WHERE student_id = ? AND class_id = ?", (student_id, class_id,)).fetchall()
    new_count = com_count[0][0] - 1

    # adjust new count in studentClass
    get_db().execute("UPDATE studentClass SET req_completion_count = ?, updated_at = ? WHERE student_id = ? AND class_id = ?", (new_count, datetime, student_id, class_id,))
    get_db().commit()

    return redirect("/student_tracker")

@app.route("/assignment_add", methods=["POST"])
@login_required
def assignment_add():
    datetime = time.asctime(time.localtime(time.time()))
    min_req_id = request.form.get("req_id")
    assignment_name = request.form.get("assignment_name")
    assignment_info = request.form.get("assignment_info")
    student_id = session["student_id"]
    class_id = session["class_id"]

    get_db().execute("INSERT INTO assignment (min_req_id, assignment_name, assignment_info, student_id, created_at, updated_at, com_tmp) VALUES (?, ?, ?, ?, ?, ?, ?)", (min_req_id, assignment_name, assignment_info, student_id, datetime, datetime, "0",))
    get_db().commit()

    return redirect("/student_tracker")

@app.route("/com_assignment", methods=["POST"])
@login_required
def com_assignment():
    datetime = time.asctime(time.localtime(time.time()))
    assignment_id = request.form.get("assignment_id")

    get_db().execute("UPDATE assignment SET com_tmp = ?, updated_at = ? WHERE id =?", (1, datetime, assignment_id,))
    get_db().commit()

    return redirect("/student_tracker")

@app.route("/undo_assignment", methods=["POST"])
@login_required
def undo_assignment():
    datetime = time.asctime(time.localtime(time.time()))
    assignment_id = request.form.get("assignment_id")

    get_db().execute("UPDATE assignment SET com_tmp = ?, updated_at = ? WHERE id =?", (0, datetime, assignment_id,))
    get_db().commit()

    return redirect("/student_tracker")
