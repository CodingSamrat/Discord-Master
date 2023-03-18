import os
import time
import discord
from discord.ext import commands
from utils import LOG

class Embed(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        LOG(self, LOG.SUCCESS, TEXT="Running successful")

    @commands.command()
    async def embed(self, ctx):
        await ctx.send(f"Embedding...")


async def setup(client):
    """
    Setting up the `Cog`

    :param client:
    :return:
    """

    await client.add_cog(Embed(client))

