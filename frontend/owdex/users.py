import flask as f
from flask import current_app as app
from argon2.exceptions import VerifyMismatchError

from .exportmanager import entries_to_record
from .usermanager import require_login

users_bp = f.Blueprint("users", __name__, template_folder="templates")


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    success = None

    if f.request.method == "POST":
        username = f.request.form["username"]
        password = f.request.form["password"]
        try:
            app.um.verify(username, password)
        except VerifyMismatchError:
            # wrong password
            success = False
        except KeyError:
            # no such username
            success = False
        else:
            # login successful
            f.session["user"] = username
            success = True

    return f.render_template("login.html", success=success)


@users_bp.route("/signup", methods=["GET", "POST"])
def signup():
    success = None

    if f.request.method == "POST":
        try:
            app.um.create(f.request.form["username"],
                          f.request.form["password"])
        except KeyError:
            success = False

    return f.render_template("signup.html", success=success)


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
