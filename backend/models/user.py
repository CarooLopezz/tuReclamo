import uuid
from backend.models.db import db
from backend.models.userTypemodels import UserType
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    dni = db.Column(db.String(20))  # si querés, lo podés traducir a "national_id"
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    userTypemodels = db.relationship("UserType", back_populates="user", uselist=False)
  # reclamos = db.relationship("Reclamo", back_populates="vecino", lazy=True) 
def __repr__(self):
    return f"<Usuario {self.id_usuario} - {self.nombre} {self.apellido}>"