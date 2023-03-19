import discord
from discord.ext import commands
from DMaster.cogs.utils import LOG


class Moderation(commands.Cog):      # <- Change ->
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        LOG(self, LOG.SUCCESS, TEXT="Running successful")

    #: write commands here
    #:

    #: Delete messages
    #:
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
        await ctx.channel.purge(limit=count)

    #: Kick messages
    #:
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, modreason):
        await ctx.guild.kick(member)

        embed = discord.Embed(title="Success", color=discord.Color.orange())
        embed.add_field(name=f"[KICKED]", value=f"{member.mention} has been kicked by {ctx.author.mention}", inline=False)
        embed.add_field(name=f"Reason:", value=modreason, inline=False)

        ctx.send(embed=embed)

    #: Ban messages
    #:
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, modreason):
        await ctx.guild.ban(member)

        embed = discord.Embed(title="Ban member", color=discord.Color.orange())
        embed.add_field(name=f"[BANED] ", value=f"{member.mention} has been baned by {ctx.author.mention}", inline=False)
        embed.add_field(name=f"[REASON] ", value=modreason, inline=False)

        await ctx.send(embed=embed)

    #: Unban messages
    #:
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id):
        user = discord.Object(user_id)
        await ctx.guild.unban(user)

        embed = discord.Embed(title="Unban member", color=discord.Color.orange())
        embed.add_field(name=f"[BANED] ", value=f"{user} has been unbaned by {ctx.author.mention}", inline=False)

        await ctx.send(embed=embed)




# Setup Cog <->
async def setup(client):
    await client.add_cog(Moderation(client))      # <- Change ->

