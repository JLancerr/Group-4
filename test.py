import sqlite3

sqlite_connection = sqlite3.connect('app.db')
cursor = sqlite_connection.cursor()

# In joined_classes, it contains the class_id of each classrooms that the user is joined in 
# The format goes like "123 321 333" which represent three classes the user is joined in with a space as a delimiter

query1 = '''
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    username VARCHAR(20),
    password VARCHAR(20),
    joined_classes TEXT 
);'''

# In questions_answers, the format is JSON where the key is the question and the answer as the value
query2 = '''
CREATE TABLE Class (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    class_name VARCHAR(50),
    questions_answers TEXT 
);'''

# Random queries to test the database
query3 = 'SELECT * FROM Users'
query4 = "INSERT INTO Users (first_name, last_name, username, password) VALUES ('Harry', 'Emelo', 'harharemem', 'em')"
query5 = "PRAGMA table_info(Users);"
query6 = "ALTER TABLE Users ADD joined_classes TEXT;"

data = cursor.execute(query5).fetchall()
print(data)

sqlite_connection.commit()