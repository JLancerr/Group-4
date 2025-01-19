from flask import Flask, render_template, session, request, redirect, url_for
from user import *
from directory import *

app = Flask(__name__)

# Secret key is required for sessions to occur
app.secret_key = "HARRY"

@app.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['POST'])
def login():
    user = User(request.form)
    login_outcome = user.login()
    
    if login_outcome != "success":
        return redirect(url_for('landing', error=login_outcome))
    else:
        # Put all user attributes to the session
        user_attributes = user.get_all_attributes()
        for key in user_attributes:
            session[f'{key}'] = user_attributes[f'{key}']

        return redirect(url_for('home'))

@app.route('/signup', methods=['POST'])
def signup():
    user = User(request.form)
    signup_outcome = user.signup()

    if signup_outcome != "success":
        # Direct user back to the login page
        return redirect(url_for('landing', error=signup_outcome))
    else:
        # Put all user attributes to the session
        user_attributes = user.get_all_attributes()

        for key in user_attributes:
            session[f'{key}'] = user_attributes[f'{key}']

        return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    user = User(session)

    # Retrieve all classrooms the user is joined in 
    classrooms_info = user.get_classrooms_info()

    # Display home page
    return render_template('home.html', user_data=user.get_all_attributes(), classrooms_info=classrooms_info)

@app.route('/display', methods=['POST'])
def display():
    directory_type = request.form['directory_type']
    children_type = children_of[f"{directory_type}"]
    authored = request.form['authored']

    if directory_type == "classroom":
        dir = Classroom(request.form)
    elif directory_type == "lesson":
        dir = Lesson(request.form)
    else:
        dir = Directory(request.form)
    contents = dir.get_directory_contents()

    return render_template(f'{children_type}s.html', contents=contents, authored=authored)

@app.route('/add_directory', method=["POST"])
def add_directory():
    directory_type = request.form['directory_type']

    if directory_type == "classroom":
        user = User(session)
        outcome = user.add_classroom(request.form['directory_name'])
        if outcome != "success":
            return redirect(url_for('home', error=outcome))
        else:
            return redirect(url_for('home'))
    elif directory_type == "question":
        dir = Question(request.form)
    else:
        dir = Directory(request.form)
    outcome = dir.add_dir_to_database()

    # Implement some sort of error handling in directory.py / add_dir_to_database
    if outcome != "success" and False:
        pass
    else:
        # Go back to display route
        session['directory_type'] = parent_of[f"{directory_type}"]
        session['directory_id'] = request.form['parent_id']
        return redirect(url_for('/display'))

@app.route('/delete_directory', method=["POST"])
def delete_directory():
    directory_type = request.form['directory_type']

    if directory_type == "classroom":
        user = User(session)
        directory_id = request.form['directory_id']
        user.delete_classroom(directory_id)
        return redirect(url_for('home'))
    elif directory_type == "lesson":
        dir = Lesson(request.form)
    elif directory_type == "question":
        dir = Question(request.form)
    else:
        dir = Directory(request.form)
        
    dir.delete_directory()
    session['directory_type'] = parent_of[f"{directory_type}"]
    session['directory_id'] = request.form['parent_id']
    return redirect(url_for('/display'))

@app.route('/edit_directory', method=["POST"])
def edit_directory():
    pass

@app.route('/join_classroom', method=["POST"])
def join_classroom():
    user = User(session)
    outcome = user.join_classroom(request.form['classroom_id'])
    if outcome != "success":
        return redirect(url_for('home', error=outcome))
    else:
        return redirect(url_for('home'))

@app.route('/leave_classroom', method=["POST"])
def leave_classroom():
    user = User(session)
    user.leave_classroom(request.form['classroom_id'])
    return redirect(url_for('home'))

@app.route('/kick_user', method=["POST"])
def kick_user():
    user = User(session)
    user.kick_user(request.form['user_id_to_kick'], request.form['classroom_id'])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
