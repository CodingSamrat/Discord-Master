import discord.utils
from discord import Member
from discord import Embed
from discord import Color
from discord import ui
from discord.ext import commands
from discord.ext.commands.context import Context

from DMaster.utils import LOG
from DMaster.utils import get_user_guilds
from DMaster.utils import get_status
from DMaster.database import Collection
from DMaster.database import get_collection
from DMaster.cards import welcome_card

from easy_pil import load_image_async


class WelcomeModal(ui.Modal):
    # channel = discord.ui.
    pass


class Welcome(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    #: Bot Events
    #: On Ready
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

    #: When a member join the server
    #:
    @commands.Cog.listener()
    async def on_member_join(self, member: Member):

        user_id = str(member.id)
        user_name = member.name
        guild_id = str(member.guild.id)
        guild_name = member.guild.name

        #: ------------ User Resister Section ------------ :#
        #: Accessing User data
        col_user = get_collection(Collection.USER)
        user_obj = col_user.find_one({"_id": user_id})

        #: Not need of return value. Only need to check user
        #: Creating new user or modifying old user
        user_guilds = get_user_guilds(user_obj, user_id, user_name, guild_id, guild_name)
        #: ------------------- END ------------------- :#

        #: ------------ Greeting Section ------------ :#
        #: Accessing Guild data
        col_guild = get_collection(Collection.GUILD)
        guild_obj = col_guild.find_one({"_id": guild_id})

        if "welcome" in guild_obj["config"].keys():
            welcome_is_enable = guild_obj["config"]["welcome"]
            welcome_msg = guild_obj["welcome"]["msg"]
            channel_id = guild_obj["welcome"]["channel_id"]
            channel_name = guild_obj["welcome"]["channel_name"]

            if welcome_is_enable:

                #: Data for card
                avatar_url = await load_image_async(str(member.avatar.url))

                if not welcome_msg:
                    welcome_msg = ""

                #: Getting greeting image
                file = welcome_card(member, guild_name, avatar_url, welcome_msg)
                # file = "12334"
                #: Send welcome message to Member
                await member.send(file=file)

                #: Getting channel
                #: Send welcome message to Welcome chanel
                if channel_id is not None:
                    channel = member.guild.get_channel(int(channel_id))
                    file = welcome_card(member, guild_name, avatar_url, welcome_msg)
                    await channel.send(file=file)

                elif channel_name is None:
                    if member.guild.system_channel:
                        channel = member.guild.system_channel
                        await channel.send(file=file)

    #: When a member Remove the server
    #:
    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
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

        #: Send Bye message
        await channel.send(f"Bye {member.mention}")
        # await member.send("By By bY")

    #: write commands here
    #:
    #: welcome
    #:
    @commands.group(name="welcome", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx: Context):
        guild = get_collection(Collection.GUILD).find_one({"_id": str(ctx.guild.id)})
        prefix = guild["config"]["prefix"]

        cmds = f"""
        -  _`channel`_: Set welcome message channel
        -  _`message`_: Set a short message for new member
        -  _`enable`_: Enable welcome message
        -  _`disable`_: Disable welcome message
        -  _`status`_: show welcome message status
        """
        example = f"""
    {prefix}welcome channel 1234567890123
    {prefix}welcome message Welcome to D-Master community
"""
        embed = Embed(title="Welcome message commands-", color=ctx.author.color)
        embed.add_field(name=f"_{prefix}welcome_", value=cmds, inline=False)
        # embed.add_field(name=f"Example", value=example, inline=False)

        await ctx.send(embed=embed)




    @welcome.command()
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

        #: Check if welcome already initiated
        if "welcome" in guild.keys():
            await ctx.send(">>> Welcome message settings updated")

        elif "welcome" not in guild.keys():
            guild_config["welcome"] = True

            guild_welcome = {
                "channel_id": None,
                "channel_name": None,
                "msg": None
            }

            col_guild.update_one(query, {"$set": {"config": guild_config, "welcome": guild_welcome}})
            await ctx.send(">>> Welcome message settings updated")

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx: Context, channel_id):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}
        print(0)
        channel_name = ctx.guild.get_channel(int(channel_id)).name
        print(1)
        #: Initiate database
        col_guild = get_collection(Collection.GUILD)
        print(2)

        #: Fetching database
        guild = col_guild.find_one(query)

        print(3)
        guild_welcome = guild["welcome"]
        guild_welcome["channel_id"] = str(channel_id)
        guild_welcome["channel_name"] = str(channel_name)
        print(4)

        col_guild.update_one(query, {"$set": {"welcome": guild_welcome}})
        print(5)
        await ctx.send(f">>> Welcome Channel id => {channel_id}")

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def message(self, ctx: Context, *, message: str):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}
        msg_len = len(str(message))

        #: Checking Welcome message length
        if msg_len > 50:
            await ctx.send(f">>> Welcome message Should be 50 characters. ```Given message length {msg_len}```")
            return

        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        guild_welcome = guild["welcome"]
        guild_welcome["msg"] = str(message)

        col_guild.update_one(query, {"$set": {"welcome": guild_welcome}})
        await ctx.send(f">>> Welcome message set => ```{message}```")

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
