import os

import flask as f
from dotenv import load_dotenv

from .usermanager import UserManager
from .page import page
from .search import search
from .add import add
from .users import users


def create_app(custom_config=None):
    app = f.Flask("owdex")

    load_dotenv()
    app.config.update(SECRET_KEY=os.environ.get("secret_key"))
    if custom_config: app.config = app.config | custom_config

    app.um = UserManager(dev_mode=app.config["DEBUG"])

    with app.app_context():
        app.register_blueprint(page)
        app.register_blueprint(search)
        app.register_blueprint(add)
        app.register_blueprint(users)

    return app
