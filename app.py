import os
from flask import Flask
from backend.models.db import db
from backend.routes.director_sector import director_sector
from backend.routes.UserTyperoutes import user_type_bp
from dotenv import load_dotenv
from backend.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS# Cargar variables del .env
load_dotenv()

app = Flask(__name__)

# Configurar SQLAlchemy con MySQL
db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("MYSQL_HOST")
db_name = os.getenv("MYSQL_DB")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar DB
db.init_app(app)
# Crea todas las tablas de tus modelos en MySQL si no existen
with app.app_context():
    db.create_all() 
 
# Registrar rutas
app.register_blueprint(director_sector)
app.register_blueprint(user_type_bp)

if __name__ == "__main__":
    app.run(debug=True)
