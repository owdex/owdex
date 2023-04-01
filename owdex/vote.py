import flask as f
from flask import current_app as app

from .usermanager import require_login

vote_bp = f.Blueprint('vote', __name__)

@vote_bp.route("/vote/<id>", methods=["POST"])
@require_login
def vote(id):
	return f.Response(status=204)
