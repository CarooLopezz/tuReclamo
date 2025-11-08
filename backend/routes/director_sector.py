from flask import Blueprint, jsonify
from flask import Blueprint, render_template, request, redirect, url_for, flash

from ..models.director_sector import DirectorSector  # import relativo correcto
from ..models.reclamo import Reclamo
from ..models.db import db
# Crear el Blueprint
director_sector = Blueprint("director_sector", __name__)

# Endpoint para obtener todos los sectores
@director_sector.route("/panel")
def get_all():
    sectores = DirectorSector.query.all()
    return jsonify([s.serialize() for s in sectores])

@director_sector.route("/reclamo/<id>/cambiar-estado", methods=["POST"])
def cambiar_estado(id):

    reclamo = Reclamo.query.get_or_404(id)
    reclamo.estado = request.form["estado"]
    db.session.commit()
    flash("Estado actualizado", "success")
    return redirect(url_for("directorSector.directorSector.html"))


@director_sector.route("/reclamo/<id>/borrar", methods=["POST"])

def borrar_reclamo(id):

    reclamo = Reclamo.query.get_or_404(id)
    db.session.delete(reclamo)
    db.session.commit()
    flash("Reclamo eliminado", "success")
    return redirect(url_for("directorSector.directorSector.html"))
