from app.db.courses import get_filtered_courses

def get_all_courses_from_instructor_service(instructor_id: int):
    return get_filtered_courses(instructor_id=instructor_id)