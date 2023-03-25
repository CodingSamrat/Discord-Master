

import random
import os
from DMaster.utils import LOG
from DMaster.database import Collection, get_collection

from discord.ext import commands
from discord.ext.commands.context import Context
from discord import (
    User,
    File
)

from easy_pil import (
    Editor,
    Canvas,
    Font,
    load_image_async
)


def get_rand_exp() -> int:
    return random.randint(1, 3)


def get_new_guild(guild_id, guild_name):
    new_guild = {
        "guild_name": guild_name,
        "guild_lvl": 1,
        "guild_exp": 0,
        "next_exp": 30
    }

    return new_guild


def get_user(users, user_id, user_name, guild_id, guild_name) -> tuple[dict, bool]:

    if users:
        user: dict = users

        return user, False
    else:
        user = {
            "_id": user_id,
            "user_name": user_name,
            "guilds": {
                f"{guild_id}": get_new_guild(guild_id, guild_name),
            }
        }

        return user, True


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

        user, is_new = get_user(users, user_id, user_name, guild_id, guild_name)
        user_guilds: dict = user["guilds"]

        #: Insert user into the database if it is new.
        if is_new:
            get_collection(Collection.USER).insert_one(user)

        else:
            #: If it is any new guild or existing one
            if guild_id not in user_guilds.keys():
                user_guilds[guild_id] = get_new_guild(guild_id, guild_name)

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

        user_name = f"{member.name}#{member.discriminator}"
        current_lvl = user["guilds"][guild_id]["guild_lvl"]
        current_exp = user["guilds"][guild_id]["guild_exp"]
        next_exp = user["guilds"][guild_id]["next_exp"]
        percentage = ((current_exp / next_exp) * 100)

        #: Creating Card
        #: Accessing Background Image
        bg_images = os.listdir("DMaster/img/card-bg/")
        bg_image = random.choice(bg_images)
        img = Editor(f"DMaster/img/card-bg/{bg_image}")

        #: Creating Bg
        #: Main Background
        main_w = 900
        main_h = 300
        background = Editor(Canvas((main_w, main_h), color="#131519"))
        background.blend(img, .30, True)

        avatar_size = 200
        avatar_url = await load_image_async(str(member.avatar.url))
        avatar = Editor(avatar_url).resize((avatar_size, avatar_size)).circle_image()

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)

        #: Right Polygon
        # card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]
        # background.polygon(card_right_shape, color="#bedbff")
        background.paste(avatar, (30, 50))

        left_align_pos = 280
        #: Progress Bar
        background.rectangle((left_align_pos, 220), width=590, height=40, color="#decfbf", radius=20)
        background.bar((left_align_pos, 220), max_width=590, height=40, color="#2b303a", percentage=percentage, radius=20, outline=(255, 255, 255, 90))

        #: Main info
        text_color = "#FFFFFF"
        background.text((left_align_pos, 40), user_name, font=poppins, color=text_color)
        background.rectangle((left_align_pos, 100), width=350, height=2, fill=text_color)
        background.text((left_align_pos, 125), f"Level - {current_lvl}", font=poppins_small, color=text_color)
        background.text((left_align_pos, 160), f"XP - {current_exp}/{next_exp}", font=poppins_small, color=text_color)

        #: Generate discord file
        file = File(fp=background.image_bytes, filename=f"lvl-card_{member.name}-{member.discriminator}.png")
        await ctx.send(file=file)


async def setup(client):
    await client.add_cog(LevelSystem(client))
