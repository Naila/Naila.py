from typing import Union

import discord
from discord.ext import commands
from utils.functions.time import get_relative_delta

__author__ = "Kanin"
__date__ = "11/19/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"


key_perms = ["kick_members", "ban_members", "administrator", "manage_channels", "manage_server", "manage_messages",
             "mention_everyone", "manage_nicknames", "manage_roles", "manage_webhooks", "manage_emojis"]

voice_perms = ["connect", "deafen_members", "move_members", "mute_members", "priority_speaker", "speak", "stream",
               "use_voice_activation"]


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_member_status(ctx, member):
        path = "status.mobile." if member.is_on_mobile() else "status."
        status = f"{ctx.emojis(path + str(member.status))} {str(member.status).capitalize()}\n\n"
        if not member.activity:
            pass
        elif member.activity.type == discord.ActivityType.playing:
            activity = member.activity.to_dict()
            status += f"Playing **{member.activity.name}**"
            if "details" in activity:
                status += f"\n{activity['details']}"
            if "state" in activity:
                status += f"\n{activity['state']}"
        elif member.activity.type == discord.ActivityType.watching:
            status += f"Watching {member.activity.name}"
        elif member.activity.type == discord.ActivityType.listening:
            status += f"Listening to {member.activity.title}\n" \
                    f"By {', '.join([x for x in member.activity.artists])}\n" \
                    f"On {member.activity.name}"
        else:
            status += f"Streaming **[{member.activity.name}]({member.activity.url})**"
        return status

    @commands.guild_only()
    @commands.group(aliases=["whois", "member", "memberinfo", "userinfo"],
                    invoke_without_command=True, description="Check a members information!")
    async def user(self, ctx, *, member: discord.Member = None):
        """{"user": [], "bot": ["embed_links"]}"""
        if not ctx.invoked_subcommand:
            guild, message, member = ctx.guild, ctx.message, member or ctx.author
            em = discord.Embed(color=member.color)
            em.set_thumbnail(url=member.avatar_url)
            em.set_author(
                name=f"{'BOT: ' if member.bot else ''}"
                     f"{' ~ '.join((str(member), member.nick)) if member.nick else str(member)}"
            )
            em.add_field(name="Status:", value=self.get_member_status(ctx, member), inline=False)
            vc = "Not connected"
            if member.voice:
                other_people = len(member.voice.channel.members) - 1
                vc = f"In {member.voice.channel.mention}"
                vc += f" with {other_people} others" if other_people else " alone"
            em.add_field(name='Voice:', value=vc, inline=False)
            em.add_field(
                name=f"Roles [{len(member.roles) - 1}]:",
                value=" ".join([x.mention for x in member.roles if x is not guild.default_role][::-1]) or "None"
                if len(member.roles) <= 41 else "Too many to display",
                inline=False
            )
            em.add_field(
                name="Key Permissions:",
                value=", ".join(
                    [str(x).replace("_", " ").title()
                     for x in [x[0] for x in iter(ctx.channel.permissions_for(member)) if x[1]] if x in key_perms]
                ) or "None",
                inline=False
            )
            em.add_field(
                name="Account created:", value=get_relative_delta(member.created_at, True, True), inline=False
            )
            em.add_field(
                name="Joined this server on:", value=get_relative_delta(member.joined_at, True, True), inline=False
            )
            em.set_footer(
                text=f"Member #{sorted(guild.members,key=lambda m: m.joined_at).index(member) + 1} • ID: {member.id}"
            )
            return await ctx.send(embed=em)

    @user.command(name="permissions", aliases=["perms"],
                  description="Check a users permissions for a given Text/Voice channel")
    async def user_permissions(self, ctx, user: discord.Member = None, *,
                               channel: Union[discord.TextChannel, discord.VoiceChannel] = None):
        """{"user": [], "bot": ["embed_links"]}"""
        user, channel = user or ctx.author, channel or ctx.channel
        perms = channel.permissions_for(user)
        perms_we_have = ""
        perms_we_dont = ""
        if isinstance(channel, discord.TextChannel):
            for perm in perms:
                if perm[0] not in voice_perms:
                    perm_name = perm[0].replace('_', ' ').title()
                    perms_we_have += f"+\t{perm_name}\n" if perm[1] else f"-\t{perm_name}\n"
        elif isinstance(channel, discord.VoiceChannel):
            for perm in perms:
                if perm[0] in voice_perms:
                    perm_name = perm[0].replace('_', ' ').title()
                    perms_we_have += f"+\t{perm_name}\n" if perm[1] else f"-\t{perm_name}\n"
        desc = f"```diff\n{perms_we_have}{perms_we_dont}\n```"
        em = discord.Embed(color=user.color, description=desc)
        em.set_author(name=f"{user.name}'s permissions in {channel}:")
        await ctx.send(embed=em)

    @user.command(name="avatar", aliases=["avi"], description="Get a users avatar")
    async def user_avatar(self, ctx, user: discord.Member = None):
        """{"user": [], "bot": ["embed_links"]}"""
        if not user:
            user = ctx.author
        url = user.avatar_url_as(static_format="png", size=1024)
        em = discord.Embed(color=user.color)
        em.description = f"[Open image]({url})"
        em.set_image(url=url)
        em.set_author(name=f"{user.name}'s avatar")
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(UserInfo(bot))
