import os
from flask import Flask, render_template
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
from dotenv import load_dotenv

load_dotenv()  # carga las variables del .env

app = Flask(__name__, template_folder='frontend/templates', static_folder="frontend/static" )


app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
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
app.register_blueprint(user_type_bp)
app.register_blueprint(reclamo_bp)
app.register_blueprint(director_sector)
app.register_blueprint(auth_bp)


with app.app_context():

    print(User.query.all())
    from backend.models.user import User
    from backend.models.UserTypemodels import UserType
    from backend.models.reclamo import Reclamo
    from backend.models.director_sector import DirectorSector
    



    db.create_all()
    
if __name__ == "__main__":
    app.run(debug=True)

