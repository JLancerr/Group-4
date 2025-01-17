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
        self.__directory_name = args_dict.get('directory_name')
        self.__directory_type = args_dict.get('directory_type')
        self.__directory_id = args_dict.get('directory_id')

        self.__children_type = children_of.get(self.__directory_type)
        self.__parent_type = parent_of.get(self.__directory_type)
        self.__parent_id = args_dict.get('parent_id')

        self.__sqlite_connection = sqlite3.connect('app.db')
        self.__cursor = self.__sqlite_connection.cursor()

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
        ids_and_names = self.__cursor.execute(query, (self.__directory_id,)).fetchall()

        for given in ids_and_names:
            id = given[0]
            name = given[1]
            children_names_and_ids[id] = name

        return children_names_and_ids

    def add_dir_to_database(self):
        
        table_name = f"{self.__directory_type}".capitalize()
        name_column_name = f"{self.__directory_type}_name"
        parent_id_column_name = f"{self.__parent_type}_parent_id"

        query = f"INSERT INTO {table_name} ({name_column_name}, {parent_id_column_name}) VALUES (?, ?)"
        self.__cursor.execute(query, (self.__directory_name, self.__parent_id))
        self.__sqlite_connection.commit()

        return "success"

    def delete_directory(self):
        pass

    def get_directory_name(self):
        return self.__directory_name
    
    def get_directory_type(self):
        return self.__directory_type
    
    def get_directory_id(self):
        return self.__directory_id
    
    def get_children_type(self):
        return self.__children_type
    
    def get_parent_type(self):
        return self.__parent_type
    
    def get_parent_id(self):
        return self.__parent_id
            