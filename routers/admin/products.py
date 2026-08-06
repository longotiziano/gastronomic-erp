from flask import Blueprint, redirect, render_template, request, url_for

from database.models.bar import Bar
from database.models.raw_material import RawMaterial
from services.products import ProductService, ProductCategoryService
from utils.auth_decorator import admin_required
from utils.flashes import flash_message
from utils.helpers import is_admin

products_bp = Blueprint("products", __name__)
product_service = ProductService()
product_category_service = ProductCategoryService()

@products_bp.get("/products")
@admin_required
def render_products():
    pagination_product = product_service.filter_sort()
    pagination_product_category = product_category_service.filter_sort()
    
    table_product = product_service.get_table_metadata(
        pagination_product.items, pagination_product, is_main=True)
    table_product_category = product_category_service.get_table_metadata(
        pagination_product_category.items, pagination_product_category, is_main=False)
    
    table_product["filters"] = product_service.get_filters_config()
    table_product_category["filters"] = product_category_service.get_filters_config()
    table_product["sorts"] = product_service.get_sorts_config()
    table_product_category["sorts"] = product_category_service.get_sorts_config()
    
    table_product["get_form_action"] = request.path
    table_product_category["get_form_action"] = request.path

    return render_template(
        "abm/products.html",
        page_title="Administrar productos",
        tables=[table_product, table_product_category],
        categories=product_category_service.repo.get_all(), # Para poblar el select del modal
        raw_materials=product_service.repo.get_all(model=RawMaterial),
        bars=product_service.repo.get_all(model=Bar),
        deactivate_row=True,
        is_modal=True,
        abm_mode=True,
        is_admin=is_admin()
    )

@products_bp.post("/products/create")
@admin_required
def create():
    form = request.form

    # Campos escalares del producto
    product_data = {
        "name": form.get("name"),
        "price": float(form.get("price")),
        "category_id": int(form.get("category_id")),
        "bar_id": int(form.get("bar_id")),
    }

    # Campos de lista (recetas)
    raw_material_ids = form.getlist("recipe_raw_material_id[]")
    amounts = form.getlist("recipe_amount[]")

    if len(raw_material_ids) != len(amounts):
        raise ValueError("Datos de receta inconsistentes")

    recipes = [
        {"raw_material_id": int(rm_id), "amount": float(amount)}
        for rm_id, amount in zip(raw_material_ids, amounts)
        if rm_id and amount
    ]

    ProductService().create(**product_data, recipes=recipes)
    flash_message("Producto creado correctamente.", category="success")
    return redirect(url_for("products.render_products"))


@products_bp.post("/products/update/<int:product_id>")
@admin_required
def update(product_id: int):
    product_service.update(product_id, request.form.to_dict())
    flash_message("Producto actualizado correctamente.", category="success")
    return redirect(url_for("products.render_products"))


@products_bp.post("/products/alt_status/<int:product_id>")
@admin_required
def alt_status(product_id: int):
    product_service.alt_status(product_id)
    flash_message("Estado del producto actualizado correctamente.", category="success")
    return redirect(url_for("products.render_products"))


@products_bp.post("/products/categories/create")
@admin_required
def create_category():
    product_category_service.create(**request.form.to_dict())
    flash_message("Categoría creada correctamente.", category="success")
    return redirect(url_for("products.render_products"))


@products_bp.post("/products/categories/update/<int:category_id>")
@admin_required
def update_category(category_id: int):
    product_category_service.update(category_id, request.form.to_dict())
    flash_message("Categoría actualizada correctamente.", category="success")
    return redirect(url_for("products.render_products"))


@products_bp.post("/products/categories/alt_status/<int:category_id>")
@admin_required
def alt_status_category(category_id: int):
    product_category_service.alt_status(category_id)
    flash_message("Estado de la categoría actualizado correctamente.", category="success")
    return redirect(url_for("products.render_products"))