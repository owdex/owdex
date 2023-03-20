import flask as f
from pysolr import SolrError

from .solr import get_dbs

search = f.Blueprint('add', __name__, template_folder="templates")


@search.route("/search")
def search_results():
    query = f.request.args.get("query")
    indices = f.request.args.getlist("index")
    sort = f.request.args.get("sort")
    results = []

    dbs = get_dbs()

    try:
        results = dbs["unstable"].search(query)
    except SolrError as e:
        if "org.apache.solr.search.SyntaxError" in str(e):
            f.flash(
                "That query seems to be causing an issue. Try again with a different search."
            )
        else:
            raise

    return f.render_template("search.html",
                             query=query,
                             indices=indices,
                             sort=sort,
                             results=results)
