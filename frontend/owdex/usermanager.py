from pymongo import MongoClient
from argon2 import PasswordHasher


class UserManager():

    def __init__(self):
        self._mongo = MongoClient("mongodb://mongo:27017/")
        self._table = self._mongo["users"]["users"]
        self._hasher = PasswordHasher()

    def create(self, username, password, admin=False):
        try:
            user = self.get(username)
        except KeyError:
            self._table.insert_one({
                "username": username,
                "password": self._hasher.hash(password),
                "admin": admin
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
