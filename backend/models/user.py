# backend/models/user.py
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
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

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.id} - {self.username} ({self.user_type.tipo if self.user_type else 'Sin tipo'})>"
