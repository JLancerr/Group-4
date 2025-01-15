import sqlite3
import json

class User:
    def __init__(self, user_id, first_name, last_name, username, password):
        self.__user_id = user_id
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
            return "username-already-exists"
        # If username does not exist in the database, insert user's info into the Users table
        else:
            self.cursor.execute("INSERT INTO Users (first_name, last_name, username, password, joined_classrooms) VALUES (?, ?, ?, ?, ?);", 
                           (self.__first_name, self.__last_name, self.__username, self.__password, ""))
            self.__user_id = self.cursor.execute("SELECT user_id FROM Users WHERE username = ?", (self.__username,))
            self.sqlite_connection.commit()
            return "success"
        
    def login(self):
        # Check if username already exists in the database
        username = self.cursor.execute('SELECT username FROM Users WHERE username = ?;', (self.__username,)).fetchall()
        # If username does not exist, login attempt fails
        if len(username) == 0:
            return "username-not-found"

        # If username exists but password does not match the user's given password
        # data[password][first_name][last_name][user_id]
        data = self.cursor.execute('SELECT password, first_name, last_name, user_id FROM Users WHERE username = ?;', (username[0][0],)).fetchall()
        if self.__password != data[0][0]:
            return "password-incorrect"
        
        # Initiliazed these vars as user is verified
        self.__first_name = data[0][1]
        self.__last_name = data[0][2]
        self.__user_id = data[0][3]
        return "success"
    
    def create_classroom(self, classroom_name):
        self.cursor.execute("INSERT INTO Classroom (classroom_name, author_user_id, users_joined) VALUES (?, ?, ?);", (classroom_name, self.__user_id, ''))
        self.sqlite_connection.commit()

    def join_classroom(self, classroom_id):
        # Check if valid class id
        retrieved_classroom_id = self.cursor.execute("SELECT classroom_id FROM Classroom WHERE classroom_id = ?", (classroom_id,)).fetchall()
        if len(retrieved_classroom_id) == 0:
            return "invalid-classroom-id"
        
        # Retrieve user list from the class
        user_joined_ids = self.cursor.execute("SELECT users_joined FROM Classroom WHERE classroom_id = ?", (classroom_id,)).fetchone()[0]
        if user_joined_ids:
            if str(self.__user_id) in user_joined_ids:
                return "classroom-already-joined"
        
        # Concat new user to the list of users
        new_user_joined_ids = (user_joined_ids + " " + str(self.__user_id)).strip()

        # Insert updated list, that contains the users who joined the class, with the new updated list
        self.cursor.execute("UPDATE Classroom SET users_joined = ? WHERE classroom_id = ?", (new_user_joined_ids, classroom_id))

        # Retrieve classroom list of the user
        joined_classroom_ids = self.cursor.execute("SELECT joined_classrooms FROM Users WHERE user_id = ?", (self.__user_id,)).fetchone()[0]
        new_joined_classroom_ids = (joined_classroom_ids + " " + classroom_id).strip()
        self.cursor.execute("UPDATE Users SET joined_classrooms = ? WHERE user_id = ?", (new_joined_classroom_ids, self.__user_id))

        self.sqlite_connection.commit()
        return "success"

    def get_joined_classrooms(self):
        # Retrieve this as a list of strings
        joined_classroom_ids = []
        print(self.__user_id)
        print(self.cursor.execute("SELECT joined_classrooms FROM Users WHERE ?", (self.__user_id,)).fetchone())
        joined_classroom_ids_string = self.cursor.execute("SELECT joined_classrooms FROM Users WHERE user_id = ?", (self.__user_id,)).fetchone()[0]
        print(joined_classroom_ids_string)
        if joined_classroom_ids_string:
            joined_classroom_ids = joined_classroom_ids_string.split(" ")
        
        # Stores all to be removed classrooms as they were most likely have been deleted
        classrooms_to_remove = []
        print(joined_classroom_ids)
        # {classroom_id: classroom_name}
        joined_classrooms_dict = {}
        for current_classroom_id in joined_classroom_ids:
            classroom_name = self.cursor.execute("SELECT classroom_name FROM Classroom WHERE classroom_id = ?", ( int(current_classroom_id), )).fetchone()
            # If classroom not found, add it to the trash bin
            if len(classroom_name) == 0:
                classrooms_to_remove.append(current_classroom_id)
            else:
                joined_classrooms_dict[f'{current_classroom_id}'] = classroom_name[0]
        
        # Empty classrooms_to_remove list
        i = 0
        for id_to_remove in classrooms_to_remove:
            for id in joined_classroom_ids:
                if id_to_remove == id:
                    joined_classroom_ids.pop(i)
                    break
                i += 1

        return joined_classrooms_dict
        

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
            'user_id': self.__user_id, 
            'first_name': self.__first_name, 
            'last_name':  self.__last_name, 
            'username':  self.__username, 
            'password':  self.__password}

class Classroom:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.questions = {}

    