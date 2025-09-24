import os
from flask import Flask
from backend.models.db import db
from backend.routes.director_sector import director_sector
from dotenv import load_dotenv

load_dotenv()  # carga las variables del .env

app = Flask(__name__)

# Configuración usando las variables del .env
db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("MYSQL_HOST")
db_name = os.getenv("MYSQL_DB")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Registrar rutas
app.register_blueprint(director_sector)
app.register_blueprint(user_type_bp)


if __name__ == "__main__":
    app.run(debug=True)

