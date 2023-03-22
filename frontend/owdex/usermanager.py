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
