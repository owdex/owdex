import flask as f
from flask import current_app as app

from .usermanager import require_login
from .exportmanager import entries_to_record

export_bp = f.Blueprint("export", __name__, template_folder="templates")


@export_bp.route("/")
@require_login(needs_admin=True)
def export():
    file = entries_to_record(app.lm.search("unstable", "*"))
    return f"File available <a href='{f.url_for('.download', file=file)}'>here</a>"


@export_bp.route("/download/<file>")
def download(file):
    return f.send_from_directory("/tmp/exports", file)
