from .db import db  # import relativo al mismo nivel

class DirectorSector(db.Model):
    __tablename__ = "director_sector"

    id_reclamo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)

    id_vecino = db.Column(db.Integer, db.ForeignKey("vecino.id_vecino"))
    id_administrador = db.Column(db.Integer, db.ForeignKey("administrador.id_administrador"))
    id_sector = db.Column(db.Integer, db.ForeignKey("sector.id_sector"))

    def serialize(self):
        return {
            "id_reclamo": self.id_reclamo,
            "descripcion": self.descripcion,
            "fecha_creacion": self.fecha_creacion,
            "estado": self.estado,
            "ubicacion": self.ubicacion,
            "id_vecino": self.id_vecino,
            "id_administrador": self.id_administrador,
            "id_sector": self.id_sector
        }
