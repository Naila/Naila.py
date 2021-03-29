from dataclasses import dataclass

import discord

from utils.ctx import Context
from utils.functions.time import parse_time


@dataclass
class Reminders:
    ctx: Context

    async def add(self, location: int, expires: str, reminder: str):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        await con.execute(
            "INSERT INTO reminders (user_id, channel_id, expires, reminder) VALUES ($1, $2, $3, $4)",
            ctx.author.id,
            location,
            parse_time(expires),
            reminder
        )
        await ctx.pool.release(con)

    @staticmethod
    async def check(bot):
        con = await bot.pool.acquire()
        reminders = await con.fetch(
            "SELECT * FROM reminders WHERE NOT expired AND expires <= now() AT TIME ZONE 'utc'"
        )
        for reminder in reminders:
            bot.log.info(f"Reminder #{reminder['id']} expired")
            await con.execute("UPDATE reminders SET expired=True WHERE id=$1", reminder["id"])
            author = bot.get_user(reminder["user_id"])
            channel = bot.get_channel(reminder["channel_id"])
            to_send = f"**Reminder** {author.mention}: {reminder['reminder']}"
            if channel:
                try:
                    await bot.pool.release(con)
                    return await channel.send(to_send)
                except (discord.Forbidden, discord.HTTPException):
                    to_send += "\n*Failed to send to channel*"
            try:
                await author.send(to_send)
            except (discord.Forbidden, discord.HTTPException):
                await bot.pool.release(con)
                return
        await bot.pool.release(con)

    async def list(self):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        reminders = await con.fetch(
            "SELECT * FROM reminders WHERE NOT expired AND user_id=$1",
            ctx.author.id
        )
        await ctx.pool.release(con)
        return reminders

    async def delete(self, reminder_id: int):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        deleted = await con.execute(
            "UPDATE reminders SET expired=null WHERE id=$1 AND user_id=$2",
            reminder_id,
            ctx.author.id
        )
        await ctx.pool.release(con)
        return deleted
