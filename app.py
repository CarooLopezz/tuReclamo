from flask import Flask, render_template
from backend.config.config import DATABASE_CONNECTION_URI
from backend.models.db import db
from backend.routes.user_routes import users 
from backend.models.user import User
from backend.models.userTypemodels import UserType
from backend.models.director_sector import DirectorSector
from backend.routes.director_sector import director_sector
from backend.routes.userTyperoutes import user_type_bp # NUEVO

app = Flask(__name__, template_folder='frontend/templates')
app.register_blueprint(users)
app.register_blueprint(director_sector)
app.register_blueprint(user_type_bp)

app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True  
app.secret_key = 'clave-repiola'

db.init_app(app)

with app.app_context():
    from backend.models.user import User
    from backend.models.userTypemodels import UserType
    from backend.models.director_sector import DirectorSector
    db.drop_all()
    db.create_all()
    

 #Registrar rutas


if __name__ == '__main__':
    app.run(debug=True)