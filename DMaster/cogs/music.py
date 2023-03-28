import discord

from DMaster.utils import LOG

from youtube_dl import YoutubeDL
from discord.ext import commands
from discord.ext.commands.context import Context
from discord import Member


class MusicSystem(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

    @commands.command()
    async def connect(self, ctx: Context):
        #: Check if User in a voice channel or not
        if ctx.author.voice is None:
            await ctx.send("`You are not in a voice channel. Join a Voice channel first.`")

        #: Getting users voice channel
        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx: Context):
        await ctx.voice_client.disconnect(force=True)

    @commands.command()
    async def play(self, ctx: Context, url):
        ctx.voice_client.stop()

        FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn"
        }
        YDL_OPTIONS = {
            "formate": "bestaudio"
        }

        vc = ctx.voice_client

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info["formats"][0]["url"]
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

            vc.play(source)

    @commands.command()
    async def pause(self, ctx: Context):
        await ctx.voice_client.pause()
        await ctx.send("Paused")

    @commands.command()
    async def pause(self, ctx: Context):
        await ctx.voice_client.resume()
        await ctx.send("Resumed")


async def setup(client):
    await client.add_cog(MusicSystem(client))

