import os
import json
from app import app
from backend.models.db import db
from backend.models.user import User
from backend.models.UserTypemodels import UserType

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


def populate_all():
    with app.app_context():
        filepath = os.path.join(DATA_DIR, "users.json")
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        print(" Insertando usuarios desde users.json (sin duplicados)...")
        created = populate_users(data)
        db.session.commit()
        print(f" {created} usuarios nuevos insertados.")


if __name__ == "__main__":
    populate_all()
