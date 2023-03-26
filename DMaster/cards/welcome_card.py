import os
import random
from discord import (
    User,
    File
)
from easy_pil import (
    Editor,
    Canvas,
    Font,
)


def level_card(member: User, guild_name, avatar_url) -> File:
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
    background = Editor(Canvas((main_w, main_h), color="#131519"))
    background.blend(img, .30, True)

    #: Avatar Properties
    avatar_size = 220
    avatar_pos_y = 20
    avatar_pos_x = int((main_w - avatar_size) / 2)
    avatar = Editor(avatar_url).resize((avatar_size, avatar_size)).circle_image()

    #: Main properties
    text_pos_x = int(main_w / 2)
    text_color = "#FFFFFF"
    poppins = Font.poppins(size=35)
    poppins_heading = Font.poppins(size=45)
    poppins_small = Font.poppins(size=30)

    #: Main scope
    background.paste(avatar, (avatar_pos_x, avatar_pos_y))
    background.rectangle((275, 260), width=350, height=2, fill=text_color)
    background.text((text_pos_x, 285), user_name, font=poppins, color=text_color, align="center")
    background.text((text_pos_x, 340), f"Welcome to {guild_name}", font=poppins_heading, color=text_color, align="center")

    #: Generate discord file
    file = File(fp=background.image_bytes, filename=f"lvl-card_{member.name}-{member.discriminator}.png")

    return file
