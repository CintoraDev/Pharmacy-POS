from flask import Blueprint, render_template, redirect, url_for, flash , request
from flask_login import login_required
from models import User, db
from werkzeug.security import generate_password_hash

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
@login_required
def index():
    users = User.query.all()
    return render_template('users/index.html', users = users)

@users_bp.route('/users/create', methods=['POST'])
@login_required
def create():
    name = request.form.get('name')
    email = request.form.get('email')
    rol = request.form.get('rol')
    password = request.form.get('password')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        flash('El correo ya está registrado', 'error')
        return redirect(url_for('users.index')) 
        

    new_user = User(
        name = name,
        email = email,
        rol = rol,
        password = generate_password_hash(password),
        status = True
    )
  
    db.session.add(new_user)
    db.session.commit()
    flash('Usuario creado correctamente', 'success')
    return redirect(url_for('users.index'))
    