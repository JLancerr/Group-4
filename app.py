from flask import Flask, render_template, session, request, redirect, url_for
import sqlite3
import json
import classes

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
    user = classes.User(session['user_id'], session['first_name'], session['last_name'], session['username'], session['password'])
    joined_classrooms = user.get_joined_classrooms()

    # Display home page
    return render_template('home.html', user_data=user.get_all_attributes(), joined_classrooms=joined_classrooms)

@app.route('/login', methods=['POST'])
def login():
    # Create instance of the user
    user = classes.User(None, None, None, request.form['username'], request.form['password'])
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
    user = classes.User(None, request.form['first_name'], request.form['last_name'], request.form['username'], request.form['password'])
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

@app.route('/join_classroom', methods=['POST'])
def join_classroom(): 
    # Retrieve instance of user from the session
    user = classes.User(session['user_id'], session['first_name'], session['last_name'], session['username'], session['password'])

    # User will use the join_class(class_id) method
    inputted_classroom_id = request.form["classroom_id"]
    join_attempt_outcome = user.join_classroom(inputted_classroom_id)

    if join_attempt_outcome != "success":
        return redirect(url_for('home', error=join_attempt_outcome))
    else:
        return redirect(url_for('home', error=join_attempt_outcome))

@app.route('/create_classroom', methods=["POST"])
def create_classroom():
    # Retrieve instance of user from the session
    user = classes.User(session['user_id'], session['first_name'], session['last_name'], session['username'], session['password'])

    # User will create classroom
    user.create_classroom(request.form['classroom_name'])

    return redirect(url_for('home'))

@app.route('/create_question', methods=["POST"])
def create_question():
    # Retrieve instance of user from the session
    user = classes.User(session['user_id'], session['first_name'], session['last_name'], session['username'], session['password'])

    # 
    pass

if __name__ == '__main__':
    app.run()
