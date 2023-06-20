import json
import os
from http import HTTPStatus

import flask as f
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import HTTPException

import box

from .linkmanager import LinkManager
from .usermanager import UserManager


def handle_error(e):
    status = (
        HTTPStatus(e.code) if isinstance(e, HTTPException) else HTTPStatus.INTERNAL_SERVER_ERROR
    )
    match status:
        case HTTPStatus.NOT_FOUND:
            explanation = "Page not found!"
        case HTTPStatus.TOO_MANY_REQUESTS:
            explanation = f"You made too many requests and hit the limit of {e.limit.limit}"
        case _:
            explanation = (
                "The server experienced an issue handling your request." if not e.args else e.args
            )
    return (
        f.render_template(
            "error.html", status=status.value, phrase=status.phrase, explanation=explanation
        ),
        status.value,
    )


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

    app.register_error_handler(Exception, handle_error)

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
