from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required
from app.service.student_service import get_course_by_student_id
from app.service.auth_service import authenticate_user
from app.service.admin_service import (
    get_all_courses_service, delete_course_service, get_all_users_service, 
    delete_user_service, add_user_service, edit_user_service, add_course_service, 
    edit_course_service, get_course_details_service, get_user_role_counts_service, 
    get_course_department_counts_service, get_student_department_counts_service, get_available_students_service, enroll_student_service, unenroll_student_service
)
from app.forms import CreateUserForm, UpdateUserForm, CourseForm, CourseInstructorForm

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
def dashboard():
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('student/dashboard.html', title='Student Dashboard')

@student.route('/dashboard/courses/', methods=['GET', 'POST'])
@login_required
def courses():
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    students_id = current_user.id
    courses = get_course_by_student_id(students_id)
    return render_template('student/courses.html', title='My Courses', courses=courses)


@student.route('/dashboard/courses/<int:course_id>')
@login_required
def course_detail(course_id):
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    
    course, enrolled_students = get_course_details_service(course_id)
    available_students = get_available_students_service(course_id)

    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('student.courses'))
        
    return render_template('student/course_detail.html', title=f'Course Detail - {course["course_name"]}', 
                          course=course, enrolled_students=enrolled_students, available_students=available_students)
