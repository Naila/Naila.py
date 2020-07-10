from dataclasses import dataclass

import discord

from utils.ctx import CustomContext
from ..functions import errors

__author__ = "Kanin"
__date__ = "11/23/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"


@dataclass
class Guild:
    ctx: CustomContext = None

    async def color(self, pool=None, guild: discord.Guild = None):
        guild = self.ctx.guild if self.ctx else guild
        con = await self.ctx.pool.acquire() if self.ctx else await pool.acquire()
        return await con.fetchval("SELECT color FROM guilds WHERE guild_id=$1", guild.id)


@dataclass
class Check:

    # async def all(self):
    #     await self.main()
    #     await self.welcomer()
    #     await self.registration()

    @staticmethod
    async def main(bot, guild: discord.Guild):
        con = await bot.pool.acquire()
        data = await con.fetch("SELECT * FROM guilds WHERE guild_id=$1", guild.id)
        if not data:
            await con.execute("INSERT INTO guilds (guild_id) VALUES ($1) ON CONFLICT DO NOTHING", guild.id)
            bot.log.info(f"Added {guild.name} to the (guilds) database")

    @staticmethod
    async def welcomer(bot, guild: discord.Guild):
        con = await bot.pool.acquire()
        data = await con.fetch("SELECT * FROM welcomer WHERE guild_id=$1", guild.id)
        if not data:
            await con.execute("INSERT INTO welcomer (guild_id) VALUES ($1) ON CONFLICT DO NOTHING", guild.id)
            bot.log.info(f"Added {guild.name} to the (welcomer) database")

    @staticmethod
    async def registration(bot, guild: discord.Guild):
        con = await bot.pool.acquire()
        data = await con.fetch("SELECT * FROM registration WHERE guild_id=$1", guild.id)
        if not data:
            await con.execute("INSERT INTO registration (guild_id) VALUES ($1) ON CONFLICT DO NOTHING", guild.id)
            bot.log.info(f"Added {guild.name} to the (registration) database")


@dataclass
class Registration:
    ctx: CustomContext

    async def data(self):
        ctx = self.ctx
        await Check().registration(ctx.bot, ctx.guild)
        data = await ctx.pool.fetchrow(
            "SELECT enabled, channel, age::json, questions::json, role FROM registration WHERE guild_id=$1",
            ctx.guild.id
        )
        return data

    async def toggle(self):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        data = await self.data()
        await con.execute("UPDATE registration SET enabled = NOT enabled WHERE guild_id=$1", ctx.guild.id)
        return not data["enabled"]

    async def update_channel(self, channel: discord.TextChannel):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        data = await self.data()
        if data["channel"] and data["channel"] == channel.id:
            return False
        await con.execute("UPDATE registration SET channel=$1 WHERE guild_id=$2", channel.id, ctx.guild.id)
        return True

    async def update_banage(self, age: int):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        await con.execute(
            "UPDATE registration SET age=jsonb_set(age, '{ban_age}', $1::jsonb) WHERE guild_id=$2",
            str(age),
            ctx.guild.id
        )


@dataclass
class Welcomer:
    ctx: CustomContext = None

    @staticmethod
    async def welcomer_data(bot, guild: discord.Guild):
        await Check().welcomer(bot, guild)
        con = await bot.pool.acquire()
        data = await con.fetchrow(
            "SELECT welcomer_background, banned_role, user_role, bot_role, welcomer_channel, welcomer_enabled,"
            " welcomer_embed, welcomer_content, welcomer_type FROM welcomer WHERE guild_id=$1",
            guild.id
        )
        return data

    async def toggle_welcomer(self):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        data = await self.welcomer_data(ctx.bot, ctx.guild)
        await con.execute(
            "UPDATE welcomer SET welcomer_enabled = NOT welcomer_enabled WHERE guild_id=$1",
            ctx.guild.id
        )
        return not data["welcomer_enabled"]

    async def toggle_welcomer_embed(self):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        data = await self.welcomer_data(ctx.bot, ctx.guild)
        await con.execute(
            "UPDATE welcomer SET welcomer_embed = NOT welcomer_embed WHERE guild_id=$1",
            ctx.guild.id
        )
        return not data["welcomer_embed"]

    async def set_welcomer_text(self, text: str = None):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        await Check().welcomer(ctx.bot, ctx.guild)
        await con.execute(
            "UPDATE welcomer SET welcomer_content=$1 WHERE guild_id=$2",
            text,
            ctx.guild.id
        )

    async def set_welcomer_type(self, image_type: int):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        await Check().welcomer(ctx.bot, ctx.guild)
        await con.execute(
            "UPDATE welcomer SET welcomer_type=$1 WHERE guild_id=$2",
            image_type,
            ctx.guild.id
        )

    async def set_welcomer_channel(self, channel: discord.TextChannel):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        await Check().welcomer(ctx.bot, ctx.guild)
        await con.execute(
            "UPDATE welcomer SET welcomer_channel=$1 WHERE guild_id=$2",
            channel.id,
            ctx.guild.id
        )

    @staticmethod
    async def disable(bot, guild: discord.Guild):
        con = await bot.pool.acquire()
        await con.execute(
            "UPDATE welcomer SET welcomer_channel=null, welcomer_enabled=false WHERE guild_id=$1",
            guild.id
        )


@dataclass
class Prefixes:
    ctx: CustomContext

    @staticmethod
    async def get(bot, message):
        con = await bot.pool.acquire()
        # Get default prefixes
        prefixes = [bot.user.mention + " "]
        prefixes.extend(bot.config()["prefixes"]["debug"] if bot.debug else bot.config()["prefixes"]["main"])

        # If we're in a guild, add the guilds custom prefixes
        if isinstance(message.channel, discord.TextChannel):
            guild = message.guild
            data = await con.fetchval("SELECT prefixes FROM guilds WHERE guild_id=$1", guild.id)
            if data:
                prefixes.extend(data)

            # Nicks are different mentions
            if guild.get_member(bot.user.id).nick:
                prefixes.append(guild.me.mention + " ")

        # Now that we have the list, let's try to see if it's in the message, if not we just return the entire list
        for prefix in prefixes:
            if message.content.lower().startswith(prefix):
                return message.content[:len(prefix)]
        return prefixes

    async def list(self):
        ctx = self.ctx
        bot = ctx.bot
        con = await bot.pool.acquire()
        # Get default prefixes
        prefixes = [bot.user.mention + " "]
        prefixes.extend(bot.config()["prefixes"]["debug"] if bot.debug else bot.config()["prefixes"]["main"])

        # If we're in a guild, add the guilds custom prefixes
        if isinstance(ctx.channel, discord.TextChannel):
            prefixes.extend(await con.fetchval("SELECT prefixes FROM guilds WHERE guild_id=$1", ctx.guild.id))

        # Make a string out of the list and return it
        return ", ".join(prefixes)

    async def add(self, prefix: str):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        # If the prefix is more than 10 characters we don't want it
        if len(prefix) > 10:
            raise errors.PrefixTooLong

        # Get the current prefixes and make sure it's not 10 in length
        current_prefixes = await con.fetchval("SELECT prefixes FROM guilds WHERE guild_id=$1", ctx.guild.id)
        if len(current_prefixes) == 10:
            raise errors.TooManyPrefixes

        # Get the default prefixes and make sure the prefix isn't in those
        default_prefixes = ctx.bot.config()["prefixes"]["main"] + ctx.bot.config()["prefixes"]["debug"]
        if prefix.lower() in current_prefixes or prefix in default_prefixes:
            raise errors.DuplicatePrefix

        # Add the prefix
        await con.execute(
            "UPDATE guilds SET prefixes=array_append(prefixes, $1) WHERE guild_id=$2",
            prefix.lower(),
            ctx.guild.id
        )

    async def remove(self, prefix: str):
        ctx = self.ctx
        con = await ctx.pool.acquire()
        # Get the current prefixes and make sure it's in them
        prefixes = await con.fetchval("SELECT prefixes FROM guilds WHERE guild_id=$1", ctx.guild.id)
        if prefix.lower() not in prefixes:
            raise errors.PrefixNotFound

        # Remove the prefix
        await con.execute(
            "UPDATE guilds SET prefixes=array_remove(prefixes, $1) WHERE guild_id=$2",
            prefix.lower(),
            ctx.guild.id
        )
