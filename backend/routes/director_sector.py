from flask import Blueprint, jsonify
from ..models.director_sector import DirectorSector  # import relativo correcto

# Crear el Blueprint
director_sector = Blueprint("director_sector", __name__, url_prefix="/director_sector")

# Endpoint para obtener todos los sectores
@director_sector.route("/")
def get_all():
    sectores = DirectorSector.query.all()
    return jsonify([s.serialize() for s in sectores])
