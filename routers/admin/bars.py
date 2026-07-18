from flask import Blueprint, redirect, render_template, request, url_for

from services.bars import alt_bar_status, create_bar, obtain_bars, update_bar
from utils.auth_decorator import admin_required
from utils.exceptions import ValidationError
from utils.flashes import flash_message
from utils.helpers import is_admin

bars_bp = Blueprint("bars", __name__)


@bars_bp.get("/bars")
@admin_required
def render_bars():
    bars = obtain_bars()
    cols = ["ID", "Nombre", "Dirección", "Fecha de creación", "Estado"]
    rows = [
        {
            "cells": [bar.id, bar.name, bar.address or "-", bar.created_at.strftime("%d-%m-%Y"), bar.record_status],
            "data": {
                "id": bar.id,
                "name": bar.name,
                "address": bar.address or "",
                "record_status": bar.record_status,
            },
        }
        for bar in bars
    ]

    return render_template(
        "abm/bars.html",
        cols=cols,
        rows=rows,
        page_title="Administrar bares",
        title="Bares",
        plus_label="Agregar bar",
        pagination=None,
        form_title="Administrar bar",
        deactivate_row=True,
        is_modal=True,
        abm_mode=True,
        form_action=url_for("bars.update", bar_id=0),
        is_admin=is_admin(),
    )


@bars_bp.post("/bars/create")
@admin_required
def create():
    name = request.form.get("name", type=str)
    address = request.form.get("address", type=str)

    if not name:
        raise ValidationError("El nombre del bar es requerido.")

    create_bar(name=name, address=address) # type: ignore
    flash_message("Bar creado correctamente.", category="success")
    return redirect(url_for("bars.render_bars"))


@bars_bp.post("/bars/update/<int:bar_id>")
@admin_required
def update(bar_id: int):
    updates = {
        "name": request.form.get("name", type=str),
        "address": request.form.get("address", type=str),
    }
    update_bar(bar_id, updates)
    flash_message("Bar actualizado correctamente.", category="success")
    return redirect(url_for("bars.render_bars"))


@bars_bp.post("/bars/alt_status/<int:bar_id>")
@admin_required
def alt_status(bar_id: int):
    alt_bar_status(bar_id)
    flash_message("Estado del bar actualizado correctamente.", category="success")
    return redirect(url_for("bars.render_bars"))
