from flask import Blueprint, redirect, url_for, render_template, request, session, jsonify

from database.models.user import User
from utils.auth_decorator import admin_required
from services.users import alt_user_status, obtain_users, create_user, update_user
from services.bars import obtain_bars
from utils.exceptions import ValidationError
from utils.flashes import flash_message
from utils.helpers import format_date, is_admin

users_bp = Blueprint("users", __name__, )

@users_bp.get("/users")
@admin_required
def render_users():
    pagination = obtain_users()
    bars = obtain_bars()
    users: list[User] = pagination.items
    print(users)
    cols = ['ID', 'Nombre', 'Email', 'Dirección', 'Rol', 'Salario diario', 'Bar', 'Fecha de creación', 'Estado']
    rows = [
        {
            "cells": [u.id, u.name, u.email, u.address, u.rol.value, 
                    u.daily_salary, u.bar.name, format_date(u.created_at), u.record_status],
            "data": {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "address": u.address,
                "rol": u.rol.value,
                "leave_at": u.leave_at,
                "daily_salary": u.daily_salary,
                "bar_id": u.bar.id,
                "created_at": format_date(u.created_at),
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
        pagination=pagination,

        form_title="Administrar usuario",
        deactivate_row=True,
        is_modal=True,
        abm_mode=True,
        form_action=url_for('users.update', user_id=0),
        bars=bars,
        is_admin=is_admin()
    )

@users_bp.post("/users/create")
@admin_required
def create():
    name = request.form.get("name", type=str)
    email = request.form.get("email", type=str)
    password = request.form.get("password", type=str)
    rol = request.form.get("rol", type=str, default="waiter")
    daily_salary = request.form.get("daily_salary", type=float, default=0.0)
    address = request.form.get("address", type=str)
    bar = request.form.get("bar_id", type=int)
    print(f"\nEL BAR ES {bar}\n")
    print(f"\nES INT: {isinstance(bar, int)}\n")
    if not name or not email or not password or not bar:
        raise ValidationError("Nombre, email, contraseña y bar son requeridos.")

    create_user(name, email, password, bar, rol, address, daily_salary)
    flash_message("Usuario creado correctamente.", category="success")
    return redirect(url_for("users.render_users", is_admin=is_admin()))

@users_bp.post("/users/update/<int:user_id>")
@admin_required
def update(user_id: int):
    updates = {
        "name": request.form.get("name", type=str),
        "email": request.form.get("email", type=str),
        "password": request.form.get("password", type=str),
        "rol": request.form.get("rol", type=str),
        "daily_salary": request.form.get("daily_salary", type=float),
        "address": request.form.get("address", type=str),
        "bar_id": request.form.get("bar_id", type=int)
    }
    update_user(user_id, updates)
    flash_message("Usuario actualizado correctamente.", category="success")
    return redirect(url_for("users.render_users", is_admin=is_admin()))

@users_bp.post("/users/alt_status/<int:user_id>")
@admin_required
def alt_status(user_id: int):
    alt_user_status(user_id)
    flash_message("Estado del usuario actualizado correctamente.", category="success")
    return redirect(url_for("users.render_users", is_admin=is_admin()))