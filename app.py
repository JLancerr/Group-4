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

@app.route('/home', methods=['POST'])
def home():
    # Trigger session
    session['logged_in'] = True

    user = classes.User(None , None, request.form['username'], request.form['password'])
    login_success = user.login()

    if login_success == False:
        return redirect('/')
    else:
        # Display home page
        return render_template('home.html', user_data=user.get_all_attributes())

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

@app.route('/join_class', methods=['POST'])
def joinclass():
    pass

if __name__ == '__main__':
    app.run()
