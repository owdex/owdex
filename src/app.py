import os

from dotenv import load_dotenv
import flask as f
import pysolr
from url_normalize import url_normalize as urlnorm
import urllib.request
import bs4

from users import UserManager

load_dotenv()
DEV_MODE = os.environ.get("OWDEX_DEVMODE")

app = f.Flask(__name__)
app.secret_key = os.environ.get("secret_key")

um = UserManager(dev_mode=DEV_MODE)

solr_domain = "solr" if not DEV_MODE else "localhost"
dbs = {
    db_name: pysolr.Solr(f"http://{solr_domain}:8983/solr/{db_name}")
    for db_name in ["stable", "unstable", "archive"]
}


@app.route("/login", methods=["GET", "POST"])
def login():
    success = None

    if f.request.method == "POST":
        email = f.request.form["email"]
        password = f.request.form["password"]
        try:
            um.verify(email, password)
        except argon2.exceptions.VerifyMismatchError:
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


@app.route("/signup", methods=["GET", "POST"])
def signup():
    success = None

    if f.request.method == "POST":
        try:
            um.create(f.request.form["email"], f.request.form["password"])
        except KeyError:
            success = False

    return f.render_template("signup.html", success=success)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return "Logged out"


@app.route("/protected")
def protected():
    if "user" in f.session:
        return f"Logged in as {um.get(f.session['user'])}"


@app.route("/")
def home():
    return f.render_template("home.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if f.request.method == "POST":
        url = urlnorm(f.request.form["url"])
        title = f.request.form["title"]
        submitter = f.request.form["submitter"]

        with urllib.request.urlopen(url) as response:
            soup = bs4.BeautifulSoup(response.read(), features="html.parser")
            content = soup.get_text()
            description = soup.find("meta", attrs={"name": "description"})
            if description:
                description = description.get("content")

        dbs["unstable"].add(
            {
                "url": url,
                "title": title,
                "description": description,
                "submitter": submitter,
                "content": content
            },
            commit=True)
        return f.render_template("add.html")

    else:
        return f.render_template("add.html")


@app.route("/about")
def about():
    return f.render_template("about.html")


@app.route("/ping")
def ping():
    if DEV_MODE:
        return dbs["stable"].ping()
    else:
        return "Not in development mode, ping not allowed!"


@app.route("/search")
def search():
    query = f.request.args.get("query")
    indices = f.request.args.getlist("index")
    sort = f.request.args.get("sort")

    results = dbs["unstable"].search(query)

    return f.render_template("search.html",
                             query=query,
                             indices=indices,
                             sort=sort,
                             results=results)


if __name__ == "__main__":
    if DEV_MODE:
        app.run(host="127.0.0.1", port="5000", debug=True)
    else:
        from waitress import serve
        port = int(os.environ.get("PORT", 80))
        serve(app, host="0.0.0.0", port=port)
