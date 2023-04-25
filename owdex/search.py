import flask as f
from flask import current_app as app

from pysolr import SolrError

search_bp = f.Blueprint("search", __name__, template_folder="templates")


@search_bp.route("/results")
def results():
    query = f.request.args.get("query")
    results = []

    try:
        results = app.lm.search(query)
    except SolrError as e:
        if "org.apache.solr.search.SyntaxError" in str(e):
            f.flash("That query seems to be causing an issue. Try again with a different search.")
        else:
            raise

    return f.render_template(
        "results.html", query=query, results=results, core=app.settings.links.defaults.search
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
