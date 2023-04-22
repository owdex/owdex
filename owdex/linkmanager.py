import re
from dataclasses import KW_ONLY, dataclass
from uuid import uuid4 as uuid

import flask as f
from flask import current_app as app

from bs4 import BeautifulSoup as bs
from pysolr import Solr
from requests import get
from url_normalize import url_normalize


@dataclass
class Link:
    _: KW_ONLY
    index: str
    id: str

    url: str
    title: str
    submitter: str

    content: str
    description: str
    score: int

    @classmethod
    def create(cls, *, url, title, submitter, index=None):
        index = "unstable" if index is None else index  # TODO: respect settings
        url = url_normalize(url)
        content, description = scrape(url)
        return cls(
            index=index,
            id=str(uuid()),
            url=url,
            title=title,
            submitter=submitter,
            content=content,
            description=description,
            score=0,
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            **{
                key: value
                for key, value in data.items()
                if key
                in ["index", "id", "url", "title", "submitter", "content", "description", "score"]
            }
        )

    def rescrape(self):
        self.content, self.description = scrape(self.url)


class LinkManager:
    """Manage link entries in multiple indices, and serves as a wrapper for the underlying Solr database."""

    def __init__(self, host, port, indices):
        """Creates a LinkManager instance.

        Args:
            indices (list): A dict from an indices.json file.
            host (str): The hostname at which the Solr instance can be reached.
            port (int): The port at which the Solr instance can be reached.
        """
        self._dbs = {
            core_name: Solr(f"http://{host}:{port}/solr/{core_name}") for core_name in indices
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
            submission_pool = app.settings.links.defaults.add.split(".")
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
            core = app.settings.links.defaults.search
        self._dbs[core].add({"id": id, "score": {"inc": 1}}, commit=True)

    def search(self, query, core=None, sort="score desc"):
        """Perform a search of the specified indices for the query.

        Args:
            query (str): The query to pass to the underlying Solr database.
            core (str): The names of the indices in which to search.

        Returns:    url: str

            list: A list of result dicts.
        """
        core = app.settings.links.defaults.search if core is None else core
        return [Link.from_dict(result) for result in self._dbs[core].search(query, sort=sort)]


def scrape(url):
    response = get(url).text
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
    if len(description) > app.settings.links.descriptions.max_length:
        description = description[: app.settings.links.descriptions.max_length - 1] + "&hellip;"

    return content, description


def get_title(url):
    return bs(get(url_normalize(url)).text, features="html.parser").find("title").text
