from app.db.users import get_all_users, delete_user
from app.db.courses import get_all_courses, delete_course

def get_all_courses_logic():
    return get_all_courses()

def delete_course_logic(course_id):
    delete_course(course_id)

def get_all_users_logic():
    return get_all_users()

def delete_user_logic(user_id):
    delete_user(user_id)