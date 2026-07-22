from flask import Blueprint, redirect, render_template, request, url_for

from services.bars import BarService
from services.products import ProductCategoryService, ProductService
from utils.auth_decorator import admin_required
from utils.exceptions import ValidationError
from utils.flashes import flash_message
from utils.helpers import is_admin

products_bp = Blueprint("products", __name__)
p_service = ProductService()
pc_service = ProductCategoryService()
bar_service = BarService()

@products_bp.get("/products")
@admin_required
def render_products():
    products = p_service.filter_sort()
    categories = pc_service.filter_sort()
    bars = bar_service.filter_sort()

    product_cols = ["Nombre", "Categoría", "Precio", "Bar", "Estado"]
    product_rows = [
        {
            "cells": [
                item.name,
                item.category.name if item.category else "-",
                item.price,
                item.bar.name if item.bar else "-",
                item.record_status,
            ],
            "data": {
                "id": item.id,
                "name": item.name,
                "category_id": item.category_id,
                "price": item.price,
                "bar_id": item.bar_id,
                "record_status": item.record_status,
            },
        }
        for item in products.items
    ]

    category_cols = ["Nombre", "Sector", "Estado"]
    category_rows = [
        {
            "cells": [cat.name, cat.sector.value if cat.sector else "-", cat.record_status],
            "data": {
                "id": cat.id,
                "name": cat.name,
                "sector": cat.sector.value if cat.sector else "",
                "record_status": cat.record_status,
            },
        }
        for cat in categories.items
    ]

    return render_template(
        "abm/products.html",
        page_title="Administrar productos",
        tables=[
            {
                "id": "products",
                "title": "Productos",
                "cols": product_cols,
                "rows": product_rows,
                "plus_label": "Agregar producto",
                "form_template": "forms/products_form.html",
                "main_content": True,
                "get_form_action": url_for("products.render_products"),
                "search_value": request.args.get("products_search", type=str, default=""),
            },
            {
                "id": "product-categories",
                "title": "Categorías",
                "cols": category_cols,
                "rows": category_rows,
                "form_template": "forms/product_categories_form.html",
                "secondary_content": True,
                "get_form_action": url_for("products.render_products"),
                "search_value": request.args.get("product-categories_search", type=str, default=""),
            },
        ],
        categories=categories,
        bars=bars,
        raw_materials=raw_materials,
        deactivate_row=True,
        is_modal=True,
        abm_mode=True,
        is_admin=is_admin(),
    )


@products_bp.post("/products/create")
@admin_required
def create():
    name = request.form.get("name", type=str)
    category_id = request.form.get("category_id", type=int)
    price = request.form.get("price", type=str)
    bar_id = request.form.get("bar_id", type=int)
    recipe_raw_material_id = request.form.get("recipe_raw_material_id", type=int)
    recipe_amount = request.form.get("recipe_amount", type=str)

    if not name or not category_id or not bar_id:
        raise ValidationError("Nombre, categoría y bar son requeridos.")

    create_product(
        name=name,
        category_id=category_id,
        price=price,
        bar_id=bar_id,
        recipe_raw_material_id=recipe_raw_material_id,
        recipe_amount=recipe_amount,
    )
    flash_message("Producto creado correctamente.", category="success")
    return redirect(url_for("products.render_products"))


@products_bp.post("/products/update/<int:product_id>")
@admin_required
def update(product_id: int):
    updates = {
        "name": request.form.get("name", type=str),
        "category_id": request.form.get("category_id", type=int),
        "price": request.form.get("price", type=str),
        "bar_id": request.form.get("bar_id", type=int),
        "recipe_raw_material_id": request.form.get("recipe_raw_material_id", type=int),
        "recipe_amount": request.form.get("recipe_amount", type=str),
    }
    update_product(product_id, updates)
    flash_message("Producto actualizado correctamente.", category="success")
    return redirect(url_for("products.render_products"))


@products_bp.post("/products/alt_status/<int:product_id>")
@admin_required
def alt_status(product_id: int):
    alt_product_status(product_id)
    flash_message("Estado del producto actualizado correctamente.", category="success")
    return redirect(url_for("products.render_products"))


@products_bp.post("/products/categories/create")
@admin_required
def create_category():
    name = request.form.get("name", type=str)
    sector = request.form.get("sector", type=str)

    if not name:
        raise ValidationError("El nombre de la categoría es requerido.")

    create_product_category(name=name, sector=sector or ProductSector.kitchen.value)
    flash_message("Categoría creada correctamente.", category="success")
    return redirect(url_for("products.render_products"))


@products_bp.post("/products/categories/update/<int:category_id>")
@admin_required
def update_category(category_id: int):
    updates = {
        "name": request.form.get("name", type=str),
        "sector": request.form.get("sector", type=str),
    }
    update_product_category(category_id, updates)
    flash_message("Categoría actualizada correctamente.", category="success")
    return redirect(url_for("products.render_products"))


@products_bp.post("/products/categories/alt_status/<int:category_id>")
@admin_required
def alt_status_category(category_id: int):
    alt_product_category_status(category_id)
    flash_message("Estado de la categoría actualizado correctamente.", category="success")
    return redirect(url_for("products.render_products"))
