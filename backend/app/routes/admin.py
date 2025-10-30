"""
Rutas para el panel de administración HTML.
"""

from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin", methods=["GET"])
def admin_panel():
    """
    Sirve el panel de administración HTML.

    Returns:
        HTML: Panel de administración con CRUD completo
    """
    return render_template("admin.html")
