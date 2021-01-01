import os
import traceback
from datetime import timedelta, datetime

import discord
from discord.ext import commands

from utils.checks.bot_checks import can_react, can_send
from utils.functions import errors
import sentry_sdk as sentry

from utils.functions.text import pagify


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_count = 0

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
        if not can_send(ctx):
            if can_react(ctx):
                return await ctx.message.add_reaction("❌")
            try:
                return await ctx.author.send(f"I cannot send messages in {ctx.guild.name}!")
            except discord.Forbidden:
                return ctx.log.error(f"Failed to respond to command in {ctx.guild.name}")
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(self.format_retry_after(error.retry_after))
        ctx.command.reset_cooldown(ctx)
        # if isinstance(error, commands.CommandInvokeError):
        #     return await ctx.send_error(error.original)
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

        self.error_count += 1
        sentry.capture_exception(error)
        # ctx.bot.log.error(repr(error), exc_info=True if ctx.bot.debug else False)
        webhook = discord.Webhook.from_url(os.getenv("ERRORS"), adapter=discord.AsyncWebhookAdapter(ctx.bot.session))
        long = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        em = discord.Embed(color=ctx.bot.error_color, description=f'`{type(error).__name__}: {str(error)}`')
        em.set_author(name="Error:")
        em.add_field(name="Content:", value=ctx.message.content)
        em.add_field(name="Invoker:", value="{}\n({})".format(ctx.message.author.mention, str(ctx.message.author)))
        if not isinstance(ctx.message.channel, discord.abc.PrivateChannel):
            em.add_field(name="Guild:", value=ctx.guild.name)
        em.add_field(
            name="Channel:",
            value="Private channel" if isinstance(ctx.channel, discord.DMChannel)
            else f"{ctx.channel.mention}\n({ctx.channel.name})"
        )
        em.timestamp = datetime.utcnow()
        await webhook.send(embed=em, username=f"Error #{self.error_count:,}")
        pages = pagify(long)
        if pages:
            for page in pages:
                await webhook.send(f"```py\n{page}\n```", username=f"Error #{self.error_count:,}")
        await ctx.send_error(error)


def setup(bot):
    bot.add_cog(Errors(bot))
