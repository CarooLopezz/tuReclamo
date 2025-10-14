from flask import Blueprint, request, jsonify,render_template
from backend.models.db import db
from backend.models.reclamo import Reclamo
from backend.models.UserTypemodels import UserType
from backend.models.user import User
from datetime import datetime
import uuid
# Prefijo para todas las rutas de reclamos
reclamo_bp = Blueprint('reclamo_bp', __name__)

# -------- LISTAR TODOS LOS RECLAMOS --------
@reclamo_bp.route('/reclamos', methods=['GET'])
def listar_reclamos():
    reclamos = Reclamo.query.all()
    return jsonify([r.serialize() for r in reclamos])

@reclamo_bp.route('/create_reclamos', methods=['POST'])
def crear_reclamo():
    data = request.get_json()

    descripcion = data.get('descripcion')
    estado = data.get('estado', 'pendiente')
    fecha_creacion = data.get('fecha_creacion', datetime.utcnow().isoformat())
    foto = data.get('foto')
    director_sector_id = data.get('director_sector_id')
    user_id = data.get('user_id')

    # Validar campos obligatorios
    if not descripcion or not director_sector_id or not user_id:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        nuevo_reclamo = Reclamo(
            id=str(uuid.uuid4()),  # genera UUID automático
            descripcion=descripcion,
            estado=estado,
            fecha_creacion=fecha_creacion,
            foto=foto,
            director_sector_id=director_sector_id,
            user_id=user_id
        )

        db.session.add(nuevo_reclamo)
        db.session.commit()

        return jsonify({
            "mensaje": "Reclamo creado correctamente",
            "id": nuevo_reclamo.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear reclamo: {str(e)}"}), 500
    
    
@reclamo_bp.route('/<string:id>/estado', methods=['PUT'])
def cambiar_estado(id):
    data = request.get_json()
    nuevo_estado = data.get('estado')

    if not nuevo_estado:
        return jsonify({'error': 'Falta el estado'}), 400

    reclamo = Reclamo.query.get(id)
    if not reclamo:
        return jsonify({'error': 'Reclamo no encontrado'}), 404

    try:
        reclamo.estado = nuevo_estado
        db.session.commit()
        return jsonify({'mensaje': f'Estado del reclamo {id} actualizado a "{nuevo_estado}"'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar estado: {str(e)}'}), 500    

def eliminar_reclamo(id):
    reclamo = Reclamo.query.get(id)

    if not reclamo:
        return jsonify({'error': 'Reclamo no encontrado'}), 404

    try:
        db.session.delete(reclamo)
        db.session.commit()
        return jsonify({'mensaje': f'Reclamo {id} eliminado correctamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar reclamo: {str(e)}'}), 500

