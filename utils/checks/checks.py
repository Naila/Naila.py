import discord
from discord.ext import commands

__author__ = "Kanin"
__date__ = "11/19/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"

# Decorators


def is_owner():
    def predicate(ctx):
        return ctx.author.id in ctx.bot.config()["owners"]
    return commands.check(predicate)


# def is_staff():
#     def predicate(ctx):
#         return False
#     return commands.check(predicate)


def is_nsfw():
    def predicate(ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            return True
        if ctx.channel.is_nsfw():
            return True
        raise commands.NSFWChannelRequired
    return commands.check(predicate)


def guild_owner_or_permissions(**perms):
    def predicate(ctx):
        if not ctx.guild:
            return False
        if ctx.author.id == ctx.guild.owner.id:
            return True
        return check_permissions(ctx, perms)
    return commands.check(predicate)


def admin_or_permissions(**perms):
    def predicate(ctx):
        if ctx.author.permissions_in(ctx.channel).manage_guild:
            return True
        return role_or_permissions(ctx, **perms)
    return commands.check(predicate)


def mod_or_permissions(**perms):
    def predicate(ctx):
        if ctx.author.permissions_in(ctx.channel).manage_messages:
            return True
        return role_or_permissions(ctx, **perms)
    return commands.check(predicate)


def guild_owner():
    return guild_owner_or_permissions()


def admin():
    return admin_or_permissions()


def mod():
    return mod_or_permissions()


def permissions(**perms):
    def predicate(ctx):
        return check_permissions(ctx, **perms)
    return commands.check(predicate)

# Utilities


def check_permissions(ctx, perms):
    # Bot owner override
    if is_owner():
        return True
    # If no perms are provided there is nothing more to check
    if not perms:
        return False
    # Perms checks the dict passed {"permission": bool}
    resolved = ctx.channel.permissions_for(ctx.author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())


# TODO: Allow server owners to set mod/admin roles
def role_or_permissions(ctx, **perms):
    if check_permissions(ctx, perms):
        return True
    # DMs don't have roles or permissions so
    if isinstance(ctx.channel, discord.DMChannel):
        return False
