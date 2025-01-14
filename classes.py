import sqlite3

class User:
    def __init__(self, first_name, last_name, username, password):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__username = username
        self.__password = password

    def signup(self):
        sqlite_connection = sqlite3.connect('app.db') # Connects to the database
        cursor = sqlite_connection.cursor() # Creates instance of a cursor which is used for executing queries

        # Check if username already exists in the database
        usernames = cursor.execute('SELECT username FROM Users WHERE username = ?;', (self.__username,)).fetchall()
        # If username already exists, signup fails
        if len(usernames) > 0:
            sqlite_connection.close()
            return False
        # If username does not exist in the database, insert user's info into the Users table
        else:
            cursor.execute("INSERT INTO Users (first_name, last_name, username, password) VALUES (?, ?, ?, ?);", 
                           (self.__first_name, self.__last_name, self.__username, self.__password))
            sqlite_connection.commit()
            sqlite_connection.close()
            return True

        
    def login(self):
        sqlite_connection = sqlite3.connect('app.db') # Connects to the database
        cursor = sqlite_connection.cursor() # Creates instance of a cursor which is used for executing queries

        # Check if username already exists in the database
        username = cursor.execute('SELECT username FROM Users WHERE username = ?;', (self.__username,)).fetchall()
        # If username does not exist, login attempt fails
        if len(username) == 0:
            sqlite_connection.close()
            return False

        # If username exists but password does not match the user's given password
        # data[password][first_name][last_name]
        data = cursor.execute('SELECT password, first_name, last_name FROM Users WHERE username = ?;', (username[0][0],)).fetchall()
        if self.__password != data[0][0]:
            sqlite_connection.close()
            return False
        
        # Initiliazed these vars as user is verified
        self.__first_name = data[0][1]
        self.__last_name = data[0][2]
        sqlite_connection.close()
        return True
        
    def get_first_name(self):
        return self.__first_name
    
    def get_last_name(self):
        return self.__last_name
    
    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password

    # Returns all attributes in dictionary form
    def get_all_attributes(self):
        return {
            'first_name': self.__first_name, 
            'last_name':  self.__last_name, 
            'username':  self.__username, 
            'password':  self.__password}

class Class:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.questions = {}

    