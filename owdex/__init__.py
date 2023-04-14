import json
import os

import flask as f

import toml
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .error import internal_server_error, page_not_found
from .linkmanager import LinkManager
from .usermanager import UserManager


def create_app(config_dict={}, indices_dict={}):
    app = f.Flask("owdex")

    for file in ("../../owdex.toml", "/owdex.toml"):
        try:
            app.config.from_file(file, load=toml.load)
        except FileNotFoundError:
            pass
    app.config = app.config | config_dict

    indices = {}
    for filename in ("../../indices.json", "/indices.json"):
        try:
            with open(filename) as file:
                indices = json.load(file)
        except FileNotFoundError:
            print(f"not find {filename}")
    indices = indices | indices_dict
    if not indices:
        raise RuntimeError("No indices file specified!")

    app.lm = LinkManager(app.config["SOLR_HOST"], app.config["SOLR_PORT"], indices)

    app.um = UserManager(
        app.config["MONGO_HOST"],
        app.config["MONGO_PORT"],
        app.config["ADMIN_USERNAME"],
        app.config["ADMIN_PASSWORD"],
    )

    app.limiter = Limiter(
        get_remote_address,
        app=app,
        storage_uri=app.um.mongo_uri,
        strategy="fixed-window-elastic-expiry",
    )

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    with app.app_context():
        from .add import add_bp
        from .page import page_bp
        from .search import search_bp
        from .users import users_bp
        from .vote import vote_bp

        app.register_blueprint(page_bp)
        app.register_blueprint(search_bp)
        app.register_blueprint(add_bp)
        app.register_blueprint(users_bp, url_prefix="/account")
        app.register_blueprint(vote_bp)

    return app
