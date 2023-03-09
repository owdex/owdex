import flask as f

static_page = f.Blueprint('static_page', __name__, template_folder="templates")


@static_page.route("/")
def home():
    return f.render_template("home.html")


@static_page.route("/about")
def about():
    return f.render_template("about.html")
