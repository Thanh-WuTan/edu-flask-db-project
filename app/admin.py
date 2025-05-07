from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required
from app.service.auth_service import authenticate_user
from app.service.admin_service import get_all_courses_logic, delete_course_logic, get_all_users_logic, delete_user_logic
from app.db.users import User

admin = Blueprint('admin', __name__)

@admin.route('/', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user, error = authenticate_user(email, password)
        if user:
            if user['role_name'] == 'admin':
                login_user(User(user))
                flash('Logged in successfully!', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('You do not have admin access.', 'danger')
        else:
            flash(error, 'danger')
    return render_template('admin/login.html', title='Admin Login')

@admin.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('admin/dashboard.html', title='Admin Dashboard')

@admin.route('/dashboard/courses/', methods=['GET', 'POST'])
@login_required
def courses():
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        if course_id:
            try:
                delete_course_logic(course_id)
                flash('Course deleted successfully!', 'success')
            except Exception as e:
                flash(f'Error deleting course: {str(e)}', 'danger')
            return redirect(url_for('admin.courses'))
    courses = get_all_courses_logic()
    return render_template('admin/courses.html', title='Courses Dashboard', courses=courses)

@admin.route('/dashboard/users/', methods=['GET', 'POST'])
@login_required
def users():
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        if user_id:
            try:
                delete_user_logic(user_id)
                flash('User deleted successfully!', 'success')
            except Exception as e:
                flash(f'Error deleting user: {str(e)}', 'danger')
            return redirect(url_for('admin.users'))
    users = get_all_users_logic()
    return render_template('admin/users.html', title='Users Dashboard', users=users)