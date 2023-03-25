from DMaster.database import Collection
from DMaster.database import get_collection


def get_new_guild(guild_name):
    new_guild = {
        "guild_name": guild_name,
        "in_guild": True,
        "guild_lvl": 1,
        "guild_exp": 0,
        "next_exp": 30
    }

    return new_guild


def create_user(users, user_id, user_name, guild_id, guild_name) -> tuple[dict, bool]:
    if users:
        user: dict = users

        return user, False
    else:
        user = {
            "_id": user_id,
            "user_name": user_name,
            "guilds": {
                f"{guild_id}": get_new_guild(guild_name),
            }
        }

        return user, True


def get_user_guilds(users, user_id, user_name, guild_id, guild_name) -> dict:
    user, is_new = create_user(users, user_id, user_name, guild_id, guild_name)
    user_guilds: dict = user["guilds"]

    #: Insert user into the database if it is new.
    if is_new:
        get_collection(Collection.USER).insert_one(user)

    else:
        #: If it is any new guild or existing one
        if guild_id not in user_guilds.keys():
            user_guilds[guild_id] = get_new_guild(guild_name)
            get_collection(Collection.USER).update_one({"_id": user_id}, {"$set": {"guilds": user_guilds}})

        elif guild_id in user_guilds.keys():
            user_guilds[guild_id]["in_guild"] = True
            get_collection(Collection.USER).update_one({"_id": user_id}, {"$set": {"guilds": user_guilds}})

    return user_guilds
