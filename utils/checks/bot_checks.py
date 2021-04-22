import discord
from discord.abc import GuildChannel
from discord.ext import commands


def can_reply(ctx: commands.Context = None, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    if not can_read_history(channel=channel):
        return False
    return can_send(channel=channel)


def check_hierarchy(ctx: commands.Context, role: discord.Role):
    return ctx.guild.me.top_role.position > role.position


def can_manage_user(ctx: commands.Context, user: discord.Member):
    return check_hierarchy(ctx, user.top_role)


def can_send(ctx: commands.Context = None, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    if isinstance(channel, discord.DMChannel):
        return True
    return ctx.guild.me.permissions_in(channel).send_messages


def can_read_history(ctx: commands.Context = None, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    if isinstance(channel, discord.DMChannel):
        return True
    return ctx.guild.me.permissions_in(channel).read_message_history


def can_embed(ctx: commands.Context = None, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    if isinstance(channel, discord.DMChannel):
        return True
    return ctx.guild.me.permissions_in(channel).embed_links


def can_react(ctx: commands.Context = None, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    if isinstance(channel, discord.DMChannel):
        return True
    return ctx.guild.me.permissions_in(channel).add_reactions


def can_delete(ctx: commands.Context, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    if isinstance(channel, discord.DMChannel):
        return False
    return ctx.guild.me.permissions_in(channel).manage_messages


def can_ban(ctx: commands.Context, member: discord.Member):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).ban_members and can_manage_user(ctx, member)


def can_kick(ctx: commands.Context, member: discord.Member):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).kick_members and can_manage_user(ctx, member)


def can_edit_user_nick(ctx: commands.Context, member: discord.Member):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).manage_nicknames and can_manage_user(ctx, member)


def can_edit_channel(ctx: commands.Context = None, channel: GuildChannel = None):
    channel = channel or ctx.channel
    if not isinstance(channel, GuildChannel):
        return False
    return ctx.guild.me.permissions_in(channel).manage_channels


def can_edit_role(ctx: commands.Context, role: discord.Role):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).manage_roles and check_hierarchy(ctx, role)
