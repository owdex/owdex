import os

import flask as f
import toml

from .usermanager import UserManager
from .page import page
from .search import search
from .add import add
from .users import users


def create_app(config_file=None, config_dict=None):
    app = f.Flask("owdex")

    if config_file:
        app.config.from_file(config_file, load=toml.load)
    if config_dict:
        app.config = app.config | config_dict

    app.um = UserManager(dev_mode=app.config["DEBUG"])

    with app.app_context():
        app.register_blueprint(page)
        app.register_blueprint(search)
        app.register_blueprint(add)
        app.register_blueprint(users)

    return app
