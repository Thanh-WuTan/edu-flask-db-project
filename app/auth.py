from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.service.auth_service import register_user, login_user 
from app.db.users import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user, error = login_user(email, password)
        if user:
            login_user(User(user))
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        flash(error, 'danger')
    return render_template('auth/login.html', title='Login')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_id, error = register_user(email, username, password, confirm_password)
        if user_id:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        flash(error, 'danger')
    return render_template('auth/register.html', title='Register')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.index'))