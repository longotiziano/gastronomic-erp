from flask import Blueprint, redirect, render_template, request, url_for

from services.bars import BarService
from utils.auth_decorator import admin_required
from utils.flashes import flash_message
from utils.helpers import is_admin

bars_bp = Blueprint("bars", __name__)
bars_service = BarService()

@bars_bp.get("/bars")
@admin_required
def render_bars():
    pagination_bars = bars_service.filter_sort()
    
    table_bars = bars_service.get_table_metadata(pagination_bars, is_main=True)
    
    table_bars["get_form_action"] = request.path

    return render_template(
        "abm/bars.html",
        page_title="Administrar bares",
        tables=[table_bars],
        deactivate_row=True,
        is_modal=True,
        abm_mode=True,
        is_admin=is_admin()
    )


@bars_bp.post("/bars/create")
@admin_required
def create():
    bars_service.create(**request.form.to_dict())
    flash_message("Bar creado correctamente.", category="success")
    return redirect(url_for("bars.render_bars"))


@bars_bp.post("/bars/update/<int:bar_id>")
@admin_required
def update(bar_id: int):
    bars_service.update(bar_id, request.form.to_dict())
    flash_message("Bar actualizado correctamente.", category="success")
    return redirect(url_for("bars.render_bars"))


@bars_bp.post("/bars/alt_status/<int:bar_id>")
@admin_required
def alt_status(bar_id: int):
    bars_service.alt_status(bar_id)
    flash_message("Estado del bar actualizado correctamente.", category="success")
    return redirect(url_for("bars.render_bars"))
