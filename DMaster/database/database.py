from filexdb import FileXdb
from DMaster.config import DATABASE

__all__ = ("Collection", "get_collection")

db_name = DATABASE["name"]
data_dir = DATABASE["data_dir"]
mode = DATABASE["mode"]


def get_collection(coll_name: str):
    DB = FileXdb(db_name=db_name, data_dir=data_dir, mode="json")
    collection = DB.collection(coll_name)
    return collection


class Collection:
    SERVER_DATA = "server_data"


data = {
    "guild_id": "guild_id",
    "guild_name": "guild_name",
    "in_guild": "in_guild",
    "config": {
        "prefix": "prefix"
    }
}
