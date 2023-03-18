import discord
from discord.ext import commands
import time


class Embed(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("[SUCCESS] Cog: Embed is loaded successfully...")

    @commands.command()
    async def embed(self, ctx):
        await ctx.send(f"Embeding...")


async def setup(client):
    """
    Setting up the `Cog`

    :param client:
    :return:
    """

    await client.add_cog(Embed(client))

