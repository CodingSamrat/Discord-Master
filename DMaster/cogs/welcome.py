from DMaster.utils import LOG

from discord.ext import commands
from discord.ext.commands.context import Context
from discord import (Member,)


class Welcome(commands.Cog):  # <- Change ->
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

    #: write commands here
    #:
    #: welcome
    #:
    @commands.command()
    async def welcome(self, ctx: Context):
        await ctx.send("welcome...")


async def setup(client):
    await client.add_cog(Welcome(client))  # <- Change ->

