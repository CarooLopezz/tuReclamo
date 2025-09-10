from flask import Blueprint, request, jsonify
from backend.models.user_type import UserType
from backend.models.db import db

user_type_bp = Blueprint('user_type', __name__, url_prefix='/user_type')

# GET: Listar todos
@user_type_bp.route('/', methods=['GET'])
def get_user_types():
    types = UserType.query.all()
    return jsonify([{
        "id": t.id,
        "id_usuario": t.id_usuario,
        "tipo": t.tipo,
        "directorSecto_id": t.directorSecto_id
    } for t in types]), 200

# POST: Crear nuevo UserType
@user_type_bp.route('/', methods=['POST'])
def create_user_type():
    data = request.get_json()
    nuevo = UserType(
        id_usuario=data['id_usuario'],
        tipo=data['tipo'],
        directorSecto_id=data.get('directorSecto_id')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"message": "UserType creado", "id": nuevo.id}), 201
