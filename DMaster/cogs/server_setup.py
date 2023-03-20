import discord
from discord.ext import commands

from DMaster.utils import LOG
from DMaster.database import Collection
from DMaster.database import get_collection


class ServerSetup(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.success(TEXT=f"Cog - `{self.__class__.__name__}` is running successfully")

    #: write commands here
    #:
    #: Setup Prefix
    #:
    @commands.command()
    async def prefix(self, ctx, new_prefix: str):
        col_server = get_collection(Collection.SERVER_DATA)

        #: Collect Guild info
        guild_id = str(ctx.guild.id)
        prefix = new_prefix

        #: Get server data from database
        data = col_server.find({"guild_id": guild_id})[0]

        #: Get server configurations
        config = data["config"]
        old_prefix = config["prefix"]

        #: Update new prefix to config
        config["prefix"] = prefix

        #: Updating database
        col_server.update({"config": config}, {"guild_id": guild_id})

        await ctx.send(f"Server Prefix Changed by {ctx.author.mention}\n[{old_prefix}] -> {prefix}")


async def setup(client):
    await client.add_cog(ServerSetup(client))

