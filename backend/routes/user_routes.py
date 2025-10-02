import os
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from backend.models.db import db
from backend.models.user import User
from backend.models.UserTypemodels import UserType

users = Blueprint('user', __name__)

# -------- LISTADO DE USUARIOS --------
@users.route("/", methods=["GET"])
def listar_usuarios():
    usuarios = User.query.all()
    return jsonify([u.serialize() for u in usuarios])

#---------- CREAR USUARIO -----------

@users.route('/create', methods=['POST'])
def crear_usuario():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    role = data.get('role')
    password = data.get('password')
    user_type = data.get('user_type')  # objeto embebido

    # Sacar el id de user_type si viene embebido
    user_type_id = None
    if user_type and isinstance(user_type, dict):
        user_type_id = user_type.get('id')

    if not username or not email or not role or not user_type_id or not password:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    # Asumiendo que la password ya viene hasheada en este caso
    nuevo_usuario = User(
        username=username,
        email=email,
        password=password,
        role=role,
        user_type_id=user_type_id
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify(nuevo_usuario.serialize()), 201



# -------- EDITAR USUARIO --------

@users.route('/<string:id>/edit', methods=['PUT'])
def editar_usuario(id):
    usuario = User.query.get_or_404(id)
    data = request.get_json()

    usuario.username = data.get('username', usuario.username)
    usuario.email = data.get('email', usuario.email)
    usuario.role = data.get('role', usuario.role)
    usuario.user_type_id = data.get('user_type_id', usuario.user_type_id)

    db.session.commit()
    return jsonify(usuario.serialize()), 200


# -------- ELIMINAR USUARIO --------
@users.route('/<string:id>/delete', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario eliminado correctamente", "success")
    return redirect(url_for('user.listar_usuarios'))
