from flask import Blueprint, render_template, redirect, url_for, flash , request
from flask_login import login_required
from models import User, db
from werkzeug.security import generate_password_hash
from utils import role_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
@role_required('admin', 'gerente')
@login_required
def index():
    users = User.query.filter_by(status=True).all()
    return render_template('users/index.html', users = users)

@users_bp.route('/users/create', methods=['POST'])
@role_required('admin', 'gerente')
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


@users_bp.route('/users/desactivate/<int:id>', methods=['POST'])
@role_required('admin', 'gerente')
@login_required
def desactivate(id):
    user = User.query.get_or_404(id)

    user.status = False
    db.session.commit()

    flash('Usuario desactivado correctamente', 'success')
    return redirect(url_for('users.index'))
    

@users_bp.route('/users/update/<int:id>', methods=['POST'])
@role_required('admin', 'gerente')
@login_required
def update(id):
    user = User.query.get_or_404(id)
    user.name = request.form.get('name')
    user.email = request.form.get('email')
    user.rol = request.form.get('rol')
    password = request.form.get('password')
    if password:
        user.password = generate_password_hash(password)

    db.session.commit()
    flash('Usuario actualizado correctamente', 'success')
    return redirect(url_for('users.index'))
    
