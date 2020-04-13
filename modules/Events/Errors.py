from datetime import timedelta

import discord
from discord.ext import commands

from utils.checks.bot_checks import can_react
from utils.functions import errors

__author__ = "Kanin"
__date__ = "11/19/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def format_retry_after(retry_after):
        delta = timedelta(seconds=int(round(retry_after, 0)))
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if days:
            fmt = f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds"
        elif hours:
            fmt = f"{hours} hours, {minutes} minutes, and {seconds} seconds"
        elif minutes:
            fmt = f"{minutes} minutes and {seconds} seconds"
        else:
            fmt = f"{seconds} seconds"
        return f"You can try again in {fmt}"

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        try:
            if isinstance(error, commands.CommandOnCooldown):
                return await ctx.send(self.format_retry_after(error.retry_after))
            ctx.command.reset_cooldown(ctx)
            if isinstance(error, commands.MissingRequiredArgument):
                return await ctx.missing_argument()
            if isinstance(error, (commands.BadArgument, commands.BadUnionArgument)):
                return await ctx.bad_argument(error)
            if isinstance(error, commands.NSFWChannelRequired):
                return await ctx.send_error(f"I can't give you the command {ctx.command} in a sfw environment.")
            if isinstance(error, commands.NoPrivateMessage):
                return await ctx.send_error("That command cannot be used in private messages!")
            if isinstance(error, commands.CheckFailure):
                if isinstance(error, errors.BotMissingPermissions):
                    if "embed_links" in error.missing_perms:
                        return await ctx.send(error)
                    return await ctx.send_error(error)
                if ctx.command.name not in ["register"]:
                    return await ctx.send_error("You don't have permission to use this command!")
                return
            if isinstance(error, errors.TooManyUsers):
                return await ctx.send_error("You provided too many users!")
            ctx.bot.sentry.capture_exception(error)
            return await ctx.send_error(error)
        except discord.Forbidden:
            if can_react(ctx):
                return await ctx.message.add_reaction("❌")
            try:
                return await ctx.author.send(f"I cannot send messages in {ctx.guild.name}!")
            except discord.Forbidden:
                return ctx.log.error(f"Failed to respond to command in {ctx.guild.name}")


def setup(bot):
    bot.add_cog(Errors(bot))
