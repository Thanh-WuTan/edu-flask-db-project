from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required
from app.role_required import role_required
from app.service.auth_service import authenticate_user
from app.service.instructor_service import get_course_by_instructor_id
from app.service.admin_service import (
    get_course_details_service,  
    get_available_students_service, 
    enroll_student_service, unenroll_student_service
)
from app.db.users import User

instructor = Blueprint('instructor', __name__)

@instructor.route('/', methods=['GET', 'POST'])
def instructor_login():
    if current_user.is_authenticated and current_user.role == 'instructor':
        return redirect(url_for('instructor.dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user, error = authenticate_user(email, password)
        if user:
            if user['role_name'] == 'instructor':
                login_user(User(user))
                flash('Logged in successfully!', 'success')
                return redirect(url_for('instructor.dashboard'))
            else:
                flash('You do not have instructor access.', 'danger')
        else:
            flash(error, 'danger')
    return render_template('instructor/login.html', title='Instructor Login')

@instructor.route('/dashboard')
@login_required
@role_required('instructor')
def dashboard():
    return render_template('instructor/dashboard.html', title='Instructor Dashboard')

@instructor.route('/dashboard/courses/', methods=['GET', 'POST'])
@login_required
@role_required('instructor')
def courses():
    instructor_id = current_user.id
    courses = get_course_by_instructor_id(instructor_id)
    print("Fetched courses:", courses)  # DEBUG LINE
    return render_template('instructor/courses.html', title='My Courses', courses=courses)

@instructor.route('/dashboard/courses/<int:course_id>')
@login_required
@role_required('instructor')
def course_detail(course_id):
    course, enrolled_students = get_course_details_service(course_id)
    available_students = get_available_students_service(course_id)

    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('instructor.courses'))
    
    return render_template('instructor/course_detail.html', title=f'Course Detail - {course["course_name"]}', 
                          course=course, enrolled_students=enrolled_students, available_students=available_students)


@instructor.route('/dashboard/courses/<int:course_id>/enroll', methods=['POST'])
@login_required
@role_required('instructor')
def enroll_student(course_id):
    student_id = request.form.get('student_id')
    if student_id:
        try:
            enroll_student_service(int(student_id), course_id)
            flash('Student enrolled successfully!', 'success')
        except Exception as e:
            flash(f'Error enrolling student: {str(e)}', 'danger')
    return redirect(url_for('instructor.course_detail', course_id=course_id))


@instructor.route('/dashboard/courses/<int:course_id>/unenroll/<int:student_id>', methods=['POST'])
@login_required
@role_required('instructor')
def unenroll_student(course_id, student_id):
    try:
        unenroll_student_service(student_id, course_id)
    except Exception as e:
        flash(f'Error unenrolling student: {str(e)}', 'danger')
    return redirect(url_for('instructor.course_detail', course_id=course_id))
