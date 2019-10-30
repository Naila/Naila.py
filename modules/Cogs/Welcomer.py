import os
import urllib
from datetime import datetime
from io import BytesIO

import discord
import pytz
from discord.ext import commands
from rethinkdb import r

from utils.checks import checks


# TODO: CLEAN THIS UP, it is SO BAD and old code, FIX IT PLS KANIN


class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    @commands.group(case_insensitive=True, description="Welcomer management")
    async def welcomer(self, ctx):
        """Welcomer management"""
        if not ctx.invoked_subcommand:
            return await ctx.group_help()

    @welcomer.command()
    async def toggle(self, ctx):
        """Toggles welcomer functionality"""
        guild = ctx.guild
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        db["enabled"] = not db["enabled"]
        await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
        if db["enabled"]:
            return await ctx.send("I have enabled welcomer!")
        await ctx.send("I have disabled welcomer!")

    @welcomer.command()
    async def test(self, ctx, background: str = None, fmt: int = 2):
        """See what welcomer will look like"""
        guild = ctx.guild
        author = ctx.author
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        background = background if background else db["background"]
        fmt = fmt if fmt else db["type"]
        await self.welcomer_handler(member=author, guild=guild, background=background, fmt=fmt, channel=ctx.channel)

    @welcomer.command()
    async def toggleembed(self, ctx):
        """Toggle the welcomer embed"""
        guild = ctx.guild
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        if db["embed"]:
            db["embed"] = False
            text = "Embeds turned off!"
        else:
            db["embed"] = True
            text = "Embeds turned on!"
        await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
        await ctx.send(text)

    @welcomer.command()
    async def settext(self, ctx, *, text: str):
        """Set the text to send along with the image"""
        if not len(text) <= 1800:
            return await ctx.send("Text must be less than 1800 characters!")
        guild = ctx.guild
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        db["content"] = text
        await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
        await ctx.send("Text set!")

    @welcomer.command()
    async def settype(self, ctx, *, type: [1, 2]):
        """Set the type of the image, 1 or 2 are acceptable"""
        if type not in [1, 2]:
            return await ctx.send("Type must be 1 or 2!")
        guild = ctx.guild
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        db["type"] = type
        await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
        await ctx.send("Type set!")

    @welcomer.command()
    async def setchannel(self, ctx, channel: discord.TextChannel = None):
        """Sets the channel where welcomer will be sent to."""
        channel = channel if channel else ctx.channel
        guild = ctx.guild
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        db["channel"] = str(channel.id)
        await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
        await ctx.send(f"Channel set to {channel.mention}!")

    @welcomer.group(name="userroles")
    async def _userroles(self, ctx):
        """Automatic user role management"""
        subcommand = str(ctx.invoked_subcommand).replace("welcomer userroles", "")
        if not subcommand:
            return await ctx.send_cmd_help(ctx)

    @_userroles.command(name="add")
    async def _add(self, ctx, role: discord.Role):
        """Add a role to the auto role list for users"""
        guild = ctx.guild
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        if len(db["user_roles"]) <= 3 and role.id not in db["user_roles"]:
            db["user_roles"].append(str(role.id))
            await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
            await ctx.send(f"I have added the **{role.name}** role to the list of auto roles!")
        else:
            await ctx.send("You already have set 3 roles or this role is already set!")

    @_userroles.command(name="remove")
    async def _remove(self, ctx, role: discord.Role):
        """Remove a role from the auto role list for users"""
        guild = ctx.guild
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        if str(role.id) in db["user_roles"]:
            db["user_roles"].remove(str(role.id))
            await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
            await ctx.send(f"I have removed the **{role.name}** role from the list of auto roles!")
        else:
            await ctx.send("Role wasn't in the list of auto roles!")

    @_userroles.command(name="list")
    async def _list(self, ctx):
        """List the auto roles for users"""
        guild = ctx.guild
        role_list = []
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        if db["user_roles"]:
            for role_id in db["user_roles"]:
                role_list.append(guild.get_role(int(role_id)).name)
            await ctx.send(", ".join(role_list))
        else:
            await ctx.send("You don't have any user roles set!")

    @welcomer.group(name="botroles")
    async def _botroles(self, ctx):
        """Automatic bot role management"""
        subcommand = str(ctx.invoked_subcommand).replace("welcomer botroles", "")
        if not subcommand:
            return await ctx.send_cmd_help(ctx)

    @_botroles.command(name="add")
    async def __add(self, ctx, role: discord.Role):
        """Add a role to the auto role list for bots"""
        guild = ctx.guild
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        if len(db["bot_roles"]) <= 3 and role.id not in db["bot_roles"]:
            db["bot_roles"].append(str(role.id))
            await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
            await ctx.send(f"I have added the **{role.name}** role to the list of auto roles!")
        else:
            await ctx.send("You already have set 3 roles or this role is already set!")

    @_botroles.command(name="remove")
    async def __remove(self, ctx, role: discord.Role):
        """Remove a role from the auto role list for bots"""
        guild = ctx.guild
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        if str(role.id) in db["bot_roles"]:
            db["bot_roles"].remove(str(role.id))
            await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
            await ctx.send(f"I have removed the **{role.name}** role from the list of auto roles!")
        else:
            await ctx.send("Role wasn't in the list of auto roles!")

    @_botroles.command(name="list")
    async def __list(self, ctx):
        """List the auto roles for bots"""
        guild = ctx.guild
        role_list = []
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        if db["bot_roles"]:
            for role_id in db["bot_roles"]:
                role_list.append(guild.get_role(int(role_id)).name)
            await ctx.send(", ".join(role_list))
        else:
            await ctx.send("You don't have any bot roles set!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.welcomer_handler(member)

    async def get_guildcolor(self, gid: str):
        color = await r.table("guilds").get(gid).get_field("color").run(self.bot.conn)
        return color

    @staticmethod
    def build_message(message: str, author: discord.Member = None,
                      user: discord.Member = None, guild: discord.Guild = None, level: int = None):
        if not message:
            return None
        if author:
            message = message.replace("{AUTHOR_MENTION}", author.mention)
            message = message.replace("{AUTHOR_NAME}", author.name)
        if user:
            message = message.replace("{USER_MENTION}", user.mention)
            message = message.replace("{USER_NAME}", user.name)
        if guild:
            message = message.replace("{GUILD_NAME}", guild.name)
            message = message.replace("{GUILD_COUNT_ALL}", str(len(guild.members)))
            message = message.replace("{GUILD_COUNT_USERS}", str(len([i for i in guild.members if not i.bot])))
            message = message.replace("{GUILD_COUNT_BOTS}", str(len([i for i in guild.members if i.bot])))
        if level:
            message = message.replace("{LEVEL}", str(level))
        return message

    async def welcomer_handler(self, member: discord.Member, guild: discord.Guild = None,
                               background: str = None, fmt: int = None, channel: discord.TextChannel = None):

        guild = member.guild if not guild else guild
        count = guild.member_count
        member_created = (pytz.timezone("UTC").localize(datetime.now()) - pytz.timezone("UTC").localize(
            member.created_at)).days
        member_sign = "❌" if member_created == 0 else "⚠" if member_created <= 3 else "✅"
        db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
        if not db["channel"] and not db["enabled"] or not db["channel"] or not db["enabled"] or not db:
            return
        channel = self.bot.get_channel(int(db["channel"])) if not channel else channel
        color = await self.get_guildcolor(str(guild.id)) if not db["color"] else db["color"]
        background = db["background"] if not background else background
        fmt = db["type"] if not fmt else fmt
        em = discord.Embed(color=color)
        em.set_thumbnail(url=str(guild.icon_url_as(static_format="png", size=1024)))
        em.description = f"{member_sign} Account created __**{member_created}**__ days ago!"
        em.description += f"\n🤖 __**Bot**__ account!" if member.bot else f"\n✅ __**User**__ account!"
        avatar = member.avatar_url_as(format="png")
        color = hex(color).split('x')[-1]
        member_url = urllib.parse.quote(str(member))
        guild_url = urllib.parse.quote(str(guild.name))
        url = f"https://ourmainfra.me/api/v2/welcomer/?avatar={avatar}&user_name={member_url}" \
              f"&guild_name={guild_url}&member_count={count}&color={color}"
        if background and background != "Transparent":
            url += f"&background={background}"
        if fmt:
            url += f"&type={fmt}"
        headers = {"Authorization": os.getenv("MAINFRAME_TOKEN")}
        async with self.bot.session.get(url, headers=headers) as resp:
            if resp.status == 200:
                response = await resp.read()
                image = BytesIO(response)
                image.seek(0)
        em.set_image(url="attachment://welcome.png")
        try:
            if db["embed"]:
                await channel.send(file=discord.File(fp=image, filename="welcome.png"), embed=em,
                                   content=self.build_message(message=db["content"], user=member, guild=guild))
            else:
                await channel.send(file=discord.File(fp=image, filename="welcome.png"),
                                   content=self.build_message(message=db["content"], user=member, guild=guild))
        except (discord.Forbidden, AttributeError):
            db["channel"] = None
            await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)


def setup(bot):
    bot.add_cog(Welcomer(bot))
