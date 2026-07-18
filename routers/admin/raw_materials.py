from flask import Blueprint, redirect, render_template, request, url_for

from services.raw_materials import create_raw_material, obtain_raw_materials, update_raw_material, alt_raw_material_status
from database.repositories.raw_materials import RawMaterialCategoryRepository
from utils.auth_decorator import admin_required
from utils.exceptions import ValidationError
from utils.flashes import flash_message
from utils.helpers import is_admin

raw_materials_bp = Blueprint("raw_materials", __name__)


@raw_materials_bp.get("/raw-materials")
@admin_required
def render_raw_materials():
    raw_materials = obtain_raw_materials()
    categories = RawMaterialCategoryRepository().get_all(active_only=False)
    cols = ["ID", "Nombre", "Categoría", "Estado"]
    rows = [
        {
            "cells": [item.id, item.name, item.category.name if item.category else "-", item.record_status],
            "data": {
                "id": item.id,
                "name": item.name,
                "category_id": item.category_id,
                "record_status": item.record_status,
            },
        }
        for item in raw_materials
    ]

    return render_template(
        "abm/raw_materials.html",
        cols=cols,
        rows=rows,
        page_title="Administrar materias primas",
        title="Materias primas",
        plus_label="Agregar materia prima",
        pagination=None,
        form_title="Administrar materia prima",
        deactivate_row=True,
        is_modal=True,
        abm_mode=True,
        form_action=url_for("raw_materials.update", raw_material_id=0),
        categories=categories,
        is_admin=is_admin(),
    )


@raw_materials_bp.post("/raw-materials/create")
@admin_required
def create():
    name = request.form.get("name", type=str)
    category_id = request.form.get("category_id", type=int)

    if not name or not category_id:
        raise ValidationError("Nombre y categoría son requeridos.")

    create_raw_material(name=name, category_id=category_id)
    flash_message("Materia prima creada correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials", is_admin=is_admin()))


@raw_materials_bp.post("/raw-materials/update/<int:raw_material_id>")
@admin_required
def update(raw_material_id: int):
    updates = {
        "name": request.form.get("name", type=str),
        "category_id": request.form.get("category_id", type=int),
    }
    update_raw_material(raw_material_id, updates)
    flash_message("Materia prima actualizada correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials", is_admin=is_admin()))


@raw_materials_bp.post("/raw-materials/alt_status/<int:raw_material_id>")
@admin_required
def alt_status(raw_material_id: int):
    alt_raw_material_status(raw_material_id)
    flash_message("Estado de la materia prima actualizado correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials", is_admin=is_admin()))
