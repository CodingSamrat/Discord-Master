import discord
from discord.ext import commands
import time


class Ping(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("[SUCCESS] Cog: Ping is loaded successfully...")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Bot latency - {self.client.latency * 1000} ms")


async def setup(client):
    """
    Setting up the `Cog`

    :param client:
    :return:
    """

    await client.add_cog(Ping(client))

