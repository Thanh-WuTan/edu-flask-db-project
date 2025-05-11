from app.db.users import get_all_users, delete_user, create_user, update_user
from app.db.courses import get_all_courses_by_instructor, delete_course, create_course, update_course

def get_all_courses_from_instructor_service(instructor_id: int):
    return get_all_courses_by_instructor(instructor_id)