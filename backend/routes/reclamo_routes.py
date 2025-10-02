from flask import Blueprint, request, jsonify
from ..models.reclamo import Reclamo

# Prefijo para todas las rutas de reclamos
reclamo_bp = Blueprint('reclamo_bp', __name__)

from flask import Blueprint, request, jsonify
from backend.models.reclamo import Reclamo

# Prefijo para todas las rutas de reclamos
reclamo_bp = Blueprint('reclamo_bp', __name__)

# -------- LISTAR TODOS LOS RECLAMOS --------
@reclamo_bp.route('/reclamos', methods=['GET'])
def listar_reclamos():
    reclamos = Reclamo.query.all()()
    return jsonify(reclamos), 200

# -------- CREAR UN NUEVO RECLAMO --------
@reclamo_bp.route('/create_reclamos', methods=['POST'])
def crear_reclamo():
    data = request.get_json()

    descripcion = data.get('descripcion')
    id_vecino = data.get('id_vecino')
    id_sector_resp = data.get('id_sector_resp')
    estado = data.get('estado', 'pendiente')
    foto = data.get('foto')

    if not descripcion or not id_vecino or not id_sector_resp:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    nuevo = Reclamo(
        descripcion=descripcion,
        id_vecino=id_vecino,
        id_sector_resp=id_sector_resp,
        estado=estado,
        foto=foto
    )
    nuevo.guardar()
    return jsonify({'mensaje': 'Reclamo creado', 'id': nuevo.id_reclamo}), 201

# -------- CAMBIAR ESTADO DEL RECLAMO --------
@reclamo_bp.route('/<int:id>/estado', methods=['PUT'])
def cambiar_estado(id):
    data = request.get_json()
    nuevo_estado = data.get('estado')

    if not nuevo_estado:
        return jsonify({'error': 'Falta el estado'}), 400

    reclamo = Reclamo(id_reclamo=id)
    actualizado = reclamo.cambiar_estado(nuevo_estado)

    if actualizado:
        return jsonify({'mensaje': 'Estado actualizado'}), 200
    else:
        return jsonify({'error': 'Reclamo no encontrado'}), 404

# -------- ELIMINAR UN RECLAMO --------
@reclamo_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_reclamo(id):
    reclamo = Reclamo(id_reclamo=id)

    eliminado = reclamo.eliminar()

    if eliminado:
        return jsonify({'mensaje': f'Reclamo {id} eliminado'}), 200
    else:
        return jsonify({'error': 'Reclamo no encontrado'}), 404