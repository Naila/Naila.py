from discord import TextChannel

from utils.ctx import Context
from utils.functions import errors


class Prefixes:

    @staticmethod
    async def get(bot, message):
        # Get default prefixes
        prefixes = [bot.user.mention + " "]  # TODO: Fix this bullshit
        prefixes.extend(bot.config.prefixes["debug"] if bot.debug else bot.config.prefixes["main"])

        # If we're in a guild, add the guilds custom prefixes
        if isinstance(message.channel, TextChannel):
            guild = message.guild
            prefixes.append(guild.me.mention + " ")

            data = await bot.pool.fetchval("SELECT prefixes FROM guilds WHERE guild_id=$1", guild.id)
            if data:
                prefixes.extend(data)

        # Now that we have the list, let's try to see if it's in the message, if not we just return the entire list
        for prefix in prefixes:
            if message.content.lower().startswith(prefix):
                return message.content[:len(prefix)]
        return prefixes

    @staticmethod
    async def list(ctx: Context):
        # Get default prefixes
        prefixes = [ctx.bot.user.mention + " "]
        prefixes.extend(ctx.bot.config.prefixes["debug"] if ctx.bot.debug else ctx.bot.config.prefixes["main"])

        # If we're in a guild, add the guilds custom prefixes
        if isinstance(ctx.channel, TextChannel):
            prefixes.extend(await ctx.pool.fetchval("SELECT prefixes FROM guilds WHERE guild_id=$1", ctx.guild.id))

        # Make a string out of the list and return it
        return ", ".join(prefixes)

    @staticmethod
    async def add(ctx: Context, prefix: str):
        # If the prefix is more than 10 characters we don't want it
        if len(prefix) > 10:
            raise errors.PrefixTooLong

        # Get the current prefixes and make sure it's not 10 in length
        current_prefixes = await ctx.pool.fetchval("SELECT prefixes FROM guilds WHERE guild_id=$1", ctx.guild.id)
        if len(current_prefixes) == 10:
            raise errors.TooManyPrefixes

        # Get the default prefixes and make sure the prefix isn't in those
        default_prefixes = ctx.bot.config.prefixes["main"] + ctx.bot.config.prefixes["debug"]
        if prefix.lower() in current_prefixes or prefix in default_prefixes:
            raise errors.DuplicatePrefix

        # Add the prefix
        await ctx.pool.execute(
            "UPDATE guilds SET prefixes=array_append(prefixes, $1) WHERE guild_id=$2",
            prefix.lower(),
            ctx.guild.id
        )

    @staticmethod
    async def remove(ctx: Context, prefix: str):
        # Get the current prefixes and make sure it's in them
        prefixes = await ctx.pool.fetchval("SELECT prefixes FROM guilds WHERE guild_id=$1", ctx.guild.id)
        if prefix.lower() not in prefixes:
            raise errors.PrefixNotFound

        # Remove the prefix
        await ctx.pool.execute(
            "UPDATE guilds SET prefixes=array_remove(prefixes, $1) WHERE guild_id=$2",
            prefix.lower(),
            ctx.guild.id
        )
