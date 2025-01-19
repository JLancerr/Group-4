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

# Requires directory_type, directory_id, and authored
@app.route('/display', methods=['GET', 'POST'])
def display():
    directory_type = request.form.get('directory_type')
    if directory_type == None:
        directory_type = session.get('directory_type')

    directory_id = request.form.get('directory_id')
    if directory_id == None:
        directory_id = session.get('directory_id')
    
    authored = request.form.get('authored')
    if authored == None:
        authored = session.get('authored')

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

    session['directory_type'] = directory_type
    session['directory_id'] = directory_id
    session['authored'] = authored
    directory_to_render = children_of[directory_type]
    directory_name = dir.get_directory_name_from_database()
    parent_info = [directory_type, directory_id, directory_name]
    return render_template(f'{directory_to_render}s.html', contents=contents, authored=authored, parent_info=parent_info)

@app.route('/add_directory', method=["POST"])
def add_directory():
    directory_type = request.form['directory_type']

    if directory_type == "classroom":
        # Requires directory_id, directory_type, directory_name
        user = User(session)
        outcome = user.add_classroom(request.form['directory_name'])
        if outcome != "success":
            return redirect(url_for('home', error=outcome))
        else:
            return redirect(url_for('home'))
    elif directory_type == "question":
        # Requires directory_id, directory_type, question, answer 
        dir = Question(request.form)
    else:
        # Requires directory_id, directory_type, and directory_name
        dir = Directory(request.form)
    dir.add_dir_to_database()

    return redirect(url_for('/display'))

# Requires directory_id, directory_type
@app.route('/delete_directory', method=["POST"])
def delete_directory():
    directory_type = request.form['directory_type']
    directory_id = request.form['directory_id']

    if directory_type == "classroom":
        user = User(session)
        user.delete_classroom(directory_id)
        return redirect(url_for('/display'))
    else:
        dir = Directory(request.form)
        dir.delete_directory()
        return redirect(url_for('/display'))

@app.route('/edit_directory', method=["POST"])
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
    else:
        # Requires directory_id, directory_type, and new_directory_name
        dir = Directory(request.form)
        dir.edit_directory(request.form['new_directory_name'])

    return redirect(url_for('/display'))

# Requires directory_id
@app.route('/join_classroom', method=["POST"])
def join_classroom():
    directory_id = request.form['directory_id']

    user = User(session)
    outcome = user.join_classroom(directory_id)

    if outcome != "success":
        return redirect(url_for('display', error=outcome))
    else:
        return redirect(url_for('display'))
    
# Requires directory_id
@app.route('/leave_classroom', method=["POST"])
def rename_classroom():
    directory_id = request.form['directory_id']
    user = User(session)
    user.rename_classroom(directory_id, request.form['new_classroom_name'])
    return redirect(url_for('display'))

# Requires directory_id
@app.route('/leave_classroom', method=["POST"])
def leave_classroom():
    directory_id = request.form['directory_id']
    user = User(session)
    user.leave_classroom(directory_id)
    return redirect(url_for('display'))

# Requires user_id_to_kick, directory_id
@app.route('/kick_user', method=["POST"])
def kick_user():
    directory_id = request.form['directory_id']
    user = User(session)
    user.kick_user(request.form['user_id_to_kick'], directory_id)
    return redirect(url_for('display'))

if __name__ == '__main__':
    app.run()
