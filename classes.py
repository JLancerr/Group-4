import sqlite3
import json

class User:
    def __init__(self, first_name, last_name, username, password):
        self.__user_id = None
        self.__first_name = first_name
        self.__last_name = last_name
        self.__username = username
        self.__password = password

        self.sqlite_connection = sqlite3.connect('app.db') # Connects to the database
        self.cursor = self.sqlite_connection.cursor() # Creates instance of a cursor which is used for executing querie

    def signup(self):
        # Check if username already exists in the database
        usernames = self.cursor.execute('SELECT username FROM Users WHERE username = ?;', (self.__username,)).fetchall()
        # If username already exists, signup fails
        if len(usernames) > 0:
            return False
        # If username does not exist in the database, insert user's info into the Users table
        else:
            self.cursor.execute("INSERT INTO Users (first_name, last_name, username, password) VALUES (?, ?, ?, ?);", 
                           (self.__first_name, self.__last_name, self.__username, self.__password))
            self.sqlite_connection.commit()
            return True
        
    def login(self):
        # Check if username already exists in the database
        username = self.cursor.execute('SELECT username FROM Users WHERE username = ?;', (self.__username,)).fetchall()
        # If username does not exist, login attempt fails
        if len(username) == 0:
            print("Username not found")
            return False

        # If username exists but password does not match the user's given password
        # data[password][first_name][last_name][user_id]
        data = self.cursor.execute('SELECT password, first_name, last_name, user_id FROM Users WHERE username = ?;', (username[0][0],)).fetchall()
        if self.__password != data[0][0]:
            print("Wrong password")
            return False
        
        # Initiliazed these vars as user is verified
        self.__first_name = data[0][1]
        self.__last_name = data[0][2]
        self.__user_id = data[0][3]
        return True
    
    def create_classroom(self, classroom_name):
        self.cursor("INSERT INTO Classroom (class_name, author_user_id) VALUES (?);", (classroom_name, self.__user_id))
        self.sqlite_connection.commit()

    def join_classroom(self, class_id):
        # Check if valid class id
        retrieved_classroom_id = self.cursor("SELECT class_id FROM Classroom WHERE = ?", (class_id,)).fetch_all()
        if len(retrieved_classroom_id) == 0:
            return False
        
        # Retrieve user list from the class
        user_joined_ids = self.cursor("SELECT users_joined FROM Classroom WHERE = ?", (class_id,)).fetch_all()[0][0]
        if str(self.__user_id) in user_joined_ids:
            return False
        
        # Concat new user to the list of users
        new_user_joined_ids = user_joined_ids + str(self.__user_id)

        # Insert update the list, that contains the users who joined the class, with the new updated list
        self.cursor("UPDATE Classroom SET users_joined = ?", (new_user_joined_ids,))
        self.sqlite_connection.commit()
        return True

    def get_first_name(self):
        return self.__first_name
    
    def get_last_name(self):
        return self.__last_name
    
    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password
    
    def get_user_id(self):
        return self.__user_id

    # Returns all attributes in dictionary form
    def get_all_attributes(self):
        return {
            'first_name': self.__first_name, 
            'last_name':  self.__last_name, 
            'username':  self.__username, 
            'password':  self.__password}

class Classroom:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.questions = {}

    