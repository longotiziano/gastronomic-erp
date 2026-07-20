from flask import Blueprint, redirect, render_template, request, url_for

from database.models.raw_material import RawMaterial, RawMaterialCategory
from services.bars import obtain_bars
from services.raw_materials import  create_raw_material, obtain_raw_materials, update_raw_material, alt_raw_material_status
from services.raw_materials_categories import obtain_raw_material_categories, create_raw_material_category, update_raw_material_category, alt_raw_material_category_status
from utils.auth_decorator import admin_required
from utils.exceptions import ValidationError
from utils.flashes import flash_message
from utils.helpers import is_admin

raw_materials_bp = Blueprint("raw_materials", __name__)

@raw_materials_bp.get("/raw-materials")
@admin_required
def render_raw_materials():
    pagination_rm = obtain_raw_materials()
    pagination_rmc = obtain_raw_material_categories()
    raw_materials: list[RawMaterial] = pagination_rm.items
    categories: list[RawMaterialCategory] = pagination_rmc.items
    

    rm_cols = ["ID", "Nombre", "Categoría", "Stock", "Estado"]
    rm_rows = [
        {
            "cells": [item.id, item.name, item.category.name if item.category else "-", item.stock.amount if item.stock else 0, item.record_status],
            "data": {
                "id": item.id,
                "name": item.name,
                "category_id": item.category_id,
                "amount": item.stock.amount if item.stock else 0,
                "record_status": item.record_status
            },
        }
        for item in raw_materials
    ]

    cat_cols = ["ID", "Nombre", "Estado"]
    cat_rows = [
        {
            "cells": [cat.id, cat.name, cat.record_status],
            "data": {
                "id": cat.id,
                "name": cat.name,
                "record_status": cat.record_status,
            },
        }
        for cat in categories
    ]

    return render_template(
        "abm/raw_materials.html",
        page_title="Administrar materias primas",
        tables=[
            {
                "id": "raw-materials",
                "title": "Materias primas",
                "cols": rm_cols,
                "rows": rm_rows,
                "plus_label": "Agregar materia prima",
                "pagination": None,
                "form_template": "forms/raw_materials_form.html",
                "main_content": True,
                "get_form_action": url_for("raw_materials.render_raw_materials"),
                "pagination": pagination_rm
            },
            {
                "id": "raw-material-categories",
                "title": "Categorías",
                "cols": cat_cols,
                "rows": cat_rows,
                "pagination": None,
                "form_template": "forms/raw_categories_form.html",
                "secondary_content": True,
                "get_form_action": url_for("raw_materials.render_raw_materials"),
                "pagination": pagination_rmc
            },
        ],

        categories=categories,  # para el <select> del form de materia prima
        deactivate_row=True,
        is_modal=True,
        abm_mode=True,
        form_action='users/update',
        is_admin=is_admin()
    )


# --- Materias primas ---

@raw_materials_bp.post("/raw-materials/create")
@admin_required
def create():
    name = request.form.get("name", type=str)
    category_id = request.form.get("category_id", type=int)

    if not name or not category_id:
        raise ValidationError("Nombre y categoría son requeridos.")

    create_raw_material(name=name, category_id=category_id)
    flash_message("Materia prima creada correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials"))


@raw_materials_bp.post("/raw-materials/update/<int:raw_material_id>")
@admin_required
def update(raw_material_id: int):
    updates = {
        "name": request.form.get("name", type=str),
        "category_id": request.form.get("category_id", type=int),
    }
    update_raw_material(raw_material_id, updates)
    flash_message("Materia prima actualizada correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials"))


@raw_materials_bp.post("/raw-materials/alt_status/<int:raw_material_id>")
@admin_required
def alt_status(raw_material_id: int):
    alt_raw_material_status(raw_material_id)
    flash_message("Estado de la materia prima actualizado correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials"))


@raw_materials_bp.post("/raw-materials/categories/create")
@admin_required
def create_category():
    name = request.form.get("name", type=str)

    if not name:
        raise ValidationError("El nombre de la categoría es requerido.")

    create_raw_material_category(name=name)
    flash_message("Categoría creada correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials"))


@raw_materials_bp.post("/raw-materials/categories/update/<int:category_id>")
@admin_required
def update_category(category_id: int):
    updates = {
        "name": request.form.get("name", type=str),
    }
    update_raw_material_category(category_id, updates)
    flash_message("Categoría actualizada correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials"))


@raw_materials_bp.post("/raw-materials/categories/alt_status/<int:category_id>")
@admin_required
def alt_status_category(category_id: int):
    alt_raw_material_category_status(category_id)
    flash_message("Estado de la categoría actualizado correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials"))