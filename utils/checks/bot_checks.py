from discord import TextChannel, Role, Member, DMChannel
from discord.abc import GuildChannel
from utils.ctx import Context


def can_reply(ctx: Context = None, channel: TextChannel = None):
    channel = channel or ctx.channel
    if not can_read_history(channel=channel):
        return False
    return can_send(channel=channel)


def check_hierarchy(ctx: Context, role: Role):
    return ctx.guild.me.top_role.position > role.position


def can_manage_user(ctx: Context, user: Member):
    return check_hierarchy(ctx, user.top_role)


def can_send(ctx: Context = None, channel: TextChannel = None):
    channel = channel or ctx.channel
    if isinstance(channel, DMChannel):
        return True
    return ctx.guild.me.permissions_in(channel).send_messages


def can_read_history(ctx: Context = None, channel: TextChannel = None):
    channel = channel or ctx.channel
    if isinstance(channel, DMChannel):
        return True
    return ctx.guild.me.permissions_in(channel).read_message_history


def can_embed(ctx: Context = None, channel: TextChannel = None):
    channel = channel or ctx.channel
    if isinstance(channel, DMChannel):
        return True
    return ctx.guild.me.permissions_in(channel).embed_links


def can_react(ctx: Context = None, channel: TextChannel = None):
    channel = channel or ctx.channel
    if isinstance(channel, DMChannel):
        return True
    return ctx.guild.me.permissions_in(channel).add_reactions


def can_delete(ctx: Context, channel: TextChannel = None):
    channel = channel or ctx.channel
    if isinstance(channel, DMChannel):
        return False
    return ctx.guild.me.permissions_in(channel).manage_messages


def can_ban(ctx: Context, member: Member):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).ban_members and can_manage_user(ctx, member)


def can_kick(ctx: Context, member: Member):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).kick_members and can_manage_user(ctx, member)


def can_edit_user_nick(ctx: Context, member: Member):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).manage_nicknames and can_manage_user(ctx, member)


def can_edit_channel(ctx: Context = None, channel: GuildChannel = None):
    channel = channel or ctx.channel
    if not isinstance(channel, GuildChannel):
        return False
    return ctx.guild.me.permissions_in(channel).manage_channels


def can_edit_role(ctx: Context, role: Role):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).manage_roles and check_hierarchy(ctx, role)
