from discord.ext import commands
from discord.ext.commands.context import Context
from discord import (
    Embed,
    Member,
    Color,
    Object
)

from DMaster.utils import LOG


class Moderation(commands.Cog):      # <- Change ->
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.success(TEXT=f"Cog - {self.__class__.__name__} is running successfully")

    #: write commands here
    #:
    #: Delete messages
    #:
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: Context, count: int):
        await ctx.channel.purge(limit=count)

    #: Kick messages
    #:
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: Context, member: Member, modreason):
        await ctx.guild.kick(member)

        embed = Embed(title="Success", color=Color.orange())
        embed.add_field(name=f"[KICKED]", value=f"{member.mention} has been kicked by {ctx.author.mention}", inline=False)
        embed.add_field(name=f"Reason:", value=modreason, inline=False)

        await ctx.send(embed=embed)

    #: Ban messages
    #:
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: Context, member: Member, modreason):
        await ctx.guild.ban(member)

        embed = Embed(title="Ban member", color=Color.orange())
        embed.add_field(name=f"[BANED] ", value=f"{member.mention} has been baned by {ctx.author.mention}", inline=False)
        embed.add_field(name=f"[REASON] ", value=modreason, inline=False)

        await ctx.send(embed=embed)

    #: Unban messages
    #:
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: Context, user_id):
        user = Object(user_id)
        await ctx.guild.unban(user)

        embed = Embed(title="Unban member", color=Color.orange())
        embed.add_field(name=f"[BANED] ", value=f"{user} has been unbaned by {ctx.author.mention}", inline=False)

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Moderation(client))      # <- Change ->

