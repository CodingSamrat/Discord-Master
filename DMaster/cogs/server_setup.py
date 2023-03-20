import discord
from discord.ext import commands
from DMaster.utils import LOG


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
    async def prefix(self, ctx, new_prefix):

        await ctx.send("setting up prefix...")


async def setup(client):
    await client.add_cog(ServerSetup(client))

