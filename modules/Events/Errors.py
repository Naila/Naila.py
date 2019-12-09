from datetime import timedelta
import traceback
import discord
from discord.ext import commands
import json

from utils.checks.bot_checks import can_react, can_send
from utils.functions import errors


class ErrorHandler(commands.Cog):
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

    @staticmethod
    async def handle_commandinvokeerror(ctx, error):
        docs = ["embed_links"] if "help" in ctx.command.name else json.loads(ctx.command.help)["bot"]
        if not can_send(ctx):
            if can_react(ctx):
                return await ctx.message.add_reaction("❌")
            try:
                return await ctx.author.send(f"I cannot send messages in {ctx.guild.name}!")
            except discord.Forbidden:
                return ctx.log.error(f"Failed to respond to command in {ctx.guild.name}")

        bot_perms = [x[0] for x in iter(ctx.channel.permissions_for(ctx.guild.me)) if x[1]]
        bot_missing_perms = [x.replace("_", " ").title() for x in docs if x not in bot_perms]
        if bot_missing_perms:
            return await ctx.send(f"I am missing permissions to {', '.join(bot_missing_perms)}!")
        ctx.log.error("".join(traceback.format_exception(type(error), error, error.__traceback__)))
        ctx.bot.sentry.capture_exception(error)
        return await ctx.send_error(error)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(self.format_retry_after(error.retry_after))
        ctx.command.reset_cooldown(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.missing_argument()
        if isinstance(error, (commands.BadArgument, commands.BadUnionArgument)):
            return await ctx.bad_argument(error)
        if isinstance(error, commands.CommandInvokeError):
            return await self.handle_commandinvokeerror(ctx, error)
        if isinstance(error, commands.NSFWChannelRequired):
            return await ctx.send_error(f"I can't give you the command {ctx.command} in a sfw environment.")
        if isinstance(error, commands.NoPrivateMessage):
            return await ctx.send_error("That command cannot be used in private messages!")
        if isinstance(error, commands.CheckFailure):
            if ctx.command.name not in ["register"]:
                return await ctx.send_error("You don't have permission to use this command!")
            return
        if isinstance(error, errors.TooManyUsers):
            return await ctx.send_error("You provided too many users!")
        ctx.log.error("".join(traceback.format_exception(type(error), error, error.__traceback__)))
        ctx.bot.sentry.capture_exception(error)
        return await ctx.send_error(error)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
