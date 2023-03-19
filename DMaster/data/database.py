from filexdb import FileXdb
from DMaster.config import DATABASE

__all__ = ("DB",)


db_name = DATABASE["name"]
data_dir = DATABASE["data_dir"]
mode = DATABASE["mode"]


DB = FileXdb(db_name=db_name, data_dir=data_dir)

