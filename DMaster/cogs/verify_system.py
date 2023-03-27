from DMaster.utils import LOG
from DMaster.utils import get_status
from DMaster.database import Collection
from DMaster.database import get_collection

from discord.ext import commands
from discord.ext.commands.context import Context
from discord import Embed


class RoleManager(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

    #: write commands here
    #:
    #: Level System
    #:
    @commands.group(name="verify", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def verify(self, ctx: Context):
        guild = get_collection(Collection.GUILD).find_one({"_id": str(ctx.guild.id)})
        prefix = guild["config"]["prefix"]

        cmds = f"""
                -  _`init`_: Initialize Verification System
                -  _`channel`_: Set Verification Channel
                -  _`role`_: Set Verified Role
                -  _`enable`_: Enable Verification System
                -  _`disable`_: Disable Verification System
                -  _`status`_: show Level Verification status
                """

        embed = Embed(title="Verification System commands -", color=ctx.author.color)
        embed.add_field(name=f"_{prefix}verify_", value=cmds, inline=False)

        await ctx.send(embed=embed)

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx: Context, channel_id):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}
        channel_name = ctx.guild.get_channel(int(channel_id)).name
        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        guild_verify = guild["verify"]
        guild_verify["channel_id"] = str(channel_id)
        guild_verify["channel_name"] = str(channel_name)

        col_guild.update_one(query, {"$set": {"verify": guild_verify}})
        await ctx.send(f"> Welcome Channel id ```{channel_id}```")

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx: Context, role_id):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}
        role_name = ctx.guild.get_role(int(role_id)).name
        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        guild_verify = guild["verify"]
        guild_verify["role_id"] = str(role_id)
        guild_verify["role_name"] = str(role_name)

        col_guild.update_one(query, {"$set": {"verify": guild_verify}})
        await ctx.send(f"> Verification System Role  ```id => {role_id} ```\n```name => {role_name}```")

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def init(self, ctx: Context):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}

        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        #: Guild Configuration
        guild_config = guild["config"]

        #: Check if verify already initiated
        if "verify" in guild_config.keys():
            await ctx.send(f"> Verification System already initiated.\n Use `{guild_config['prefix']}verify` for more")

        elif "verify" not in guild_config.keys():
            guild_config["verify"] = True

            guild_verify = {
                "channel_id": None,
                "channel_name": None,
                "role_id": None,
                "role_name": None
            }

            col_guild.update_one(query, {"$set": {"config": guild_config, "verify": guild_verify}})
            await ctx.send("> Verification System initiated successfully")

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx: Context):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}

        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        #: Guild Configuration
        guild_config = guild["config"]

        if "verify" in guild_config.keys():
            guild_config["verify"] = True

            get_collection(Collection.GUILD).update_one(query, {"$set": {"config": guild_config}})
            await ctx.send("> Level System enabled successfully")

        else:
            await ctx.send(
                f"> Verification System is not initiated.\nPlease initiate it first.\n - Try {guild_config['prefix']}verify")

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx: Context):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}

        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        #: Guild Configuration
        guild_config = guild["config"]

        if "verify" in guild_config.keys():
            guild_config["verify"] = False

            get_collection(Collection.GUILD).update_one(query, {"$set": {"config": guild_config}})

            await ctx.send("> Level System disabled successfully")

        else:
            await ctx.send(f"> Verification System is not initiated.\nPlease initiate it first.\n - Try {guild_config['prefix']}verify")

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def status(self, ctx: Context):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}

        #: Initiate database
        #: Fetching database
        col_guild = get_collection(Collection.GUILD)
        guild = col_guild.find_one(query)

        #: Guild Configuration
        guild_config = guild["config"]

        if "verify" in guild_config.keys():
            embed = Embed(title="Verification System Status-", color=ctx.author.color)
            embed.add_field(name=get_status(guild_config["level"]), value="", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"> Verification System is not initiated.\nPlease initiate it first.\n - Try {guild_config['prefix']}verify")


async def setup(client):
    await client.add_cog(RoleManager(client))  # <- Change ->

