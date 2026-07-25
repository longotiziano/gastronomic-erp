from flask import Blueprint, render_template
from utils.helpers import is_admin

sales_bp = Blueprint("sales", __name__)

@sales_bp.route("/sales")
def render_sales():
    
    return render_template("sections/sales.html",

        is_admin=is_admin())