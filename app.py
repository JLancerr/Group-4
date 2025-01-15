from flask import Flask, render_template, session, request, redirect
import sqlite3
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
    user = classes.User(None , None, request.form['username'], request.form['password'])
    login_success = user.login()

    if login_success == False:
        return redirect('/')
    else:
        # Put all user attributes to the session
        user_attributes = user.get_all_attributes()

        for key in user_attributes:
            session[f'{key}'] = user_attributes[f'{key}']

        # Display home page
        return render_template('home.html', user_data=user.user_attributes)

@app.route('/signup', methods=['POST'])
def signup():
    # This route doesn't display anything
    # This is for verifying data inputted by the user during signup

    # Create instance of user
    user = classes.User(request.form['first_name'], request.form['last_name'], request.form['username'], request.form['password'])
    
    signup_success = user.signup()

    if signup_success == False:
        # Direct user back to the login page
        return redirect('/')
    else:
        # Direct user back to the landing page
        return redirect('/')

@app.route('/join_classroom', methods=['POST'])
def join_classroom(): 
    # Retrieve instance of user from the session
    user = classes.User()

    # User will use the join_class(class_id) method
    inputted_classroom_id = request.form["classroom_id"]
    join_success = user.join_classroom(inputted_classroom_id)

    # 
    if join_success == False:
        return redirect('/home', message="Error")

@app.route('/create_classroom', methods=["POST"])
def create_classroom():
    # Retrieve instance of user from the session
    # User will use the create_class(classroom_name)
    pass

@app.route('/create_question', methods=["POST"])
def create_question():
    # Retrieve instance of user from the session
    pass

if __name__ == '__main__':
    app.run()
