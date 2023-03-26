import os
import random

from discord import User
from discord import File

from easy_pil import Editor
from easy_pil import Canvas
from easy_pil import Font


def level_up_card(user_name, guild_name, level, avatar_url) -> File:

    #: Creating Card
    #: Accessing Background Image
    img_path = "DMaster/cards/bg/"
    bg_images = os.listdir(img_path)
    bg_image = random.choice(bg_images)
    img = Editor(f"{img_path}/{bg_image}")

    #: Creating canvas
    main_w = 900
    main_h = 350
    background = Editor(Canvas((main_w, main_h), color="#131519"))
    background.blend(img, .30, True)

    #: Parameters
    #:
    #: Font Styles & Colors----------------------------------------
    color_main = "#ff8846"
    color_basic = "#FFFFFF"
    color_sec = "#00d2fe"

    poppins_h = Font.poppins(variant="bold", size=60)
    poppins_h1 = Font.poppins(variant="bold", size=90)
    poppins_h2 = Font.poppins(variant="italic", size=45)
    poppins_h3 = Font.poppins(variant="italic", size=30)

    background.text((20, 20), f"Congratulations".upper(), font=poppins_h, color=color_sec)
    #: Creating Avatar -----------------
    avatar_size = 200
    avatar_bg_size = 210

    avatar_pos_y = 30
    avatar_pos_x = int((main_w - (avatar_size + avatar_pos_y)))

    avatar = Editor(avatar_url).resize((avatar_size, avatar_size)).circle_image()
    avatar_bg = Editor(Canvas((avatar_bg_size, avatar_bg_size), color=color_main)).circle_image()

    background.paste(avatar_bg, (avatar_pos_x - 5, avatar_pos_y - 5))
    background.paste(avatar, (avatar_pos_x, avatar_pos_y))

    #: Creating Level Text -----------------
    t = 250
    b = 340
    rt = 350
    rb = 430

    lvl_up_x = 60
    lvl_up_y = 175

    coordinates = [(0, t), (0, b), (rb, b), (rt, t)]
    background.polygon(coordinates, color=color_main)

    background.text((lvl_up_x, lvl_up_y), f"Level Up!!! ", font=poppins_h2, color=color_basic)
    background.rectangle((lvl_up_x - 35, lvl_up_y + 50), width=300, height=1, fill=color_main)
    background.rectangle((lvl_up_x - 40, lvl_up_y + 53), width=300, height=1, fill=color_main)

    background.text((190, 260), f"{level}", font=poppins_h1, color="#282c34", align="center")

    #: User & Guild name -----------------
    background.text((870, 250), f"{user_name}", font=poppins_h3, color=color_basic, align="right")
    background.text((870, 290), f"{guild_name}", font=poppins_h3, color=color_basic, align="right")

    #: Generate discord file
    file = File(fp=background.image_bytes, filename=f"lvl-card_{user_name}-{level}.png")

    return file
