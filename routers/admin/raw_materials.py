from flask import Blueprint, redirect, render_template, request, url_for

from services.raw_materials import RawMaterialService, RawMaterialCategoryService
from utils.auth_decorator import admin_required
from utils.flashes import flash_message
from utils.helpers import is_admin

raw_materials_bp = Blueprint("raw_materials", __name__)
rm_service = RawMaterialService()
rmc_service = RawMaterialCategoryService()

@raw_materials_bp.get("/raw-materials")
@admin_required
def render_raw_materials():
    pagination_rm = rm_service.filter_sort()
    pagination_rmc = rmc_service.filter_sort()
    
    table_rm = rm_service.get_table_metadata(pagination_rm, is_main=True)
    table_rmc = rmc_service.get_table_metadata(pagination_rmc, is_main=False)
    
    table_rm["get_form_action"] = request.path
    table_rmc["get_form_action"] = request.path

    return render_template(
        "abm/raw_materials.html",
        page_title="Administrar materias primas",
        tables=[table_rm, table_rmc],
        categories=rmc_service.repo.get_all(),
        deactivate_row=True,
        is_modal=True,
        abm_mode=True,
        is_admin=is_admin()
    )

@raw_materials_bp.post("/raw-materials/create")
@admin_required
def create():
    rm_service.create(**request.form.to_dict())
    flash_message("Materia prima creada correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials"))


@raw_materials_bp.post("/raw-materials/update/<int:raw_material_id>")
@admin_required
def update(raw_material_id: int):
    rm_service.update(raw_material_id, request.form.to_dict())
    flash_message("Materia prima actualizada correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials"))


@raw_materials_bp.post("/raw-materials/alt_status/<int:raw_material_id>")
@admin_required
def alt_status(raw_material_id: int):
    rm_service.alt_status(raw_material_id)
    flash_message("Estado de la materia prima actualizado correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials"))


@raw_materials_bp.post("/raw-materials/categories/create")
@admin_required
def create_category():
    rmc_service.create(**request.form.to_dict())
    flash_message("Categoría creada correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials"))


@raw_materials_bp.post("/raw-materials/categories/update/<int:category_id>")
@admin_required
def update_category(category_id: int):
    rmc_service.update(category_id, request.form.to_dict())
    flash_message("Categoría actualizada correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials"))


@raw_materials_bp.post("/raw-materials/categories/alt_status/<int:category_id>")
@admin_required
def alt_status_category(category_id: int):
    rmc_service.alt_status(category_id)
    flash_message("Estado de la categoría actualizado correctamente.", category="success")
    return redirect(url_for("raw_materials.render_raw_materials"))