""" import sys
import os
import pytest

# Agregar la ruta raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.models.db import db
import json
from app import app as flask_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.config.config import DATABASE_CONNECTION_URI
from backend.models.user import User
from backend.models.UserTypemodels import UserType




# ------------------------------
# FIXTURE: Base de datos aislada (mock)
# ------------------------------
@pytest.fixture
def app():
    #Crea una app Flask temporal con base de datos mock.
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # base en memoria
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with flask_app.app_context():
        db.create_all()  # crea las tablas
        yield flask_app
        db.drop_all()  # elimina las tablas al finalizar


@pytest.fixture
def client(app):
    #Crea un cliente de prueba vinculado a la app mock.
    return app.test_client()


# ------------------------------
# TEST 1: Crear usuario en base mock
# ------------------------------
def test_crear_usuario_en_db_mock(app):
    #Verifica que se puede crear y leer un usuario en la base de datos de prueba.
    with app.app_context():
        user = User(username="mockuser", email="mock@example.com", password="1234")
        db.session.add(user)
        db.session.commit()

        user_en_db = User.query.filter_by(email="mock@example.com").first()
        assert user_en_db is not None
        assert user_en_db.username == "mockuser"


# ------------------------------
# TEST 2: Asegurar aislamiento (no persiste entre tests)
# ------------------------------
def test_db_mock_aislada(app):
    #La base de datos en memoria se resetea en cada test.
    with app.app_context():
        usuarios = User.query.all()
        assert len(usuarios) == 0  # No debe haber usuarios de otros tests


# ------------------------------
# TEST 3: Endpoint con mock DB
# ------------------------------
def test_register_con_mock(client, app):
    #Prueba la ruta /register usando la base de datos mock.
    json = {
        "username": "caro",
        "email": "caro@example.com",
        "password": "1234"
    }
    response = client.post("/register", data=json, follow_redirects=True)
    assert response.status_code in (200, 302)

    # Verificar que se haya insertado en la base de datos mock
    with app.app_context():
        user = User.query.filter_by(email="caro@example.com").first()
        assert user is not None
 """