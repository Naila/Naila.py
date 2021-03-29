import re

import discord
from discord.ext import commands
from discord.utils import oauth_url

from bot import Bot
from config import regex, config
from utils.ctx import Context
from utils.database.GuildSettings import Prefixes, Check


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx: Context = await self.bot.get_context(message)
        # Adding some statistics
        self.bot.counter["messages"] += 1
        # Checking if the author of the message is a bot
        if message.author.bot:
            return
        if isinstance(message.channel, discord.DMChannel):
            invite_ids: list = list(dict.fromkeys(re.findall(regex.invite_url, message.content)))[:10]
            invites: list = []
            for invite_id in invite_ids:
                try:
                    invite: discord.Invite = await self.bot.fetch_invite(invite_id)
                except discord.NotFound:
                    invites.append(f"Could not find a server for the `{invite_id}` invite!")
                else:
                    guild: discord.Guild = invite.guild
                    if not guild:
                        invites.append(f"Could not find a server for the `{invite_id}` invite!")
                    else:
                        url = oauth_url(
                            self.bot.user.id,
                            permissions=config.permissions,
                            guild=guild
                        ).replace("scope=bot", "scope=applications.commands+bot")
                        invites.append(f"[{guild.name}]({url})")
            em = discord.Embed(
                color=self.bot.color,
                description="\n".join(invites),
                title=f"Invite {self.bot.user.name} to:"
            )
            await ctx.send(embed=em, reference=message)
        else:
            await Check().main(ctx.bot, ctx.guild)
        # Mention the bot to list prefixes
        if re.match(f"<@!?{self.bot.user.id}>", message.content):
            await ctx.send(f"My prefixes here are:\n{await Prefixes(ctx).list()}", reference=message)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        message, command = ctx.message, ctx.command

        cmd = command.qualified_name.replace(" ", "_")
        self.bot.commands_used[cmd] += 1
        self.bot.counter["commands_ran"] += 1

        destination = "Private Message" if isinstance(ctx.channel, discord.DMChannel) else \
            f"#{message.channel.name} ({message.guild.name})"

        self.bot.log.info(f"{message.author} in {destination}: {message.content}")


def setup(bot):
    bot.add_cog(Messages(bot))
