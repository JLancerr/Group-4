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
    print("Users: " + str(cursor.execute("SELECT * FROM Users").fetchall()))
    print("Classrooms: " + str(cursor.execute("SELECT * FROM Classrooms").fetchall()))
    print("Subjects: " + str(cursor.execute("SELECT * FROM Subjects").fetchall()))
    print("Lessons: " + str(cursor.execute("SELECT * FROM Lessons").fetchall()))
    print("Questions: " + str(cursor.execute("SELECT * FROM Questions").fetchall()))
    print("Rels: " + str(cursor.execute("SELECT * FROM Users_Classrooms_Relationship").fetchall()))

def del_all():
    cursor.execute("DELETE FROM Users_Classrooms_Relationship WHERE 1")
    cursor.execute("DELETE FROM Classrooms WHERE 1")
    cursor.execute("DELETE FROM Subjects WHERE 1")
    cursor.execute("DELETE FROM Lessons WHERE 1")
    cursor.execute("DELETE FROM Questions WHERE 1")

def check_schema():
    print(cursor.execute("PRAGMA table_info(Classrooms)").fetchall())


if 0:
    del_all()
if 1:
    show_all()
if 0:
    check_schema()

sqlite_connection.commit()