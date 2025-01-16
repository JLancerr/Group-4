from flask import Flask, render_template, session, request, redirect, url_for
from user import User
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
    user = User(session['user_id'], session['first_name'], session['last_name'], session['username'], session['password'])

    # Create instance of a classroom
    classroom = Classroom(user.get_user_id)

    # Retrieve all 
    classroom.get_subdirectories_info()

    # Display home page
    return render_template('home.html', user_data=user.get_all_attributes())

@app.route('/login', methods=['POST'])
def login():
    # Create instance of the user
    user = User(None, None, None, request.form['username'], request.form['password'])
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
    user = User(None, request.form['first_name'], request.form['last_name'], request.form['username'], request.form['password'])
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
    directory_id = request.form['directory_id']

    if directory_type == "question":
        pass
    else:
        dir = Directory(directory_type, directory_id)
        children_names_and_ids = dir.get_subdirectories_info()
        return render_template('generic_directory.html', children_names_and_ids=children_names_and_ids)


if __name__ == '__main__':
    app.run()
