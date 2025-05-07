from app.db.users import get_all_users, delete_user, create_user, update_user
from app.db.courses import get_all_courses, delete_course, create_course, update_course

def get_all_courses_service():
    return get_all_courses()

def delete_course_service(course_id):
    delete_course(course_id)

def add_course_service(course_name, department_id, instructor_id, location, schedule, semester):
    create_course(course_name, department_id, instructor_id, location, schedule, semester)

def edit_course_service(course_id, course_name, department_id, instructor_id, location, schedule, semester):
    update_course(course_id, course_name, department_id, instructor_id, location, schedule, semester)

def get_all_users_service():
    return get_all_users()

def delete_user_service(user_id):
    delete_user(user_id)

def add_user_service(email, username, password, role_name, phone, department_id):
    create_user(email, username, password, role_name, phone, department_id)

def edit_user_service(user_id, username, email, role_name, phone, department_id):
    update_user(user_id, username, email, role_name, phone, department_id)