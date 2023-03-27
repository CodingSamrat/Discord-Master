import random
import os

from DMaster.utils import LOG
from DMaster.utils import get_status
from DMaster.utils import get_user_guilds
from DMaster.database import Collection
from DMaster.database import get_collection
from DMaster.cards import level_card
from DMaster.cards import level_up_card

from easy_pil import load_image_async

from discord.ext import commands
from discord.ext.commands.context import Context
from discord import Embed
from discord import User


def get_rand_exp() -> int:
    return random.randint(1, 3)


class LevelSystem(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:

        #: Initiating database (user) collection
        self.col_users = get_collection(Collection.USER)

        self.client = client

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

    @commands.Cog.listener()
    async def on_message(self, message: Context):
        if message.author.id == self.client.user.id:
            return


        user_id = str(message.author.id)
        user_name = message.author.name
        guild_id = str(message.guild.id)
        guild_name = message.guild.name

        #: Initiating database (user) collection
        col_users = get_collection(Collection.USER)
        users = col_users.find_one({"_id": user_id})

        user_guilds = get_user_guilds(users, user_id, user_name, guild_id, guild_name)

        guild = get_collection(Collection.GUILD).find_one({"_id": guild_id})
        guild_config = guild["config"]
        if "level" in guild_config.keys():
            if guild_config["level"]:
                rand_exp = get_rand_exp()
                user_guilds[guild_id]["guild_exp"] += rand_exp

                current_lvl = user_guilds[guild_id]["guild_lvl"]
                current_exp = user_guilds[guild_id]["guild_exp"]
                next_exp = user_guilds[guild_id]["next_exp"]

                #: Checking if level up
                if current_exp >= next_exp:
                    current_lvl += 1
                    current_exp = 0

                    if current_lvl == 2:
                        next_exp = 50
                    elif current_lvl >= 3:
                        next_exp += 50

                    user_guilds[guild_id]["guild_lvl"] = current_lvl
                    user_guilds[guild_id]["guild_exp"] = current_exp
                    user_guilds[guild_id]["next_exp"] = next_exp

                    col_users.update_one({"_id": user_id}, {"$set": {"guilds": user_guilds}})

                    #: Level up card
                    avatar_url = await load_image_async(str(message.author.avatar.url))
                    file = level_up_card(user_name, guild_name, current_lvl, avatar_url)
                    LOG.debug(TEXT="done")
                    await message.channel.send(f"Congratulations {message.author.mention}```Level Up! \n{current_lvl-1} -> {current_lvl}```")
                    await message.author.send(file=file)
                else:
                    await col_users.update_one({"_id": user_id}, {"$set": {"guilds": user_guilds}})

    #: write commands here
    #:
    #: Level
    @commands.command(aliases=["rank", "lvl"])
    async def level(self, ctx: Context, user: User = None):
        member = ctx.author
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)

        if user is not None:
            member = user
            user_id = str(user.id)

        user = get_collection(Collection.USER).find_one({"_id": user_id})

        #: Generate card
        avatar_url = await load_image_async(str(member.avatar.url))
        try:
            file = level_card(member, user, guild_id, avatar_url)
            await ctx.send(file=file)
        except Exception as e:
            print(e)

    #: Level System
    #:
    @commands.group(name="level-system", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def level_system(self, ctx: Context):
        guild = get_collection(Collection.GUILD).find_one({"_id": str(ctx.guild.id)})
        prefix = guild["config"]["prefix"]

        cmds = f"""
                -  _`init`_: Initialize Level System
                -  _`enable`_: Enable Level System
                -  _`disable`_: Disable Level System
                -  _`status`_: show Level System status
                """

        embed = Embed(title="Level System commands-", color=ctx.author.color)
        embed.add_field(name=f"_{prefix}level-system", value=cmds, inline=False)

        await ctx.send(embed=embed)

    @level_system.command()
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

        #: Check if Level already initiated
        if "level" in guild_config.keys():
            await ctx.send(f"> Level System already initiated.\n Use `{guild_config['prefix']}level` for more")

        elif "level" not in guild_config.keys():
            guild_config["level"] = True

            col_guild.update_one(query, {"$set": {"config": guild_config}})
            await ctx.send("> Level System initiated")

    @level_system.command()
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

        if "level" in guild_config.keys():
            guild_config["level"] = True

            get_collection(Collection.GUILD).update_one(query, {"$set": {"config": guild_config}})
            await ctx.send("> Level System enabled successfully")

        else:
            await ctx.send(f"> Level System is not initiated.\nPlease initiate it first.\n - Try {guild_config['prefix']}level-system")

    @level_system.command()
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

        if "level" in guild_config.keys():
            guild_config["level"] = False

            get_collection(Collection.GUILD).update_one(query, {"$set": {"config": guild_config}})

            await ctx.send("> Level System disabled successfully")

        else:
            await ctx.send(f"> Level System is not initiated.\nPlease initiate it first.\n - Try {guild_config['prefix']}level-system")

    @level_system.command()
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

        if "level" in guild_config.keys():
            embed = Embed(title="Level System Status-", color=ctx.author.color)
            embed.add_field(name=get_status(guild_config["level"]), value="", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"> Level System is not initiated.\nPlease initiate it first.\n - Try {guild_config['prefix']}level-system")


async def setup(client):
    await client.add_cog(LevelSystem(client))
