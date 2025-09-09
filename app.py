from flask import Flask
from backend.models.db import db
from backend.routes.director_sector import director_sector
from backend.routes.reclamos import reclamos_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tu_base_de_datos.db'
app.register_blueprint(reclamos_bp)  # ✅ registramos rutas de reclamos

db.init_app(app)

 #Registrar rutas
app.register_blueprint(director_sector)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ✅ crea las tablas en la BD si no existen
    app.run(debug=True)


