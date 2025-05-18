from app.db.courses import get_filtered_courses, db_get_course_by_student_id

def get_all_courses_from_students_service(students_id: int):
    return get_filtered_courses(students_id=students_id)


def get_course_by_student_id(students_id: int):
    return db_get_course_by_student_id(students_id)