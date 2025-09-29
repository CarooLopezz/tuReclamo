import uuid
from backend.models.db import db;
from datetime import datetime

class Reclamo(db.Model):
    __tablename__ = "reclamo"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    descripcion = db.Column(db.String(500), nullable=False)
    estado = db.Column(db.String(50), default="pendiente")
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    foto = db.Column(db.String(255), nullable=True)

    # Foreign Keys
    vecino_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    director_sector_id = db.Column(db.String(36), db.ForeignKey("director_sector.id"), nullable=True)

    # Relaciones
    vecino = db.relationship("User", back_populates="reclamos")
    director_sector = db.relationship("DirectorSector", back_populates="reclamos")

    def __repr__(self):
        return f"<Reclamo {self.id} - {self.descripcion[:30]}...>"