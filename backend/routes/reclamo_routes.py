from flask import Blueprint, request, jsonify
from models.reclamo import Reclamo

# Prefijo para todas las rutas de reclamos
reclamo_bp = Blueprint('reclamo_bp', __name__, url_prefix='/reclamos')

# GET /reclamos → Listar todos los reclamos
@reclamo_bp.route('/', methods=['GET'])
def listar_reclamos():
    reclamos = Reclamo.obtener_todos()
    return jsonify(reclamos), 200

# POST /reclamos → Crear un nuevo reclamo
@reclamo_bp.route('/', methods=['POST'])
def crear_reclamo():
    data = request.get_json()
    nuevo = Reclamo(
        descripcion=data.get('descripcion', ''),
        id_vecino=data.get('id_vecino'),
        id_sector_resp=data.get('id_sector_resp'),
        estado=data.get('estado', 'pendiente'),
        foto=data.get('foto')
    )
    nuevo.guardar()
    return jsonify({'mensaje': 'Reclamo creado', 'id': nuevo.id_reclamo}), 201

# PUT /reclamos/<id>/estado → Cambiar el estado de un reclamo
@reclamo_bp.route('/<int:id>/estado', methods=['PUT'])
def cambiar_estado(id):
    data = request.get_json()
    nuevo_estado = data.get('estado')
    
    if not nuevo_estado:
        return jsonify({'error': 'Falta el estado'}), 400

    reclamo = Reclamo(id_reclamo=id)
    reclamo.cambiar_estado(nuevo_estado)
    return jsonify({'mensaje': 'Estado actualizado'}), 200
