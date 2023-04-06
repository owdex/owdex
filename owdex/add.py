import flask as f
from flask import current_app as app

add_bp = f.Blueprint('add', __name__, template_folder="templates")


@add_bp.route("/add", methods=["GET", "POST"])
def add():
    if f.request.method == "POST":
        app.lm.add(url=f.request.form["url"],
                   title=f.request.form["title"],
                   submitter=f.request.form["submitter"],
                   index="unstable")
        f.flash("Successfully added webpage!")
        return f.render_template("add.html",
                                 submitter=f.request.form["submitter"]), 201

    else:
        try:
            submitter = app.um.get_current()["username"]
        except KeyError:
            submitter = app.config["ANONYMOUS_SUBMITTER"]

        return f.render_template("add.html", submitter=submitter)
