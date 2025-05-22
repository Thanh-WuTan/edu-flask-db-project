from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.role_required import role_required
from app.service.main_service import get_department_options, get_schedule_options
from app.db.courses import db_get_filtered_courses, db_get_course_view_by_id
from app.db.enrollment import get_enrolled_students, db_enroll_student, db_unenroll_student
main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    if current_user.is_authenticated and current_user.role == 'instructor':
        return redirect(url_for('instructor.dashboard'))
    if current_user.is_authenticated and current_user.role == 'student':
        return redirect(url_for('student.dashboard'))
    return render_template('index.html', title='Home')

@main.route('/courses/')
@login_required
def courses():
    # Check if user is a guest
    if current_user.is_authenticated and current_user.role == 'guest':
        flash('Guests are not authorized to view courses.', 'danger')
        return redirect(url_for('main.index'))

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
    courses, total = db_get_filtered_courses(search_query, department_id, schedule, instructor_id, page, per_page)

    # Calculate pagination details
    total_pages = (total + per_page - 1) // per_page
    departments = get_department_options()
    schedules = get_schedule_options()

    return render_template('courses.html', courses=courses, page=page, total_pages=total_pages, 
                          search_query=search_query, department_id=department_id or 0, schedule=schedule,
                          instructor_id=instructor_id or 0, departments=departments, schedules=schedules, 
                          instructors=None)

@main.route('/courses/<int:course_id>')
def course_detail(course_id):
    course = db_get_course_view_by_id(course_id)
    enrolled_students = get_enrolled_students(course_id)
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('course_detail.html', title=f'Course Detail - {course["course_name"]}', course=course, enrolled_students=enrolled_students)

@main.route('/courses/<int:course_id>/enroll', methods=['POST'])
@login_required
@role_required('student')
def enroll_student(course_id):
    student_id = request.form.get('student_id')
    if student_id:
        try:
            db_enroll_student(int(student_id), course_id)
            flash('Enrolled successfully!', 'success')
        except Exception as e:
            flash(f'Error enrolling: {str(e)}', 'danger')
    return redirect(url_for('main.course_detail', course_id=course_id))


@main.route('/courses/<int:course_id>/unenroll/<int:student_id>', methods=['POST'])
@login_required
@role_required('student')
def unenroll_student(course_id, student_id):
    try:
        db_unenroll_student(student_id, course_id)
        flash('Unenrolled successfully!', 'success')
    except Exception as e:
        flash(f'Error unenrolling: {str(e)}', 'danger')
    return redirect(url_for('main.course_detail', course_id=course_id))