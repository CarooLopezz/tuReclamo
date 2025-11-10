# backend/routes/auth_routes.py

from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from backend.models.user import User
from backend.models.UserTypemodels import UserType
from backend.models.db import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import current_app as app
from functools import wraps
from datetime import datetime, timedelta
from flask_login import current_user


auth_bp = Blueprint("auth", __name__,  template_folder='templates' )
# -------------------- DECORADOR PARA TOKEN --------------------
def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if "token" in session:
                token = session["token"]
     
            elif "Authorization" in request.headers:
                token = request.headers["Authorization"].split()[1]

            if not token:
                return jsonify({"message": "Falta el token"}), 401

            try:
                data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
                current_user = User.query.get(data["id"])
                if not current_user:
                    return jsonify({"message": "Usuario no encontrado"}), 404
                if role and current_user.role != role:
                    return jsonify({"message": "No autorizado"}), 403
            except Exception as e:
                return jsonify({"message": "Token inválido", "error": str(e)}), 401

            return f(current_user, *args, **kwargs)
        return decorated
    return decorator
#---------------------REGISTER-------------------------

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            data = request.get_json()
            print("Datos recibidos:", data)

            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            role = data.get("role")

            if not all([username, email, password, role]):
                return jsonify({"message": "Todos los campos son obligatorios"}), 400

            # Verificar si el email ya existe
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({"message": "El email ya está registrado"}), 400

            # Encriptar la contraseña
            hashed_password = generate_password_hash(password)

            # 🔸 Asignar tipo de usuario según el rol elegido
            if role.lower() == "director":
                tipo = UserType.query.filter_by(nombre="Director").first()
            else:
                tipo = UserType.query.filter_by(nombre="Vecino").first()

            if not tipo:
                return jsonify({"message": "Tipo de usuario no configurado"}), 500

            nuevo_user = User(
                username=username,
                email=email,
                password=hashed_password,
                role=role,
                user_type_id=tipo.id
            )

            db.session.add(nuevo_user)
            db.session.commit()

            return jsonify({"message": "Usuario registrado correctamente"}), 201

        except Exception as e:
            print("ERROR EN /register:", e)
            return jsonify({"error": str(e)}), 500

    return render_template("auth/register.html")

# -------------------- LOGIN --------------------
@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        try:
            data = request.get_json()  
        except Exception as e:
            print("Error leyendo JSON:", e)
            return jsonify({"message": "Error al leer JSON"}), 400

        if not data:
            return jsonify({"message": "No se recibieron datos"}), 400

        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({"message": "Email o contraseña incorrectos"}), 401

        token = jwt.encode(
            {"id": user.id, "exp": datetime.utcnow() + timedelta(hours=1)},
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        # 🔥 Redirección según rol
        if user.role == "Director":
            redirect_url = "/dashboard"
        else:
            redirect_url = "/dashboardSector"

        return jsonify({
            "message": "Login exitoso",
            "token": token,
            "role": user.role,
            "username": user.username,
            "redirect": redirect_url
        }), 200

    return render_template("auth/login.html")

# -------------------- DASHBOARD VECINO --------------------

""" @auth_bp.route("/dashboard", methods=["GET"])
def dashboard():
    auth_header = request.headers.get("Authorization") 

    if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "No hay token"}), 401

    token = auth_header.split(" ")[1] 

    try: 
        decoded = jwt.decode( app.config["SECRET_KEY"], algorithms=["HS256"])
        user = User.query.get(decoded["id"])

        if not user:
                return jsonify({"message": "Usuario no encontrado"}), 404

        if user.role == "director":
                return render_template("directorSector/directorSector.html", user=user)
        else:
                return render_template("dashboard/dashboard.html", user=user)

    except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expirado"}), 401
    except jwt.InvalidTokenError:
            return jsonify({"message": "Token inválido"}), 401  """
@auth_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard/dashboard.html")


""" @dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    reclamos = Reclamo.query.order_by(Reclamo.id.desc()).all()
    return render_template("dashboard.html", reclamos=reclamos) 
# -------------------- LOGOUT -------------------- cierra sesión
@auth_bp.route("/logout")
def logout():
    session.pop("token", None)
    flash("Has cerrado sesión", "success")
    return redirect(url_for("auth.login"))
 """
