import re

from discord import Embed, DMChannel, Invite, NotFound, Guild
from discord.ext.commands import Cog
from discord.utils import oauth_url

from bot import Bot
from config import regex, config
from utils.ctx import Context
from utils.functions.prefix import Prefixes


async def check_data(ctx: Context):
    data = await ctx.pool.fetch("SELECT * FROM guilds WHERE guild_id=$1", ctx.guild.id)
    if not data:
        await ctx.pool.execute("INSERT INTO guilds (guild_id) VALUES ($1) ON CONFLICT DO NOTHING", ctx.guild.id)
        ctx.log.info(f"Added {ctx.guild.name} to the (guilds) database")


class Messages(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @Cog.listener()
    async def on_message(self, message):
        ctx: Context = await self.bot.get_context(message)
        # Adding some statistics
        self.bot.counter["messages"] += 1
        # Checking if the author of the message is a bot
        if message.author.bot:
            return
        if isinstance(message.channel, DMChannel):
            invite_ids: list = list(dict.fromkeys(re.findall(regex.invite_url, message.content)))[:10]
            invites: list = []
            for invite_id in invite_ids:
                try:
                    invite: Invite = await self.bot.fetch_invite(invite_id)
                except NotFound:
                    invites.append(f"Could not find a server for the `{invite_id}` invite!")
                else:
                    guild: Guild = invite.guild
                    if not guild:
                        invites.append(f"Could not find a server for the `{invite_id}` invite!")
                    else:
                        url = oauth_url(
                            self.bot.user.id,
                            permissions=config.permissions,
                            guild=guild,
                            scopes=["bot", "applications.commands"]
                        )
                        invites.append(f"[{guild.name}]({url})")
            em = Embed(
                color=self.bot.color,
                description="\n".join(invites),
                title=f"Invite {self.bot.user.name} to:"
            )
            if invites:
                await ctx.reply(embed=em)
        else:
            await check_data(ctx)
        # Mention the bot to list prefixes
        if re.fullmatch(f"<@!?{self.bot.user.id}>", message.content):
            await ctx.reply(f"My prefixes here are:\n{await Prefixes.list(ctx)}")

    @Cog.listener()
    async def on_command(self, ctx: Context):
        message, command = ctx.message, ctx.command

        cmd = command.qualified_name.replace(" ", "_")
        self.bot.commands_used[cmd] += 1
        self.bot.counter["commands_ran"] += 1

        destination = "Private Message" if isinstance(ctx.channel, DMChannel) else \
            f"#{message.channel.name} ({message.guild.name})"

        self.bot.log.info(f"{message.author} in {destination}: {message.content}")


def setup(bot):
    bot.add_cog(Messages(bot))
