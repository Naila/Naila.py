import discord
from discord.ext import commands


def check_hierarchy(ctx: commands.Context, role: discord.Role):
    return ctx.guild.me.top_role.position > role.position


def can_manage_user(ctx: commands.Context, user: discord.Member):
    return ctx.guild.me.top_role > user.top_role


def can_send(ctx: commands.Context, channel: discord.TextChannel = None):
    channel = ctx.channel if not channel else channel
    if isinstance(channel, discord.DMChannel):
        return True
    return ctx.guild.me.permissions_in(channel).send_messages


def can_embed(ctx: commands.Context, channel: discord.TextChannel = None):
    channel = ctx.channel if not channel else channel
    return ctx.guild.me.permissions_in(channel).embed_links


def can_react(ctx: commands.Context, channel: discord.TextChannel = None):
    channel = ctx.channel if not channel else channel
    return ctx.guild.me.permissions_in(channel).add_reactions


def can_delete(ctx: commands.Context):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).manage_messages


def can_ban(ctx: commands.Context, member: discord.Member):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).ban_members and check_hierarchy(ctx, member.top_role)


def can_kick(ctx: commands.Context, member: discord.Member):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).kick_members and check_hierarchy(ctx, member.top_role)


def can_edit_user_nick(ctx: commands.Context, member: discord.Member):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).manage_nicknames and check_hierarchy(ctx, member.top_role)


def can_edit_channel(ctx: commands.Context):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).manage_channels


def can_edit_role(ctx: commands.Context, role: discord.Role):
    if not ctx.guild:
        return False
    return ctx.guild.me.permissions_in(ctx.channel).manage_roles and check_hierarchy(ctx, role)
