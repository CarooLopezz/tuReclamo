
from db import get_connection
from datetime import datetime

class Reclamo:
    def __init__(self, id_reclamo=None, descripcion="", id_vecino=None, id_sector_resp=None,
                 estado="pendiente", foto=None, fecha_creacion=None):
        self.id_reclamo = id_reclamo
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion if fecha_creacion else datetime.now()
        self.estado = estado
        self.id_vecino = id_vecino
        self.id_sector_resp = id_sector_resp
        self.foto = foto

    def __str__(self):
        return f"Reclamo({self.id_reclamo}, {self.descripcion}, {self.estado})"

    # Guardar un nuevo reclamo en la base de datos
    def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO reclamos (descripcion, estado, id_vecino, id_sector_resp, foto)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (self.descripcion, self.estado, self.id_vecino, self.id_sector_resp, self.foto)
        cursor.execute(sql, valores)
        conn.commit()
        self.id_reclamo = cursor.lastrowid
        cursor.close()
        conn.close()

    # Cambiar el estado de un reclamo
    def cambiar_estado(self, nuevo_estado):
        conn = get_connection()
        cursor = conn.cursor()
        sql = "UPDATE reclamos SET estado = %s WHERE id_reclamo = %s"
        cursor.execute(sql, (nuevo_estado, self.id_reclamo))
        conn.commit()
        self.estado = nuevo_estado
        cursor.close()
        conn.close()

    # Obtener todos los reclamos (lista de diccionarios)
    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reclamos")
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados
