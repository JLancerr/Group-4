from flask import Flask, render_template, session, request, redirect, url_for, send_from_directory
from user import *
from directory import *
import sqlite3

app = Flask(__name__)

# Secret key is required for sessions to occur
app.secret_key = "HARRY"

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<page_name>')
def render_page(page_name):
    return render_template(f'{page_name}.html')

@app.route('/login')
def login():
    error = request.args.get('error')
    if error == None:
        return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/attempt_login', methods=['POST'])
def attempt_login():
    user = User(request.form)
    login_outcome = user.login()
    
    if login_outcome != "success":
        return redirect(url_for('login', error=login_outcome))
    else:
        # Login as admin if username is admin
        if user.get_username() == 'admin':
            return redirect(url_for('admin'))
        
        # Put all user attributes to the session
        session.update(user.get_all_attributes())

        return redirect(url_for('home'))

@app.route('/signup')
def signup():
    error = request.args.get('error')
    if error == None:
        return render_template('signup.html', error=error)
    return render_template('signup.html')

@app.route('/attempt_signup', methods=['POST'])
def attempt_signup():
    user = User(request.form)
    signup_outcome = user.signup()

    if signup_outcome != "success":
        # Direct user back to the login page
        return redirect(url_for('signup', error=signup_outcome))
    else:
        # Put all user attributes to the session
        session.update(user.get_all_attributes())

        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    user = User(session)

    # Retrieve all classrooms the user is joined in 
    classrooms_info = user.get_classrooms_info()
    
    # Display home page
    return render_template('home.html', user_data=user.get_all_attributes(), classrooms_info=classrooms_info)

# Requires directory_type, directory_id
# Note that any other routes that tries to redirect to /display will need to provide a directory_type
@app.route('/display', methods=['GET'])
def display():
    directory_type = request.args.get('directory_type')
    directory_id = request.args.get('directory_id')

    args_dict = {
        'directory_type' : directory_type,
        'directory_id' : directory_id
    }
    
    if directory_type == "classroom":
        dir = Classroom(args_dict)
    elif directory_type == "lesson":
        dir = Lesson(args_dict)
    else:
        dir = Directory(args_dict)
    contents = dir.get_directory_contents()

    # Get all necessary data for the page to utilize
    if session:
        user = User(session)
        user_data = user.get_all_attributes()
        authored = dir.authorize_user(user.get_user_id())
    else:
        user_data = None
        authored = '0'

    parent_directory_name = dir.get_directory_name_from_database()

    # Determine page to render
    directory_to_render = f"{children_of[directory_type]}s"
    return render_template(f'{directory_to_render}.html', user_data=user_data, contents=contents, authored=authored, 
                           parent_directory_name=parent_directory_name, parent_directory_type=directory_type, parent_directory_id=directory_id)

@app.route('/quiz', methods=["GET"])
def quiz():
    quiz_type = request.args['quiz_type']
    lesson_id = request.args['parent_id']
    args_dict = {
        'directory_type' : 'lesson',
        'directory_id' : lesson_id
    }
    lesson = Lesson(args_dict)
    contents = lesson.get_directory_contents()
    return render_template(f'learningview/{quiz_type}.html', contents=contents)

@app.route('/add_directory', methods=["POST"])
def add_directory():
    directory_type = request.form['directory_type']

    if directory_type == "classroom":
        # Requires directory_id, directory_type, directory_name, parent_id
        user = User(session)
        outcome = user.add_classroom(request.form['directory_name'])
        if outcome != "success":
            return redirect(url_for('home', error=outcome))
        else:
            return redirect(url_for('home'))
    elif directory_type == "question":
        # Requires directory_type, question, answer, parent_id
        dir = Question(request.form)
    else:
        # Requires directory_id, directory_type, and directory_name, parent_id
        dir = Directory(request.form)
    dir.add_dir_to_database()

    previous_dir_type = parent_of[f'{directory_type}']
    previous_dir_id = request.form['parent_id']
    return redirect(url_for('display', directory_id=previous_dir_id, directory_type=previous_dir_type))

# Requires directory_id, directory_type
@app.route('/delete_directory', methods=["POST"])
def delete_directory():
    directory_type = request.form['directory_type']

    if directory_type == "classroom":
        classroom = Classroom(request.form)
        classroom.delete_directory()
        return redirect(url_for('home'))
    else:
        dir = Directory(request.form)
        dir.delete_directory()
        previous_dir_type = parent_of[f'{directory_type}']
        previous_dir_id = request.form['parent_id']
        return redirect(url_for('display', directory_id=previous_dir_id, directory_type=previous_dir_type))

@app.route('/edit_directory', methods=["POST"])
def edit_directory():
    directory_type = request.form['directory_type']
    directory_id = request.form['directory_id']

    if directory_type == "question":
        # Requires directory_id, directory_type, new_question, and new_answer
        question = Question(request.form)
        question.edit_directory(request.form['new_question'], request.form['new_answer'])
    elif directory_type == "classroom":
        # Requires directory_id, directory_type, and new_classroom_name
        user = User(session)
        user.rename_classroom(directory_id, request.form['new_classroom_name'])
        return redirect(url_for('home'))
    else:
        # Requires directory_id, directory_type, and new_directory_name
        dir = Directory(request.form)
        dir.edit_directory(request.form['new_directory_name'])

    previous_dir_type = parent_of[f'{directory_type}']
    previous_dir_id = request.form['parent_id']
    return redirect(url_for('display', directory_id=previous_dir_id, directory_type=previous_dir_type))

# Requires user_id_to_kick, directory_id
@app.route('/kick_user', methods=["POST"])
def kick_user():
    directory_id = request.form['directory_id']
    user = User(session)
    user.kick_user(request.form['user_id_to_kick'], directory_id)

    previous_dir_type = "classroom"
    previous_dir_id = directory_id
    return redirect(url_for('display', directory_id=previous_dir_id, directory_type=previous_dir_type))

# Requires directory_id
@app.route('/leave_classroom', methods=["POST"])
def leave_classroom():
    directory_id = request.form['directory_id']
    user = User(session)
    user.leave_classroom(directory_id)
    
    return redirect(url_for('home'))

# Requires directory_id
@app.route('/join_classroom', methods=["POST"])
def join_classroom():
    directory_id = request.form['directory_id']

    user = User(session)
    outcome = user.join_classroom(directory_id)

    if outcome != "success":
        return redirect(url_for('home', error=outcome))
    else:
        return redirect(url_for('home'))
    
@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    user = User(request.form)
    previous_page = None
    for name in request.form:
        if name == 'previous_page':
            previous_page = request.form[name]
            continue
        outcome = user.edit_profile(name, request.form[name])
        if outcome != "success":
            return redirect(url_for(f'{previous_page}', error=outcome))

    return redirect(url_for(f'{previous_page}'))
    
# Required user_id
@app.route('/delete_user', methods=['POST'])
def delete_profile():
    user = User(request.form)
    user.delete_self()
    return redirect(url_for('admin'))

@app.route('/admin', methods=['GET'])
def admin():
    sqlite_connection = sqlite3.connect('app.db') 
    cursor = sqlite_connection.cursor() 
    all_users = cursor.execute("SELECT * FROM Users").fetchall()
    list_users = []
    i = 0
    for one_user in all_users:
        converted = list(one_user)
        converted.append(i)
        if converted[6] == None:
            converted[6] = 'null'
        list_users.append(converted)
        i += 1
    total_users = len(list_users)

    total_subscription = cursor.execute("SELECT COUNT(user_id) FROM Users WHERE membership_type = 'pro'").fetchone()[0]
    return render_template('admin.html', all_users=list_users, total_users=total_users, total_subscription=total_subscription)

# Requires user_id, duration_option ('option_1' for 12 months, 'option_2' for 6 months)
@app.route('/upgrade_plan', methods=['POST'])
def upgrade_plan():
    duration_option = request.form['duration_option']
    user = User(session)
    user.upgrade_plan(duration_option)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
