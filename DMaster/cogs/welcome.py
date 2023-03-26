from DMaster.utils import LOG
from DMaster.utils import get_user_guilds
from DMaster.utils import get_status
from DMaster.database import Collection
from DMaster.database import get_collection

import discord
from discord.ext import commands
from discord.ext.commands.context import Context


class Welcome(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    #: Bot Events
    #:
    #: On Ready
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

    @commands.Cog.listener()
    async def on_message(self, message: Context):
        if message.author.id == self.client.user.id:
            return
        # await message.author.send("from welcome")

    #: When a member join the server
    #:
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.system_channel
        user_id = str(member.id)
        user_name = member.name
        guild_id = str(member.guild.id)
        guild_name = member.guild.name
        query = {"_id": user_id}

        #: Accessing database
        col_user = get_collection(Collection.USER)

        #: Fetch user object
        user_obj = col_user.find_one(query)

        user_guilds = get_user_guilds(user_obj, user_id, user_name, guild_id, guild_name)

        #: Send welcome message
        await member.send(f"welcome {member.mention}")
        await channel.send(f"welcome {member.mention}")

    #: When a member Remove the server
    #:
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        user_id = str(member.id)
        user_name = member.name
        guild_id = str(member.guild.id)
        guild_name = member.guild.name

        #: Accessing database
        query = {"_id": user_id}
        col_user = get_collection(Collection.USER)

        user = col_user.find_one(query)

        user_guilds = user["guilds"]
        user_guilds[guild_id]["in_guild"] = False

        #: Update database
        col_user.update_one(query, {"$set": {"guilds": user_guilds}})
        LOG.debug(TEXT=f"by.. from {guild_name}")
        #: Send Bye message
        await channel.send(f"Bye {member.mention}")
        try:
            await member.send(f"Bye {member.mention}")
        except Exception as e:
            print(e)

    #: write commands here
    #:
    #: welcome
    #:
    @commands.group(name="welcome", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx: Context):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}

        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        #: Guild Configuration
        guild_config = guild["config"]
        guild_config["welcome"] = True

        guild_welcome = {
            "channel_id": "234354365765",
            "channel_name": "Welcome",
            "msg": "Lets make game"
        }

        col_guild.update_one(query, {"$set": {"config": guild_config, "welcome": guild_welcome}})
        await ctx.send(">>> Welcome message settings updated")

    @welcome.command()
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
        guild_config["welcome"] = True

        get_collection(Collection.GUILD).update_one(query, {"$set": {"config": guild_config}})
        await ctx.send(">>> Welcome msg enabled successfully")

    @welcome.command()
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
        guild_config["welcome"] = False

        get_collection(Collection.GUILD).update_one(query, {"$set": {"config": guild_config}})

        await ctx.send(">>> Welcome msg disabled successfully")

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def status(self, ctx: Context):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}

        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        #: Guild Configuration
        guild_config = guild["config"]
        guild_welcome = guild["welcome"]

        msg = f"""
```
Welcome message - {ctx.guild.name}.

    - Status: {get_status(guild_config["welcome"])}
    - Channel Name: {guild_welcome["channel_name"]}
    - Channel ID: {guild_welcome["channel_id"]}
    - Message: {guild_welcome["msg"]}
```
            """

        await ctx.send(msg)




async def setup(client):
    await client.add_cog(Welcome(client))
