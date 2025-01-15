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
    joined_classrooms TEXT 
);'''

# In questions_answers, the format is JSON where the key is the question and the answer as the value
query2 = '''
CREATE TABLE Classroom (
    classroom_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    classroom_name VARCHAR(50),
    author_user_id INT,
    users_joined TEXT,
    questions_answers TEXT 
);'''

# Random queries to test the database
def show_all():
    query3 = 'SELECT * FROM Classroom'
    query4 = 'SELECT * FROM Users'
    print("\n\n")
    print(cursor.execute(query3).fetchall())
    print(cursor.execute(query4).fetchall(), end="\n\n\n")

def del_all():
    query3 = 'DELETE FROM Classroom'
    query4 = 'DELETE FROM Users'
    cursor.execute(query3)
    cursor.execute(query4)

def check_schema():
    print(cursor.execute("PRAGMA table_info(Classroom)").fetchall())

# del_all()
show_all()
sqlite_connection.commit()