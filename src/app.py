import flask as f
import os
import pysolr
import bs4
from url_normalize import url_normalize as urlnorm
import urllib.request

DEV_MODE = True

app = f.Flask(__name__)

db_prefix = "http://solr:8983/solr/" if not DEV_MODE else "http://localhost:8983/solr/"
dbs = {db: pysolr.Solr(db_prefix + db) for db in ["stable", "unstable", "archive"]}

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
            description = soup.find("meta", attrs={"name" : "description"})
            if description:
                description = description.get("content")

        dbs["unstable"].add({
            "url": url,
            "title": title,
            "description": description,
            "submitter": submitter,
            "content": content
        }, commit=True)
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
    query = f.request.args.get('query')
    indices = f.request.args.getlist('index')
    sort = f.request.args.get('sort')

    results = dbs["unstable"].search(query)

    return f.render_template("search.html", query=query, indices=indices, sort=sort, results=results)


if __name__ == '__main__':
    from waitress import serve
    port = int(os.environ.get('PORT', 80))
    serve(app, host='0.0.0.0', port=port)
