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
    'directory_id' : 26
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

c = Directory(classroom_info)
print(c.get_directory_contents())
sqlite_connection.commit()