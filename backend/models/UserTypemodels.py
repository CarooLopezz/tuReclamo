# Aquí definimos los modelos de la base de datos
from .db import db

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo_usuario = db.Column(db.String(50), nullable=False)  # "vecino" o "administrador"

class Vecino(Usuario):
    __tablename__ = "vecinos"
    id_vecino = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), primary_key=True)
    direccion = db.Column(db.String(200), nullable=False)

class Administrador(Usuario):
    __tablename__ = "administradores"
    id_admin = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), primary_key=True)
    director_sector = db.Column(db.String(100), nullable=False)
