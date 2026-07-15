from flask import Blueprint, render_template, request, session

from database.models.user import User
from services.users import login_user
from utils.auth_decorator import admin_required
from services.users import obtain_users

users_bp = Blueprint("users", __name__, )

@users_bp.get("/users")
@admin_required
def render_users():
    pagination = obtain_users()
    users: list[User] = pagination.items
    cols = ['ID', 'Nombre', 'Email', 'Dirección', 'Rol', 'Salario diario', 'Bar', 'Fecha de creación', 'Estado']
    rows = [
    {
        "cells": [u.id, u.name, u.email, u.address, u.rol, 
                  u.leave_at, u.daily_salary, u.bar.name, u.created_at, u.record_status],
        "data": {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "address": u.address,
            "rol": u.rol,
            "leave_at": u.leave_at,
            "daily_salary": u.daily_salary,
            "bar_id": u.bar.name,
            "created_at": u.created_at,
            "record_status": u.record_status
        }
    }
    for u in users
    ]

    return render_template('admin/abm/users.html',
        cols=cols,
        rows=rows,
        page_title="Administrar usuarios",
        title="Usuarios",
        plus_label="Agregar usuario",
        admin_user=True,
        pagination=pagination
    )

@users_bp.get("/auth/signup")
@admin_required
def signup():
    return render_template("auth/signup.html")

@users_bp.post("/auth/login")
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return render_template("auth/login.html", error="Email y contraseña son requeridos")
    
    user = login_user(email, password)
    session["user_role"] = user.rol.value if user.rol else None
    session["user_id"] = user.id
    return render_template("index.html")

@users_bp.post("/auth/logout")
def logout():
    session.clear()
    return render_template("index.html")