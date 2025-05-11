from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required
from app.service.auth_service import authenticate_user
from app.service.instructor_service import get_all_courses_from_instructor_service
from app.forms import CreateUserForm, UpdateUserForm, CourseForm, CourseInstructorForm

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
def dashboard():
    if current_user.role != 'instructor':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('instructor/dashboard.html', title='Instructor Dashboard')

@instructor.route('/dashboard/courses/', methods=['GET', 'POST'])
@login_required
def courses():
    if current_user.role != 'instructor':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    # if request.method == 'POST':
    #     course_id = request.form.get('course_id')
    #     if course_id:
    #         try:
    #             delete_course_service(course_id)
    #             flash('Course deleted successfully!', 'success')
    #         except Exception as e:
    #             flash(f'Error deleting course: {str(e)}', 'danger')
    #         return redirect(url_for('admin.courses'))
    current_user_id = current_user.id
    courses = get_all_courses_from_instructor_service(current_user_id)
    # Populate instructor choices dynamically
    # users = get_all_users()
    # instructors = [(user['id'], user['username']) for user in users if user['role_name'] == 'instructor']
    course_form = CourseInstructorForm()
    # course_form.instructor_id.choices = instructors 
    return render_template('instructor/courses.html', title='Courses Dashboard', courses=courses, course_form=course_form)
