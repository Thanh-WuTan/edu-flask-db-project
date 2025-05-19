from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Optional, ValidationError
import re


class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('admin', 'admin'), ('student', 'student'), ('instructor', 'instructor'), ('guest', 'guest')], validators=[DataRequired()])
    phone = StringField('Phone', validators=[Optional()])
    department_id = SelectField('Department ID', choices=[
        (1, 'CECS'),
        (2, 'CAS'),
        (3, 'CBM'),
        (4, 'CHS'),
        (5, 'guest')
    ], coerce=int, validators=[DataRequired()])

class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('admin', 'admin'), ('student', 'student'), ('instructor', 'instructor'), ('guest', 'guest')], validators=[DataRequired()])
    phone = StringField('Phone', validators=[Optional()])
    department_id = SelectField('Department ID', choices=[
        (1, 'CECS'),
        (2, 'CAS'),
        (3, 'CBM'),
        (4, 'CHS'),
        (5, 'guest')
    ], coerce=int, validators=[DataRequired()])

class CourseForm(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired()])
    department_id = SelectField('Department', choices=[
        (1, 'CECS'),
        (2, 'CAS'),
        (3, 'CBM'),
        (4, 'CHS'),
        (5, 'guest')
    ], coerce=int, validators=[DataRequired()])
    instructor_id = SelectField('Instructor', choices=[], coerce=int, validators=[DataRequired()])
    location = StringField('Location', validators=[Optional()])
    schedule = StringField('Schedule', validators=[Optional()])
    semester = StringField('Semester', validators=[Optional()])
    availability = IntegerField('Availability', validators=[DataRequired()])

    def validate_semester(self, field):
        pattern = r'^(Spring|Fall|Summer) \d{4}$'
        if field.data and not re.match(pattern, field.data.strip()):
            raise ValidationError('Semester must be in the format "Spring/Fall/Summer 2024".')

    def validate_schedule(self, field):
        pattern = r'^(M|T|W|TH|F|S|SU)(,\s*(M|T|W|TH|F|S|SU))*$'
        if field.data and not re.match(pattern, field.data.strip()):
            raise ValidationError('Schedule must be comma-separated codes like "M, W, F" (M=Mon, T=Tue, etc.).')

class CourseInstructorForm(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired()])
    location = StringField('Location', validators=[Optional()])
    schedule = StringField('Schedule', validators=[Optional()])
    semester = StringField('Semester', validators=[Optional()])

    def validate_semester(self, field):
        pattern = r'^(Spring|Fall|Summer) \d{4}$'
        if field.data and not re.match(pattern, field.data.strip()):
            raise ValidationError('Semester must be in the format "Spring/Fall/Summer 2024".')

    def validate_schedule(self, field):
        pattern = r'^(M|T|W|TH|F|S|SU)(,\s*(M|T|W|TH|F|S|SU))*$'
        if field.data and not re.match(pattern, field.data.strip()):
            raise ValidationError('Schedule must be comma-separated codes like "M, W, F" (M=Mon, T=Tue, etc.).')