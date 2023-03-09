import flask as f

from .solr import get_dbs

search = f.Blueprint('add', __name__, template_folder="templates")


@search.route("/search")
def search_results():
    query = f.request.args.get("query")
    indices = f.request.args.getlist("index")
    sort = f.request.args.get("sort")

    dbs = get_dbs()
    results = dbs["unstable"].search(query)

    return f.render_template("search.html",
                             query=query,
                             indices=indices,
                             sort=sort,
                             results=results)
