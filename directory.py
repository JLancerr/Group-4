import sqlite3

children_of = {"user" : "classroom",
               "classroom" : "subject",
               "subject" : "lesson",
               "lesson" : "question"}

parent_of = {  "classroom" : "user",
               "subject" : "classroom",
               "lesson" : "subject",
               "question" : "lesson"}

class Directory:
    def __init__(self, args_dict):
        self._directory_name = args_dict.get('directory_name')
        self._directory_type = args_dict.get('directory_type')
        self._directory_id = args_dict.get('directory_id')

        self._children_type = children_of.get(self._directory_type)
        self._parent_type = parent_of.get(self._directory_type)
        self._parent_id = args_dict.get('parent_id')

        if args_dict.get('connection') == None:
            self._sqlite_connection = sqlite3.connect('app.db') 
            self._cursor = self._sqlite_connection.cursor() 
        else:
            self._sqlite_connection = args_dict.get('connection')
            self._cursor = args_dict.get('cursor')

    # Gets all children names and ids of a specific directory
    # This is for the purpose of displaying the sub-directories of a parent directory
    # Example: this code is ran to show all the Lessons contained in a specific Subject
    # Return type: children_names_and_ids{ id : name }
    # Works with classroom, subject, lesson directory types
    # Requires directory_type, directory_id
    def get_directory_contents(self):
        children_names_and_ids = []

        # String variables for creating custom query
        children_id_column_name = f"{self._children_type}_id"
        children_name_column_name = f"{self._children_type}_name"
        children_table_name = f"{self._children_type}s".capitalize()
        parent_id = f"{self._directory_type}_parent_id"

        query = f"SELECT {children_id_column_name}, {children_name_column_name} FROM {children_table_name} WHERE {parent_id} = ?"
        
        ids_and_names = self._cursor.execute(query, (self._directory_id,)).fetchall()

        for given in ids_and_names:
            id = given[0]
            name = given[1]
            children_names_and_ids.append([ id, name ])

        return children_names_and_ids

    # Works with classroom, subject, lesson directory types
    # Requires parent_id, directory_type, and directory_name
    def add_dir_to_database(self):
        
        table_name = f"{self._directory_type}s".capitalize()
        name_column_name = f"{self._directory_type}_name"
        parent_id_column_name = f"{self._parent_type}_parent_id"

        query = f"INSERT INTO {table_name} ({name_column_name}, {parent_id_column_name}) VALUES (?, ?)"
        self._cursor.execute(query, (self._directory_name, self._parent_id))
        self._sqlite_connection.commit()

        return "success"

    # Works with every directory type
    # Needs directory_id and directory_type to delete
    def delete_directory(self): 
        children_ids = self._get_children_directory_ids()

        current_dir_table_name = f"{self._directory_type}s".capitalize()
        current_dir_id_column_name = f"{self._directory_type}_id"
        query = f"DELETE FROM {current_dir_table_name} WHERE {current_dir_id_column_name} = ?"
        
        self._cursor.execute(query, (self._directory_id,))
        self._sqlite_connection.commit()

        if self._children_type == None:
            return 

        for id in children_ids:
            Directory({'directory_type' : self._children_type, 'directory_id' : id}).delete_directory()

    # Edits the name of the given directory type
    # Requires directory_id, directory_type, and new_directory_name
    def edit_directory(self, new_directory_name):
        table_name = f"{self._directory_type}s".capitalize()
        name_column_name = f"{self._directory_type}_name"
        id_column_name = f"{self._directory_type}_id"

        query = f"UPDATE {table_name} SET {name_column_name} = ? WHERE {id_column_name} = ?"
        self._cursor.execute(query, (new_directory_name, self._directory_id))
        self._sqlite_connection.commit()

    def _get_children_directory_ids(self):
        if self._children_type == None:
            return []
        
        children_ids = []

        # String variables for creating custom query
        children_id_column_name = f"{self._children_type}_id"
        children_table_name = f"{self._children_type}s".capitalize()
        parent_id = f"{self._directory_type}_parent_id"

        query = f"SELECT {children_id_column_name} FROM {children_table_name} WHERE {parent_id} = ?"
        queried_ids = self._cursor.execute(query, (self._directory_id,)).fetchall()

        for id in queried_ids:
            children_ids.append(id[0])

        return children_ids

    def get_directory_name_from_database(self):
        name_column_name = f"{self._directory_type}_name"
        table_name = f"{self._directory_type}s".capitalize()
        id_column_name = f"{self._directory_type}_id"
        query = f"SELECT {name_column_name} FROM {table_name} WHERE {id_column_name} = ?"
        return self._cursor.execute(query, (self._directory_id,)).fetchone()[0]
    
    # Requires user_id, directory_type
    def authorize_user(self, user_id):
        target = "user_parent_id"

        current_parent_type = self._parent_type
        current_id = self._directory_id
        current_dir_type = self._directory_type
        while True:
            parent_id_column_name = f"{current_parent_type}_parent_id"
            dir_table_name = f"{current_dir_type}s".capitalize()
            id_column_name = f"{current_dir_type}_id"
            query1 = f"SELECT {parent_id_column_name} FROM {dir_table_name} WHERE {id_column_name} = ?"
            print(query1)
            parent_id = self._cursor.execute(query1, (current_id,)).fetchone()[0]
            if parent_id_column_name != target:
                current_dir_type = current_parent_type
                current_parent_type = parent_of[f'{current_parent_type}']
                current_id = parent_id
            else:
                break
        if parent_id == user_id:
            return "1"
        else:
            return "0"

    def get_directory_name(self):
        return self._directory_name

    def get_directory_type(self):
        return self._directory_type
    
    def get_directory_id(self):
        return self._directory_id
    
    def get_children_type(self):
        return self._children_type
    
    def get_parent_type(self):
        return self._parent_type
    
    def get_parent_id(self):
        return self._parent_id
            

# This Classroom variant of Directory exist cuz classroom needs to access the Users_Classrooms_Relationship to get participators of the classoom
class Classroom(Directory):
    def get_directory_contents(self):
        subjects_names_and_ids = super().get_directory_contents()
        names_of_users_joined = []

        query1 = "SELECT user_id FROM Users_Classrooms_Relationship WHERE classroom_id = ?"
        user_id_list = self._cursor.execute(query1, (self._directory_id,)).fetchall()
        for id in user_id_list:
            query2 = "SELECT first_name, last_name, username FROM Users WHERE user_id = ?"
            user_info = self._cursor.execute(query2, (id[0],)).fetchone()
            names_of_users_joined.append([ id[0], user_info[0], user_info[1], user_info[2] ])

        return [ subjects_names_and_ids, names_of_users_joined ]

# This Lesson variant of Directory exist cuz the child of Lessons is Questions which has an extra column, which is answer, that queries do not account for in the Parent class
class Lesson(Directory):
    def get_directory_contents(self):
        questions_info = []
        query1 = "SELECT question_id, question, answer FROM Questions WHERE lesson_parent_id = ?"
        questions_list = self._cursor.execute(query1, (self._directory_id,)).fetchall()
        for row in questions_list:
            questions_info.append([ row[0], row[1], row[2] ])
        return questions_info

class Question(Directory):
    def __init__(self, args_dict):
        self._question = args_dict.get('question')
        self._answer = args_dict.get('answer')
        super().__init__(args_dict)

    # Requires question, answer, parent_id
    def add_dir_to_database(self):
        query = "INSERT INTO Questions (question, answer, lesson_parent_id) VALUES (?, ?, ?)"
        self._cursor.execute(query, (self._question, self._answer, self._parent_id))
        self._sqlite_connection.commit()

        return "success"
    
    def edit_directory(self, new_question, new_answer):
        if new_question != None:
            query1 = "UPDATE Questions SET question = ? WHERE question_id = ?"
            self._cursor.execute(query1, (new_question, self._directory_id))
        if new_answer != None:
            query2 = "UPDATE Questions SET answer = ? WHERE question_id = ?"
            self._cursor.execute(query2, (new_answer, self._directory_id))
        self._sqlite_connection.commit()

    # This disables this inherited method because Questions does not have any children directories to display
    def get_directory_contents(self):
        return None