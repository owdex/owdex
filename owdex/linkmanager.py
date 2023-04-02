import flask as f
from flask import current_app as app

import pysolr

from urllib import request
from bs4 import BeautifulSoup as bs
from url_normalize import url_normalize


class LinkManager:

    def __init__(self, indices, host="solr", port=8983):
        self._indices = {}
        for index_name in indices:
            self._indices[index_name] = pysolr.Solr(
                f"http://{host}:{port}/solr/{index_name}")

    def add(self, *, index, url, title, submitter=None):
        # We force arguments to be named for readability by using *
        url = url_normalize(url)

        submitter = submitter if submitter \
            else app.config["ANONYMOUS_SUBMITTER"]
        # this can't be the default param because current_app isn't available initially

        with request.urlopen(url) as response:
            soup = bs(response.read(), features="html.parser")
            content = soup.get_text()
            description = soup.find("meta", attrs={"name": "description"})

            # if there was a description, set that, otherwise just use content
            description = description.get(
                "content") if description else content

            if len(description) > app.config["DESCRIPTION_MAX_LENGTH"]:
                description = description[:app.
                                          config["DESCRIPTION_MAX_LENGTH"] -
                                          1] + "&hellip;"
                # we subtract 1 extra so we have space to add the ellipsis

        self._indices[index].add(
            {
                "url": url,
                "title": title,
                "submitter": submitter,
                "content": content,
                "description": description,
                "votes": 1
            },
            commit=True)
    
    def vote(self, index, id):
        self._indices[index].add({
            "id": id,
            "votes": {"inc": 1}
        }, commit=True)

    def search(self, index, query):
        return self._indices[index].search(query)
