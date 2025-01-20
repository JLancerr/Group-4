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
    # Authorization
    authored = dir.authorize_user(session['user_id'])
    directory_to_render = children_of[directory_type]
    parent_directory_name = dir.get_directory_name_from_database()
    return render_template(f'{directory_to_render}s.html', contents=contents, authored=authored, parent_directory_name=parent_directory_name, parent_directory_type=directory_type, parent_directory_id=directory_id)

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
    directory_id = request.form['directory_id']

    if directory_type == "classroom":
        user = User(session)
        user.delete_classroom(directory_id)
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

# Requires directory_id
@app.route('/leave_classroom', methods=["POST"])
def leave_classroom():
    directory_id = request.form['directory_id']
    user = User(session)
    user.leave_classroom(directory_id)
    return redirect(url_for('display'))

# Requires user_id_to_kick, directory_id
@app.route('/kick_user', methods=["POST"])
def kick_user():
    directory_id = request.form['directory_id']
    user = User(session)
    user.kick_user(request.form['user_id_to_kick'], directory_id)
    return redirect(url_for('display'))

if __name__ == '__main__':
    app.run()
