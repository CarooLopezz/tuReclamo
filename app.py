from flask import Flask
from backend.models.db import db
from backend.routes.director_sector import director_sector
from backend.routes.UserTyperoutes import user_type_bp  # NUEVO




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tu_base_de_datos.db'

db.init_app(app)

 #Registrar rutas
app.register_blueprint(director_sector)
app.register_blueprint(user_type_bp)
app.register_blueprint()
app.register_blueprint(user_type_bp)


if __name__ == '__main__':
    app.run(debug=True)

