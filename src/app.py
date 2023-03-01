import flask as f
import os
import pysolr

app = f.Flask(__name__)

DEV_MODE = True

db_prefix = "http://solr:8983/solr/" if not DEV_MODE else "http://localhost:8983/solr/"

db = {
    "stable": pysolr.Solr(db_prefix + "stable"),
    "unstable": pysolr.Solr(db_prefix + "unstable"),
    "archive": pysolr.Solr(db_prefix + "archive")
}

@app.route("/")
def home():
    return f.render_template("home.html")

@app.route("/add")
def add():
    return f.render_template("add.html")

@app.route("/about")
def about():
    return f.render_template("about.html")

@app.route("/ping")
def ping():
    if DEV_MODE:
        return db["stable"].ping()
    else:
        return "Not in development mode, ping not allowed!"

@app.route("/search")
def search():
    query = f.request.args.get('query')
    indices = f.request.args.getlist('index')
    sort = f.request.args.get('sort')
    results = [
        {"url":"https://example.com","title":"An example webpage","extract":"This is an extract from an example webpage."},
        {"url":"https://example.com","title":"An example webpage","extract":"This is an extract from an example webpage."},
        {"url":"https://example.com","title":"An example webpage","extract":"This is an extract from an example webpage."},
        {"url":"https://example.com","title":"An example webpage","extract":"This is an extract from an example webpage."},
        {"url":"https://example.com","title":"An example webpage","extract":"This is an extract from an example webpage."}
    ]
    return f.render_template("search.html", query=query, indices=indices, sort=sort, results=results)

if __name__ == '__main__':
    from waitress import serve
    port = int(os.environ.get('PORT', 80))
    serve(app, host='0.0.0.0', port=port)
