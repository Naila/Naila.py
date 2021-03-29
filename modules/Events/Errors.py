import os
import traceback
from datetime import timedelta, datetime

import discord
import sentry_sdk as sentry
from discord.ext import commands

from bot import Bot
from utils.checks.bot_checks import can_react, can_send
from utils.ctx import Context
from utils.functions import errors
from utils.functions.text import pagify, readable_list


# _ = CustomContext.translator


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.error_count = 0

    @staticmethod
    def format_retry_after(retry_after):
        delta = timedelta(seconds=retry_after)
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        strings = []
        if days:
            # target = "time.days" if days > 1 else "time.day"
            # strings.append(f"{days} {_('common', target)}")
            string = "days" if days > 1 else "day"
            strings.append(f"{days} {string}")
        if hours:
            # target = "time.hours" if hours > 1 else "time.hour"
            # strings.append(f"{hours} {_('common', target)}")
            string = "hours" if hours > 1 else "hour"
            strings.append(f"{hours} {string}")
        if minutes:
            # target = "time.minutes" if minutes > 1 else "time.minute"
            # strings.append(f"{minutes} {_('common', target)}")
            string = "minutes" if minutes > 1 else "minute"
            strings.append(f"{minutes} {string}")
        if seconds:
            # target = "time.seconds" if seconds > 1 else "time.second"
            # strings.append(f"{seconds} {_('common', target)}")
            string = "seconds" if seconds > 1 else "second"
            strings.append(f"{seconds} {string}")
        if not strings:
            ms = int(round(delta.microseconds / 1000, 0))
            strings.append(f"{ms}ms")
        timestr = readable_list(strings)
        # TODO: Figure out when the best time to delete the message is
        delete_after = 0 if delta.total_seconds() > 10 else 1 if delta.total_seconds() < 1 else delta.total_seconds()
        # return _("errors", "on_cooldown", time=timestr)
        return f"You can try again in {timestr}!", delete_after

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if not can_send(ctx):
            if can_react(ctx):
                return await ctx.message.add_reaction("❌")
            try:
                # return await ctx.author.send(_("errors", "cannot_respond", guild=str(ctx.guild)))
                return await ctx.author.send(f"I cannot send messages in {ctx.guild}!")
            except discord.Forbidden:
                return ctx.log.error(f"Failed to respond to command in {ctx.guild.name}")
        if isinstance(error, commands.CommandOnCooldown):
            string, delete_after = self.format_retry_after(error.retry_after)
            return await ctx.send(string, delete_after=delete_after)
        ctx.command.reset_cooldown(ctx)
        # if isinstance(error, commands.CommandInvokeError):
        #     return await ctx.send_error(error.original)
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.missing_argument()
        if isinstance(error, (commands.BadArgument, commands.BadUnionArgument)):
            return await ctx.bad_argument(error)
        if isinstance(error, commands.NSFWChannelRequired):
            # return await ctx.send_error(_("errors", "no_nsfw", command=str(ctx.command)))
            return await ctx.send_error(f"I cannot give you the command `{ctx.command}` in a sfw environment!")
        if isinstance(error, commands.NoPrivateMessage):
            # return await ctx.send_error(_("errors", "no_pms", command=str(ctx.command)))
            return await ctx.send_error(f"{ctx.command} cannot be used in private messages!")
        if isinstance(error, commands.CheckFailure):
            if isinstance(error, errors.BotMissingPermissions):
                if "embed_links" in error.missing_perms:
                    # noinspection PyTypeChecker
                    return await ctx.send(error)
                return await ctx.send_error(error)
            if isinstance(error, errors.UserMissingPermissions):
                return await ctx.send_error(error)
            # return await ctx.send_error(_("errors", "user_cannot_use"))
            return await ctx.send_error("You cannot use this command!")

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
