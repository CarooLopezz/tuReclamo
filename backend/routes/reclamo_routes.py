from flask import Blueprint, request, jsonify,render_template,session,app, current_app
from backend.models.db import db
from backend.models.reclamo import Reclamo
from backend.models.UserTypemodels import UserType
from backend.models.user import User
from datetime import datetime
import uuid
import jwt
import os
from werkzeug.utils import secure_filename
import base64


reclamo_bp = Blueprint('reclamo_bp', __name__)

@reclamo_bp.route("/crear-reclamo", methods=[ "GET","POST"])

def crear_reclamo():
    if request.method == "GET":
        return render_template("reclamos/add_reclamos.html")

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "No hay token de autorización"}), 401

    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        user_id = decoded["id"]
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido"}), 401

    # 🔹 Obtener datos como JSON (no form)
    data = request.get_json()

    categoria = data.get("categoria")
    direccion = data.get("direccion")
    descripcion = data.get("descripcion")
    foto_base64 = data.get("foto")  # ⚠️ Esto llega del frontend en formato base64
    
 

    # 🔹 Crear reclamo con imagen base64 directamente
    nuevo_reclamo = Reclamo(
        user_id=user_id,
        categoria=categoria,
        direccion=direccion,
        descripcion=descripcion,
        foto=foto_base64  # 🔸 se guarda directamente en la base
    )

    db.session.add(nuevo_reclamo)
    db.session.commit()

    return jsonify({"message": "Reclamo creado correctamente"}), 201
#poner debajo de la pagina
@reclamo_bp.route("/api/reclamos", methods=["GET"])
def obtener_reclamos():
    reclamos = Reclamo.query.all()  # o .order_by(Reclamo.id.desc()) si querés últimos primero
    reclamos_data = []

    for r in reclamos:
        print("📸 FOTO:", r.foto[:100] if r.foto else "SIN FOTO") 
        reclamos_data.append({
            "id": r.id,
            "categoria": r.categoria,
            "direccion": r.direccion,
            "descripcion": r.descripcion,
            "foto": r.foto if r.foto else "/static/images/tureclamo.png",
            "usuario": getattr(r.user, "username", "Anónimo")  # <-- así evitás crash
        })

    return jsonify(reclamos_data)


# -------- LISTAR TODOS LOS RECLAMOS --------
@reclamo_bp.route('/reclamos', methods=['GET'])
def listar_reclamos():
    reclamos = Reclamo.query.all()
    return jsonify([r.serialize() for r in reclamos])

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

"""
chart js
Procesador de VOz speech recognition
onpencv
podes manejar el mouse con el dedo

pop up se registro
notificacion dell reclamo
es para detectar problemas antes del deploy o que el cliente lo este usando
test unitario -- una funcion 
test de integracion -- es un bloque de la aplicacion
end to end -- toda la aplicación
genera una calidad en el sistema
test_routes_
pytest
los tests tiene que se rindependiente de la servidor , el servidor de la app apagado
test integrairon
-indicar donde estan las carpetas
segun lo que importo levanta eso
ruta=controlador
base e datos-ruta-view no involucra toda la aplicacion
assert es compara
mock: simulación de la base de datos y simular la vista para el unitest
end-to end probas la aplicacion caja blanca y caja negra, prueba de fuerza bruta,cada
fila espera su turno
"""

