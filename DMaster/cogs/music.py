from DMaster.utils import LOG

from discord.ext import commands
from discord.ext.commands.context import Context
from discord import Member


class MusicSystem(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

    #: write commands here
    #:
    #: Music
    #:
    @commands.command()
    async def music(self, ctx: Context):
        await ctx.send("music")


async def setup(client):
    await client.add_cog(MusicSystem(client))

