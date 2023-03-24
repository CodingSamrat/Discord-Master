from DMaster.utils import LOG

from discord.ext import commands
from discord.ext.commands.context import Context
from discord import (Member,)


class RoleManager(commands.Cog):  # <- Change ->
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.success(TEXT=f"Cog - {self.__class__.__name__} is running successfully")

    #: write commands here
    #:
    #: ___
    #:
    @commands.command()
    async def ___(self, ctx: Context):
        await ctx.send("___")


async def setup(client):
    await client.add_cog(RoleManager(client))  # <- Change ->

