from flask import Flask, render_template
from backend.config.config import DATABASE_CONNECTION_URI
from backend.models.db import db
from backend.models.user import User
from backend.models.UserTypemodels import UserType
from backend.models.reclamo import Reclamo
from backend.models.director_sector import DirectorSector
from backend.routes.user_routes import users
from backend.routes.UserTyperoutes import user_type_bp # NUEVO
from backend.routes.reclamo_routes import reclamo_bp # NUEVO
from backend.routes.director_sector import director_sector



app = Flask(__name__, template_folder='frontend/templates')
app.register_blueprint(users)
app.register_blueprint(user_type_bp)
app.register_blueprint(reclamo_bp)
app.register_blueprint(director_sector)

app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["TEMPLATES_AUTO_RELOAD"] = True  
app.secret_key = 'clave-repiola'

db.init_app(app)

with app.app_context():
    from backend.models.user import User
    from backend.models.UserTypemodels import UserType
    from backend.models.reclamo import Reclamo
    from backend.models.director_sector import DirectorSector
    
    db.drop_all()
    db.create_all()
    

 #Registrar rutas


if __name__ == '__main__':
    app.run(debug=True)

