from app.db.courses import get_filtered_courses
from app.db.departments import get_all_departments

def get_courses_with_filters(search_query=None, department_id=None, schedule=None, instructor_id=None, page=1, per_page=10):
    courses, total = get_filtered_courses(search_query, department_id, schedule, instructor_id, page, per_page)
    return courses, total

def get_department_options():
    departments = get_all_departments()
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
