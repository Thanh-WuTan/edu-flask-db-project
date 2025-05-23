from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.service.main_service import get_full_course_details_service
from app.role_required import role_required
from app.db.courses import db_get_course_by_instructor_id
from app.db.enrollment import db_enroll_student, db_unenroll_student

instructor = Blueprint('instructor', __name__)

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
    courses = db_get_course_by_instructor_id(instructor_id)
    print("Fetched courses:", courses)  # DEBUG LINE
    return render_template('instructor/courses.html', title='My Courses', courses=courses)

@instructor.route('/dashboard/courses/<int:course_id>')
@login_required
@role_required('instructor')
def course_detail(course_id):
    course, enrolled_students, available_students = get_full_course_details_service(course_id)
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
            db_enroll_student(int(student_id), course_id)
            flash('Student enrolled successfully!', 'success')
        except Exception as e:
            flash(f'Error enrolling student: {str(e)}', 'danger')
    return redirect(url_for('instructor.course_detail', course_id=course_id))


@instructor.route('/dashboard/courses/<int:course_id>/unenroll/<int:student_id>', methods=['POST'])
@login_required
@role_required('instructor')
def unenroll_student(course_id, student_id):
    try:
        db_unenroll_student(student_id, course_id)
    except Exception as e:
        flash(f'Error unenrolling student: {str(e)}', 'danger')
    return redirect(url_for('instructor.course_detail', course_id=course_id))
