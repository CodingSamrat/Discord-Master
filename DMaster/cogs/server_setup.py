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
        LOG(self, LOG.SUCCESS, TEXT="Running successful")

    #: write commands here
    #:
    #: Setup Prefix
    #:
    @commands.command()
    async def set_prefix(self, ctx):
        await ctx.send("setting up prefix...")


async def setup(client):
    await client.add_cog(ServerSetup(client))

