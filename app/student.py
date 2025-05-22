from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required
from app.role_required import role_required
from app.service.student_service import get_course_by_student_id
from app.service.auth_service import authenticate_user
from app.service.admin_service import (
    get_course_details_service, get_available_students_service
)

from app.db.users import User

student = Blueprint('student', __name__)

@student.route('/', methods=['GET', 'POST'])
def student_login():
    if current_user.is_authenticated and current_user.role == 'student':
        return redirect(url_for('student.dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user, error = authenticate_user(email, password)
        if user:
            if user['role_name'] == 'student':
                login_user(User(user))
                flash('Logged in successfully!', 'success')
                return redirect(url_for('student.dashboard'))
            else:
                flash('You do not have student access.', 'danger')
        else:
            flash(error, 'danger')
    return render_template('student/login.html', title='Student Login')

@student.route('/dashboard')
@login_required
@role_required('student')
def dashboard():
    return render_template('student/dashboard.html', title='Student Dashboard')

@student.route('/dashboard/courses/', methods=['GET', 'POST'])
@login_required
@role_required('student')
def courses():
    students_id = current_user.id
    courses = get_course_by_student_id(students_id)
    return render_template('student/courses.html', title='My Courses', courses=courses)


@student.route('/dashboard/courses/<int:course_id>')
@login_required
@role_required('student')
def course_detail(course_id):
    course, enrolled_students = get_course_details_service(course_id)
    available_students = get_available_students_service(course_id)

    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('student.courses'))
        
    return render_template('student/course_detail.html', title=f'Course Detail - {course["course_name"]}', 
                          course=course, enrolled_students=enrolled_students, available_students=available_students)
