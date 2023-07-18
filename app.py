from flask import Flask, render_template, url_for, request, g, redirect, session
from database import connect_to_DB, getDatabase
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import csv
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.teardown_appcontext
def close_database(error):
    if hasattr(g, "app_database_db"):
        g.app_database_db.close()

def get_current_user():
    user_result = None
    if 'user' in session:
        user = session['user']
        db = getDatabase()
        
        # Check in "students" table
        student_cursor = db.execute("SELECT * FROM students WHERE name = ?", [user])
        student_result = student_cursor.fetchone()
        if student_result:
            user_result = student_result
        else:
            # Check in "users" table
            user_cursor = db.execute("SELECT * FROM users WHERE name = ?", [user])
            user_result = user_cursor.fetchone()
    return user_result


@app.route("/")
def index():
    user = get_current_user()
    return render_template("index.html", user = user)

@app.route("/dashboard")
def dashboard():
    user = get_current_user()
    return render_template("dashboard.html", user = user)

@app.route("/login", methods = ["POST", "GET"])
def login():
    user = get_current_user()
    error = None
    if request.method == "POST":
        name = request.form['username']
        password = request.form['password']
        
        db = getDatabase()
        users_cursor = db.execute("SELECT * FROM users WHERE name = ?", [name])
        dbuser = users_cursor.fetchone()
                
        if not dbuser:
            students_cursor = db.execute("SELECT * FROM students WHERE name = ?", [name])
            dbuser = students_cursor.fetchone()
        
        if dbuser:
            if check_password_hash(dbuser['password'], password):
                session['user'] = dbuser['name']
                return redirect(url_for('dashboard'))
            else:
                error = "Incorrect username or password"
                return render_template("login.html", error = error)
        else:
                error = "Incorrect username or password"
                return render_template("login.html", error = error)
    return render_template("login.html", user = user, error = error)

@app.route("/register", methods = ["POST", "GET"])
def register():
    user = get_current_user()
    if request.method == "POST":
        if 'role' not in request.form:
            error = "Please select a role"
            return render_template("register.html", user = user, error=error)
        
        db = getDatabase()
        name = request.form['username']
        password = request.form['password']
        role = request.form['role']
        fullname = request.form['fullname']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password or password == "":
            error = "Password not thesame"
            return render_template("register.html", user = user, error = error)
        
        user_fetching_cursor = db.execute("SELECT * FROM users WHERE name = ? UNION SELECT * FROM students WHERE name = ?", [name, name])
        existing_user = user_fetching_cursor.fetchone()
        if existing_user or name == "":
            error = "Username already taken"
            return render_template("register.html", user = user, error = error)
        
        hashed_pass = generate_password_hash(password, method='sha256')
        db.execute("insert into users (name, fullname, password, role) values (?,?,?,?)",
                   [name, fullname, hashed_pass, role])
        db.commit()
        
        if True:
            msg = "New " + role + " added Successfully"
            return render_template("register.html", user = user, error = msg)    
    return render_template("register.html", user = user)

@app.route("/register_student", methods = ["POST", "GET"])
def register_student():
    user = get_current_user()
    if request.method == "POST":
        if 'klass' not in request.form:
            error = "Please select a class"
            return render_template("register_student.html", user = user, error=error,)
        
        db = getDatabase()
        name = request.form['username']
        password = request.form['password']
        klass = request.form['klass']
        fullname = request.form['fullname']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password or password == "":
            error = "Password not thesame"
            return render_template("register_student.html", user = user, error = error)
        
        user_fetching_cursor = db.execute("SELECT * FROM users WHERE name = ? UNION SELECT * FROM students WHERE name = ?", [name, name])
        existing_user = user_fetching_cursor.fetchone()
        if existing_user or name == "":
            error = "Username already taken"
            return render_template("register_student.html", user = user, error = error)
              
        hashed_pass = generate_password_hash(password, method='sha256')
        db.execute("insert into students (name, fullname, password, klass) values (?,?,?,?)",
                   [name, fullname, hashed_pass, klass])
        db.commit()
        
        if True:
            msg = "Student added Successfully"
            return render_template("register_student.html", user = user, error = msg)
    return render_template("register_student.html", user = user)

@app.route("/resetpassword", methods=['GET','POST'])
def resetpassword():
    user = get_current_user()
    if request.method == "POST":
        db = getDatabase()
        name = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password or password == "":
            error = "Password not thesame"
            return render_template("resetpassword.html", user = user, error = error)
        
        users_cursor = db.execute("SELECT * FROM users WHERE name = ?", [name])
        dbuser = users_cursor.fetchone()
        
        if not dbuser:
            students_cursor = db.execute("SELECT * FROM students WHERE name = ?", [name])
            db_students = students_cursor.fetchone()
        
        if dbuser and name != "":
            hashed_pass = generate_password_hash(password, method='sha256')
            db.execute("UPDATE users set password = ? where name = ?", [hashed_pass, name])
            db.commit()        
            msg = "Users password was sucessfully changed."
            return render_template('resetpassword.html', user = user, error = msg)
        
        elif db_students and name != "":
            hashed_pass = generate_password_hash(password, method='sha256')
            db.execute("UPDATE students set password = ? where name = ?", [hashed_pass, name])
            db.commit()    
            msg = "Student password was sucessfully changed."
            return render_template('resetpassword.html', user = user, error = msg)
        
        else:
            msg = "Username not found. Try again!"            
            return render_template('resetpassword.html', user = user, error = msg)     
    return render_template("resetpassword.html", user = user)
    
@app.route("/deleteuser", methods = ["POST", "GET"])
def deleteuser():
    user = get_current_user()
    if request.method == "POST":
        db = getDatabase()
        name = request.form['username']
        password = request.form['password']
        
        if password != "admin-delete":
            error = "Incorrect admin password"
            return render_template("deleteuser.html", user = user, error = error)  
        
        users_cursor = db.execute("SELECT * FROM users WHERE name = ?", [name])
        dbuser = users_cursor.fetchone()
        
        if not dbuser:
            students_cursor = db.execute("SELECT * FROM students WHERE name = ?", [name])
            db_students = students_cursor.fetchone()
        
        if dbuser and name != "":
            db.execute("DELETE from users where name = ?", [name])
            db.commit()        
            msg = "User: " + user[2] +" deleted"
            return render_template('allusers.html', success = msg, user = user) 
        
        elif db_students and name != "":
            db.execute("DELETE from students where name = ?", [name])
            db.commit()        
            msg = "User: " + user[2] +" deleted"
            return render_template('allusers.html', success = msg, user = user) 
        
        else:
            msg = "Username not found. Try again!"            
            return render_template('allusers.html', user = user, error = msg) 
          
    return render_template("deleteuser.html", user = user)

@app.route("/allusers", methods = ["POST", "GET"])
def allusers():
    user = get_current_user()
    db = connect_to_DB()
    show = request.form.get('role2')
    
    user_cursor = db.execute("select * from users where role = ?", [show])
    allusers = user_cursor.fetchall()
    all_students = ""
    if show == "student":
        student_cursor = db.execute("select * from students")
        all_students = student_cursor.fetchall()
    
    return render_template("allusers.html", user = user, allusers = allusers, all_students = all_students)

@app.route("/create_test", methods = ['GET', 'POST'])
def create_test():
    user = get_current_user()
    sample_csv_url = url_for("static", filename="sample.csv")
    if request.method == "POST":        
        teacher_name = user[1]        
        
        conn = getDatabase()
        test_title = request.form.get('quiz_title')
       
        conn.execute('INSERT INTO tests (title, teacher_name, assigned_test, assigned_klass, test_id) VALUES (?, ?, ?, ?, ?)',
                     (test_title, teacher_name, 0, "Not Assigned", 0))
        
        test_id = conn.execute('SELECT id FROM tests WHERE title = ? AND teacher_name = ?',
                               (test_title, teacher_name)).fetchone()[0]
        
        conn.execute(
            "UPDATE tests SET test_id = ? WHERE id = ?",
            [test_id, test_id]
        )
        
        # Get the test_teacher of the newly created test
        test_teacher = conn.execute('SELECT teacher_name FROM tests WHERE title = ? AND teacher_name = ?', 
                                    (test_title, teacher_name)).fetchone()[0]
                
        csv_file = request.files['csv_file']
        upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'questions')
        if not os.path.exists(upload_folder):
            os.mkdir(upload_folder)

        # Save the file to the upload folder
        filename = secure_filename(csv_file.filename)
        if not csv_file.filename.endswith('.csv'):
            conn.execute('DELETE FROM tests WHERE title = ? AND teacher_name = ? AND test_id = ?', (test_title, teacher_name, test_id))
            conn.commit()
                    
            return render_template("create_test.html", user = user,  error = "Error: Only CSV files are allowed.")
                
        file_path = os.path.join(upload_folder, filename)
        csv_file.save(file_path)        
        with open(file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            expected_columns = ['qnumber', 'question', 'optionA', 'optionB', 'optionC', 'optionD', 'answer', 'explanation']
            for row in reader:
                if all(column in row for column in expected_columns):
                    qnumber = row['qnumber']
                    question = row['question']
                    optionA = row['optionA']
                    optionB = row['optionB']
                    optionC = row['optionC']
                    optionD = row['optionD']
                    answer = row['answer'] 
                    explanation = row['explanation'] 
                                     
                    query = f"INSERT INTO questions (test_id, test_teacher, qnumber, question, optionA, optionB, optionC, optionD, answer, explanation) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                        
                    conn.execute(query, (test_id, test_teacher, qnumber, question, optionA, optionB, optionC, optionD, answer, explanation))
                    conn.commit()
                 
                else:
                    conn.execute('DELETE FROM tests WHERE title = ? AND teacher_name = ? AND test_id = ?', (test_title, teacher_name, test_id))
                    conn.commit()

                    return render_template("create_test.html", user = user,  error = "CSV header error. Download \"sample.csv\" to confirm")
                 
        return render_template("create_test.html", user = user,  success = "Questions successfully uploaded")
    
    return render_template("create_test.html", user = user, sample_csv_url=sample_csv_url)

@app.route("/viewquiz",  methods = ["POST", "GET"])
def viewquiz():
    user = get_current_user()
    db = connect_to_DB()
    teacher_name = user[1]
    query = db.execute("SELECT * FROM tests WHERE teacher_name = ? AND test_id != 0", (teacher_name,))
    tests = query.fetchall()
    return render_template("viewquiz.html", user = user, tests = tests)

@app.route("/take_test", methods=["POST", "GET"])
def take_test():
    user = get_current_user()
    db = connect_to_DB()

    klass = user["klass"] 
    query = db.execute("SELECT * FROM tests WHERE assigned_klass = ? AND assigned_test = 1", [klass])
    tests = query.fetchall()
    
    return render_template("take_test.html", user=user, tests=tests)

@app.route("/tests_given", methods=["POST", "GET"])
def tests_given():
    user = get_current_user()
    db = connect_to_DB()

    student_name = user[1] 
    query = db.execute("SELECT * FROM completed WHERE student_name = ?", [student_name])
    tests = query.fetchall()

    return render_template("tests_given.html", user=user, tests=tests)

@app.route("/assign_test", methods=["POST", "GET"])
def assign_test():
    user = get_current_user()
    db = connect_to_DB()
    teacher_name = user[1]
    query = db.execute("SELECT * FROM tests WHERE teacher_name = ?", [teacher_name])
    tests = query.fetchall()

    if request.method == "POST":
        test_id = request.form.get("test_id")
        test_teacher = request.form.get("test_teacher")
        klass = request.form.get("klass")

        if klass == "select":
            error = "Please select a class."
            return render_template("assign_test.html", user=user, tests=tests, error=error)

        # Check if the test is already assigned
        assigned_test = db.execute(
            "SELECT * FROM assigned_tests WHERE test_id = ? AND test_teacher = ? AND klass = ?",
            [test_id, test_teacher, klass],
        ).fetchone()

        if assigned_test:
            # Test is already assigned, show an error message
            error = "Test is already assigned to the class"
            return render_template("assign_test.html", user=user, tests=tests, error=error)

        if request.form.get("cancel") == "cancel":
            # Cancel the assigned test
            db.execute(
                "DELETE FROM assigned_tests WHERE test_id = ?" ,
                [test_id],
            )
            db.commit()

            # Update the assigned_test attribute of the test in the tests table
            db.execute(
                "UPDATE tests SET assigned_test = 0, assigned_klass = 'Not Assigned' WHERE id = ?",
                [test_id],
            )
            db.commit()

        else:
            # Assign the test to the class
            db.execute(
                "INSERT INTO assigned_tests (test_id, test_teacher, klass) VALUES (?, ?, ?)",
                [test_id, test_teacher, klass],
            )
            db.commit()

            # Update the assigned_test attribute of the test in the tests table
            db.execute(
                "UPDATE tests SET assigned_test = 1, assigned_klass = ? WHERE id = ?",
                [klass, test_id],
            )
            db.commit()

        return redirect(url_for("assign_test"))

    return render_template("assign_test.html", user=user, tests=tests)


@app.route("/tests_created/<test_id>/")
def tests_created(test_id):
    user = get_current_user()
    db = connect_to_DB()
    
    #student_name check for both teacher and students
    student_name = user[1]
    
    quiz_cursor = db.execute(f"SELECT * FROM questions where test_id = ?", [test_id])
    quiz_questions = quiz_cursor.fetchall()
    
    query = db.execute("SELECT title FROM tests WHERE test_id = ?", [test_id])
    tests = query.fetchone()[0]
    
    query = db.execute("SELECT assigned_klass FROM tests WHERE test_id = ?", [test_id])
    result = query.fetchone()    
    klass = result[0]
    
    # Retrieve the selected_answers for the student
    query = db.execute("SELECT selections FROM selected_answers WHERE student_name = ? AND test_id = ?", [student_name, test_id])
    result = query.fetchone()
    
    if result is not None:
        selections_string = result[0] 
        
        # Convert the selections string back to a dictionary
        user_selections = json.loads(selections_string)
    else:
        # Handle the case when the selections are not found
        user_selections = {}
    
    # Check if the current user is a teacher
    chk = db.execute("SELECT name FROM users WHERE name = ?", (student_name,))
    teacher = chk.fetchone()
    
    if teacher:
        return render_template("tests_created.html", user = user, quiz_questions = quiz_questions, tests = tests, test_id = test_id, teacher = True, user_selections=user_selections)
    
    query = db.execute("SELECT * FROM completed WHERE student_name = ? AND klass = ? AND test_id = ?",
                    [student_name, klass, test_id])
    existing_test = query.fetchone()

    if existing_test:
        score = existing_test["score"]
        total = existing_test["total"]
        
        return render_template("tests_created.html", user = user, quiz_questions = quiz_questions, tests = tests, test_id = test_id, score=score, total= total, test_taken = True, user_selections=user_selections)
    
    db.close()
    
    return render_template("tests_created.html",  user = user, quiz_questions = quiz_questions, tests = tests, test_id = test_id, user_selections=user_selections)

@app.route("/submit_test/<test_id>/", methods=["POST", "GET"])
def submit_test(test_id): 
    user = get_current_user()
    db = connect_to_DB()
    student_name = user[1]
    student_fullname = user[2]
    klass = user[4]
   
    # Retrieve the total count of questions for the test_id
    query = db.execute("SELECT COUNT(*) FROM questions WHERE test_id = ?", [test_id])
    total = query.fetchone()[0]

    # Retrieve the submitted answers from the form
    submitted_answers = {}

    # Create a dictionary to store the user's selections
    user_selections = {}

    for key, value in request.form.items():
        if key.startswith('q'):
            question_id = int(key[1:])
            submitted_answers[question_id] = value  # Store the answer as a string

            # Store the user's selection in the dictionary
            user_selections[question_id] = value

    # Convert the user_selections dictionary to a string or JSON format
    selections_string = json.dumps(user_selections)  # JSON format

    # Store the user's selections in the database in a single row
    db.execute(
        "INSERT INTO selected_answers (student_name, student_fullname, klass, test_id, selections) VALUES (?, ?, ?, ?, ?)",
        (student_name, student_fullname, klass, test_id, selections_string)
    )
    db.commit()

    # Retrieve the correct answers from the database
    query = db.execute("SELECT id, answer FROM questions WHERE test_id = ?", [test_id])
    # Store the answer as a string
    correct_answers = {row[0]: row[1] for row in query.fetchall()}  
    
    # Compare submitted answers with correct answers and calculate the score
    score = 0
    for question_id, submitted_answer in submitted_answers.items():
        if question_id in correct_answers and submitted_answer == correct_answers[question_id]:
            score += 1
           
    query = db.execute("SELECT title, teacher_name, assigned_klass FROM tests WHERE test_id = ?", [test_id])
    result = query.fetchone()
    
    test_id = test_id
    title = result[0]
    score = score
    teacher_name = result[1]
    query_teacher = db.execute("SELECT fullname FROM users WHERE name = ?", [teacher_name])
    teacher_fullname = query_teacher.fetchone()[0]
    
    if student_name != teacher_name:
        db.execute("INSERT INTO completed (student_name, student_fullname, klass, test_id, title, score, total, teacher_name, teacher_fullname) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [student_name, student_fullname, klass, test_id, title, score, total, teacher_name, teacher_fullname])
        
        db.execute(
            "UPDATE tests SET assigned_test = 2 WHERE id = ?",
            [test_id]
        )
        db.commit()              
	
    return redirect(url_for("view_result", user=user, test_id=test_id, total = total, score = score))

@app.route("/view_result/<test_id>/", methods=["POST", "GET"])
def view_result(test_id):
    user = get_current_user()
    db = connect_to_DB()
    query = db.execute("SELECT title, score, total, student_fullname FROM completed WHERE test_id = ?", [test_id])
    result = query.fetchone()
    
    title = result[0]
    score = result[1]
    total = result[2]
    student_fullname = result[3]
    
    return render_template("view_result.html", user = user, test_id=test_id, title=title, score=score, total=total, student_fullname=student_fullname)

@app.route("/results_student", methods = ["POST", "GET"])
def results_student():
    user = get_current_user()
    db = connect_to_DB()
    
    klass = user[4]
    student_name = user[1]
    student_fullname = user[2]
    user_cursor = db.execute("SELECT * FROM completed WHERE student_name = ?", [student_name])
    results_student = user_cursor.fetchall()
    
    return render_template("results_student.html", user=user, results_student=results_student, klass=klass, student_fullname = student_fullname)

@app.route("/results_teacher", methods = ["POST", "GET"])
def results_teacher():
    user = get_current_user()
    db = connect_to_DB()
    teacher_name = user[1]
    query = db.execute("SELECT * FROM completed WHERE test_id != 0 AND teacher_name = ?", [teacher_name])
    tests = query.fetchall()
    return render_template("results_teacher.html", user = user, tests = tests)

@app.route("/view_std_result/<test_id>/")
def view_std_result(test_id):
    user = get_current_user()
    db = connect_to_DB()
    
    teacher_name = user[1]
    teacher_fullname = user[2]
    
    query = db.execute("SELECT * FROM completed WHERE test_id = ? AND teacher_name = ?", [test_id, teacher_name])
    results_student = query.fetchall()
    
    details = db.execute("SELECT title, assigned_klass FROM tests WHERE test_id = ? AND teacher_name = ?", [test_id, teacher_name])
    results_details = details.fetchone()
    
    title = results_details['title']
    assigned_klass = results_details['assigned_klass']
   
    return render_template("view_std_result.html", user=user, results_student =results_student, teacher_fullname= teacher_fullname, title = title, klass = assigned_klass)


@app.route("/results_admin", methods = ["POST", "GET"])
def results_admin():
    user = get_current_user()
    db = connect_to_DB()
    klass = request.form.get('klass')
    teacher_name = user[1]
    teacher_fullname = user[2]
    user_cursor = db.execute("SELECT * FROM completed WHERE teacher_name = ? AND klass = ?", [teacher_name, klass])
    results_teacher = user_cursor.fetchall()
    
    if not results_teacher:
        if klass != "None":
            message = "No results found for "
        else:
            message = ""
    else:
        message = ""

    return render_template("results_admin.html", user=user, results_teacher=results_teacher, message=message, klass=klass, teacher_fullname = teacher_fullname)

@app.route("/delete_test", methods = ["POST", "GET"])
def delete_test():
    user = get_current_user()
    db = connect_to_DB()
    teacher_name = user[1]
    
    if request.method == "POST":
        test_id = request.form.get("test_id")
        # Delete the test from the tests table
        db.execute("DELETE FROM tests WHERE id = ? AND teacher_name = ?", [test_id, teacher_name])
        # Delete all questions associated with the test from the questions table
        db.execute("DELETE FROM questions WHERE test_id = ?", [test_id])
        db.commit()
    
    query = db.execute("SELECT * FROM tests WHERE teacher_name = ?", [teacher_name])    
    tests = query.fetchall()
    
    return render_template("delete_test.html", user=user, tests=tests)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# Error handler for TypeError
@app.errorhandler(TypeError)
def handle_type_error(error):
    print(error)
    # Redirect to the login page
    msg = "You are not logged in! "
    # return redirect(url_for('login'), error = error)
    return render_template("login.html", error = msg)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'questions')
    app.run(debug=True)
    # app.debug(debug=False, host='0.0.0.0')