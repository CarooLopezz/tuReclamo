import os
import jwt
from flask import Flask, render_template,send_from_directory
from backend.config.config import DATABASE_CONNECTION_URI
from backend.models.db import db
from backend.models.user import User
from backend.models.UserTypemodels import UserType
from backend.models.reclamo import Reclamo
from backend.models.director_sector import DirectorSector
from backend.routes.user_routes import users
from backend.routes.UserTyperoutes import user_type_bp 
from backend.routes.reclamo_routes import reclamo_bp 
from backend.routes.director_sector import director_sector
from backend.routes.auth_routes import auth_bp
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from flask_cors import CORS
from flask_mail import Mail
load_dotenv()  # carga las variables del .env
app = Flask(__name__, template_folder='frontend/templates', static_folder="frontend/static")

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tuemail@gmail.com'
app.config['MAIL_PASSWORD'] = 'tu_clave_de_aplicacion'
app.config['MAIL_DEFAULT_SENDER'] = 'tuemail@gmail.com'

mail = Mail(app)

CORS(app, supports_credentials=True)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'clave-repiola'

db.init_app(app)
migrate = Migrate(app, db)

# Configuración usando las variables del .env
db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("MYSQL_HOST")
db_name = os.getenv("MYSQL_DB")

app.register_blueprint(users)
app.register_blueprint(reclamo_bp)
app.register_blueprint(user_type_bp)
app.register_blueprint(director_sector)
app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()
    print(User.query.all())

    directores_data = [
        {"username": "director_oeste", "email": "oeste@municipio.com", "password": "1234"},
        {"username": "director_este", "email": "este@municipio.com", "password": "1234"},
        {"username": "director_norte", "email": "norte@municipio.com", "password": "1234"},
        {"username": "director_sur", "email": "sur@municipio.com", "password": "1234"}
    ]

    director_tipo = UserType.query.filter_by(tipo="director_sector").first()
    if not director_tipo:
        print("⚠️ No existe el tipo 'director_sector'. Cargalo primero con init_user_types.py")
    else:
        for data in directores_data:
            if not User.query.filter_by(email=data["email"]).first():
                hashed_password = generate_password_hash(data["password"])
                nuevo_director = User(
                    username=data["username"],
                    email=data["email"],
                    password=hashed_password,
                    user_type_id=director_tipo.id
                )
                db.session.add(nuevo_director)
                print(f"✅ Director {data['username']} agregado")

        db.session.commit()
        print("✔️ Todos los directores de sector fueron cargados.")



    @app.route('/images/images_reclamo/<filename>')
    def serve_reclamo_image(filename):
        image_dir = os.path.join(os.getcwd(), 'images', 'images_reclamo')
        return send_from_directory(image_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
