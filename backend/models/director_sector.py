from .db import db  # import relativo al mismo nivel

class DirectorSector(db.Model):
    __tablename__ = "director_sector"

    
    id_director = db.Column(db.Integer, primary_key=True, autoincrement=True)
    

    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    user = db.relationship("User")

    # Reclamos que supervisa
    """ id_reclamo = db.Column(db.Integer, db.ForeignKey("reclamo.id_reclamo"), nullable=False)
    reclamo = db.relationship("Reclamo") """

    

    def __repr__(self):
        return f"<DirectorSector {self.id_director} - Usuario {self.id_usuario}>"