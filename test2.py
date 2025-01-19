from user import *
from directory import *

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
    'directory_id' : 22
}
subject_info = {
    'directory_id' : 17,
    'directory_type' : 'subject',
    'directory_name' : 'GNED 04',
    'parent_id' : 23
}
lesson_info = {
    'directory_type' : 'lesson',
    'directory_name' : 'Inheritance',
    'parent_id' : 17
}
ques_info = {
    'directory_id' : 16,
    'question' : 'What is Inheritance?',
    'answer' : 'Inheritance is when you want a variation of an already existing class',
    'parent_id' : 18
}
user = User(user_info)
"""
user.rename_classroom(23, "LMfAO")

user.add_classroom(20)


subject = Directory(subject_info)
subject.edit_directory("DCIT24A")


lesson = Directory(lesson_info)
lesson.add_dir_to_database()
"""
ques = Question(ques_info)
ques.edit_directory("What is Polymorphism", "Not this one lol")


sqlite_connection.commit()