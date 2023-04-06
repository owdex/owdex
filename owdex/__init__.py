import os

import flask as f
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import toml

from .usermanager import UserManager
from .linkmanager import LinkManager


def create_app(config_dict=None):
    app = f.Flask("owdex")

    for file in ("../../owdex.toml", "/owdex.toml"):
        try:
            app.config.from_file(file, load=toml.load)
        except FileNotFoundError:
            pass

    if config_dict:
        app.config = app.config | config_dict

    app.um = UserManager(
        app.config["MONGO_HOST"],
        app.config["MONGO_PORT"],
        app.config["ADMIN_USERNAME"],
        app.config["ADMIN_PASSWORD"]
    )

    app.lm = LinkManager(
        app.config["SOLR_HOST"],
        app.config["SOLR_PORT"],
        [
            "stable", 
            "unstable", 
            "archive"
        ]
        )
    
    app.limiter = Limiter(
        get_remote_address,
        app = app,
        storage_uri = app.um.mongo_uri,
        strategy = "fixed-window-elastic-expiry"
    )

    with app.app_context():
        from .page import page_bp
        from .search import search_bp
        from .add import add_bp
        from .users import users_bp
        from .vote import vote_bp

        app.register_blueprint(page_bp)
        app.register_blueprint(search_bp)
        app.register_blueprint(add_bp)
        app.register_blueprint(users_bp)
        app.register_blueprint(vote_bp)

    return app
