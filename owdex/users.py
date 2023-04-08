from http import HTTPStatus

import flask as f
from flask import current_app as app
from argon2.exceptions import VerifyMismatchError

from .error import error
from .usermanager import require_login

users_bp = f.Blueprint("users", __name__, template_folder="templates")


@users_bp.route("/login", methods=["GET", "POST"])
@app.limiter.limit(
    "5/minute;10/hour;25/day",
    scope="users",
    deduct_when=lambda response: response.status_code != HTTPStatus.OK,
)
def login():
    if f.request.method == "POST":
        username = f.request.form["username"]
        password = f.request.form["password"]
        try:
            app.um.verify(username, password)
        except VerifyMismatchError:
            return error(HTTPStatus.UNAUTHORIZED,
                         explanation="Wrong username or password")
        except KeyError:
            return error(HTTPStatus.UNAUTHORIZED,
                         explanation="Wrong username or password")
        else:
            f.session["user"] = username
    return f.render_template("login.html")


@users_bp.route("/signup", methods=["GET", "POST"])
@app.limiter.limit(
    "5/minute;10/hour;25/day",
    scope="users",
)
def signup():
    if f.request.method == "POST":
        try:
            app.um.create(f.request.form["username"],
                          f.request.form["password"])
        except KeyError:
            return error(HTTPStatus.CONFLICT, explanation="A user with that username already exists!")
        else:
            status = HTTPStatus.CREATED
    else:
        status = HTTPStatus.OK
    return f.render_template("signup.html"), status


@users_bp.route("/logout")
def logout():
    f.session.pop("user", None)
    return "Logged out"


@users_bp.route("/protected")
@require_login
def protected():
    return f"Logged in as {app.um.get_current()['username']}"


@users_bp.route("/admin")
@require_login(needs_admin=True)
def admin():
    return f.render_template("admin.html")
