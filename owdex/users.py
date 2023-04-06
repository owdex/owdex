import flask as f
from flask import current_app as app
from argon2.exceptions import VerifyMismatchError

from .usermanager import require_login

users_bp = f.Blueprint("users", __name__, template_folder="templates")


@users_bp.route("/login", methods=["GET", "POST"])
@app.limiter.limit(
    "5/minute;10/hour;25/day",
    scope="users",
    deduct_when=lambda response: response.status_code != 200,
)
def login():
    status = None

    if f.request.method == "POST":
        username = f.request.form["username"]
        password = f.request.form["password"]
        try:
            app.um.verify(username, password)
        except VerifyMismatchError:
            # wrong password
            status = 401
        except KeyError:
            # no such username
            status = 401
        else:
            # login successful
            f.session["user"] = username
            status = 200

    return f.render_template("login.html"), status


@users_bp.route("/signup", methods=["GET", "POST"])
@app.limiter.limit(
    "5/minute;10/hour;25/day",
    scope="users",
)
def signup():
    status = None

    if f.request.method == "POST":
        try:
            app.um.create(f.request.form["username"],
                          f.request.form["password"])
        except KeyError:
            # username already exists
            status = 409
        else:
            status = 200

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
