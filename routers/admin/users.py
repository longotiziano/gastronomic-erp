from flask import Blueprint, redirect, url_for, render_template, request, session, jsonify

from database.models.user import User
from database.repositories.bars import BarRepository
from database.repositories.users import UserRepository
from utils.auth_decorator import admin_required
from services.base_service import BaseCrudService
from utils.exceptions import ValidationError
from utils.flashes import flash_message
from utils.helpers import format_date, is_admin

users_bp = Blueprint("users", __name__, )
users_service = BaseCrudService(repo=UserRepository(), entity_name="usuario")  # Placeholder for the actual repository
bars_service = BaseCrudService(repo=BarRepository(), entity_name="bar")  # Placeholder for the actual repository

@users_bp.get("/users")
@admin_required
def render_users():
    pagination = users_service.filter_sort("users")
    bars = bars_service.repo.get_all(active_only=True)
    users: list[User] = pagination.items

    cols = ['Nombre', 'Email', 'Dirección', 'Rol', 'Salario diario', 'Bar', 'Fecha de creación', 'Estado']
    rows = [
        {
            "cells": [u.name, u.email, u.address or "-", u.rol.value,
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

    return render_template('abm/users.html',
        page_title="Administrar usuarios",
        tables=[
            {
                "id": "users", # for `crud.js` recognition
                "title": "Usuarios",
                "cols": cols,
                "rows": rows,
                "pagination": pagination,
                "form_template": "forms/auth_form.html",
            }
        ],
        deactivate_row=True,
        is_modal=True,
        abm_mode=True,
        form_action='users/update',
        bars=bars, # used by the users' form
        is_admin=is_admin()
    )

@users_bp.post("/users/create")
@admin_required
def create():
    users_service.create(**request.form.to_dict())
    flash_message("Usuario creado correctamente.", category="success")
    return redirect(url_for("users.render_users"))

@users_bp.post("/users/update/<int:user_id>")
@admin_required
def update(user_id: int):
    users_service.update(user_id, request.form.to_dict())
    flash_message("Usuario actualizado correctamente.", category="success")
    return redirect(url_for("users.render_users"))

@users_bp.post("/users/alt_status/<int:user_id>")
@admin_required
def alt_status(user_id: int):
    users_service.alt_status(user_id)
    flash_message("Estado del usuario actualizado correctamente.", category="success")
    return redirect(url_for("users.render_users"))