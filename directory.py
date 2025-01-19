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

        self._sqlite_connection = sqlite3.connect('app.db')
        self._cursor = self._sqlite_connection.cursor()

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

    # Most likely works with every directory type
    # Needs directory_id to delete
    def delete_directory(self): 
        dir_contents = self.get_directory_contents()
        if dir_contents == None:
            dir_contents = []

        current_dir_table_name = f"{self._directory_type}s".capitalize()
        current_dir_id_column_name = f"{self._directory_type}_id"
        query = f"DELETE FROM {current_dir_table_name} WHERE {current_dir_id_column_name} = ?"
        
        self._cursor.execute(query, (self._directory_id,))
        self._sqlite_connection.commit()

        if self._children_type == None:
            return 
        
        for content in dir_contents:
            if self._children_type == 'lesson':
                Lesson({'directory_type' : self._children_type, 'directory_id' : content[0]}).delete_directory()
            elif self._children_type == 'question':
                Question({'directory_type' : self._children_type, 'directory_id' : content[0]}).delete_directory()
            else:
                Directory({'directory_type' : self._children_type, 'directory_id' : content[0]}).delete_directory()


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
            print(id)
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

    # This disables this inherited method because Questions does not have any children directories to display
    def get_directory_contents(self):
        return None

    # Requires question, answer, parent_id
    def add_dir_to_database(self):
        query = "INSERT INTO Questions (question, answer, lesson_parent_id) VALUES (?, ?, ?)"
        self._cursor.execute(query, (self._question, self._answer, self._parent_id))
        self._sqlite_connection.commit()

        return "success"