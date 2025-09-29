# backend/routes/auth_routes.py
from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from backend.models.user import User
from backend.models.db import db

auth_bp = Blueprint("auth", __name__,  template_folder='templates' )

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

        user = User(username=username, email=email)
        user.set_password(password)
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
        if not user or not user.check_password(password):
            flash("Email o contraseña incorrectos", "danger")
            return redirect(url_for("auth.login"))

    

    return render_template("auth/login.html")

