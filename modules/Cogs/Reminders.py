from discord.ext.commands import Cog, command, group
from discord import Forbidden, HTTPException
from bot import Bot
from utils.ctx import Context
from utils.functions.text import escape, pagify
from utils.functions.time import get_relative_delta, parse_time


class DB:

    @staticmethod
    async def add(ctx: Context, location: int, expires: str, reminder: str):
        await ctx.pool.execute(
            "INSERT INTO reminders (user_id, channel_id, expires, reminder) VALUES ($1, $2, $3, $4)",
            ctx.author.id,
            location,
            parse_time(expires),
            reminder
        )

    @staticmethod
    async def check(bot):
        reminders = await bot.pool.fetch(
            "SELECT * FROM reminders WHERE NOT expired AND expires <= now() AT TIME ZONE 'utc'"
        )
        for reminder in reminders:
            bot.log.info(f"Reminder #{reminder['id']} expired")
            await bot.pool.execute("UPDATE reminders SET expired=True WHERE id=$1", reminder["id"])
            author = bot.get_user(reminder["user_id"])
            channel = bot.get_channel(reminder["channel_id"])
            to_send = f"**Reminder** <@!{reminder['user_id']}>: {reminder['reminder']}"
            if channel:
                try:
                    return await channel.send(to_send, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))
                except (Forbidden, HTTPException):
                    to_send += "\n*Failed to send to channel*"
            try:
                if author:
                    await author.send(to_send)
            except (Forbidden, HTTPException):
                return

    @staticmethod
    async def list(ctx: Context):
        reminders = await ctx.pool.fetch(
            "SELECT * FROM reminders WHERE NOT expired AND user_id=$1",
            ctx.author.id
        )
        return reminders

    @staticmethod
    async def delete(ctx: Context, reminder_id: int):
        deleted = await ctx.pool.execute(
            "UPDATE reminders SET expired=null WHERE id=$1 AND user_id=$2",
            reminder_id,
            ctx.author.id
        )
        return deleted


class Reminders(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @group(case_insensitive=True)
    async def remind(self, ctx: Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @remind.command(name="me")
    async def remind_me(self, ctx: Context, time: str, *, reminder: str):
        if len(reminder) > 1500:
            return await ctx.send_error("That's quite a long reminder... let's slow down a bit!")
        await DB.add(ctx, ctx.author.id, time, reminder)
        await ctx.reply(
            f"{ctx.author.mention}, I will remind you about this"
            f" {get_relative_delta(parse_time(time), append_small=True, bold_string=True)}"
        )

    @remind.command(name="here")
    async def remind_here(self, ctx: Context, time: str, *, reminder: str):
        if len(reminder) > 1500:
            return await ctx.send_error("That's quite a long reminder... let's slow down a bit!")
        await DB.add(ctx, ctx.channel.id, time, escape(reminder, False, False, False))
        await ctx.reply(
            f"{ctx.author.mention}, I will remind you about this"
            f" {get_relative_delta(parse_time(time), append_small=True, bold_string=True)}"
        )

    @command()
    async def reminders(self, ctx: Context):
        reminders = await DB.list(ctx)
        to_send = "**Your reminders:**\n"
        if reminders:
            for reminder in reminders:
                if reminder["channel_id"] == ctx.author.id:
                    location = "Private Messages"
                else:
                    location = f"<#{reminder['channel_id']}>"
                to_send += f"\n**{reminder['id']}**: {location}: \"{reminder['reminder']}\" -" \
                           f" {get_relative_delta(reminder['expires'], append_small=True, append_seconds=False)}"
        else:
            to_send += "\n**You don't currently have any reminders set!**"
        to_send += f"\n\nSet a reminder with `{ctx.prefix}remind <here|me> <time> <reminder>`\n" \
                   f"Remove a reminder with `{ctx.prefix}delreminder <id>`"
        pages = pagify(to_send)
        try:
            for page in pages:
                await ctx.author.send(page)
        except:
            return await ctx.reply("I cannot DM you!")
        await ctx.reply("I sent your reminders to you!")

    @command(aliases=["delreminder"])
    async def deletereminder(self, ctx: Context, reminder_id: int):
        deleted = await DB.delete(ctx, reminder_id)
        if deleted == "UPDATE 1":
            return await ctx.reply("I have deleted that reminder!")
        await ctx.send_error("Hmm I couldn't seem to find that reminder for you, make sure the id is correct!")


def setup(bot):
    bot.add_cog(Reminders(bot))
