import discord
from discord.ext import commands


class NotDJ(commands.CommandError):
    pass


def is_owner_check(ctx):
    return ctx.author.id in [
        173237945149423619  # Kanin
    ]


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
    await nsfw_not_permitted(ctx)
    return False


async def nsfw_not_permitted(ctx):
    command = ctx.command.name
    em = discord.Embed(color=ctx.bot.error_color,
                       description=f"I can't give you the command {command} in a sfw environment.")
    return await ctx.send(embed=em)


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


def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True
    if isinstance(ctx.channel, discord.DMChannel):
        return False
    if check:
        return True


def mod_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, ctx.author.permissions_in(ctx.channel).manage_roles, **perms)

    return commands.check(predicate)


def admin_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, ctx.author.permissions_in(ctx.channel).manage_guild, **perms)

    return commands.check(predicate)


def guild_owner_or_permissions(**perms):
    def predicate(ctx):
        guild = ctx.message.guild
        if not guild:
            return False

        if ctx.message.author.id == guild.owner.id:
            return True

        return check_permissions(ctx, perms)

    return commands.check(predicate)


def guild_owner():
    return guild_owner_or_permissions()


def admin():
    return admin_or_permissions()


def mod():
    return mod_or_permissions()
