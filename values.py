from werkzeug.security import check_password_hash, generate_password_hash
import time
import datetime

def values():
    datetime = time.asctime(time.localtime(time.time()))
    passwordhash = generate_password_hash("check")

    # make 1 admin
    get_db().execute("INSERT INTO user (email, username, pw_hash, created_at, updated_at, firstname, lastname) VALUES (?, ?, ?, ?, ?, ?, ?)",
               ("admin@test.com", "admin", passwordhash, datetime, datetime, "Ada", "Anderson",))
    get_db().commit()

    get_db().execute("INSERT INTO adviser (user_id, created_at, updated_at) VALUES (?, ?, ?)",
                ("1", datetime, datetime,))
    get_db().commit()

    # make 3 teachers

    # teacher 1
    get_db().execute("INSERT INTO user (email, username, pw_hash, created_at, updated_at, firstname, lastname) VALUES (?, ?, ?, ?, ?, ?, ?)",
               ("teacher1@test.com", "teacher1", passwordhash, datetime, datetime, "Brett", "Bjornstad",))
    get_db().commit()

    get_db().execute("INSERT INTO teacher (user_id, created_at, updated_at) VALUES (?, ?, ?)",
                ("2", datetime, datetime,))
    get_db().commit()

    # teacher 2
    get_db().execute("INSERT INTO user (email, username, pw_hash, created_at, updated_at, firstname, lastname) VALUES (?, ?, ?, ?, ?, ?, ?)",
               ("teacher2@test.com", "teacher2", passwordhash, datetime, datetime, "Cathy", "Carson",))
    get_db().commit()

    get_db().execute("INSERT INTO teacher (user_id, created_at, updated_at) VALUES (?, ?, ?)",
                ("3", datetime, datetime,))
    get_db().commit()

    # teacher 3
    get_db().execute("INSERT INTO user (email, username, pw_hash, created_at, updated_at, firstname, lastname) VALUES (?, ?, ?, ?, ?, ?, ?)",
               ("teacher3@test.com", "teacher3", passwordhash, datetime, datetime, "Dan", "Dunder",))
    get_db().commit()

    get_db().execute("INSERT INTO teacher (user_id, created_at, updated_at) VALUES (?, ?, ?)",
                ("3", datetime, datetime,))
    get_db().commit()


    # Make students
    # Student 1
    get_db().execute("INSERT INTO student (firstname_s, lastname_s, grade, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               ("Adam", "Aarons", 12, datetime, datetime,))
    get_db().commit()

    # Student 2
    get_db().execute("INSERT INTO student (firstname_s, lastname_s, grade, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               ("Bionca", "Byron", 11, datetime, datetime,))
    get_db().commit()

    # Student 3
    get_db().execute("INSERT INTO student (firstname_s, lastname_s, grade, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               ("Carl", "Campbell", 10, datetime, datetime,))
    get_db().commit()


    # Create classes

    # Humanities
    get_db().execute("INSERT INTO class (class_title, credit, req_count, department, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
               ("English", 1 , 3, "humanities", datetime, datetime,))
    get_db().commit()
    # Science
    get_db().execute("INSERT INTO class (class_title, credit, req_count, department, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
               ("Biology", 1 , 3, "science", datetime, datetime,))
    get_db().commit()
    # Math
    get_db().execute("INSERT INTO class (class_title, credit, req_count, department, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
               ("Algebra 1", 1 , 3, "math", datetime, datetime,))
    get_db().commit()
    # Foreign language
    get_db().execute("INSERT INTO class (class_title, credit, req_count, department, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
               ("Spanish 1", 1 , 3, "foreignlanguage", datetime, datetime,))
    get_db().commit()
    # Technology
    get_db().execute("INSERT INTO class (class_title, credit, req_count, department, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
               ("Design Thinking", 1 , 3, "technology", datetime, datetime,))
    get_db().commit()
    # Social Studies
    get_db().execute("INSERT INTO class (class_title, credit, req_count, department, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
               ("American History", 1 , 3, "socialstudies", datetime, datetime,))
    get_db().commit()


    #Minimum Requirements

    # English
    # 1
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (1, "Research Paper", "Write at least one research paper in MLA format.", datetime, datetime,))
    get_db().commit()
    # 2
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (1, "Shakespeare", "Read any Shakespeare play with appropriate scaffolding.", datetime, datetime,))
    get_db().commit()
    # 3
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (1, "Poetry", "Read and analyze a selection of poetry from different eras and cultures.", datetime, datetime,))
    get_db().commit()

    # Biology
    # 1
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (2, "Cells", "Investigate the function and anatomy of cells.", datetime, datetime,))
    get_db().commit()
    # 2
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (2, "Energy Cycles", "Understand how energy cycles through living things and the sun.", datetime, datetime,))
    get_db().commit()
    # 3
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (2, "Evolution", "Understand the theory of evolution and how it pertains to the evolution of humans", datetime, datetime,))
    get_db().commit()

    # Algebra
    # 1
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (3, "Graphing", "Graph linear equations, mastering slope and intercepts.", datetime, datetime,))
    get_db().commit()
    # 2
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (3, "Systems of Equations", "Solve systems of equations with two and three variables.", datetime, datetime,))
    get_db().commit()
    # 3
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (3, "Factor", "Capably factor common quadratic equations.", datetime, datetime,))
    get_db().commit()

    # Spanish
    # 1
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (4, "Greetings", "Be able to greet the teacher and fellow students.", datetime, datetime,))
    get_db().commit()
    # 2
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (4, "Counting", "Count to a hundred.", datetime, datetime,))
    get_db().commit()
    # 3
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (4, "Ordering at a Resturaunt", "Carry on a short conversation with a waiter to order food.", datetime, datetime,))
    get_db().commit()

    # Design Thinking
    # 1
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (5, "Design Principles", "Master all five design principles.", datetime, datetime,))
    get_db().commit()
    # 2
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (5, "Community Project", "Design and implement something for the community.", datetime, datetime,))
    get_db().commit()
    # 3
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (5, "Independent Project", "Design a project independently from beginning to end.", datetime, datetime,))
    get_db().commit()

    # Am History
    # 1
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (6, "American Revolution", "Understand the events and objectives of the Revolution.", datetime, datetime,))
    get_db().commit()
    # 2
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (6, "Civil War", "Understand the causes and effects of the Civil War.", datetime, datetime,))
    get_db().commit()
    # 3
    get_db().execute("INSERT INTO min_req (class_id, req_title, req_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (6, "Age of Terror", "Understand the events of the Age of Terror and its effect upon the modern world.", datetime, datetime,))
    get_db().commit()


    # Student classes

    # Student 1
    get_db().execute("INSERT INTO studentClass (student_id, class_id, teacher_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (1, 1, 1, datetime, datetime,))
    get_db().commit()

    get_db().execute("INSERT INTO studentClass (student_id, class_id, teacher_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (1, 2, 2, datetime, datetime,))
    get_db().commit()

    get_db().execute("INSERT INTO studentClass (student_id, class_id, teacher_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (1, 3, 3, datetime, datetime,))
    get_db().commit()

    # Student 2
    get_db().execute("INSERT INTO studentClass (student_id, class_id, teacher_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (2, 4, 1, datetime, datetime,))
    get_db().commit()

    get_db().execute("INSERT INTO studentClass (student_id, class_id, teacher_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (2, 5, 2, datetime, datetime,))
    get_db().commit()

    get_db().execute("INSERT INTO studentClass (student_id, class_id, teacher_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (2, 6, 3, datetime, datetime,))
    get_db().commit()

    # Student 3
    get_db().execute("INSERT INTO studentClass (student_id, class_id, teacher_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (3, 1, 1, datetime, datetime,))
    get_db().commit()

    get_db().execute("INSERT INTO studentClass (student_id, class_id, teacher_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (3, 3, 2, datetime, datetime,))
    get_db().commit()

    get_db().execute("INSERT INTO studentClass (student_id, class_id, teacher_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
               (3, 6, 3, datetime, datetime,))
    get_db().commit()
