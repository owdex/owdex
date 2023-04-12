import flask as f
from flask import current_app as app

import pysolr

from requests import get
from bs4 import BeautifulSoup as bs
from url_normalize import url_normalize


class LinkManager:
    """Manage link entries in multiple indices, and serves as a wrapper for the underlying Solr database.
    """

    def __init__(self, host, port, indices):
        """Creates a LinkManager instance.

        Args:
            host (str): The hostname at which the Solr instance can be reached.
            port (int): The port at which the Solr instance can be reached.
            indices (list): A list of index names.
            default_indices (list): A list of indices to search by default. Must be a subset of indices.
        """
        self._indices = {}
        for index_name in indices:
            self._indices[index_name] = pysolr.Solr(
                f"http://{host}:{port}/solr/{index_name}")

    def add(self, *, index, url, title, submitter=None):
        """Add an entry to the specified index.

        Args:
            index (str): The name of the index to which the entry should be added.
            url (str): The URL of the entry.
            title (str): The title of the entry.
            submitter (str, optional): The person who submitted the entry. Defaults to None. Should it equal None, it will be replaced with ANONYMOUS_SUBMITTER from owdex.toml.
        """
        # We force arguments to be named for readability by using *

        submitter = submitter if submitter else app.config[
            "ANONYMOUS_SUBMITTER"]
        # this can't be the default param because current_app isn't available initially

        soup = bs(get(url_normalize(url)).text, features="html.parser")
        content = soup.get_text()
        description = soup.find("meta", attrs={"name": "description"})

        # if there was a description, set that, otherwise just use content
        description = description.get("content") if description else content

        if len(description) > app.config["DESCRIPTION_MAX_LENGTH"]:
            description = description[:app.config["DESCRIPTION_MAX_LENGTH"] -
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
        """Register a vote for an entry.

        Args:
            index (str): The name of the index on which the entry is stored.
            id (str): The internal ID of the entry.
        """
        self._indices[index].add({"id": id, "votes": {"inc": 1}}, commit=True)

    def search(self, query, indices):
        """Perform a search of the specified indices for the query.

        Args:
            query (str): The terms being searched for.
            indices (str): The names of the indices in which to search.

        Returns:
            list: A list of         response = result dicts.
        """
        results = []

        try:
            for index_name in indices:
                index_results = self._indices[index_name].search(query)
                for result in index_results:
                    # we add the index attribute so we can show the index this result was pulled from
                    result.update({"index": index_name})
                results.extend(index_results)

        except SolrError as e:
            if "org.apache.solr.search.SyntaxError" in str(e):
                pass  # it's a malformed query, just return what we have -- typically an empty array
            else:
                raise

        return results


def get_title(url, format_for_autocomplete=False):
    return bs(get(url_normalize(url)).text,
              features="html.parser").find("title").text
