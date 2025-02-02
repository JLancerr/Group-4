import sqlite3
from directory import *
from datetime import date, timedelta

children_of = {"user" : "classroom",
               "classroom" : "subject",
               "subject" : "lesson",
               "lesson" : "question"}

class User:
    def __init__(self, args_dict):
        self.__user_id = args_dict.get('user_id')
        self.__first_name = args_dict.get('first_name')
        self.__last_name = args_dict.get('last_name')
        self.__username = args_dict.get('username')
        self.__password = args_dict.get('password')
        self.__membership_type = args_dict.get('membership_type')
        self.__expiration_date = args_dict.get('membership_type')

        if args_dict.get('connection') == None:
            self.__sqlite_connection = sqlite3.connect('app.db') 
            self.__cursor = self.__sqlite_connection.cursor() 
        else:
            self.__sqlite_connection = args_dict.get('connection')
            self.__cursor = args_dict.get('cursor')

    def signup(self):
        # Check if username already exists in the database
        usernames = self.__cursor.execute('SELECT username FROM Users WHERE username = ?;', (self.__username,)).fetchall()
        # If username already exists, signup fails
        if len(usernames) > 0:
            return "username-already-exists"
        # If username does not exist in the database, insert user's info into the Users table
        else:
            self.__cursor.execute("INSERT INTO Users (first_name, last_name, username, password, membership_type) VALUES (?, ?, ?, ?, ?);", 
                           (self.__first_name, self.__last_name, self.__username, self.__password, 'free'))
            
            self.__user_id = self.__cursor.execute("SELECT user_id FROM Users WHERE username = ?", (self.__username,)).fetchone()[0]
            self.__sqlite_connection.commit()
            return "success"
        
    def login(self):
        # Check if username already exists in the database
        username = self.__cursor.execute('SELECT username FROM Users WHERE username = ?;', (self.__username,)).fetchall()
        # If username does not exist, login attempt fails
        if len(username) == 0:
            return "username-not-found"

        # If username exists but password does not match the user's given password
        # data[password][first_name][last_name][user_id][membership_type][expiration_date]
        data = self.__cursor.execute('SELECT password, first_name, last_name, user_id, membership_type, expiration_date FROM Users WHERE username = ?;', (username[0][0],)).fetchall()
        if self.__password != data[0][0]:
            return "password-incorrect"
        
        # Initiliazed these vars as user is verified
        self.__first_name = data[0][1]
        self.__last_name = data[0][2]
        self.__user_id = data[0][3]
        self.__membership_type = data[0][4]
        self.__expiration_date = data[0][5]
        return "success"

    # Gets info of user's joined and authored classrooms
    def get_classrooms_info(self):
        authored_classroom_names_and_ids = {}
        joined_classroom_names_and_ids = {}

        # Retrieve the user's authored classrooms
        query1 = "SELECT classroom_id, classroom_name FROM Classrooms WHERE user_parent_id = ?"
        ids_and_names = self.__cursor.execute(query1, (self.__user_id,)).fetchall()

        for given in ids_and_names:
            id = given[0]
            name = given[1]
            authored_classroom_names_and_ids[id] = name

        # Retrieve classrooms the user is joined in but not authored
        query2 = "SELECT classroom_id FROM Users_Classrooms_Relationship WHERE user_id = ?"
        query3 = "SELECT classroom_name FROM Classrooms WHERE classroom_id = ? AND user_parent_id != ?"
        classroom_ids = self.__cursor.execute(query2, (self.__user_id,)).fetchall()
        for id in classroom_ids:
            joined_classroom_name = self.__cursor.execute(query3, (id[0], self.__user_id)).fetchone()
            if joined_classroom_name != None:
                joined_classroom_names_and_ids[id[0]] = joined_classroom_name[0]

        return [authored_classroom_names_and_ids, joined_classroom_names_and_ids]

    def add_classroom(self, classroom_name):
        # Disallow multiple classrooms to have the same name and the same author
        query = "SELECT classroom_id FROM Classrooms WHERE classroom_name = ? AND user_parent_id = ?"
        duplicate_classrooms = self.__cursor.execute(query, (classroom_name, self.__user_id)).fetchall()
        if len(duplicate_classrooms) > 0:
            return "no-duplicated-classrooms"

        # Disallow more than 3 classrooms if user is not member
        if self.__membership_type != 'pro':
            query4 = "SELECT COUNT(classroom_id) FROM Classrooms WHERE user_parent_id = ?"
            classroom_count = self.__cursor.execute(query4, (self.__user_id,)).fetchone()[0]
            if classroom_count >= limit['classroom']:
                return "reached-classroom-limit"

        query1 = "INSERT INTO Classrooms (classroom_name, user_parent_id) VALUES (?, ?)"
        self.__cursor.execute(query1, (classroom_name, self.__user_id))

        # If the error handling before is not implemented, this might fail
        query2 = "SELECT classroom_id FROM Classrooms WHERE classroom_name = ? AND user_parent_id = ?"
        classroom_id = self.__cursor.execute(query2, (classroom_name, self.__user_id)).fetchone()[0]

        query3 = "INSERT INTO Users_Classrooms_Relationship (user_id, classroom_id) VALUES (?, ?)"
        self.__cursor.execute(query3, (self.__user_id, classroom_id))

        self.__sqlite_connection.commit()
        return "success"
    
    def join_classroom(self, classroom_id):
        query3 = "SELECT classroom_id FROM Classrooms WHERE classroom_id = ?"
        found_classroom = self.__cursor.execute(query3, (classroom_id,)).fetchone()

        if found_classroom == None:
            return "classroom-does-not-exist"

        query1 = "SELECT user_id FROM Users_Classrooms_Relationship WHERE user_id = ? AND classroom_id = ?"
        duplicates = self.__cursor.execute(query1, (self.__user_id, classroom_id)).fetchall()
        if len(duplicates) > 0:
            return "already-joined-classroom"

        query4 = "SELECT membership_type FROM Users WHERE user_id = (SELECT user_parent_id FROM Classrooms WHERE classroom_id = ? LIMIT 1)"
        author_membership_type = self.__cursor.execute(query4, (classroom_id,)).fetchone()[0]
        print(author_membership_type)
        if author_membership_type != 'pro':
            query3 = "SELECT COUNT(user_id) FROM Users_Classrooms_Relationship WHERE classroom_id = ?"
            user_joined_count = self.__cursor.execute(query3, (classroom_id,)).fetchone()[0]
            print(user_joined_count)
            if user_joined_count >= limit['student']:
                return "classroom-full"

        query2 = "INSERT INTO Users_Classrooms_Relationship (user_id, classroom_id) VALUES (?, ?)"
        self.__cursor.execute(query2, (self.__user_id, classroom_id))
        self.__sqlite_connection.commit()
        return "success"
    
    def leave_classroom(self, classroom_id):
        # If the user leaving the classroom is the author of that classroom, delete the classroom
        query1 = "SELECT user_parent_id FROM Classrooms WHERE classroom_id = ?"
        user_parent_id = self.__cursor.execute(query1, (classroom_id,)).fetchone()

        if user_parent_id[0] == self.__user_id:
            Classroom({'directory_id' : classroom_id}).delete_directory()

        query2 = "DELETE FROM Users_Classrooms_Relationship WHERE user_id = ? AND classroom_id = ?"
        self.__cursor.execute(query2, (self.__user_id, classroom_id))
        self.__sqlite_connection.commit()
        return "success"

    def kick_user(self, user_id_to_kick, classroom_id):
        query = "DELETE FROM Users_Classrooms_Relationship WHERE user_id = ? AND classroom_id = ?"
        self.__cursor.execute(query, (user_id_to_kick, classroom_id))
        self.__sqlite_connection.commit()
        return "success"

    def rename_classroom(self, classroom_id, new_classroom_name):
        query = "UPDATE Classrooms SET classroom_name = ? WHERE classroom_id = ?"
        self.__cursor.execute(query, (new_classroom_name, classroom_id))
        self.__sqlite_connection.commit()
        return "success"

    def edit_profile(self, column_to_update, new_value):
        if column_to_update == 'username':
            info = self.__cursor.execute('SELECT user_id, username FROM Users WHERE username = ?;', (new_value,)).fetchall()
            if len(info) > 0:
                if int(info[0][0]) != int(self.__user_id):
                    return "username-already-exists"
            
        query1 = f"UPDATE Users SET {column_to_update} = ? WHERE user_id = ?"
        self.__cursor.execute(query1, (new_value, self.__user_id))
        self.__sqlite_connection.commit()
        return "success"

    def upgrade_plan(self, duration_option):
        options = {
            'option_1' : 365,
            'option_2' : 182
        }
        query1 = "SELECT membership_type, expiration_date FROM Users WHERE user_id = ?"
        membership_info = self.__cursor.execute(query1, (self.__user_id,)).fetchone()
        if membership_info[0] == 'free':
            membership_expiration_date = str(date.today() + timedelta(days = options[f'{duration_option}']))
        else:
            membership_expiration_date = str(date.fromisoformat(membership_info[1]) + timedelta(days = options[f'{duration_option}']))
        query2 = "UPDATE Users SET membership_type = 'pro', expiration_date = ? WHERE user_id = ?"
        self.__cursor.execute(query2, (membership_expiration_date, self.__user_id))
        self.__sqlite_connection.commit()

    def delete_self(self):
        args_dict = {
            'directory_id' : self.__user_id,
            'directory_type' : "user"
        }
        Directory(args_dict).delete_directory()

    def get_all_attributes(self):
        query = 'SELECT * FROM Users WHERE user_id = ?'
        info = self.__cursor.execute(query, (self.__user_id,)).fetchone()
        return {
            'user_id': info[0], 
            'first_name': info[1], 
            'last_name':  info[2], 
            'username':  info[3], 
            'password':  info[4], 
            'membership_type':  info[5],
            'expiration_date':  info[6]}

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
    
    def get_membership_type(self):
        return self.__membership_type
    
    def get_expiration_date(self):
        return self.__expiration_date
    
    # # Returns all attributes in dictionary form
    # def get_all_attributes(self):
    #     return {
    #         'user_id': self.__user_id, 
    #         'first_name': self.__first_name, 
    #         'last_name':  self.__last_name, 
    #         'username':  self.__username, 
    #         'password':  self.__password, 
    #         'membership_type':  self.__membership_type,
    #         'expiration_date':  self.__expiration_date}

