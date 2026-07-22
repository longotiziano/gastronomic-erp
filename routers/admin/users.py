from flask import Blueprint, redirect, render_template, request, url_for

from database.models.bar import Bar
from services.users import UserService
from utils.auth_decorator import admin_required
from utils.flashes import flash_message
from utils.helpers import is_admin

users_bp = Blueprint("users", __name__)
users_service = UserService()

@users_bp.get("/users")
@admin_required
def render_users():
    pagination_users = users_service.filter_sort()
    
    table_users = users_service.get_table_metadata(pagination_users, is_main=True)
    
    table_users["get_form_action"] = request.path

    return render_template(
        "abm/users.html",
        page_title="Administrar usuarios",
        tables=[table_users],
        bars=users_service.repo.get_all(model=Bar),
        deactivate_row=True,
        is_modal=True,
        abm_mode=True,
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
