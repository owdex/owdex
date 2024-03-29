import flask as f
from flask import current_app as app

from .linkmanager import Link, get_title, normalized_url

add_bp = f.Blueprint("add", __name__, template_folder="templates")


@add_bp.route("/add", methods=["GET", "POST"])
def add():
    if f.request.method == "POST":
        l = Link.create(
            url=f.request.form["url"],
            title=f.request.form["title"],
            submitter=f.request.form["submitter"],
        )
        app.lm.add(l)
        f.flash("Successfully added webpage!")
        return f.render_template("add.html", submitter=f.request.form["submitter"]), 201

    else:
        try:
            submitter = app.um.get_current()["username"]
        except KeyError:
            if app.settings.links.anonymous.allowed:
                submitter = app.settings.links.anonymous.submitter
            else:
                raise

        return f.render_template("add.html", submitter=submitter)


@add_bp.route("/fetch_title")
def fetch_title():
    title = get_title(f.request.args.get("url"))
    return f.render_template("htmx/title_input.html", value=title)


@add_bp.route("/norm_url")
def normalize_url():
    url = normalized_url(f.request.args.get("url"))
    return f.render_template("htmx/url_input.html", value=url)
