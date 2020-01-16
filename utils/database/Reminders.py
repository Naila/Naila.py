from dataclasses import dataclass

import discord

from utils.ctx import CustomContext
from utils.functions.time import parse_time

__author__ = "Kanin"
__date__ = "01/14/2020"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"


@dataclass
class Reminders:
    ctx: CustomContext

    async def add(self, location: int, expires: str, reminder: str):
        ctx = self.ctx
        await ctx.pool.execute(
            "INSERT INTO reminders (user_id, guild_id, channel_id, expires, reminder) VALUES ($1, $2, $3, $4, $5)",
            ctx.author.id,
            ctx.guild.id or None,
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
            to_send = f"**Reminder** {author.mention}: {reminder['reminder']}"
            if channel:
                try:
                    return await channel.send(to_send)
                except (discord.Forbidden, discord.HTTPException):
                    to_send += "\n*Failed to send to channel*"
            try:
                await author.send(to_send)
            except (discord.Forbidden, discord.HTTPException):
                return

    async def list(self):
        ctx = self.ctx
        reminders = await ctx.pool.fetch(
            "SELECT * FROM reminders WHERE NOT expired AND user_id=$1",
            ctx.author.id
        )
        return reminders

    async def delete(self, reminder_id: int):
        ctx = self.ctx
        deleted = await ctx.pool.execute(
            "UPDATE reminders SET expired=null WHERE id=$1 AND user_id=$2",
            reminder_id,
            ctx.author.id
        )
        return deleted
