import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio

# Configuring Intents
intents = discord.Intents.default()
intents.message_content = True

# Initiating Bot
client = commands.Bot(command_prefix="dm/", intents=intents)


#: -------------------
#:  Events Start Here
#:
@client.event
async def on_ready():
    print("[SUCCESS] Bot is running...")
    print('Logged on as', client.user)


async def load_cogs() -> None:
    """
    Loading `Cogs`

    :return: None
    """
    cog_ignore_list = ["__init__.py", "utils.py"]
    for filename in os.listdir("DMaster/cogs"):
        if filename in cog_ignore_list:
            continue

        if filename.endswith(".py"):
            await client.load_extension(f"DMaster.cogs.{filename[:-3]}")


async def main(token) -> None:
    """
    Entrypoint of Bot

    :return: None
    """
    async with client:
        await load_cogs()
        await client.start(token)


def boot():
    # Loading Bot Token & Other information
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    # Entrypoint
    asyncio.run(main(TOKEN))


if __name__ == "__main__":
    pass
