import flask as f
from flask import current_app as app

import pysolr

from urllib import request
from bs4 import BeautifulSoup as bs
from url_normalize import url_normalize


class Link:

    def __init__(self, url, title, submitter=None):
        self.url = url_normalize(url)
        self.title = title
        self.submitter = submitter if submitter else app.config[
            "ANONYMOUS_SUBMITTER"]

        with request.urlopen(url) as response:
            soup = bs(response.read(), features="html.parser")
            self.content = soup.get_text()
            description = soup.find("meta", attrs={"name": "description"})
            if description:
                self.description = description.get("content")

    def to_dict(self, export_to="db"):
        dict = {
            "url": self.url,
            "title": self.title,
            "submitter": self.submitter,
        }
        if export_to == "db":
            # Add info we need for adding to the database but not for export
            dict = dict | {
                "description": self.description,
                "content": self.content
            }
        return dict


class LinkManager:

    def __init__(self, indices, host="solr", port=8983):
        self._indices = {}
        for index_name in indices:
            self._indices[index_name] = pysolr.Solr(
                f"http://{host}:{port}/solr/{index_name}")

    def add(self, *, index, url, title, submitter):
        # We force arguments to be named for readability by using *
        link = Link(url, title, submitter)
        self._indices[index].add(link.to_dict(), commit=True)
        return link

    def search(self, index, query):
        return self._indices[index].search(query)
