from discord.ext import commands
from DMaster.utils import LOG


class Embed(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG(self, LOG.SUCCESS, TEXT="Running successful")

    #: write commands here
    #:
    #: Embed Message
    #:
    @commands.command()
    async def embed(self, ctx):
        await ctx.send(f"Embedding...")


async def setup(client):
    await client.add_cog(Embed(client))

