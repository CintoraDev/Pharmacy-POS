from flask import Blueprint, render_template, request, redirect, url_for , flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/login' , methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard.index'))


        else:
            flash('Correo o contraseña incorrectos', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))