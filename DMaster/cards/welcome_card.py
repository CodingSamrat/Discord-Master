import os
import random

from discord import Member
from discord import File

from easy_pil import Editor
from easy_pil import Canvas
from easy_pil import Font


def welcome_card(member: Member, guild_name, avatar_url, welcome_msg) -> File:
    user_name = f"{member.name}#{member.discriminator}"
    #: Creating Card
    #: Accessing Background Image
    img_path = "DMaster/cards/bg/"
    bg_images = os.listdir(img_path)
    bg_image = random.choice(bg_images)
    img = Editor(f"{img_path}/{bg_image}")
    #: Creating Bg
    #: Main Background
    main_w = 900
    main_h = 500
    color_bg = "#ff8846"
    background = Editor(Canvas((main_w, main_h), color="#131519"))
    background.blend(img, .30, True)

    #: Avatar Properties
    avatar_size = 220
    avatar_bg_size = 230
    avatar_pos_y = 20
    avatar_pos_x = int((main_w - avatar_size) / 2)
    # avatar_url = await load_image_async(str(member.avatar.url))
    avatar_bg = Editor(Canvas((avatar_bg_size, avatar_bg_size), color=color_bg)).circle_image()
    avatar = Editor(avatar_url).resize((avatar_size, avatar_size)).circle_image()

    #: Main properties
    text_pos_x = int(main_w / 2)
    text_color = "#FFFFFF"
    poppins = Font.poppins(size=35)
    poppins_heading = Font.poppins(variant="bold", size=45)
    poppins_small = Font.poppins(size=20)

    #: Main scope
    background.paste(avatar_bg, (avatar_pos_x - 5, avatar_pos_y - 5))
    background.paste(avatar, (avatar_pos_x, avatar_pos_y))

    background.rectangle((275, 260), width=350, height=1, fill=text_color)
    background.rectangle((315, 270), width=270, height=1, fill=text_color)
    background.rectangle((355, 280), width=190, height=1, fill=text_color)

    background.text((text_pos_x, 320), user_name, font=poppins_heading, color="#00d2fe", align="center")
    background.text((text_pos_x, 400), f"Welcome to {guild_name}", font=poppins, color=text_color, align="center")
    background.text((text_pos_x, 440), welcome_msg, font=poppins_small, color=text_color, align="center")

    #: Generate discord file
    file = File(fp=background.image_bytes, filename=f"lvl-card_{member.name}-{member.discriminator}.png")

    return file
