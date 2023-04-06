from functools import wraps, partial
from http import HTTPStatus

import flask as f
from flask import current_app as app

from pymongo import MongoClient
from argon2 import PasswordHasher

from .error import error


class UserManager():
    """Manage users, and serves as a wrapper for the underlying Mongo database and password hasher.
    """
    def __init__(self, host, port, admin_username, admin_password):
        """Create a UserManager instance.

        Args:
            host (str): The hostname for the MongoDB database.
            port (int): The port number for the MongoDB database.
            admin_username (str): The username for the admin user.
            admin_password (str): The password for the admin user.
        """
        self.mongo_uri = f"mongodb://{host}:{port}/"
        self._mongo = MongoClient(self.mongo_uri)
        self._table = self._mongo["users"]["users"]
        self._hasher = PasswordHasher()

        try:
            self.create(admin_username, admin_password, admin=True, hash=False)
        except KeyError:
            pass  # Admin already exists

    def create(self, username, password, admin=False, hash=True):
        """Create a new user with the specified username and password.

        Args:
            username (str): The user's username.
            password (str): The user's password. This will be stored in a hashed form as long as hash is not set to False.
            admin (bool, optional): Whether the user is an admin. Defaults to False.
            hash (bool, optional): Whether to hash the user's password. This may be set to False should the passed password already be hashed. Defaults to True.

        Raises:
            KeyError: A user already exists with the given username.
        """
        try:
            user = self.get(username)
        except KeyError:
            self._table.insert_one({
                "username":
                username,
                "password":
                self._hasher.hash(password) if hash else password,
                "admin":
                admin
            })
        else:
            raise KeyError(
                f"User already exists with given username {username}!")

    def get(self, username):
        """Given a username, return a dict from the database representing that user.

        Args:
            username (str): The unique username to get.

        Raises:
            KeyError: No such user exists with the given username.

        Returns:
            dict: A dict from the database with information on the user.
        """
        user = self._table.find_one({"username": username})
        if user:
            return user
        else:
            raise KeyError("No such user!")

    def verify(self, username, given_password):
        """Look up the stored hash for a user and validates it against a given password.

        Args:
            username (str): The username to check.
            given_password (str): The supposedly associated password.

        Raises:
            argon2.exceptions.VerifyMismatchError: The given password did not match the 
        """
        self._hasher.verify(self.get(username)["password"], given_password)

    def get_current(self):
        """A small utility function to get the current logged in username.

        Raises:
            KeyError: No such user exists with the given username. This generally should not happen, unless an account has been deleted.

        Returns:
            str: The username of the user currently logged in.
        """
        return self.get(f.session['user'])


def require_login(endpoint=None, needs_admin=False):
    """A decorator to require a login and optional admin status on a Flask endpoint.

    Args:
        needs_admin (bool, optional): Whether admin priviliges should be required. Defaults to False.
    """
    if endpoint is None:
        return partial(require_login, needs_admin=needs_admin)

    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        if "user" not in f.session:
            return error(HTTPStatus.UNAUTHORIZED, "Not logged in!")
        elif needs_admin and not app.um.get_current()["admin"]:
            return error(HTTPStatus.FORBIDDEN, "Not an admin!")
        else:
            return endpoint(*args, **kwargs)

    return wrapper
