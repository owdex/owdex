import os

import flask as f
import toml

from .usermanager import UserManager
from .linkmanager import LinkManager
from .page import page
from .search import search
from .add import add
from .users import users


def create_app(config_dict=None):
    app = f.Flask("owdex")

    for file in ("../../owdex.toml", "/owdex.toml"):
        try:
            app.config.from_file(file, load=toml.load)
        except FileNotFoundError:
            pass

    if config_dict:
        app.config = app.config | config_dict

    app.um = UserManager(app.config["ADMIN_USERNAME"],
                         app.config["ADMIN_PASSWORD"])

    app.lm = LinkManager(["stable", "unstable", "archive"])

    with app.app_context():
        app.register_blueprint(page)
        app.register_blueprint(search)
        app.register_blueprint(add)
        app.register_blueprint(users)

    return app
