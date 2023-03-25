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


def level_card(member: User, user_data, guild_id, avatar_url) -> File:

    user_name = f"{member.name}#{member.discriminator}"
    current_lvl = user_data["guilds"][guild_id]["guild_lvl"]
    current_exp = user_data["guilds"][guild_id]["guild_exp"]
    next_exp = user_data["guilds"][guild_id]["next_exp"]
    percentage = ((current_exp / next_exp) * 100)

    #: Creating Card
    #: Accessing Background Image
    img_path = "DMaster/cards/bg/"
    bg_images = os.listdir(img_path)
    bg_image = random.choice(bg_images)
    img = Editor(f"{img_path}/{bg_image}")

    #: Creating Bg
    #: Main Background
    main_w = 900
    main_h = 300
    background = Editor(Canvas((main_w, main_h), color="#131519"))
    background.blend(img, .30, True)

    avatar_size = 200
    # avatar_url = await load_image_async(str(member.avatar.url))
    avatar = Editor(avatar_url).resize((avatar_size, avatar_size)).circle_image()

    poppins = Font.poppins(size=40)
    poppins_small = Font.poppins(size=30)

    background.paste(avatar, (30, 50))

    left_align_pos = 280
    #: Progress Bar
    background.rectangle((left_align_pos, 220), width=590, height=40, color="#decfbf", radius=20)
    background.bar((left_align_pos, 220), max_width=590, height=40, color="#2b303a", percentage=percentage, radius=20,
                   outline=(255, 255, 255, 90))

    #: Main info
    text_color = "#FFFFFF"
    background.text((left_align_pos, 40), user_name, font=poppins, color=text_color)
    background.rectangle((left_align_pos, 100), width=350, height=2, fill=text_color)
    background.text((left_align_pos, 125), f"Level - {current_lvl}", font=poppins_small, color=text_color)
    background.text((left_align_pos, 160), f"XP - {current_exp}/{next_exp}", font=poppins_small, color=text_color)

    #: Generate discord file
    file = File(fp=background.image_bytes, filename=f"lvl-card_{member.name}-{member.discriminator}.png")

    return file
