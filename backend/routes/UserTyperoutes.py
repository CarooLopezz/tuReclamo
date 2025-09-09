# Este archivo maneja las rutas de los reclamos
from flask import Blueprint, request, jsonify

reclamos_bp = Blueprint("reclamos", __name__)

# Lista simulada de reclamos (más adelante se puede conectar a la BD)
reclamos = []

@reclamos_bp.route("/reclamos", methods=["POST"])
def crear_reclamo():
    """
    Ruta para crear un nuevo reclamo.
    Espera un JSON con 'descripcion' y 'usuario'.
    """
    data = request.json
    reclamos.append(data)
    return jsonify({"mensaje": "Reclamo creado", "reclamo": data}), 201

@reclamos_bp.route("/reclamos", methods=["GET"])
def listar_reclamos():
    """
    Ruta para listar todos los reclamos registrados.
    """
    return jsonify(reclamos), 200
