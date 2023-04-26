import flask as f
from flask import current_app as app

from pysolr import SolrError

search_bp = f.Blueprint("search", __name__, template_folder="templates")


@search_bp.route("/results")
def results():
    query = f.request.args.get("query", "*")
    core = f.request.args.get("core", app.settings.links.defaults.search)
    indices = f.request.args.getlist("indices")
    sort = f.request.args.get("sort", "score desc")  # TODO: default sort in config

    sort = {"relevance": "score desc"}[sort]

    try:
        results = app.lm.search(query, core, indices, sort)
    except SolrError as e:
        if "org.apache.solr.search.SyntaxError" in str(e):
            f.flash("That query seems to be causing an issue. Try again with a different search.")
            results = []
        else:
            raise

    return f.render_template(
        "results.html", query=query, core=core, indices=indices, sort=sort, results=results
    )


@search_bp.route("/advanced")
def advanced():
    return f.render_template(
        "advanced.html",
        cores=app.lm.cores.keys(),
        indices=app.lm.cores[app.settings.links.defaults.search],
    )


@search_bp.route("/fetch_indices")
def fetch_indices():
    core = f.request.args.get("core")
    return f.render_template("htmx/index_input.html", indices=app.lm.cores[core])
