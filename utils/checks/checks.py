import discord
from discord.ext import commands


class NoNSFW(commands.CommandError):
    pass


def is_owner_check(ctx):
    return ctx.author.id in ctx.bot.config()["owners"]


def is_owner():
    return commands.check(is_owner_check)


def is_staff_check():
    return False


def is_staff():
    return commands.check(is_staff_check)


async def check_nsfw(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        return True
    if ctx.channel.is_nsfw():
        return True
    raise NoNSFW


def is_nsfw():
    return commands.check(check_nsfw)


def check_permissions(ctx, perms):
    if is_owner_check(ctx):
        return True
    if not perms:
        return False
    author, channel = ctx.author, ctx.channel
    resolved = channel.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())


# TODO: Allow server owners to set mod/admin roles
def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True
    if isinstance(ctx.channel, discord.DMChannel):
        return False
    if check:
        return True


def mod_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, ctx.author.permissions_in(ctx.channel).manage_messages, **perms)
    return commands.check(predicate)


def admin_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, ctx.author.permissions_in(ctx.channel).manage_guild, **perms)
    return commands.check(predicate)


def guild_owner_or_permissions(**perms):
    def predicate(ctx):
        guild = ctx.guild
        if not guild:
            return False
        if ctx.author.id == guild.owner.id:
            return True
        return check_permissions(ctx, perms)
    return commands.check(predicate)


def guild_owner():
    return guild_owner_or_permissions()


def admin():
    return admin_or_permissions()


def mod():
    return mod_or_permissions()
