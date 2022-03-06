import os
import pymongo

from pymongo import MongoClient
from pymongo.collection import Collection, Cursor
from config.env import load_env
from dataclasses import dataclass

load_env()

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
PROJECT = os.environ["PROJECT"]
DB = os.environ["DB_NAME"]
COLLECTION = os.environ["COLLECTION"]
CONN = f"mongodb+srv://{USERNAME}:{PASSWORD}@{PROJECT}.bm8pt.mongodb.net/?retryWrites=true&w=majority"


@dataclass
class MongoDB:
    client: MongoClient = None
    collection: Collection = None

    def __init__(self) -> None:
        self.connect()

    def connect(self) -> None:
        self.client = pymongo.MongoClient(CONN)
        self.collection = self.client[DB][COLLECTION]

    def find_users(self, username: str = None) -> Cursor:
        if not username:
            return self.collection.find()

        return self.collection.find({"username": username})

    def update(self, username: str, target: str) -> None:
        self.collection.update_one({"username": username}, {"$set": target})
