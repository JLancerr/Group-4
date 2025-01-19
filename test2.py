from user import *
from directory import *
from test import *
sqlite_connection = sqlite3.connect('app.db')
cursor = sqlite_connection.cursor()

user_info = {
    'user_id' : 9,
    'first_name' : 'Harry',
    'last_name' : 'Harry',
    'username' : 'harryharry',
    'password' : '123'
}
classroom_info = {
    'directory_type' : 'classroom',
    'directory_id' : 18
}
subject_info = {
    'directory_type' : 'subject',
    'directory_name' : 'GNED 04',
    'parent_id' : 18
}
lesson_info = {
    'directory_type' : 'lesson',
    'directory_name' : 'Inheritance',
    'parent_id' : 9
}
ques_info = {
    'question' : 'What is Inheritance?',
    'answer' : 'Inheritance is when you want a variation of an already existing class',
    'parent_id' : 10
}
user = User(user_info)
user.delete_classroom(18)
"""
user.add_classroom("shit")
subject = Directory(subject_info)
subject.add_dir_to_database()

lesson = Directory(lesson_info)
lesson.add_dir_to_database()

ques = Question(ques_info)
ques.add_dir_to_database()
"""
sqlite_connection.commit()