import random
import os

from DMaster.utils import LOG
from DMaster.utils import get_user_guilds
from DMaster.database import Collection
from DMaster.database import get_collection
from DMaster.cards import level_card

from easy_pil import load_image_async

from discord.ext import commands
from discord.ext.commands.context import Context
from discord import (
    User
)


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

        #: Initiating database (user) collection
        col_users = get_collection(Collection.USER)

        user_id = str(message.author.id)
        user_name = message.author.name
        guild_id = str(message.guild.id)
        guild_name = message.guild.name

        col_users = get_collection(Collection.USER)
        users = col_users.find_one({"_id": user_id})

        user_guilds = get_user_guilds(users, user_id, user_name, guild_id, guild_name)

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

            await message.channel.send("LEVEL UP!")
        else:
            await col_users.update_one({"_id": user_id}, {"$set": {"guilds": user_guilds}})

    #: write commands here
    #:
    #: Level
    #:
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



async def setup(client):
    await client.add_cog(LevelSystem(client))
