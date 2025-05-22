from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app.role_required import role_required
from app.db.enrollment import get_enrolled_students, get_available_students
from app.db.courses import db_get_course_view_by_id, db_get_course_by_student_id

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
    course = db_get_course_view_by_id(course_id)
    enrolled_students = get_enrolled_students(course_id)
    available_students = get_available_students(course_id)

    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('student.courses'))
        
    return render_template('student/course_detail.html', title=f'Course Detail - {course["course_name"]}', 
                          course=course, enrolled_students=enrolled_students, available_students=available_students)
