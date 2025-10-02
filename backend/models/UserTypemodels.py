# backend/models/user_type.py
import uuid
from backend.models.db import db

class UserType(db.Model):
    __tablename__ = "user_type"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tipo = db.Column(db.String(50), nullable=False, unique=True)  # 'vecino', 'director', 'admin'
    director_sector = db.relationship("DirectorSector", back_populates="user_types")
    # Relaciones
    users = db.relationship("User", back_populates="user_type")
    director_sector = db.relationship("DirectorSector", back_populates="user_type")

    def __repr__(self):
        return f"<UserType {self.id} - {self.tipo}>"
