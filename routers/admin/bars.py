from flask import Blueprint, redirect, render_template, request, url_for

from services.base_service import BaseCrudService
from database.repositories.bars import BarRepository
from utils.auth_decorator import admin_required
from utils.exceptions import ValidationError
from utils.flashes import flash_message
from utils.helpers import is_admin

bars_bp = Blueprint("bars", __name__)
bars_service = BaseCrudService(BarRepository(), entity_name="bar")

@bars_bp.get("/bars")
@admin_required
def render_bars():
    bars = bars_service.filter_sort("bars")
    cols = ["Nombre", "Dirección", "Fecha de creación", "Estado"]
    rows = [
        {
            "cells": [bar.name, bar.address or "-", bar.created_at.strftime("%d-%m-%Y"), bar.record_status],
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
        page_title="Administrar bares",
        tables=[
            {
                "id": "bars",
                "title": "Bares",
                "cols": cols,
                "rows": rows,
                "pagination": None,
                "form_template": "forms/bars_form.html",
            }
        ],

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
