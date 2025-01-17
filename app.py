from flask import Flask, render_template, session, request, redirect, url_for
from user import *
from directory import *

app = Flask(__name__)

# Secret key is required for sessions to occur
app.secret_key = "HARRY"

@app.route('/', methods=['GET', 'POST'])
def landing():
    # Display landing page
    return render_template('landing.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    # Create instance of the user
    user = User(session)

    # Retrieve all classrooms the user is joined in 
    classrooms_info = user.get_classrooms_info()

    # Display home page
    return render_template('home.html', user_data=user.get_all_attributes(), classrooms_info=classrooms_info)

@app.route('/login', methods=['POST'])
def login():
    # Create instance of the user
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
    # This route doesn't display anything
    # This is for verifying data inputted by the user during signup

    # Create instance of user
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

@app.route('/display', methods=['POST'])
def display():
    directory_type = request.form['directory_type']

    if directory_type == "question":
        pass
    else:
        # Needs directory_type and directory_id
        dir = Directory(request.form)
        children_names_and_ids = dir.get_subdirectories_info()

        # This is volatile, remember to change it when files to render in this route are not named as the format below
        return render_template(f'{directory_type}.html', children_names_and_ids=children_names_and_ids)

@app.route('/add_directory', method=["POST"])
def add_directory():
    directory_type = request.form['directory_type']

    if directory_type == "question":
        pass
    else:
        # Needs directory_name and parent_id
        dir = Directory(request.form)
        outcome = dir.add_dir_to_database()

        # Implement some sort of error handling in directory.py / add_dir_to_database
        if outcome != "success" and False:
            pass
        else:
            # This is volatile, remember to change it when files to render in this route are not named as the format below
            return redirect(url_for('/display'))

@app.route('/delete_directory', method=["POST"])
def delete_directory():
    dir = Directory(request.form)
    outcome = dir.delete_directory()

    # Implement some sort of error handling in directory.py / add_dir_to_database
    if outcome != "success" and False:
        pass
    else:
        # This is volatile, remember to change it when files to render in this route are not named as the format below
        return render_template(f'{directory_type}.html')

if __name__ == '__main__':
    app.run()
