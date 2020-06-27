from datetime import datetime
from urllib.parse import quote as parse

import discord
from discord.ext import commands

from utils.checks import checks
from utils.ctx import CustomContext
from utils.database.GuildSettings import Guild, Welcomer as Welcome
from utils.functions.api import welcomer

__author__ = "Kanin"
__date__ = "11/19/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"


class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.guild_only()
    # @commands.group(case_insensitive=True, description="Welcomer management")
    # @checks.admin_or_permissions()
    # async def welcomer(self, ctx):
    #     if not ctx.invoked_subcommand:
    #         return await ctx.send_help(ctx.command)
    #
    # @welcomer.command(name="toggle", description="Toggle welcomer entirely")
    # @checks.admin_or_permissions()
    # @checks.custom_bot_has_permissions(embed_links=True)
    # async def welcomer_toggle(self, ctx):
    #     """{"user": ["manage_guild"], "bot": ["embed_links"]}"""
    #     update = await Welcome(ctx).toggle_welcomer()
    #     if update:
    #         return await ctx.send("I have enabled welcomer!")
    #     await ctx.send("I have disabled welcomer!")
    #
    # @welcomer.command(name="test", description="Test what welcomer will look like")
    # @checks.admin_or_permissions()
    # @checks.custom_bot_has_permissions(embed_links=True)
    # async def welcomer_test(self, ctx, fmt: int = 2, background: str = None):
    #     """{"user": ["manage_guild"], "bot": ["embed_links"]}"""
    #     if fmt not in [1, 2]:
    #         return await ctx.send_error("fmt must either be 1 or 2!")
    #     data = await Welcome().welcomer_data(ctx.bot, ctx.guild)
    #     background = background if background else data["welcomer_background"]
    #     fmt = fmt if fmt else data["welcomer_type"]
    #     await self.welcomer_handler(member=ctx.author, ctx=ctx, background=background, fmt=fmt)
    #
    # @welcomer.command(name="embed", description="Toggle the embed")
    # @checks.admin_or_permissions()
    # @checks.custom_bot_has_permissions(embed_links=True)
    # async def welcomer_embed(self, ctx):
    #     """{"user": ["manage_guild"], "bot": ["embed_links"]}"""
    #     data = await Welcome(ctx).toggle_welcomer_embed()
    #     if data:
    #         return await ctx.send("Embeds have been enabled for welcomer!")
    #     await ctx.send("Embeds have been disabled for welcomer!")
    #
    # @welcomer.command(name="text", description="Set the content of the message | --current | --clear")
    # @checks.admin_or_permissions()
    # @checks.custom_bot_has_permissions(embed_links=True)
    # async def welcomer_text(self, ctx, *, text: str):
    #     """{"user": ["manage_guild"], "bot": ["embed_links"]}"""
    #     data = await Welcome().welcomer_data(ctx.bot, ctx.guild)
    #     if text == "--current":
    #         return await ctx.send(f"Current text:\n```{data['welcomer_content']}```")
    #     if text == "--clear":
    #         await Welcome(ctx).set_welcomer_text()
    #         return await ctx.send("Welcomer text has been cleared!")
    #     if len(text) >= 1800:
    #         return await ctx.send_error("Text must be less than 1800 characters!")
    #     await Welcome(ctx).set_welcomer_text(text)
    #     await ctx.send("Welcomer text has been set!")
    #
    # @welcomer.command(name="type", description="Change the image type | 1 or 2")
    # @checks.admin_or_permissions()
    # @checks.custom_bot_has_permissions(embed_links=True)
    # async def welcomer_type(self, ctx, *, image_type: int):
    #     """{"user": ["manage_guild"], "bot": ["embed_links"]}"""
    #     if image_type not in [1, 2]:
    #         return await ctx.send_error("Type must be 1 or 2!")
    #     await Welcome(ctx).set_welcomer_type(image_type)
    #     await ctx.send("Type set!")
    #
    # @welcomer.command(name="channel", description="Set the output channel")
    # @checks.admin_or_permissions()
    # @checks.custom_bot_has_permissions(embed_links=True)
    # async def welcomer_channel(self, ctx, channel: discord.TextChannel):
    #     """{"user": ["manage_guild"], "bot": ["embed_links"]}"""
    #     await Welcome(ctx).set_welcomer_channel(channel)
    #     await ctx.send(f"Channel set to {channel.mention}!")

    # TODO: Fix auto roles and extend on welcomers functionality
    # @welcomer.group(name="userroles")
    # async def _userroles(self, ctx):
    #     """{"user": ["manage_guild"], "bot": ["embed_links"]}"""
    #     subcommand = str(ctx.invoked_subcommand).replace("welcomer userroles", "")
    #     if not subcommand:
    #         return await ctx.send_cmd_help(ctx)
    #
    # @_userroles.command(name="add")
    # async def _add(self, ctx, role: discord.Role):
    #     """Add a role to the auto role list for users"""
    #     guild = ctx.guild
    #     db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
    #     if len(db["user_roles"]) <= 3 and role.id not in db["user_roles"]:
    #         db["user_roles"].append(str(role.id))
    #         await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
    #         await ctx.send(f"I have added the **{role.name}** role to the list of auto roles!")
    #     else:
    #         await ctx.send("You already have set 3 roles or this role is already set!")
    #
    # @_userroles.command(name="remove")
    # async def _remove(self, ctx, role: discord.Role):
    #     """Remove a role from the auto role list for users"""
    #     guild = ctx.guild
    #     db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
    #     if str(role.id) in db["user_roles"]:
    #         db["user_roles"].remove(str(role.id))
    #         await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
    #         await ctx.send(f"I have removed the **{role.name}** role from the list of auto roles!")
    #     else:
    #         await ctx.send("Role wasn't in the list of auto roles!")
    #
    # @_userroles.command(name="list")
    # async def _list(self, ctx):
    #     """List the auto roles for users"""
    #     guild = ctx.guild
    #     role_list = []
    #     db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
    #     if db["user_roles"]:
    #         for role_id in db["user_roles"]:
    #             role_list.append(guild.get_role(int(role_id)).name)
    #         await ctx.send(", ".join(role_list))
    #     else:
    #         await ctx.send("You don't have any user roles set!")
    #
    # @welcomer.group(name="botroles")
    # async def _botroles(self, ctx):
    #     """Automatic bot role management"""
    #     subcommand = str(ctx.invoked_subcommand).replace("welcomer botroles", "")
    #     if not subcommand:
    #         return await ctx.send_cmd_help(ctx)
    #
    # @_botroles.command(name="add")
    # async def __add(self, ctx, role: discord.Role):
    #     """Add a role to the auto role list for bots"""
    #     guild = ctx.guild
    #     db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
    #     if len(db["bot_roles"]) <= 3 and role.id not in db["bot_roles"]:
    #         db["bot_roles"].append(str(role.id))
    #         await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
    #         await ctx.send(f"I have added the **{role.name}** role to the list of auto roles!")
    #     else:
    #         await ctx.send("You already have set 3 roles or this role is already set!")
    #
    # @_botroles.command(name="remove")
    # async def __remove(self, ctx, role: discord.Role):
    #     """Remove a role from the auto role list for bots"""
    #     guild = ctx.guild
    #     db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
    #     if str(role.id) in db["bot_roles"]:
    #         db["bot_roles"].remove(str(role.id))
    #         await r.table("welcomer").insert(db, conflict="update").run(self.bot.conn)
    #         await ctx.send(f"I have removed the **{role.name}** role from the list of auto roles!")
    #     else:
    #         await ctx.send("Role wasn't in the list of auto roles!")
    #
    # @_botroles.command(name="list")
    # async def __list(self, ctx):
    #     """List the auto roles for bots"""
    #     guild = ctx.guild
    #     role_list = []
    #     db = await r.table("welcomer").get(str(guild.id)).run(self.bot.conn)
    #     if db["bot_roles"]:
    #         for role_id in db["bot_roles"]:
    #             role_list.append(guild.get_role(int(role_id)).name)
    #         await ctx.send(", ".join(role_list))
    #     else:
    #         await ctx.send("You don't have any bot roles set!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.welcomer_handler(member)

    @staticmethod
    def build_message(message: str, user: discord.Member, guild: discord.Guild):
        if not message:
            return
        message = message.replace("{USER_MENTION}", user.mention)
        message = message.replace("{USER_NAME}", user.name)
        message = message.replace("{GUILD_NAME}", guild.name)
        message = message.replace("{GUILD_COUNT_ALL}", str(len(guild.members)))
        message = message.replace("{GUILD_COUNT_USERS}", str(len([i for i in guild.members if not i.bot])))
        message = message.replace("{GUILD_COUNT_BOTS}", str(len([i for i in guild.members if i.bot])))
        return message

    async def welcomer_handler(self, member: discord.Member, ctx: CustomContext = None,
                               background: str = None, fmt: int = None):

        guild = member.guild
        data = await Welcome().welcomer_data(self.bot, guild)
        warning = ""
        if not data["welcomer_enabled"] or not data["welcomer_channel"]:
            if not ctx:
                return
            warning += "You either don't have welcomer enabled or don't have a channel set so this will not work!"
            await ctx.send_error(warning)
        member_created = (datetime.utcnow() - member.created_at).days
        member_sign = "❌" if member_created == 0 else "⚠" if member_created <= 3 else "✅"
        channel = ctx.channel if ctx else self.bot.get_channel(data["welcomer_channel"])
        color = await Guild().color(self.bot.pool, guild)
        background = background or data["welcomer_background"]
        fmt = fmt or data["welcomer_type"]
        content = self.build_message(data["welcomer_content"], member, guild)
        embed = data["welcomer_embed"]
        desc = [f"{member_sign} Account created __**{member_created}**__ days ago!"
                if member_created else f"{member_sign} Account created __**Today!**__",
                f"🤖 __**Bot**__ account!" if member.bot else f"✅ __**User**__ account!"]
        desc = '\n'.join(desc)
        em = discord.Embed(color=color, description=desc)
        if embed:
            em.set_thumbnail(url=guild.icon_url_as(static_format="png", size=1024))
            em.set_image(url="attachment://welcome.png")
        else:
            if content:
                content += f"\n\n{desc}"
            else:
                content = desc
        params = {
            "type": fmt,
            "avatar": member.avatar_url_as(format="png"),
            "user_name": parse(str(member)),
            "guild_name": parse(guild.name),
            "member_count": guild.member_count,
            "color": hex(color).split('x')[-1]
        }
        if background:
            params["background"] = background
        image = await welcomer(self.bot.session, params)
        try:
            return await channel.send(
                file=discord.File(fp=image, filename="welcome.png"),
                embed=em if embed else None,
                content=content)
        except (discord.Forbidden, AttributeError):
            await Welcome().disable(self.bot, guild)


def setup(bot):
    bot.add_cog(Welcomer(bot))
