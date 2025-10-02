# backend/models/user.py
import uuid
from backend.models.db import db

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="user")  # campo extra por si querés roles de sistema

    # Relación con UserType
    user_type_id = db.Column(db.String(36), db.ForeignKey("user_type.id"), nullable=False)
    user_type = db.relationship("UserType", back_populates="users")
    reclamos = db.relationship("Reclamo", back_populates="user")

    
    
    def serialize(self):
            return {
                "id": self.id,
                "username": self.username,
                "email": self.email,
                "role": self.role,
                "user_type": {
                    "id": self.user_type.id if self.user_type else None,
                    "tipo": self.user_type.tipo if self.user_type else None
            }
        }