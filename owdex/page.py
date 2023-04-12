import flask as f

page_bp = f.Blueprint("page", __name__, template_folder="templates")


@page_bp.route("/")
def home():
    return f.render_template("home.html")


@page_bp.route("/about")
def about():
    return f.render_template("about.html")
