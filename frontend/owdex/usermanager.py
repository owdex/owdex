from pymongo import MongoClient
from argon2 import PasswordHasher


class UserManager():

    def __init__(self, dev_mode=False):
        self._mongo = MongoClient("mongodb://mongo:27017/" if not dev_mode else
                                  "mongodb://localhost:27017")
        self._table = self._mongo["users"]["users"]
        self._hasher = PasswordHasher()

    def create(self, email, password):
        try:
            user = self.get(email)
        except KeyError:
            self._table.insert_one({
                "email": email,
                "password": self._hasher.hash(password)
            })
        else:
            raise KeyError(f"User already exists with given email {email}!")

    def get(self, email):
        user = self._table.find_one({"email": email})
        if user:
            return user
        else:
            raise KeyError("No such user!")

    def verify(self, email, given_password):
        user = self.get(email)
        return self._hasher.verify(self.get(email)["password"], given_password)
