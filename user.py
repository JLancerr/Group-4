import sqlite3

children_of = {"user" : "classroom",
               "classroom" : "subject",
               "subject" : "lesson",
               "lesson" : "question"}

class User:
    def __init__(self, user_id, first_name, last_name, username, password):
        self.__user_id = user_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__username = username
        self.__password = password

        self.sqlite_connection = sqlite3.connect('app.db') # Connects to the database
        self.cursor = self.sqlite_connection.cursor() # Creates instance of a cursor which is used for executing queries

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

    def get_subdirectories_info(self, directory_type, directory_id):
        children_type = children_of[directory_type]
        children_names_and_ids = {}

        # String variables for creating custom query
        children_id_column_name = f"{children_type}_id"
        children_name_column_name = f"{children_type}_name"
        children_table_name = f"{children_type}s".capitalize()
        parent_id = f"{directory_type}_id"

        query = f"SELECT {children_id_column_name}, {children_name_column_name} FROM {children_table_name} WHERE {parent_id} = ?"
        ids_and_names = self.cursor.execute(query, (directory_id,)).fetchall()

        for given in ids_and_names:
            id = given[0]
            name = given[1]
            children_names_and_ids[id] = name

        return children_names_and_ids   

    def get_classrooms_info(self):

        classroom_list = []
        classroom_names_and_ids = User.get_subdirectories_info("classroom", self.__user_id)

        # Loop through each classroom
        for id in classroom_names_and_ids:
            classroom_information = []
            classroom_information.append(id, classroom_names_and_ids[id])

            # Query the author id
            query1 = "SELECT user_parent_id FROM Classrooms WHERE classroom_id = ?"
            author_id = self.cursor.execute(query1, (id,)).fetchone()[0]

            # Query the author info
            query2 = "SELECT first_name, last_name, username FROM Users WHERE user_id = ?"
            # Return type: (first_name, last_name, username)
            author_info = self.cursor.execute(query2, (author_id,)).fetchone()
            classroom_information.append(list(author_info))

            # Query the participators' id of the given classroom
            query3 = "SELECT user_id FROM Users_Classrooms_Relationship WHERE classroom_id = ?"
            participator_ids = self.cursor.execute(query3, (id,)).fetchall()

            # Get all participators' info of the given classroom
            participator_list = []
            for user_id in participator_ids:
                query4 = "SELECT first_name, last_name, username FROM Users WHERE user_id = ?"
                participator_info = self.cursor.execute(query4, (user_id,)).fetchone()
                participator_list.append(list(participator_info))

            classroom_information.append(participator_list)

        return classroom_list

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

