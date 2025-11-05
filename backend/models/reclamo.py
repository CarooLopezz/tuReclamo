import uuid
from backend.models.db import db;
from datetime import datetime

class Reclamo(db.Model):
    __tablename__ = "reclamo"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    categoria = db.Column(db.String(100)) 
    direccion = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    estado = db.Column(db.String(50), default="pendiente")
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    foto = db.Column(db.String(255), nullable=True)

    # Foreign Keys
    director_sector_id = db.Column(db.String(36), db.ForeignKey("director_sector.id"), nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False) 
    user = db.relationship("User", back_populates="reclamos")
    # Relaciones
   
    director_sector = db.relationship("DirectorSector", back_populates="reclamos")
    def serialize(self):
        return {
            "id": self.id,
            "categoria":self.categoria ,
            "direccion":self.direccion,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "foto": self.foto,
            "director_sector_id": self.director_sector_id,
            "user_id": self.user_id
        }

    def __repr__(self):
        return f"<Reclamo {self.id} - {self.descripcion[:30]}...>"