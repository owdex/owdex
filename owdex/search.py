import flask as f
from flask import current_app as app

from pysolr import SolrError

search_bp = f.Blueprint("search", __name__, template_folder="templates")


@search_bp.route("/search")
def search_results():
    query = f.request.args.get("query")
    results = []

    results = app.lm.search(query, app.config["DEFAULT_INDICES"])

    return f.render_template(
        "search.html", query=query, indices=app.config["DEFAULT_INDICES"], results=results
    )
