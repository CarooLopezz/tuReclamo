from backend.models.db import db

class UserType(db.Model):
    __tablename__ = "user_type"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'vecino', 'administrador'
    director_sector_id = db.Column(db.Integer, db.ForeignKey('director_sector.id_reclamo'), nullable=True)

    user = db.relationship('User', backref='userTypemodels', lazy=True)

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'vecino', 'administrador'
    directorSecto_id = db.Column(db.Integer, db.ForeignKey('directorSecto.id'), nullable=True)

    usuario = db.relationship('Usuario', backref='user_types', lazy=True)
    directorSecto = db.relationship('DirectorSecto', backref='user_types', lazy=True)


    def __repr__(self):
        return f"<UserType {self.id} - {self.tipo}>"
