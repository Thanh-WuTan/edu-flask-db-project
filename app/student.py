from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required
from app.service.student_service import get_course_by_student_id
from app.service.auth_service import authenticate_user

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
