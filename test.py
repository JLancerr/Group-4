import sqlite3

sqlite_connection = sqlite3.connect('app.db')
cursor = sqlite_connection.cursor()

# All schema of tables in the database
query1 = '''
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    username VARCHAR(20),
    password VARCHAR(20)
);'''

query2 = '''
CREATE TABLE Classrooms (
    classroom_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    classroom_name VARCHAR(40),
    user_parent_id INT
);'''

query3 = '''
CREATE TABLE Subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    subject_name VARCHAR(40),
    classroom_parent_id INT
);'''

query4 = '''
CREATE TABLE Lessons (
    lesson_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    lesson_name VARCHAR(40),
    subjects_parent_id INT
);'''

query5 = '''
CREATE TABLE Questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    question VARCHAR(255),
    answer VARCHAR(100),
    lesson_parent_id INT
);'''

query6 = '''
CREATE TABLE Users_Classrooms_Relationship (
    user_id INT,
    classroom_id INT
)
'''

# Random queries to test the database
def show_all():
    print(cursor.execute("SELECT * FROM Users").fetchall())
    pass

def del_all():
    pass

def check_schema():
    print(cursor.execute("PRAGMA table_info(Classrooms)").fetchall())

if 1:
    show_all()
if 0:
    del_all()
if 0:
    check_schema()

"""cursor.execute("INSERT INTO Classrooms (classroom_name, user_parent_id) VALUES ('DCIT24A', 1)")

cursor.execute("INSERT INTO Users_Classrooms_Relationship (user_id, classroom_id) VALUES (1, 1)")"""

sqlite_connection.commit()