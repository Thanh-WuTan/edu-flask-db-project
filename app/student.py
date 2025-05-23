from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app.service.main_service import get_full_course_details_service
from app.role_required import role_required
from app.db.courses import db_get_course_by_student_id

student = Blueprint('student', __name__)

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
    courses = db_get_course_by_student_id(students_id)
    return render_template('student/courses.html', title='My Courses', courses=courses)


@student.route('/dashboard/courses/<int:course_id>')
@login_required
@role_required('student')
def course_detail(course_id):
    course, enrolled_students, available_students = get_full_course_details_service(course_id)
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('student.courses'))
        
    return render_template('student/course_detail.html', title=f'Course Detail - {course["course_name"]}', 
                          course=course, enrolled_students=enrolled_students, available_students=available_students)
