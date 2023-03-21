from discord.ext import commands
from discord.ext.commands.context import Context

from DMaster.utils import LOG
from DMaster.config import DEFAULT_CONFIG
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
    #: Resat all config
    #:
    @commands.command()
    async def resetconfig(self, ctx: Context):
        col_guild = get_collection(Collection.GUILD)
        #: Collect Guild info
        guild_id = str(ctx.guild.id)
        config = DEFAULT_CONFIG

        #: Updating database
        col_guild.update({"config": config}, {"guild_id": guild_id})

    #: Setup Prefix
    #:
    @commands.command()
    async def setprefix(self, ctx: Context, new_prefix: str):
        col_guild = get_collection(Collection.GUILD)

        #: Collect Guild info
        guild_id = ctx.guild.id
        prefix = new_prefix

        #: Get server data from database
        data = col_guild.find_one({"guild_id": guild_id})

        #: Get server configurations
        config = data["config"]
        old_prefix = config["prefix"]

        #: Update new prefix to config
        config["prefix"] = prefix

        #: Updating database
        col_guild.update({"config": config}, {"guild_id": guild_id})

        await ctx.send(f"Server Prefix Changed by {ctx.author.mention}\n[{old_prefix}] -> {prefix}")


async def setup(client):
    await client.add_cog(ServerSetup(client))

