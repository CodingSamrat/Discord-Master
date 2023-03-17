import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Configuring Intents
intents = discord.Intents.default()
intents.message_content = True

# Initiating Bot
bot = commands.Bot(command_prefix="/", intents=intents)


#: -------------------
#:  Events Start Here
#:
@bot.event
async def on_ready():
    print('Logged on as', bot.user)


async def on_message(message):
    # don't respond to ourselves
    if message.author == bot.user:
        return

    if message.content == 'ping':
        await message.channel.send(f'pong {str(message.author)}')


#: -------------------
#:  Commands Start Here
#:
@bot.command()
async def info(ctx):
    await ctx.send('Info--')


@bot.command()
async def info2(ctx):
    await ctx.send('Info2222')
    await ctx.author.send("ddddddddddddddd")


if __name__ == "__main__":
    # Loading Bot Token & Other information
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    # Running Bot
    bot.run(TOKEN)
