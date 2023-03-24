from functools import wraps, partial

import flask as f
from flask import current_app as app

from pymongo import MongoClient
from argon2 import PasswordHasher


class UserManager():

    def __init__(self, admin_username, admin_password):
        self._mongo = MongoClient("mongodb://mongo:27017/")
        self._table = self._mongo["users"]["users"]
        self._hasher = PasswordHasher()

        try:
            self.create(admin_username, admin_password, admin=True, hash=False)
        except KeyError:
            pass  # Admin already exists

    def create(self, username, password, admin=False, hash=True):
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
        user = self._table.find_one({"username": username})
        if user:
            return user
        else:
            raise KeyError("No such user!")

    def verify(self, username, given_password):
        user = self.get(username)
        return self._hasher.verify(
            self.get(username)["password"], given_password)

    def get_current(self):
        return self.get(f.session['user'])


def require_login(endpoint=None, needs_admin=False):
    if endpoint is None:
        return partial(require_login, needs_admin=needs_admin)

    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        if "user" not in f.session:
            return "Not logged in!", 401
        elif needs_admin and not app.um.get_current()["admin"]:
            return "Not an admin!", 403
        else:
            return endpoint(*args, **kwargs)

    return wrapper
