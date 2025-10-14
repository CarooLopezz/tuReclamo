import os
import json
from app import app
from backend.models.db import db
from backend.models.user import User
from backend.models.UserTypemodels import UserType
from backend.models.reclamo import Reclamo
from backend.models.director_sector import DirectorSector
from datetime import datetime


DATA_DIR = "backend/data"

def populate_users(data):
    created = 0
    for item in data:
        user_id = item.get("id")
        username = item.get("username")
        email = item.get("email")
        password = item.get("password")  
        role = item.get("role")

        # Obtener datos del tipo de usuario
        user_type_data = item.get("user_type")
        if not user_type_data:
            print(f"El usuario {username} no tiene user_type, se omite.")
            continue

        ut_id = user_type_data.get("id")
        ut_tipo = user_type_data.get("tipo")

        #  Buscar el tipo de usuario (forma nueva SQLAlchemy 2.0)
        user_type = db.session.get(UserType, ut_id)
        if not user_type:
            user_type = UserType(id=ut_id, tipo=ut_tipo)
            db.session.add(user_type)

        #  Verificar duplicado por ID, username o email
        exists = User.query.filter(
            (User.id == user_id) |
            (User.username == username) |
            (User.email == email)
        ).first()

        if exists:
            continue

        #  Crear nuevo usuario
        user = User(
            id=user_id,
            username=username,
            email=email,
            password=password,
            role=role,
            user_type_id=ut_id
        )
        db.session.add(user)
        created += 1

    return created

def populate_user_types(data):
    created = 0
    for item in data:
        id = item.get("id")
        tipo = item.get("tipo")

        if not id or not tipo:
            print("Tipo de usuario inválido, se omite.")
            continue

        exists = db.session.get(UserType, id)
        if exists:
            continue

        user_type = UserType(id=id, tipo=tipo)
        db.session.add(user_type)
        created += 1

    return created


# ---------------- RECLAMOS ----------------
def populate_reclamos(data):
    created = 0
    for item in data:
        reclamo_id = item.get("id")
        descripcion = item.get("descripcion")
        estado = item.get("estado", "pendiente")
        foto = item.get("foto")
        user_id = item.get("user_id")
        director_sector_id = item.get("director_sector_id")
        fecha_creacion = item.get("fecha_creacion", datetime.now().isoformat())

        # Validaciones
        if not descripcion or not user_id:
            print(f"Reclamo inválido: falta descripcion o user_id.")
            continue

        if not db.session.get(User, user_id):
            print(f"Usuario {user_id} no existe, reclamo omitido.")
            continue

        if director_sector_id and not db.session.get(DirectorSector, director_sector_id):
            print(f"Director sector {director_sector_id} no existe, reclamo omitido.")
            continue

        # Validar duplicado por descripción y usuario
        exists = Reclamo.query.filter_by(descripcion=descripcion, user_id=user_id).first()
        if exists:
            print(f"Reclamo duplicado encontrado, se omite: {descripcion}")
            continue

        # Validar fecha
        try:
            fecha = datetime.fromisoformat(fecha_creacion)
        except ValueError:
            print(f"Fecha inválida '{fecha_creacion}', usando datetime.now()")
            fecha = datetime.now()

        reclamo = Reclamo(
            id=reclamo_id,
            descripcion=descripcion,
            estado=estado,
            foto=foto,
            user_id=user_id,
            director_sector_id=director_sector_id,
            fecha_creacion=fecha
        )

        db.session.add(reclamo)
        created += 1
        print(f"Reclamo creado: {descripcion[:30]}...")

    return created

def populate_director_sectores(data):
    created = 0
    for item in data:
        id = item.get("id")
        name = item.get("name")
        user_type_id = item.get("user_type_id")

        if not name or not user_type_id:
            print(f"❌ Sector inválido: falta nombre o user_type_id.")
            continue

    # Verificar que el user_type exista
        user_type = db.session.get(UserType, user_type_id)
        if not user_type:
            print(f"❌ El user_type_id {user_type_id} no existe, se omite el sector {name}.")
            continue


        exists = DirectorSector.query.get(id)
        if exists:
            continue

        director = DirectorSector(id=id, name=name, user_type_id=user_type_id)
        db.session.add(director)
        created += 1

    return created

def populate_all():
    with app.app_context():
        # --- USER TYPES ---
        filepath_types = os.path.join(DATA_DIR, "user_types.json")
        if os.path.exists(filepath_types):
            with open(filepath_types, "r", encoding="utf-8") as file:
                types_data = json.load(file)
            print("📌 Insertando tipos de usuario desde user_types.json...")
            created_types = populate_user_types(types_data)
            print(f"✅ {created_types} tipos de usuario insertados.")
        else:
            print("❌ No se encontró user_types.json")

        # --- DIRECTOR SECTORES ---
        filepath_sectores = os.path.join(DATA_DIR, "director_sectores.json")
        if os.path.exists(filepath_sectores):
            with open(filepath_sectores, "r", encoding="utf-8") as file:
                director_data = json.load(file)
            print("📌 Insertando director_sectores desde director_sectores.json...")
            created_sectores = populate_director_sectores(director_data)
            print(f"✅ {created_sectores} director_sectores insertados.")
        else:
            print("❌ No se encontró director_sectores.json")

        # --- USERS ---
        filepath_users = os.path.join(DATA_DIR, "users.json")
        if os.path.exists(filepath_users):
            with open(filepath_users, "r", encoding="utf-8") as file:
                user_data = json.load(file)
            print("📌 Insertando usuarios desde users.json...")
            created_users = populate_users(user_data)
            print(f"✅ {created_users} usuarios insertados.")
        else:
            print("❌ No se encontró users.json")

        # --- RECLAMOS ---
        filepath_reclamos = os.path.join(DATA_DIR, "reclamos.json")
        if os.path.exists(filepath_reclamos):
            with open(filepath_reclamos, "r", encoding="utf-8") as file:
                reclamo_data = json.load(file)
            print("📌 Insertando reclamos desde reclamos.json...")
            created_reclamos = populate_reclamos(reclamo_data)
            print(f"✅ {created_reclamos} reclamos insertados.")
        else:
            print("❌ No se encontró reclamos.json")

        # 💾 COMMIT final
        db.session.commit()
        print("🚀 Seed completado con éxito.")


if __name__ == "__main__":
    populate_all()