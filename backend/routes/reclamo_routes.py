from flask import Blueprint, request, jsonify,render_template,session,app, current_app,send_from_directory
from backend.models.db import db
from backend.models.reclamo import Reclamo
from backend.models.UserTypemodels import UserType
from backend.models.user import User
from datetime import datetime
import uuid
import jwt
import os
from werkzeug.utils import secure_filename



reclamo_bp = Blueprint('reclamo_bp', __name__)

@reclamo_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    uploads_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'images')
    return send_from_directory(uploads_dir, filename)

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Verifica si la extensión del archivo es válida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --------------------- CREAR RECLAMO ---------------------
@reclamo_bp.route("/crear-reclamo", methods=["GET", "POST"])
def crear_reclamo():
    if request.method == "GET":
        return render_template("reclamos/add_reclamos.html")

    # Verificación del token
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

    # Si la solicitud viene con archivos (FormData)
    categoria = request.form.get("categoria")
    direccion = request.form.get("direccion")
    descripcion = request.form.get("descripcion")

    foto = request.files.get("foto")
    imagen_path = None  

    if foto and foto.filename:
        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{foto.filename}")

        upload_folder = os.path.join("images", "images_reclamo")
        os.makedirs(upload_folder, exist_ok=True)

        foto_path = os.path.join(upload_folder, filename)
        foto.save(foto_path)

        # 👇 esta es la ruta que vas a guardar en la base de datos
        imagen_path = f"images/images_reclamo/{filename}"
    else:
        imagen_path = None
        #


    # Crear el reclamo
    nuevo_reclamo = Reclamo(
        user_id=user_id,
        categoria=categoria,
        direccion=direccion,
        descripcion=descripcion,
        foto=imagen_path  
    )

    db.session.add(nuevo_reclamo)
    db.session.commit()

    return jsonify({"message": "Reclamo creado correctamente"}), 201


@reclamo_bp.route("/api/reclamos", methods=["GET"])
def obtener_reclamos():
    reclamos = Reclamo.query.all()
    reclamos_data = []

    for r in reclamos:
        if r.foto:
    # foto guarda algo como "images/20251108131044_residuos.jpeg"
            filename = os.path.basename(r.foto)
            foto_url = f"images/images_reclamo/{filename}"
        else:
            foto_url = None

        reclamos_data.append({
            "id": r.id,
            "categoria": r.categoria,
            "direccion": r.direccion,
            "descripcion": r.descripcion,
            "foto": foto_url,
            "usuario": getattr(r.user, "username", "Anónimo")
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
      
@reclamo_bp.route("/api/reclamos/<int:id>", methods=["DELETE"])   

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

