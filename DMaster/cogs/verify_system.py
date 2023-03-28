
from DMaster.utils import LOG
from DMaster.utils import get_status
from DMaster.database import Collection
from DMaster.database import get_collection

from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ui import button
from discord.ui import View
from discord import Embed
from discord import Interaction
from discord import Color
from discord import ButtonStyle


class VerifyButton(View):
    def __int__(self):
        super().__int__(timeout=None)

    @button(label="Verify", style=ButtonStyle.green, emoji="✅")
    async def verify_button(self, interaction: Interaction, button):
        user = interaction.user

        #: Fetching database
        guild = get_collection(Collection.GUILD).find_one({"_id": str(user.guild.id)})

        try:
            #: Accessing Role
            role_id = guild["verify"]["role_id"]
            role = user.guild.get_role(int(role_id))

            #: Give user the verified role
            await user.add_roles(role)

            #: Send conformation message
            user_embed = Embed(title="Congratulations!", color=interaction.user.color)
            user_embed.add_field(name=f"Verification of {interaction.guild.name} is successful", value="", inline=False)
            user_embed.add_field(name=f"Let's start discussion with others", value="", inline=False)
            await user.send(embed=user_embed)

            await interaction.response.send_message(embed=user_embed, ephemeral=True)
        except Exception as e:
            msg = "`Some error occurred, Please contact to Server maintainers`"
            await interaction.response.send_message(msg, ephemeral=True)


class Verification(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

        #: Sending Veryfi Button
        for _guild in self.client.guilds:
            guild_id = str(_guild.id)
            query = {"_id": guild_id}

            #: Fetching database
            guild = get_collection(Collection.GUILD).find_one(query)
            guild_config = guild["config"]

            if "verify" in guild_config.keys() and guild_config["verify"] is True:
                if guild["verify"]["channel_id"] is not None:
                    try:
                        channel = _guild.get_channel(int(guild["verify"]["channel_id"]))

                        #: Delete the Old Button
                        await channel.purge(limit=1)

                        #: Send new button
                        message = "Click the ✅ Verify button to got verified"
                        embed = Embed(title="Verification", color=Color.orange())
                        embed.add_field(name="", value=message, inline=False)
                        await channel.send(embed=embed, view=VerifyButton())
                    except:
                        pass

    #: write commands here
    #:
    #: Level System
    #:
    @commands.group(name="verify", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def verify(self, ctx: Context):
        guild = get_collection(Collection.GUILD).find_one({"_id": str(ctx.guild.id)})
        prefix = guild["config"]["prefix"]

        cmds = f"""
                -  **`init`**: Initialize Verification System
                -  **`channel`**: Set Verification Channel
                -  **`role`**: Set Verified Role
                -  **`start`**: Generate verify button with message
                -  **`enable`**: Enable Verification System
                -  **`disable`**: Disable Verification System
                -  **`status`**: show Level Verification status
                """

        embed = Embed(title="Verification System commands -", color=ctx.author.color)
        embed.add_field(name=f"**`{prefix}verify`**", value=cmds, inline=False)

        await ctx.send(embed=embed)

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def init(self, ctx: Context):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}

        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        #: Guild Configuration
        guild_config = guild["config"]

        #: Check if verify already initiated
        if "verify" in guild_config.keys():
            embed = Embed(title="Verification System is already initiated ", color=ctx.author.color)
            embed.add_field(name=f"Try `{guild_config['prefix']}verify` for more", value="", inline=False)

            await ctx.send(embed=embed)

        elif "verify" not in guild_config.keys():
            guild_config["verify"] = True

            guild_verify = {
                "channel_id": None,
                "channel_name": None,
                "role_id": None,
                "role_name": None
            }

            col_guild.update_one(query, {"$set": {"config": guild_config, "verify": guild_verify}})
            await ctx.send("```Verification System initiated successfully```")

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def start(self, ctx: Context, *, message: str | None):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}

        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        guild_config = guild["config"]

        if "verify" in guild_config.keys():
            #: delete the command
            await ctx.channel.purge(limit=1)
            #: Check if message is empty
            if message is None:
                message = "Click the ✅ Verify button to got verified"

            embed = Embed(title="Verification", color=ctx.author.color)
            embed.add_field(name="", value=message, inline=False)
            await ctx.send(embed=embed, view=VerifyButton())

        else:
            embed = Embed(title="Verification System is not initiated\nPlease initiate it first",
                          color=ctx.author.color)
            embed.add_field(name=f"Try `{guild_config['prefix']}verify init`", value="", inline=False)

            await ctx.send(embed=embed)

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx: Context, channel_id):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}
        channel_name = ctx.guild.get_channel(int(channel_id)).name
        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        guild_config = guild["config"]

        if "verify" in guild_config.keys():
            guild_verify = guild["verify"]
            guild_verify["channel_id"] = str(channel_id)
            guild_verify["channel_name"] = str(channel_name)

            col_guild.update_one(query, {"$set": {"verify": guild_verify}})

            embed = Embed(title="Verification System Channel -\nSetup Successful!", color=ctx.author.color)
            embed.add_field(name="ID: ", value=channel_id, inline=False)
            embed.add_field(name="Name: ", value=channel_name, inline=False)

            await ctx.send(embed=embed)
        else:
            embed = Embed(title="Verification System is not initiated\nPlease initiate it first",
                          color=ctx.author.color)
            embed.add_field(name=f"Try `{guild_config['prefix']}verify init`", value="", inline=False)

            await ctx.send(embed=embed)

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx: Context, role_id):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}
        role_name = ctx.guild.get_role(int(role_id)).name
        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        guild_config = guild["config"]

        if "verify" in guild_config.keys():
            guild_verify = guild["verify"]
            guild_verify["role_id"] = str(role_id)
            guild_verify["role_name"] = str(role_name)

            col_guild.update_one(query, {"$set": {"verify": guild_verify}})
            embed = Embed(title="Verification System Role -\nSetup Successful!", color=ctx.author.color)
            embed.add_field(name="ID: ", value=role_id, inline=False)
            embed.add_field(name="Name: ", value=role_name, inline=False)

            await ctx.send(embed=embed)
        else:
            embed = Embed(title="Verification System is not initiated\nPlease initiate it first",
                          color=ctx.author.color)
            embed.add_field(name=f"Try `{guild_config['prefix']}verify init`", value="", inline=False)

            await ctx.send(embed=embed)

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx: Context):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}

        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        #: Guild Configuration
        guild_config = guild["config"]

        if "verify" in guild_config.keys():
            guild_config["verify"] = True

            get_collection(Collection.GUILD).update_one(query, {"$set": {"config": guild_config}})
            await ctx.send("```Verification System enabled successfully```")

        else:
            embed = Embed(title="Verification System is not initiated\nPlease initiate it first",
                          color=ctx.author.color)
            embed.add_field(name=f"Try `{guild_config['prefix']}verify init`", value="", inline=False)

            await ctx.send(embed=embed)

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx: Context):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}

        #: Initiate database
        col_guild = get_collection(Collection.GUILD)

        #: Fetching database
        guild = col_guild.find_one(query)

        #: Guild Configuration
        guild_config = guild["config"]

        if "verify" in guild_config.keys():
            guild_config["verify"] = False

            get_collection(Collection.GUILD).update_one(query, {"$set": {"config": guild_config}})

            await ctx.send("```Verification System disabled successfully```")

        else:
            embed = Embed(title="Verification System is not initiated\nPlease initiate it first",
                          color=ctx.author.color)
            embed.add_field(name=f"Try `{guild_config['prefix']}verify init`", value="", inline=False)

            await ctx.send(embed=embed)

    @verify.command()
    @commands.has_permissions(administrator=True)
    async def status(self, ctx: Context):
        guild_id = str(ctx.guild.id)
        query = {"_id": guild_id}

        #: Initiate database
        #: Fetching database
        col_guild = get_collection(Collection.GUILD)
        guild = col_guild.find_one(query)

        #: Guild Configuration
        guild_config = guild["config"]

        if "verify" in guild_config.keys():
            embed = Embed(title="Verification System Status-", color=ctx.author.color)
            embed.add_field(name=get_status(guild_config["verify"]), value="", inline=False)

            await ctx.send(embed=embed)
        else:
            embed = Embed(title="Verification System is not initiated\nPlease initiate it first",
                          color=ctx.author.color)
            embed.add_field(name=f"Try `{guild_config['prefix']}verify init`", value="", inline=False)

            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Verification(client))
