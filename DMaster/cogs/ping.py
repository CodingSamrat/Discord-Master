from discord.ext import commands
from DMaster.utils import LOG


class Ping(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG(self, LOG.SUCCESS, TEXT="Running successful")

    #: write commands here
    #:
    #: Ping
    #:
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Bot latency - {self.client.latency * 1000} ms")


async def setup(client):
    await client.add_cog(Ping(client))

