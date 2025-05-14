from flask import Blueprint, render_template, request
from app.service.main_service import get_courses_with_filters, get_department_options, get_schedule_options

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', title='Home')


@main.route('/courses/')
def courses():
    # Get query parameters
    page = int(request.args.get('page', 1))
    per_page = 10
    search_query = request.args.get('search', '').strip()
    department_id = request.args.get('department_id', '')
    department_id = int(department_id) if department_id.isdigit() and int(department_id) > 0 else None
    schedule = request.args.get('schedule', '')
    instructor_id = request.args.get('instructor_id', '')
    instructor_id = int(instructor_id) if instructor_id.isdigit() and int(instructor_id) > 0 else None

    # Fetch courses with filters
    courses, total = get_courses_with_filters(search_query, department_id, schedule, instructor_id, page, per_page)

    # Calculate pagination details
    total_pages = (total + per_page - 1) // per_page
    departments = get_department_options()
    schedules = get_schedule_options()

    return render_template('courses.html', courses=courses, page=page, total_pages=total_pages, 
                          search_query=search_query, department_id=department_id or 0, schedule=schedule,
                          instructor_id=instructor_id or 0, departments=departments, schedules=schedules, 
                          instructors=None)