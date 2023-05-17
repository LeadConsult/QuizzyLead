from flask import Flask, render_template, url_for, request, g, redirect, session
from database import connect_to_DB, getDatabase
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import csv
import sqlite3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
        user_cursor = db.execute("select * from users where name = ?", [user])
        user_result = user_cursor.fetchone()
    return user_result


# def login_required(role):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorated_view(*args, **kwargs):
#             if not current_user.is_authenticated:
#                 return current_app.login_manager.unauthorized()
#             if not current_user.has_role(role):
#                 abort(403)
#             return fn(*args, **kwargs)
#         return decorated_view
#     return wrapper

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
        dbuser_cursor = db.execute("select * from users where name =?", [name])
        dbuser = dbuser_cursor.fetchone()
        
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
            return render_template("register.html", error=error)
        
        db = getDatabase()
        name = request.form['username']
        password = request.form['password']
        role = request.form['role']
        fullname = request.form['fullname']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password or password == "":
            error = "Password not thesame"
            return render_template("register.html", error = error)
        
        user_fetching_cursor = db.execute("select * from users where name = ?", [name])
        existing_user = user_fetching_cursor.fetchone()
        if existing_user or name == "":
            error = "Username already taken"
            return render_template("register.html", error = error)
        
        hashed_pass = generate_password_hash(password, method='sha256')
        db.execute("insert into users (name, fullname, password, role) values (?,?,?,?)",
                   [name, fullname, hashed_pass, role])
        db.commit()
        session['user'] = name
        return redirect(url_for('register'))     
    return render_template("register.html", user = user)

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
            return render_template("resetpassword.html", error = error)
        
        user_fetching_cursor = db.execute("select * from users where name = ?", [name])
        existing_user = user_fetching_cursor.fetchone()
        if existing_user and name != "":
            hashed_pass = generate_password_hash(password, method='sha256')
            db.execute("UPDATE users set password = ? where name = ?", [hashed_pass, name])
            db.commit()
            session['user'] = name
            return render_template('login.html', success="Your password was sucessfully changed.")     
    return render_template("resetpassword.html", user = user,)
    
@app.route("/deleteuser", methods = ["POST", "GET"])
def deleteuser():
    user = get_current_user()
    if request.method == "POST":
        db = getDatabase()
        name = request.form['username']
        password = request.form['password']
        
        if password != "admin-delete":
            error = "Incorrect admin password"
            return render_template("deleteuser.html", error = error)
        
        user_fetching_cursor = db.execute("select * from users where name = ?", [name])
        existing_user = user_fetching_cursor.fetchone()
        if existing_user and name != "":
            db.execute("DELETE from users where name = ?", [name])
            db.commit()
            session['user'] = name
            return render_template('allusers.html', success="Users sucessfully deleted.")     
    return render_template("deleteuser.html", user = user)

@app.route("/allusers", methods = ["POST", "GET"])
def allusers():
    user = get_current_user()
    db = connect_to_DB()
    show = request.form.get('role2')
    user_cursor = db.execute("select * from users where role = ?", [show])
    allusers = user_cursor.fetchall()
    return render_template("allusers.html", user = user, allusers = allusers)

@app.route("/create_test", methods = ['GET', 'POST'])
def create_test():
    user = get_current_user()
    if request.method == "POST":        
        teacher_name = user[1]
        # print(user[0])
        # print(teacher_name)
        
        conn = getDatabase()
        test_title = request.form.get('quiz_title')

        # conn.execute('INSERT INTO tests (title, teacher_name) VALUES (?, ?)',
        #              (test_title, teacher_name))
        # conn.commit()        
        # db = getDatabase()
        conn.execute('INSERT INTO tests (title, teacher_name) VALUES (?, ?)',
                     (test_title, teacher_name))
        # conn.commit()
        
        # Get the test_teacher of the newly created test
        test_teacher = conn.execute('SELECT teacher_name FROM tests WHERE title = ? AND teacher_name = ?',
                               (test_title, teacher_name)).fetchone()[0]
        test_id = conn.execute('SELECT id FROM tests WHERE title = ? AND teacher_name = ?',
                               (test_title, teacher_name)).fetchone()[0]
        
                
        csv_file = request.files['csv_file']
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.mkdir(upload_folder)

        # Save the file to the upload folder
        filename = secure_filename(csv_file.filename)
        if not csv_file.filename.endswith('.csv'):
            return render_template("create_test.html", user = user,  error = "Error: Only CSV files are allowed.")
        file_path = os.path.join(upload_folder, filename)
        csv_file.save(file_path)
        
        
        with open(file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                qnumber = row['qnumber']
                question = row['question']
                option1 = row['option1']
                option2 = row['option2']
                option3 = row['option3']
                option4 = row['option4']
                answer = row['answer']
                query = f"INSERT INTO questions (test_id, test_teacher, qnumber, question, option1, option2, option3, option4, answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                conn.execute(query, (test_id, test_teacher, qnumber, question, option1, option2, option3, option4, answer))
                conn.commit()
        return render_template("create_test.html", user = user,  success = "Questions successfully uploaded")
    return render_template("create_test.html", user = user)

# @app.route("/take_test",  methods = ["POST", "GET"])
# def take_test():
#     user = get_current_user()
#     db = connect_to_DB()
#     submitted_answers = request.form.getlist('answers')
#     correct_answers = db.execute("SELECT answer FROM questions WHERE test_id = 30").fetchall()
    
#     score = 0
#     for i in range(len(submitted_answers)):
#         if submitted_answers[i] == correct_answers[i][0]:
#             score += 1
#         print(score)
    
#     quiz_cursor = db.execute(f"SELECT * FROM questions where test_id = 30")
#     quiz_questions = quiz_cursor.fetchall()
    
#     return render_template("take_test.html", user = user, quiz_questions = quiz_questions)


@app.route("/viewquiz",  methods = ["POST", "GET"])
def viewquiz():
    user = get_current_user()
    db = connect_to_DB()
    teacher_name = user[1]
    query = db.execute(f"SELECT * FROM tests where teacher_name = ?", [teacher_name])    
    tests = query.fetchall()
    return render_template("viewquiz.html", user = user, tests = tests)

@app.route("/tests_created/<test_id>/")
def tests_created(test_id):
    user = get_current_user()
    db = connect_to_DB()
    quiz_cursor = db.execute(f"SELECT * FROM questions where test_id = ?", [test_id])
    quiz_questions = quiz_cursor.fetchall()
    return render_template("tests_created.html",  user = user, quiz_questions = quiz_questions)

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

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'questions' # Define the upload directory
    app.run(debug=True)