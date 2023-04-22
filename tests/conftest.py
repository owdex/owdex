import box
import pytest

from owdex import create_app
from owdex.usermanager import UserManager


@pytest.fixture
def app():
    app = create_app(settings=box.Box({"DEBUG": True, "TESTING": True}))

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return appp.test_cli_runner()
