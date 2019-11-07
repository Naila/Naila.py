import discord
from discord.ext import commands
from rethinkdb import r


# TODO: Rewrite ALL OF THIS, it's all horrible and I just need to get the bot back up for now


class TooManyPrefixes(commands.BadArgument):
    pass


class PrefixTooLong(commands.BadArgument):
    pass


class PrefixNotFound(commands.UserInputError):
    pass


class DuplicatePrefix(commands.UserInputError):
    pass


async def add_prefix(bot, guild_id: str, prefix: str):
    if len(prefix) > 10:
        raise PrefixTooLong
    db = await r.table("guilds").get(str(guild_id)).run(bot.conn)
    if len(db["prefixes"]) == 10:
        raise TooManyPrefixes
    if prefix.lower() in db["prefixes"] or prefix in bot.config()["prefixes"]["main"]:
        raise DuplicatePrefix
    db["prefixes"].append(prefix.lower())
    await r.table("guilds").insert(db, conflict="replace").run(bot.conn)


async def get_prefixes(bot, msg):
    if bot.testing:
        return "n!"
    prefixes = [bot.user.mention + " "]
    prefixes.extend(bot.config()["prefixes"]["debug"] if bot.debug else bot.config()["prefixes"]["main"])
    content = msg.content.lower()
    if isinstance(msg.channel, discord.DMChannel):
        for prefix in prefixes:
            if content.startswith(prefix):
                return msg.content[:len(prefix)]
        return prefixes
    guild = msg.guild
    if guild.get_member(bot.user.id).nick:
        prefixes.append(guild.me.mention + " ")
    prefixes.extend(await r.table("guilds").get(str(guild.id)).get_field("prefixes").run(bot.conn))
    for prefix in prefixes:
        if content.startswith(prefix):
            return msg.content[:len(prefix)]
    return prefixes


async def list_prefix(bot, msg):
    prefixes = [bot.user.mention + " "]
    prefixes.extend(bot.config()["prefixes"]["debug"] if bot.debug else bot.config()["prefixes"]["main"])
    if isinstance(msg.channel, discord.DMChannel):
        return prefixes
    gid = msg.guild.id
    prefixes.extend(await r.table("guilds").get(str(gid)).get_field("prefixes").run(bot.conn))
    return ", ".join(prefixes)


async def remove_prefix(bot, guild_id: str, prefix: str):
    try:
        db = await r.table("guilds").get(str(guild_id)).run(bot.conn)
        db["prefixes"].remove(prefix)
        await r.table("guilds").insert(db, conflict="replace").run(bot.conn)
    except ValueError:
        raise PrefixNotFound
