import math
import asyncio
import random
from DMaster.utils import LOG
from DMaster.database import Collection, get_collection

from discord.ext import commands
from discord.ext.commands.context import Context
from discord import (
    Member,
    User
)


def get_new_guild(guild_id, guild_name):
    new_guild = {
        "guild_id": guild_id,
        "guild_name": guild_name,
        "guild_lvl": 1,
        "guild_exp": 0
    }


def get_user(users, user_id, user_name, guild_id, guild_name) -> tuple[dict, bool]:
    new_guild = {
        "guild_id": guild_id,
        "guild_name": guild_name,
        "guild_lvl": 1,
        "guild_exp": 0
    }
    if users:
        user: dict = users[0]

        return user, False
    else:
        user = {
            "user_id": user_id,
            "user_name": user_name,
            "guilds": {
                f"{guild_id}": new_guild,
            }
        }

        return user, True


class LevelSystem(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:

        #: Initiating database (user) collection
        self.col_users = get_collection(Collection.USER)

        self.client = client

    @commands.command()
    async def lvl(self, ctx: Context, user: User = None):
        user_id = ctx.author.id
        guild_id = ctx.guild.id

        user = get_collection(Collection.USER).find({"user_id": user_id})[0]
        lvl = user["guilds"][guild_id]["guild_lvl"]
        exp = user["guilds"][guild_id]["guild_exp"]

        await ctx.send(f" - {user}\n\n * Level -> {lvl}\n * Exp -> {exp}")
    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.success(TEXT=f"Cog - `{self.__class__.__name__}` is running successfully")

    @commands.Cog.listener()
    async def on_message(self, message: Context):
        if message.author.id == self.client.user.id:
            return

        user_id = str(message.author.id)
        user_name = message.author.name
        guild_id = str(message.guild.id)
        guild_name = message.guild.name

        col_users = get_collection(Collection.USER)
        users = col_users.find({"user_id": user_id})

        user, is_new = get_user(users, user_id, user_name, guild_id, guild_name)
        user_guilds: dict = user["guilds"]

        #: Insert user into the database if it is new.
        if is_new:
            await get_collection(Collection.USER).insert(user)

        else:
            #: If it is any new guild or existing one
            if guild_id not in user_guilds.keys():
                new_guild = {
                    "guild_id": guild_id,
                    "guild_name": guild_name,
                    "guild_lvl": 1,
                    "guild_exp": 0
                }
                user_guilds[guild_id] = new_guild
                await message.channel.send("new guild found")

        rand_exp = random.randint(3, 9)
        user_guilds[guild_id]["guild_exp"] += rand_exp

        current_lvl = user_guilds[guild_id]["guild_lvl"]
        current_exp = user_guilds[guild_id]["guild_exp"]

        if current_exp >= math.ceil(6 * (current_lvl ** 4) / 2.1):
            user_guilds[guild_id]["guild_lvl"] += 1
            await message.channel.send("LEVEL UP!")

        await get_collection(Collection.USER).update({"guilds": user_guilds}, {"user_id": user_id})

    #: write commands here
    #:
    #: Level
    #:
    @commands.command()
    async def level(self, ctx: Context, user: User = None):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)

        if user is not None:
            user_id = str(user.id)

        user = get_collection(Collection.USER).find({"user_id": user_id})[0]
        lvl = user["guilds"][guild_id]["guild_lvl"]
        exp = user["guilds"][guild_id]["guild_exp"]

        # await ctx.send(f" - {user['user_name']}\n\n * Level -> {lvl}\n * Exp -> {exp}")
        await ctx.send(f" - {ctx.author.mention}\n\n * Level -> {lvl}\n * Exp -> {exp}")



async def setup(client):
    await client.add_cog(LevelSystem(client))
