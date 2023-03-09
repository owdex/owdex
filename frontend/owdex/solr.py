import flask as f
import pysolr


def get_dbs():
    solr_domain = "solr" if not f.current_app.config["DEBUG"] else "localhost"
    dbs = {
        db_name: pysolr.Solr(f"http://{solr_domain}:8983/solr/{db_name}")
        for db_name in ["stable", "unstable", "archive"]
    }
    return dbs
