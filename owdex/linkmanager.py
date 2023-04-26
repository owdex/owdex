import re
from dataclasses import KW_ONLY, dataclass
from typing import Self
from urllib.parse import urlparse, urlunparse
from uuid import uuid4 as uuid

import flask as f
from flask import current_app as app

from box import Box
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
    votes: int

    @classmethod
    def create(cls, *, url: str, title: str, submitter: str, index: str = None) -> Self:
        """Return a Link instance from minimal information by scraping the page linked to by url.

        Args:
            url (str): The URL of a page to scrape.
            title (str): A title describing the link's contents.
            submitter (str): The user who submitted the link to the index.
            index (str, optional): The index storing the link.. Defaults to "unstable".

        Returns:
            Self: A Link instance with scraped information
        """
        index = "unstable" if index is None else index  # TODO: respect settings
        url = normalized_url(url)
        content, description = scrape(url)
        return cls(
            index=index,
            id=str(uuid()),
            url=url,
            title=title,
            submitter=submitter,
            content=content,
            description=description,
            votes=0,
        )

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Return a Link instance from a dict that already contains all needed information.

        Args:
            data (dict): A dict representing a serialised Link object.

        Returns:
            Self: A Link instance with information from data
        """
        return cls(
            **{
                key: value
                for key, value in data.items()
                if key
                in ["index", "id", "url", "title", "submitter", "content", "description", "votes"]
            }
        )

    def rescrape(self) -> None:
        self.content, self.description = scrape(self.url)


class LinkManager:
    """Manage link entries in multiple indices, and serve as a wrapper for an underlying Solr database."""

    def __init__(self, host: str, port: int, cores: dict) -> None:
        """Create a LinkManager instance.

        Args:
            indices (list): A dict from an indices.json file.
            host (str): The hostname at which the Solr instance can be reached.
            port (int): The port at which the Solr instance can be reached.
        """
        self._dbs = {
            core_name: Solr(f"http://{host}:{port}/solr/{core_name}") for core_name in cores
        }
        self.cores = cores

    def get(self, id: str, core: str = None) -> Link:
        """Get an entry by its id.

        Args:
            id (str): The UUID for the desired entry.
            core (str, optional): The core to search. Defaults to a value defined in owdex.toml.

        Returns:
            Link: The link with the desired UUID.
        """
        return self.search(f"id:{id}", core=core)[0]

    def add(self, entry: Link, core: str = None) -> None:
        """Add an entry to the specified core.

        If core is specified and the link has an index attribute, those values will be used.
        Otherwise, default values from owdex.toml will be used.

        Args:
            core (str, optional): A core in the LinkManager. Defaults to a value defined in owdex.toml.
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
                "votes": entry.votes,
                "title": entry.title,
                "content": entry.content,
                "description": entry.description,
            },
            commit=True,
        )

    def vote(self, id: str, core: str):
        """Register a vote for an entry.

        Args:
            id (str): The internal ID of the entry.
            core (str): The core of the entry.
        """
        self._dbs[core].add({"id": id, "votes": {"inc": 1}}, commit=True)

    def search(self, query: str, core: str, indices: str, sort: str) -> list[Link]:
        """Perform a search using Solr query and sort notation.

        An index can be specified in the query string.

        Args:
            query (str): A query string in Solr query notation.
            core (str): The core to search. Defaults to a value defined in owdex.toml.
            indices (str): The indices within the core to search.
            sort (str): The sorting method to use. Defaults to "score desc", which is Solr's default sorting method.

        Returns:
            list[Link]: A list of Link objects matching the query and sorted in the given manner.
        """

        params = {}
        match sort:
            case "relevance":
                params["sort"] = "score desc"
            case "votes":
                params["sort"] = "votes desc"
            case "magic":
                params["boost"] = "votes"

        return [
            Link.from_dict(result)
            for result in self._dbs[core].search(query, defType="edismax", **params)
        ]


def scrape(url: str) -> tuple[str, str]:
    """Get the content and a description for a given webpage.

    Args:
        url (str): The URL of the page to scrape.

    Returns:
        tuple[str, str]: The content and description, respectively.
    """
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


def get_title(url: str) -> str:
    """Get the title of a webpage from its <title> element.

    Args:
        url (str): The URL to scrape.

    Returns:
        str: The title for the page.
    """
    return bs(get(url_normalize(url)).text, features="html.parser").find("title").text


def normalized_url(url: str) -> str:
    """Normalizes a URL and ensures it uses the HTTPS scheme.

    Args:
        url (str): The URL to normalize.

    Returns:
        str: A normalized URL.
    """
    return urlunparse(urlparse(url_normalize(url))._replace(scheme="https"))
