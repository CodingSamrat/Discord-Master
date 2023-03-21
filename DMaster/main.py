import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from discord import (
    Intents,
    Guild
)

from DMaster.utils import LOG
from DMaster.config import DEFAULT_CONFIG
from DMaster.database import Collection
from DMaster.database import get_collection

__all__ = ("boot",)

#: Configuring Intents
intents = Intents.default()
intents.message_content = True


def get_server_prefix(client, message) -> str:
    guild_id = message.guild.id
    guild_name = message.guild.name

    #: Getting Guild data Collection
    col_guild = get_collection(Collection.GUILD)

    #: Getting Server data
    server_data = col_guild.find_one({"guild_id": guild_id})

    if server_data:
        #: Fetching Prefix
        prefix = server_data["config"]["prefix"]

        return prefix
    else:
        server_data = {
            "guild_id": guild_id,
            "guild_name": guild_name,
            "in_guild": True,
            "config": DEFAULT_CONFIG
        }

        col_guild.insert_one(server_data)

        return DEFAULT_CONFIG["prefix"]


#: Initiating Bot
client = commands.Bot(command_prefix=get_server_prefix, intents=intents)


#: -------------------
#:  Events Start Here
#:
@client.event
async def on_ready():
    print("[SUCCESS] Bot is running...")
    print('Logged on as', client.user.name, "\n")


@client.event
async def on_guild_join(guild: Guild):

    #: Getting server data Collection
    col_guild = get_collection(Collection.GUILD)

    #: Collect Guild info
    guild_id = guild.id
    guild_name = guild.name
    in_guild = True
    config = DEFAULT_CONFIG

    #: Get server data from database
    server_data = col_guild.find_one({"guild_id": guild_id})

    #: Check if data server data already exist
    if server_data:
        # ({"in_guild": in_guild}, {"guild_id": guild_id})
        col_guild.update_one()

    else:
        #: Insert Data into database
        server_data = {
            "guild_id": guild_id,
            "guild_name": guild_name,
            "in_guild": in_guild,
            "config": config
        }
        #: writing to database
        col_guild.insert(server_data)


@client.event
async def on_guild_remove(guild: Guild):

    #: Getting server data Collection
    col_guild = get_collection(Collection.GUILD)

    #: Collect Guild info
    guild_id = guild.id
    in_guild = False

    #: Get server data from database
    server_data = col_guild.find_one({"guild_id": guild_id})

    #: Updating database
    col_guild.update({"in_guild": in_guild}, {"guild_id": guild_id})


async def load_cogs() -> None:
    """ Loading `Cogs` """

    cog_ignore_list = ["__init__.py", "utils.py"]
    for filename in os.listdir("DMaster/cogs"):
        if filename in cog_ignore_list:
            continue

        if filename.endswith(".py"):
            await client.load_extension(f"DMaster.cogs.{filename[:-3]}")


async def main(token) -> None:
    """
    Entrypoint of Bot

    :return: None
    """
    async with client:
        await load_cogs()
        await client.start(token)


def boot():
    #: Loading Bot Token & Other information
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    #: Entrypoint
    asyncio.run(main(TOKEN))


if __name__ == "__main__":
    pass
