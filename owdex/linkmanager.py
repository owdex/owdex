import re
from uuid import uuid4 as uuid

import flask as f
from flask import current_app as app

from bs4 import BeautifulSoup as bs
from pysolr import Solr
from requests import get
from url_normalize import url_normalize


class Link:
    def __init__(
        self,
        *,
        url,
        title,
        submitter,
        index=None,
        id=None,
        content=None,
        description=None,
        score=0,
        **kwargs,
    ):
        self.url = url_normalize(url)
        self.title = title
        self.index = index
        self.submitter = submitter
        self.score = score
        self.__dict__.update(kwargs)

        if content and description and id:
            self.content, self.description, self.id = content, description, id
        else:
            self.id = str(uuid())
            self.content, self.description = self.scrape()

    def scrape(self):
        response = get(self.url).text
        soup = bs(response, features="html.parser")

        # get all "text" content from the HTML
        content = soup.get_text()
        # replace all whitespace (including sequential blocks) with a single space
        content = re.sub(r"\s+", " ", content)

        # get description from meta
        meta_description = soup.find("meta", attrs={"name": "description"})
        # get description from opengraph
        og_description = soup.find("meta", attrs={"property": "og:description"})
        # if there was a description, set that, otherwise just use content
        description = (
            meta_description.get("content")
            if meta_description
            else og_description.get("content")
            if og_description
            else content
        )

        # normalise description length. we subtract 1 extra so we have space to add the ellipsis.
        if len(description) > app.config["DESCRIPTION_MAX_LENGTH"]:
            description = description[: app.config["DESCRIPTION_MAX_LENGTH"] - 1] + "&hellip;"

        return content, description


class LinkManager:
    """Manage link entries in multiple indices, and serves as a wrapper for the underlying Solr database."""

    def __init__(self, host, port, indices):
        """Creates a LinkManager instance.

        Args:
            indices (list): A dict from an indices.json file.
            host (str): The hostname at which the Solr instance can be reached.
            port (int): The port at which the Solr instance can be reached.
        """
        self.config = indices["config"]
        self._dbs = {
            core_name: Solr(f"http://{host}:{port}/solr/{core_name}")
            for core_name in indices["indices"]
        }

    def get(self, id, core=None):
        return self.search(f"id:{id}", core=core)[0]

    def add(self, entry, core=None):
        """Add an entry to the specified index on the specified core.

        Args:
            core (str): A core in the LinkManager.
            entry (Link): The entry to add.
        """

        if core and entry.index:
            index = entry.index
        else:
            submission_pool = self.config["default_add"].split(".")
            core = submission_pool[0]
            index = submission_pool[1]

        self._dbs[core].add(
            {
                "index": index,
                "id": entry.id,
                "url": entry.url,
                "submitter": entry.submitter,
                "score": entry.score,
                "title": entry.title,
                "content": entry.content,
                "description": entry.description,
            },
            commit=True,
        )

    def vote(self, id, core=None):
        """Register a vote for an entry.

        Args:
            id (str): The internal ID of the entry.
        """
        if not core:
            core = self.config["default_search"]
        self._dbs[core].add({"id": id, "score": {"inc": 1}}, commit=True)

    def search(self, query, core=None, sort="score desc"):
        """Perform a search of the specified indices for the query.

        Args:
            query (str): The query to pass to the underlying Solr database.
            core (str): The names of the indices in which to search.

        Returns:
            list: A list of result dicts.
        """
        if not core:
            core = self.config["default_search"]
        results = []
        for result in self._dbs[core].search(query, sort=sort):
            results.append(Link(**{attr: result[attr] for attr in result}))
        return results


def get_title(url):
    return bs(get(url_normalize(url)).text, features="html.parser").find("title").text
