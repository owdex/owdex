from http import HTTPStatus

import flask as f
from flask import current_app as app
from werkzeug import exceptions

from argon2.exceptions import VerifyMismatchError

from .usermanager import require_login

users_bp = f.Blueprint("users", __name__, template_folder="templates")


@users_bp.route("/", methods=["GET"])
def account():
    return f.render_template("account.html")


@users_bp.route("/login", methods=["POST"])
@app.limiter.limit(
    "3/minute;10/hour;20/day",
    scope="users",
    deduct_when=lambda response: response.status_code == HTTPStatus.UNAUTHORIZED,
)
def login():
    try:
        username = f.request.form["username"]
        password = f.request.form["password"]
        app.um.verify(username, password)
    except (VerifyMismatchError, KeyError):
        raise exceptions.Unauthorized("Wrong username or password!")
    else:
        f.session["user"] = username
        return f.redirect(f.url_for("page.home"))


@users_bp.route("/signup", methods=["POST"])
@app.limiter.limit(
    "3/minute;10/hour;20/day",
    scope="users",
    deduct_when=lambda response: response.status_code in (HTTPStatus.CONFLICT, HTTPStatus.CREATED),
)
def signup():
    try:
        app.um.create(f.request.form["username"], f.request.form["password"])
    except KeyError:
        raise exceptions.Conflict("A user with that username already exists!")
    else:
        f.session["user"] = f.request.form["username"]
        return f.redirect(f.url_for("page.home")), HTTPStatus.CREATED


@users_bp.route("/logout")
def logout():
    f.session.pop("user", None)
    return f.redirect(f.url_for("page.home"))
