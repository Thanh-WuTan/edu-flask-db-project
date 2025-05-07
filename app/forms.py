from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Optional

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
