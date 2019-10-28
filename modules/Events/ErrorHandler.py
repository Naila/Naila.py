import traceback
from datetime import timedelta

import discord
from discord.ext import commands

from utils.checks.bot_checks import can_send, can_embed, can_react


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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(self.format_retry_after(error.retry_after))
        ctx.command.reset_cooldown(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.missing_argument(ctx)
        if isinstance(error, (commands.BadArgument, commands.BadUnionArgument)):
            return await ctx.bad_argument(ctx, error)
        if isinstance(error, commands.CommandInvokeError):
            if not isinstance(ctx.channel, discord.DMChannel):
                if not can_send(ctx) or not can_embed(ctx):
                    if can_react(ctx):
                        return await ctx.message.add_reaction("❌")
                    try:
                        return await ctx.author.send("Missing permissions to `Send Messages` and/or `Embed Links`!")
                    except discord.Forbidden:
                        return self.bot.log.error("Could not respond to command, all checks failed!")
        if isinstance(error, commands.CheckFailure):
            return await ctx.send_error(ctx, "You don't have permission to use this command!")
        long = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        print(long)
        self.bot.log.error(error)
        return await ctx.send_error(ctx, error)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
