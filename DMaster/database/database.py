import os
import pymongo
from dotenv import load_dotenv

__all__ = ("Collection", "get_collection")

#: Load Environment Variable 
load_dotenv()
con_str = os.getenv('MONGO_URL')

#: Make connection
client = pymongo.MongoClient(con_str)


def get_collection(coll_name: str):
    #: Initiating Database
    db = client["dmaster"]

    #: Creating Collection
    collection = db[coll_name]

    return collection


class Collection:
    GUILD = "guild"
    USER = "user"


