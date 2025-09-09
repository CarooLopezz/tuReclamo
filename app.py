from flask import Flask
from backend.models.db import db
from backend.routes.director_sector import director_sector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tu_base_de_datos.db'

db.init_app(app)

 #Registrar rutas
app.register_blueprint(director_sector)

if __name__ == '__main__':
    app.run(debug=True)

