from app.db.courses import get_filtered_courses, db_get_course_by_instructor_id

def get_all_courses_from_instructor_service(instructor_id: int):
    return get_filtered_courses(instructor_id=instructor_id)

def get_course_by_instructor_id(instructor_id: int):
    return db_get_course_by_instructor_id(instructor_id)



