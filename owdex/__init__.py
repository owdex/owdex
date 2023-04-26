import json
import os

import flask as f
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import box

from .error import internal_server_error, page_not_found
from .linkmanager import LinkManager
from .usermanager import UserManager


def create_app(settings={}):
    app = f.Flask("owdex")

    app.settings = box.Box.from_toml(filename="/owdex.toml") | settings

    for key, value in {
        "DEBUG": app.settings.runtime.debug,
        "SECRET_KEY": app.settings.security.secret_key,
    }.items():
        app.config[key] = value

    app.lm = LinkManager(
        app.settings.databases.solr.host, app.settings.databases.solr.port, app.settings.indices
    )

    app.um = UserManager(
        app.settings.databases.mongo.host,
        app.settings.databases.mongo.port,
        app.settings.security.admin.username,
        app.settings.security.admin.password,
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
