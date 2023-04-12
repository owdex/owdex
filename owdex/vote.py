import flask as f
from flask import current_app as app

from .usermanager import require_login

vote_bp = f.Blueprint("vote", __name__)


@vote_bp.route("/vote", methods=["POST"])
@require_login
def vote():
    app.lm.vote(f.request.form["index"], f.request.form["id"])
    return f.Response(status=204)
