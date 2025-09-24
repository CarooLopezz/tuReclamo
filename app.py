from flask import Flask
from backend.models.db import db
from backend.routes.director_sector import director_sector
from backend.routes.UserTyperoutes import user_type_bp  # NUEVO
from backend.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tu_base_de_datos.db'
# Configuración para MySQL desde config.py
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
# Crea todas las tablas de tus modelos en MySQL si no existen
with app.app_context():
    db.create_all() 
 
 #Registrar rutas
app.register_blueprint(director_sector)
app.register_blueprint(user_type_bp)


if __name__ == '__main__':
    app.run(debug=True)

