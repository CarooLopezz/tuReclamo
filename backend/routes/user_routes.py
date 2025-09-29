import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.db import db
from backend.models.user import User

users = Blueprint('user', __name__)

# -------- INICIO --------
@users.route('/inicio')
def inicio():
    return render_template('inicio/inicio.html')

# -------- LISTADO DE USUARIOS  --------
@users.route('/', methods=['GET'])
def get_user():
    users_list = User.query.all()
    print("RUTA GET /user OK")
    return render_template('reclamos/reclamos.html', users=users_list)


# -------- REGISTRO --------
@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # "vecino" o "admin"

        # validar si el mail ya existe
        if User.query.filter_by(email=email).first():
            flash("Ese correo ya está registrado", "danger")
            return redirect(url_for('user.register'))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw, role=role)

        db.session.add(new_user)
        db.session.commit()

        flash("Usuario registrado correctamente", "success")
        return redirect(url_for('user.login'))

    return render_template('auth/register.html')


# -------- LOGIN --------
@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for('user.login'))

        # Guardar sesión
        session['user_id'] = user.id
        session['role'] = user.role

        # Redirigir según el rol
        if user.role == "admin":
            return redirect(url_for('user.admin_dashboard'))
        else:
            return redirect(url_for('user.vecino_dashboard'))

    return render_template('auth/login.html')


# -------- DASHBOARDS --------
@users.route('/dashboard/admin')
def admin_dashboard():
    return render_template('dashboards/admin.html')

@users.route('/dashboard/vecino')
def vecino_dashboard():
    return render_template('dashboards/vecino.html')
