import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.role_required  import role_required
from app.service.main_service import get_instructor_choices
from app.db.departments import db_get_all_departments
from app.db.users import db_delete_user, db_create_user, db_update_user, db_get_filtered_users
from app.db.courses import db_get_filtered_courses, db_delete_course, db_create_course, db_update_course, db_get_course_view_by_id
from app.db.enrollment import db_get_enrolled_students, db_get_available_students, db_enroll_student, db_unenroll_student
from app.db.stored_procs import db_get_user_role_counts, db_get_course_department_counts, db_get_student_department_counts, db_get_course_count_by_semester
from app.forms import CreateUserForm, UpdateUserForm, CourseForm


admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():    
    user_role_counts = db_get_user_role_counts()
    course_dept_counts = db_get_course_department_counts()
    student_dept_counts = db_get_student_department_counts()
    course_semester_counts = db_get_course_count_by_semester()

    return render_template('admin/dashboard.html', title='Admin Dashboard', 
                          user_role_counts=user_role_counts, course_dept_counts=course_dept_counts, student_dept_counts=student_dept_counts, 
                          course_semester_counts=course_semester_counts)

@admin.route('/dashboard/courses/')
@login_required
@role_required('admin')
def courses():
    # Pagination and search parameters
    page = int(request.args.get('page', 1))
    per_page = 10
    search_query = request.args.get('search', '').strip()
    department_id = request.args.get('department_id', '')
    department_id = int(department_id) if department_id.isdigit() and int(department_id) > 0 else None
    schedule = request.args.get('schedule', '')
    department_names = db_get_all_departments()

    # Fetch courses with filters
    courses, total = db_get_filtered_courses(search_query=search_query, department_id=department_id, schedule=schedule, page=page, per_page=per_page)
    total_pages = (total + per_page - 1) // per_page

    # Populate instructor choices dynamically
    course_form = CourseForm()
    course_form.instructor_id.choices = get_instructor_choices()
    return render_template('admin/courses.html', title='Courses Dashboard', courses=courses, 
                          course_form=course_form, page=page, total_pages=total_pages,
                          department_names=department_names, department_id=department_id or 0, schedule=schedule)

@admin.route('/dashboard/courses/add', methods=['POST'])
@login_required
@role_required('admin')
def add_course():
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
            db_create_course(course_name, department_id, instructor_id, location, schedule, semester, availability)
            flash('Course added successfully', 'success')
            return redirect(url_for('admin.courses'))
        except Exception as e:
            flash(f'Error adding course: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')
    return redirect(url_for('admin.courses'))

@admin.route('/dashboard/courses/delete/<int:course_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_course(course_id):
    try:
        db_delete_course(course_id)
        flash('Course deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting course: {str(e)}', 'danger')
    return redirect(url_for('admin.courses'))

@admin.route('/dashboard/courses/<int:course_id>')
@login_required
@role_required('admin')
def course_detail(course_id):    
    course = db_get_course_view_by_id(course_id)
    enrolled_students = db_get_enrolled_students(course_id)
    available_students = db_get_available_students(course_id)

    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('admin.courses'))
    
    return render_template('admin/course_detail.html', title=f'Course Detail - {course["course_name"]}', 
                          course=course, enrolled_students=enrolled_students, available_students=available_students)


@admin.route('/dashboard/courses/<int:course_id>/enroll', methods=['POST'])
@login_required
@role_required('admin')
def enroll_student(course_id):
    student_id = request.form.get('student_id')
    if student_id:
        try:
            db_enroll_student(int(student_id), course_id)
            flash('Student enrolled successfully!', 'success')
        except Exception as e:
            flash(f'Error enrolling student: {str(e)}', 'danger')
    return redirect(url_for('admin.course_detail', course_id=course_id))


@admin.route('/dashboard/courses/<int:course_id>/unenroll/<int:student_id>', methods=['POST'])
@login_required
@role_required('admin')
def unenroll_student(course_id, student_id):
    try:
        db_unenroll_student(student_id, course_id)
    except Exception as e:
        flash(f'Error unenrolling student: {str(e)}', 'danger')
    return redirect(url_for('admin.course_detail', course_id=course_id))

@admin.route('/dashboard/courses/edit/<int:course_id>', methods=['POST'])
@login_required
@role_required('admin')
def edit_course(course_id):
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
            db_update_course(course_id, course_name, department_id, instructor_id, location, schedule, semester, availability)
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
@role_required('admin')
def users():    
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        if user_id:
            try:
                db_delete_user(user_id)
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
    department_names = db_get_all_departments()
    # Fetch filtered users
    users, total = db_get_filtered_users(email, department_id, role_name, page, per_page)
    
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
@role_required('admin')
def add_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = form.role.data
        phone = form.phone.data
        department_id = form.department_id.data
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            db_create_user(email, username, hashed_password, role, phone, department_id)

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
@role_required('admin')
def edit_user(user_id):
    form = UpdateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        role = form.role.data
        phone = form.phone.data
        department_id = form.department_id.data
        try:
            db_update_user(user_id, username, email, role, phone, department_id)
            flash('User updated successfully', 'success')
            return redirect(url_for('admin.users'))
        except Exception as e:
            flash(f'Error updating user: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')
    return redirect(url_for('admin.users'))