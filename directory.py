import sqlite3

children_of = {"user" : "classroom",
               "classroom" : "subject",
               "subject" : "lesson",
               "lesson" : "question"}

class Directory:
    def __init__(self, directory_type, directory_id):
        self.__directory_type = directory_type
        self.__children_type = children_of["directory_type"]
        self.__directory_id = directory_id
        # self.__parent_id = None

        self.sqlite_connection = sqlite3.connect('app.db')
        self.cursor = self.sqlite_connection.cursor()

    # Gets all children names and ids of a specific directory
    # This is for the purpose of displaying the sub-directories of a parent directory
    # Example: this code is ran to show all the Lessons contained in a specific Subject
    # Return type: children_names_and_ids{ id : name }
    def get_subdirectories_info(self):
        children_names_and_ids = {}

        # String variables for creating custom query
        children_id_column_name = f"{self.__children_type}_id"
        children_name_column_name = f"{self.__children_type}_name"
        children_table_name = f"{self.__children_type}s".capitalize()
        parent_id = f"{self.__directory_type}_id"

        query = f"SELECT {children_id_column_name}, {children_name_column_name} FROM {children_table_name} WHERE {parent_id} = ?"
        ids_and_names = self.cursor.execute(query, (self.__directory_id,)).fetchall()

        for given in ids_and_names:
            id = given[0]
            name = given[1]
            children_names_and_ids[id] = name

        return children_names_and_ids

    def add(self):
        pass

class Classroom(Directory):
    def __init__(self, user_id):
        super().__init__("classroom", user_id)

    # Gets all names, ids, author's info, and participators' info of all classrooms the user is joined in
    # Return type: classroom_list[ classroom_information[classroom_id, classroom_name, author_info[], participator_list[ participator_info[] ] ]
    def get_subdirectories_info(self):

        classroom_list = []
        classroom_names_and_ids = super().get_subdirectories_info()

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

            