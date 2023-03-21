import flask as f
import pysolr


def get_dbs():
    dbs = {
        db_name: pysolr.Solr(f"http://solr:8983/solr/{db_name}")
        for db_name in ["stable", "unstable", "archive"]
    }
    return dbs
