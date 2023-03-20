from filexdb import FileXdb
from DMaster.config import DATABASE

__all__ = ("DB", "SERVER")


db_name = DATABASE["name"]
data_dir = DATABASE["data_dir"]
mode = DATABASE["mode"]

#: Initiating Database
DB = FileXdb(db_name=db_name, data_dir=data_dir)

#: Creating prefix collection
SERVER = DB.collection("server_data")

s = {
    gui
}