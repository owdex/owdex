from functools import wraps, partial

import flask as f
from argon2.exceptions import VerifyMismatchError

users = f.Blueprint("users", __name__, template_folder="templates")


def get_current_user():
    return f.current_app.um.get(f.session['user'])


def require_login(endpoint=None, needs_admin=False):
    if endpoint is None:
        return partial(require_login, needs_admin=needs_admin)

    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        if "user" not in f.session:
            return "Not logged in!", 401
        elif needs_admin and not get_current_user()["admin"]:
            return "Not an admin!", 403
        else:
            return endpoint(*args, **kwargs)

    return wrapper


@users.route("/login", methods=["GET", "POST"])
def login():
    success = None

    if f.request.method == "POST":
        email = f.request.form["email"]
        password = f.request.form["password"]
        try:
            f.current_app.um.verify(email, password)
        except VerifyMismatchError:
            # wrong password
            success = False
        except KeyError:
            # no such email
            success = False
        else:
            # login successful
            f.session["user"] = email
            success = True

    return f.render_template("login.html", success=success)


@users.route("/signup", methods=["GET", "POST"])
def signup():
    success = None

    if f.request.method == "POST":
        try:
            f.current_app.um.create(f.request.form["email"],
                                    f.request.form["password"])
        except KeyError:
            success = False

    return f.render_template("signup.html", success=success)


@users.route("/logout")
def logout():
    f.session.pop("user", None)
    return "Logged out"


@users.route("/protected")
@require_login
def protected():
    return f"Logged in as {get_current_user()}"


@users.route("/admin")
@require_login(needs_admin=True)
def admin():
    return f.render_template("admin.html")
