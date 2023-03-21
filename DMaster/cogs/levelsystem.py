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


class LevelSystem(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:

        #: Initiating database (user) collection
        self.col_users = get_collection(Collection.USERS)

        self.client = client

    def new_guild(self, guild_id) -> dict:
        guild = dict()
        guild["guild_id"] = guild_id
        guild["guild_lvl"] = 1
        guild["guild_exp"] = 0
        return guild
    def level_up(self, guild_id: int, guilds: list) -> tuple[bool, list]:

        #: Iterate all guild of user
        for guild in guilds:
            if guild["guild_id"] == guild_id:

                #: Set Guild data
                if guild["guild_exp"] >= math.ceil(9 * (guild["guild_lvl"] ** 4) / 2.3):
                    guild["guild_lvl"] += 1
                    return True, guilds
                else:
                    return False, guilds

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.success(TEXT=f"Cog - `{self.__class__.__name__}` is running successfully")

    @commands.Cog.listener()
    async def on_message(self, message: Context):
        if message.author.id == self.client.user.id:
            return

        user_id = message.author.id
        guild_id = message.guild.id

        users = self.col_users.find({"user_id": user_id})
        user = dict()

        if users:
            user = users[0]
        else:
            user["user_id"] = user_id
            user["guilds"] = []

            user["guilds"].append(self.new_guild(guild_id))

            self.col_users.insert(user)

        user_guilds = user["guilds"]
        EXP = random.randint(3, 9)

        for guild in user_guilds:
            if guild["guild_id"] == guild_id:
                guild["guild_exp"] += EXP

        #: Checking if level up
        is_level_up, guilds = self.level_up(guild_id, user_guilds)
        guild_list = []
        if is_level_up:
            for guild in guilds:
                guild_list.append(guild_id)

                if guild["guild_id"] == guild_id:
                    await message.channel.send(f"Level -> {guild['guild_lvl']}\nExp -> {guild['guild_exp']}")

        if guild_id not in guilds:
            user_guilds.append(self.new_guild(guild_id))

        get_collection(Collection.USERS).update({"guilds": user_guilds}, {"user_id": user_id})

        # await LOG.success(TEXT=f"[{ccc}] -> {message}")
        await message.channel.send(f"{self.col_users.find().prettify()}")

    #: write commands here
    #:
    #: Level
    #:
    @commands.command(aliases=["rank", "lvl"])
    async def level(self, ctx: Context, user: User | None):
        await ctx.send(f"___ {user}")


async def setup(client):
    await client.add_cog(LevelSystem(client))
