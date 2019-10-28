from datetime import datetime
from typing import Union

import discord
from dateutil.relativedelta import relativedelta
from discord.ext import commands

key_perms = ["kick_members", "ban_members", "administrator", "manage_channels", "manage_server", "manage_messages",
             "mention_everyone", "manage_nicknames", "manage_roles", "manage_webhooks", "manage_emojis"]

voice_perms = ["connect", "deafen_members", "move_members", "mute_members", "priority_speaker", "speak", "stream",
               "use_voice_activation"]

statuses = {
    "idle":
        "<:IDLE:591344823622041600>",
    "dnd":
        "<:DND:591344889384534036>",
    "online":
        "<:ON:591344804307402793>",
    "streaming":
        "<:STRE:591345161766961178>",
    "offline":
        "<:OFF:591344910905376779>"
}


def get_relative_delta(time):
    delta = relativedelta(datetime.now(), time)
    tme = []
    msg = time.strftime("%A, %B %d %Y @ %I:%M%p %Z")
    if delta.years:
        years = delta.years
        tme.append(f"{years} years" if years != 1 else "1 year")
    if delta.months:
        months = delta.months
        tme.append(f"{months} months" if months != 1 else "1 month")
    if delta.days:
        days = delta.days
        tme.append(f"{days} days" if days != 1 else "1 day")
    if len(tme) == 0:
        return msg + "\nToday!"
    msg += "\n"
    msg += ", ".join(tme)
    msg += " ago"
    if len(tme) != 1:
        msg += f" ({(datetime.now() - time).days} days)"
    return msg


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(aliases=["whois"], invoke_without_command=True, description="Check a users information!")
    async def user(self, ctx, *, user: discord.Member = None):
        """{"permissions": {"user": [], "bot": ["embed_links"]}}"""
        if not ctx.invoked_subcommand:
            author, server, message = ctx.author, ctx.guild, ctx.message
            if not user:
                user = author
            em = discord.Embed(color=user.color)
            game = f"{'📱' if user.is_on_mobile() else ''}{statuses[str(user.status)]}" \
                   f" {str(user.status).capitalize()}\n\n"
            if user.activity is None:
                pass
            elif user.activity.type == discord.ActivityType.playing:
                activity = user.activity.to_dict()
                game += f"Playing **{user.activity.name}**"
                if "details" in activity:
                    game += f"\n{activity['details']}"
                if "state" in activity:
                    game += f"\n{activity['state']}"
            elif user.activity.type == discord.ActivityType.watching:
                game += f"Watching {user.activity.name}"
            elif user.activity.type == discord.ActivityType.listening:
                game += f"Listening to {user.activity.title}\n" \
                        f"By {', '.join([x for x in author.activity.artists])}\n" \
                        f"On {user.activity.name}"
            else:
                game += f"Streaming **[{user.activity.name}]({user.activity.url})**"
            em.add_field(name="Status:", value=game, inline=False)

            if user.voice:
                other_people = len(user.voice.channel.members) - 1
                voice = f"In {user.voice.channel.mention}"
                voice += f" with {other_people} others" if other_people else " alone"
            else:
                voice = "Not connected"
            em.add_field(name='Voice:', value=voice, inline=False)

            if len(user.roles) <= 41:
                roles = " ".join([x.mention for x in user.roles if x.name != "@everyone"][::-1])
                roles = roles if roles else "None"
                em.add_field(name=f"Roles [{len(user.roles) - 1}]:", value=roles, inline=False)
            else:
                em.add_field(name=f"Roles [{len(user.roles) - 1}]:", value="Too many to display", inline=False)

            perms = [x[0] for x in iter(ctx.channel.permissions_for(user)) if x[1]]
            permissions = ", ".join([str(x).replace("_", " ").title() for x in perms if x in key_perms])
            permissions = permissions if permissions else "None"
            em.add_field(name="Key Permissions:", value=permissions)

            member_number = sorted(server.members, key=lambda m: m.joined_at).index(user) + 1
            em.set_footer(text=f"Member #{member_number} • User ID: {user.id}")

            name = "BOT: " if user.bot else ""
            name += " ~ ".join((str(user), user.nick)) if user.nick else str(user)

            if user.avatar_url:
                em.set_thumbnail(url=user.avatar_url)
            em.set_author(name=name)

            em.add_field(name="Joined Discord on:", value=get_relative_delta(user.created_at), inline=False)
            em.add_field(name="Joined this server on:", value=get_relative_delta(user.joined_at), inline=False)

            return await ctx.send(embed=em)

    @user.command(name="permissions", aliases=["perms"],
                  description="Check a users permissions for a given Text/Voice channel")
    async def user_permissions(self, ctx, user: discord.Member = None, *,
                               channel: Union[discord.TextChannel, discord.VoiceChannel] = None):
        """
        {"permissions": {"user": [], "bot": ["embed_links"]}}
        """
        if not user:
            user = ctx.author
        if not channel:
            channel = ctx.channel
        perms = channel.permissions_for(user)
        perms_we_have = ""
        perms_we_dont = ""
        if isinstance(channel, discord.TextChannel):
            for perm in perms:
                if perm[0] not in voice_perms:
                    perm_name = perm[0].replace('_', ' ').title()
                    if perm[1]:
                        perms_we_have += f"+\t{perm_name}\n"
                    else:
                        perms_we_dont += f"-\t{perm_name}\n"
        elif isinstance(channel, discord.VoiceChannel):
            for perm in perms:
                if perm[0] in voice_perms:
                    perm_name = perm[0].replace('_', ' ').title()
                    if perm[1]:
                        perms_we_have += f"+\t{perm_name}\n"
                    else:
                        perms_we_dont += f"-\t{perm_name}\n"
        desc = f"```diff\n{perms_we_have}{perms_we_dont}\n```"
        em = discord.Embed(color=user.color, description=desc)
        em.set_author(name=f"{user.name}'s permissions in {channel}:")
        await ctx.send(embed=em)

    @user.command(name="avatar", aliases=["avi"], description="Get a users avatar")
    async def user_avatar(self, ctx, user: discord.Member = None):
        """
        {"permissions": {"user": [], "bot": ["embed_links"]}}
        """
        if not user:
            user = ctx.author
        url = user.avatar_url_as(static_format="png", size=1024)
        em = discord.Embed(color=user.color)
        em.description = f"[Open image]({url})"
        em.set_image(url=url)
        em.set_author(name=f"{user.name}'s avatar")
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Info(bot))
