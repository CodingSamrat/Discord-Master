import pymongo

__all__ = ("Collection", "get_collection")

con_str = "mongodb+srv://the_sam963:Samrat.mongo.23@discordcluster.fgt0jov.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(con_str)


def get_collection(coll_name: str) :
    #: Initiating Database
    db = client["dmaster"]

    #: Creating Collection
    collection = db[coll_name]

    return collection


class Collection:
    GUILD = "guild"
    USER = "user"


