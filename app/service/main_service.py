from app.db.departments import db_get_all_departments
from app.db.courses import db_get_course_view_by_id
from app.db.enrollment import get_enrolled_students, db_enroll_student, db_unenroll_student
from app.db.users import db_get_all_users

def get_department_options():
    departments = db_get_all_departments()
    return [(0, 'All Departments')] + [(d[0], d[1]) for d in departments]

def get_schedule_options():
    return [
        ('', 'All Schedules'),
        ('M', 'Monday'),
        ('T', 'Tuesday'),
        ('W', 'Wednesday'),
        ('R', 'Thursday'),
        ('F', 'Friday')
    ]

def get_course_details_service(course_id):
    course = db_get_course_view_by_id(course_id)
    enrolled_students = get_enrolled_students(course_id)
    return course, enrolled_students

def get_instructor_choices():
    users = db_get_all_users()
    return [(user['id'], user['username']) for user in users if user['role_name'] == 'instructor']

def enroll_student_service(student_id, course_id):
    db_enroll_student(student_id, course_id)

def unenroll_student_service(student_id, course_id):
    db_unenroll_student(student_id, course_id)