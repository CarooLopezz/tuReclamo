# backend/routes/auth_routes.py
from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from backend.models.user import User
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
            token = request.headers.get("Authorization") or session.get("token")
            if not token:
                return jsonify({"message": "Falta el token"}), 401
            try:
                if " " in token:
                    token = token.split()[1]  # Bearer <token>
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
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("El email ya está registrado", "danger")
            return redirect(url_for("auth.register"))

        # Encriptar la contraseña antes de guardarla
        hashed_password = generate_password_hash(password)

        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Registro exitoso. Inicia sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

# -------------------- LOGIN --------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Email o contraseña incorrectos", "danger")
            return redirect(url_for("auth.login"))

        # 🔑 Crear token JWT
        token = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.utcnow() + timedelta(hours=1)
            },
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        # 🔹 Guardamos el token en sesión si querés usarlo en plantillas
        session["token"] = token

        flash("Inicio de sesión exitoso", "success")
        return jsonify({"message": "Login exitoso", "token": token})

    return render_template("auth/login.html")

""" 
# -------------------- DASHBOARD --------------------
@auth_bp.route("/dashboard")
@token_required()
def dashboard(current_user):
    return render_template("inicio/inicio.html", username=current_user.username, role=current_user.role)

# -------------------- LISTA DE USUARIOS (ADMIN) --------------------
@auth_bp.route("/users")
@token_required(role="admin")
def list_users(current_user):
    users = User.query.all()
    users_data = [{"id": u.id, "username": u.username, "email": u.email, "role": u.role} for u in users]
    return render_template("auth/users.html", users=users_data)

# -------------------- LOGOUT -------------------- cierra sesión
@auth_bp.route("/logout")
def logout():
    session.pop("token", None)
    flash("Has cerrado sesión", "success")
    return redirect(url_for("auth.login"))
 """
