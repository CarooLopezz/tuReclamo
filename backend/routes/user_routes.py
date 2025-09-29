import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.models.db import db
from backend.models.user import User

users = Blueprint('user', __name__, url_prefix="/users")

# -------- LISTADO DE USUARIOS --------
@users.route('/', methods=['GET'])
def listar_usuarios():
    users_list = User.query.all()
    return render_template('users/listar.html', users=users_list)


# -------- CREAR USUARIO --------
@users.route('/create', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']

        nuevo_usuario = User(
            username=username,
            email=email,
            role=role
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario creado correctamente", "success")
        return redirect(url_for('user.listar_usuarios'))

    return render_template('users/create.html')


# -------- EDITAR USUARIO --------
@users.route('/<int:id>/edit', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = User.query.get_or_404(id)

    if request.method == 'POST':
        usuario.username = request.form['username']
        usuario.email = request.form['email']
        usuario.role = request.form['role']

        db.session.commit()
        flash("Usuario actualizado correctamente", "success")
        return redirect(url_for('user.listar_usuarios'))

    return render_template('users/edit.html', usuario=usuario)


# -------- ELIMINAR USUARIO --------
@users.route('/<int:id>/delete', methods=['POST'])
def eliminar_usuario(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario eliminado correctamente", "success")
    return redirect(url_for('user.listar_usuarios'))
