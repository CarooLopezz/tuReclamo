import sys
import os
import pytest

# Agrega el path raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from backend.models.db import db
from backend.models.user import User
from backend.models.UserTypemodels import UserType

@pytest.fixture
def client():
    """Crea un cliente de prueba con una base SQLite temporal"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 🔹 Base temporal
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        # Insertar datos de prueba
        user = User(username="pietro", email="pietro@example.com", password="123" )
        db.session.add(user)
        db.session.commit()

    # Cliente Flask
    client = app.test_client()

    yield client  # <- acá se ejecutan los tests

    # Limpieza después del test
    with app.app_context():
        db.drop_all()

def test_get_users(client):
    """Prueba que el endpoint /users devuelva correctamente el usuario de prueba"""
    response = client.get('/users/')
    assert response.status_code == 200
    assert b"pietro" in response.data
