# backend/__init__.py
from flask import Flask
from dotenv import load_dotenv
import os
from backend.models.db import db
from backend.routes.user_routes import users
from backend.routes.UserTyperoutes import user_type_bp
from backend.routes.reclamo_routes import reclamo_bp
from backend.routes.director_sector import director_sector

load_dotenv()  # carga variables desde .env

def create_app():
    app = Flask(__name__, template_folder='frontend/templates')

    # Construir la URL de conexión MySQL desde .env
    user = os.environ.get("MYSQL_USER", "root")
    password = os.environ.get("MYSQL_PASSWORD", "")
    host = os.environ.get("MYSQL_HOST", "127.0.0.1")
    db_name = os.environ.get("MYSQL_DB", "tureclamo")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.secret_key = os.environ.get("SECRET_KEY", "clave-repiola")

    # Inicializar la DB
    db.init_app(app)

    # Registrar Blueprints
    app.register_blueprint(users)
    app.register_blueprint(user_type_bp)
    app.register_blueprint(reclamo_bp)
    app.register_blueprint(director_sector)

    return app
