from pymongo import MongoClient


class MongoDB:

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["xyz_bank"]
        self.users = self.db["users"]

    def user_exists(self, username):
        user = self.users.find_one({"username": username})
        return user is not None

    def create_user(self, username, password):
        self.users.insert_one({"username": username, "password": password})
        return True

mongodb = MongoDB()
