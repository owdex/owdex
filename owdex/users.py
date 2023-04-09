from http import HTTPStatus

import flask as f
from flask import current_app as app
from argon2.exceptions import VerifyMismatchError

from .error import error
from .usermanager import require_login

users_bp = f.Blueprint("users", __name__, template_folder="templates")

@users_bp.route("/account/<action>", methods=["POST"])
@users_bp.route("/account", methods=["GET"])
@app.limiter.limit(
    "3/minute;10/hour;20/day",
    scope="users",
    deduct_when=lambda response: response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.CONFLICT, HTTPStatus.CREATED)
    # this will rate-limit failed logins, and both successful and failed creations.
)
def account(action=None):
    if not action:
        return f.render_template("account.html")

    if action == "login":
        try:
            username = f.request.form["username"]
            password = f.request.form["password"]
            app.um.verify(username, password)
        except (VerifyMismatchError, KeyError):
            return error(HTTPStatus.UNAUTHORIZED, explanation=f"Wrong username or password!")
        else:
            f.session["user"] = username
            return f.redirect(f.url_for("page.home"))

    elif action == "signup":
        try:
            app.um.create(f.request.form["username"], f.request.form["password"])
        except KeyError:
            return error(HTTPStatus.CONFLICT, explanation="A user with that username already exists!")
        else:
            f.session["user"] = f.request.form["username"]
            return f.redirect(f.url_for("page.home")), HTTPStatus.CREATED
    
    else:
        return f.render_template("account.html"), HTTPStatus.BAD_REQUEST

    


@users_bp.route("/logout")
def logout():
    f.session.pop("user", None)
    return f.redirect(f.url_for("page.home"))
