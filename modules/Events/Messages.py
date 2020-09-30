import re

import discord
from discord.ext import commands

from utils.database.GuildSettings import Prefixes, Check


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        # Adding some statistics
        self.bot.counter["messages"] += 1
        # Checking if the author of the message is a bot
        if message.author.bot:
            return
        if not isinstance(message.channel, discord.DMChannel):
            await Check().main(ctx.bot, ctx.guild)
        # Mention the bot to list prefixes
        if re.match(f"<@!?{self.bot.user.id}>", message.content):
            await ctx.send(f"My prefixes here are:\n{await Prefixes(ctx).list()}")

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
