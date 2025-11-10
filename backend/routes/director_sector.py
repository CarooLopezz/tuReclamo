from flask import Blueprint, jsonify
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message
from ..models.director_sector import DirectorSector  # import relativo correcto
from ..models.reclamo import Reclamo
from ..models.db import db
from flask_mail import Mail, Message
import os
# Crear el Blueprint
director_sector = Blueprint("director_sector", __name__)

#--------------------------------- DASHBOARD SECTOR-------------------------

@director_sector.route("/dashboardSector")
def director_sector_dashboard():
    return render_template("directorSector/dashboardSector.html")

@director_sector.route("/panelSector")
def director_sector_panel():
    return render_template("directorSector/panelSector.html")


@director_sector.route("/api/reclamos/borrar/<int:id>", methods=["DELETE"])
def borrar_reclamo_dashboard(id):
    reclamo = Reclamo.query.get(id)
    if not reclamo:
        return jsonify({"error": "Reclamo no encontrado"}), 404

    db.session.delete(reclamo)
    db.session.commit()
    return jsonify({"message": "Reclamo eliminado correctamente"}), 200


# Endpoint para obtener todos los sectores
""" @director_sector.route("/panel")
def get_all():
    sectores = DirectorSector.query.all()
    return jsonify([s.serialize() for s in sectores]) """
    
@director_sector.route("/api/reclamos/director")
def reclamos_director():
    reclamos = Reclamo.query.all()
    reclamos_data = []

    for r in reclamos:
        # Armamos la ruta correcta de la foto
        if r.foto:
            filename = os.path.basename(r.foto)
            foto_url = f"/images/images_reclamo/{filename}"
        else:
            foto_url = None

        reclamos_data.append({
            "id": r.id,
            "usuario": r.user.username if r.user else "Anónimo",
            "categoria": r.categoria,
            "direccion": r.direccion,
            "descripcion": r.descripcion,
            "foto": foto_url
        })

    return jsonify(reclamos_data)

@director_sector.route("/reclamo/<id>/cambiar-estado", methods=["POST"])
def cambiar_estado(id):

    reclamo = Reclamo.query.get_or_404(id)
    reclamo.estado = request.form["estado"]
    db.session.commit()
    flash("Estado actualizado", "success")
    return redirect(url_for("directorSector.directorSector.html"))


@director_sector.route("/panelSector/borrar/<int:id>", methods=["DELETE"])

def borrar_reclamo(id):
    reclamo = Reclamo.query.get(id)
    if not reclamo:
        return jsonify({"error": "Reclamo no encontrado"}), 404

    db.session.delete(reclamo)
    db.session.commit()
    return jsonify({"message": "Reclamo eliminado correctamente"}), 200

@director_sector.route("/api/reclamos/<int:id>/notificar", methods=["POST"])
def notificar_reclamo(id):
    data = request.get_json()
    nuevo_estado = data.get("estado")

    reclamo = Reclamo.query.get(id)
    if not reclamo:
        return jsonify({"error": "Reclamo no encontrado"}), 404

    # Actualizamos el estado
    reclamo.estado = nuevo_estado
    db.session.commit()

    # Enviamos el correo
    try:
        msg = Message(
            subject="Actualización de tu reclamo",
            recipients=[reclamo.user.email],  # Asegúrate de tener user.email en tu modelo
            body=f"Hola {reclamo.user.username},\n\nTu reclamo sobre '{reclamo.categoria}' se encuentra ahora en estado: {nuevo_estado.upper()}.\n\nGracias por usar nuestra plataforma."
        )
        mail.send(msg)
        return jsonify({"message": "Notificación enviada correctamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al enviar email: {str(e)}"}), 500