import urllib.request

import flask as f
from flask import current_app as app

import bs4
from url_normalize import url_normalize as urlnorm

from .solr import get_dbs

add = f.Blueprint('search', __name__, template_folder="templates")


@add.route("/add", methods=["GET", "POST"])
def add_page():
    if f.request.method == "POST":
        url = urlnorm(f.request.form["url"])
        title = f.request.form["title"]
        submitter = f.request.form["submitter"]

        if not submitter:
            submitter = app.config["ANONYMOUS_SUBMITTER"]

        with urllib.request.urlopen(url) as response:
            soup = bs4.BeautifulSoup(response.read(), features="html.parser")
            content = soup.get_text()
            description = soup.find("meta", attrs={"name": "description"})
            if description:
                description = description.get("content")

        dbs = get_dbs()
        dbs["unstable"].add(
            {
                "url": url,
                "title": title,
                "description": description,
                "submitter": submitter,
                "content": content
            },
            commit=True)

        f.flash("Successfully added webpage!")
        return f.render_template("add.html", submitter=submitter), 201

    else:
        try:
            submitter = app.um.get_current()["username"]
        except KeyError:
            submitter = app.config["ANONYMOUS_SUBMITTER"]

        return f.render_template("add.html", submitter=submitter)
