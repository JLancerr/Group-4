# This doesn't work, just a file to store unused code
class User:
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