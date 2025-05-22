from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required
from app.service.auth_service import authenticate_user
from app.service.admin_service import (
    get_instructor_choices,
    get_all_courses_service, delete_course_service, get_filtered_users_service, 
    delete_user_service, add_user_service, edit_user_service, add_course_service, 
    edit_course_service, get_course_details_service, get_user_role_counts_service, 
    get_course_department_counts_service, get_student_department_counts_service, get_available_students_service, enroll_student_service, unenroll_student_service
)
from app.db.users import User
from app.db.departments import get_all_departments
from app.forms import CreateUserForm, UpdateUserForm, CourseForm

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
    
    user_role_counts = get_user_role_counts_service()
    course_dept_counts = get_course_department_counts_service()
    student_dept_counts = get_student_department_counts_service()

    return render_template('admin/dashboard.html', title='Admin Dashboard', 
                          user_role_counts=user_role_counts, course_dept_counts=course_dept_counts, student_dept_counts=student_dept_counts)

@admin.route('/dashboard/courses/')
@login_required
def courses():
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    
    # Pagination and search parameters
    page = int(request.args.get('page', 1))
    per_page = 10
    search_query = request.args.get('search', '').strip()
    
    # Fetch courses with search filter
    courses, total = get_all_courses_service(page=page, per_page=per_page, search_query=search_query)
    total_pages = (total + per_page - 1) // per_page

    # Populate instructor choices dynamically
    
    course_form = CourseForm()
    course_form.instructor_id.choices = get_instructor_choices()
    return render_template('admin/courses.html', title='Courses Dashboard', courses=courses, 
                          course_form=course_form, page=page, total_pages=total_pages)

@admin.route('/dashboard/courses/delete/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('admin.courses'))
    try:
        delete_course_service(course_id)
        flash('Course deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting course: {str(e)}', 'danger')
    return redirect(url_for('admin.courses'))

@admin.route('/dashboard/courses/<int:course_id>')
@login_required
def course_detail(course_id):
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    
    course, enrolled_students = get_course_details_service(course_id)
    available_students = get_available_students_service(course_id)

    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('admin.courses'))
    
    return render_template('admin/course_detail.html', title=f'Course Detail - {course["course_name"]}', 
                          course=course, enrolled_students=enrolled_students, available_students=available_students)


@admin.route('/dashboard/courses/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll_student(course_id):
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('admin.course_detail', course_id=course_id))
    
    student_id = request.form.get('student_id')
    if student_id:
        try:
            enroll_student_service(int(student_id), course_id)
            flash('Student enrolled successfully!', 'success')
        except Exception as e:
            flash(f'Error enrolling student: {str(e)}', 'danger')
    return redirect(url_for('admin.course_detail', course_id=course_id))


@admin.route('/dashboard/courses/<int:course_id>/unenroll/<int:student_id>', methods=['POST'])
@login_required
def unenroll_student(course_id, student_id):
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('admin.course_detail', course_id=course_id))
    
    try:
        unenroll_student_service(student_id, course_id)
    except Exception as e:
        flash(f'Error unenrolling student: {str(e)}', 'danger')
    return redirect(url_for('admin.course_detail', course_id=course_id))

@admin.route('/dashboard/courses/add', methods=['POST'])
@login_required
def add_course():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('admin.courses'))
    form = CourseForm()
    form.instructor_id.choices = get_instructor_choices()
    if form.validate_on_submit():
        course_name = form.course_name.data
        department_id = form.department_id.data
        instructor_id = form.instructor_id.data
        location = form.location.data
        schedule = form.schedule.data
        semester = form.semester.data
        availability = form.availability.data
        try:
            add_course_service(course_name, department_id, instructor_id, location, schedule, semester, availability)
            flash('Course added successfully', 'success')
            return redirect(url_for('admin.courses'))
        except Exception as e:
            flash(f'Error adding course: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')
    return redirect(url_for('admin.courses'))

@admin.route('/dashboard/courses/edit/<int:course_id>', methods=['POST'])
@login_required
def edit_course(course_id):
    if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('admin.courses'))
    form = CourseForm()
    form.instructor_id.choices = get_instructor_choices()
    if form.validate_on_submit():
        course_name = form.course_name.data
        department_id = form.department_id.data
        instructor_id = form.instructor_id.data
        location = form.location.data
        schedule = form.schedule.data
        semester = form.semester.data
        try:
            edit_course_service(course_id, course_name, department_id, instructor_id, location, schedule, semester)
            flash('Course updated successfully', 'success')
            return redirect(url_for('admin.courses'))
        except Exception as e:
            flash(f'Error updating course: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')
    return redirect(url_for('admin.courses'))



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
                delete_user_service(user_id)
                flash('User deleted successfully!', 'success')
            except Exception as e:
                flash(f'Error deleting user: {str(e)}', 'danger')
            return redirect(url_for('admin.users'))

    # Get query parameters for filtering
    page = int(request.args.get('page', 1))
    per_page = 10
    email = request.args.get('email', '').strip()
    department_id = request.args.get('department_id', '')
    department_id = int(department_id) if department_id.isdigit() and int(department_id) > 0 else None
    role_name = request.args.get('role_name', '')
    department_names = get_all_departments()
    # Fetch filtered users
    users, total = get_filtered_users_service(email, department_id, role_name, page, per_page)
    
    # Calculate pagination details
    total_pages = (total + per_page - 1) // per_page

    create_form = CreateUserForm()
    update_form = UpdateUserForm()

    return render_template('admin/users.html', title='Users Dashboard', users=users,
                          department_names=department_names, 
                          create_form=create_form, update_form=update_form, 
                          page=page, total_pages=total_pages, 
                          email=email, department_id=department_id or 0, role_name=role_name)
@admin.route('/dashboard/users/add', methods=['POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('admin.users'))
    form = CreateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = form.role.data
        phone = form.phone.data
        department_id = form.department_id.data
        try:
            add_user_service(email, username, password, role, phone, department_id)
            flash('User added successfully', 'success')
            return redirect(url_for('admin.users'))
        except Exception as e:
            flash(f'Error adding user: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')
    return redirect(url_for('admin.users'))

@admin.route('/dashboard/users/edit/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('admin.users'))
    form = UpdateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        role = form.role.data
        phone = form.phone.data
        department_id = form.department_id.data
        try:
            edit_user_service(user_id, username, email, role, phone, department_id)
            flash('User updated successfully', 'success')
            return redirect(url_for('admin.users'))
        except Exception as e:
            flash(f'Error updating user: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')
    return redirect(url_for('admin.users'))