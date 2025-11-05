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


# -------------------- REGISTER --------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            data = request.get_json()
            print("Datos recibidos:", data)

            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

    
            vecino_tipo = UserType.query.filter_by(tipo="vecino").first()
            if not vecino_tipo:
                return jsonify({"error": "El tipo 'vecino' no existe. Cargalo con init_user_types.py"}), 400

            hashed_password = generate_password_hash(password)
            nuevo_user = User(
                username=username,
                email=email,
                password=hashed_password,
                role="user",
                user_type_id=vecino_tipo.id
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
        

        return jsonify({
            "message": "Login exitoso",
            "token": token,
            "role": user.role,
            "username": user.username
        }), 200

    return render_template("auth/login.html")

# -------------------- DASHBOARD --------------------
@auth_bp.route("/dashboard") # solo los usuarios autenticados pueden entrar al dashboard
def dashboard():
    return render_template("dashboard/dashboard.html")
""" 
@dashboard_bp.route("/dashboard")
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
