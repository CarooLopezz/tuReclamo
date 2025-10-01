import uuid
from .db import db  # import relativo al mismo nivel
class DirectorSector(db.Model):
    __tablename__ = "director_sector"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)

    # Relaciones
    user_types = db.relationship("UserType", back_populates="director_sector", lazy=True)
    reclamos = db.relationship("Reclamo", back_populates="director_sector", lazy=True)

    def __repr__(self):
        return f"<DirectorSector {self.id} - {self.name}>"
