import discord
from discord.ext import commands

from utils.Database.Add import addtodb
from utils.Database.Prefix import list_prefix


class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.bot.is_ready():
            return
        author = message.author
        # Adding some statistics
        self.bot.counter["messages"] += 1
        # Checking if the author of the message is a bot
        if author.bot:
            return
        await addtodb(self.bot, message.guild if message.guild else None, message.author)
        # Mention the bot to list prefixes
        mentions = [self.bot.user.mention]
        if not isinstance(message.channel, discord.DMChannel):
            mentions.append(message.guild.me.mention)
        if message.content in mentions:
            await message.channel.send(f"My prefixes here are:\n{await list_prefix(self.bot, message)}")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        message, command = ctx.message, ctx.command
        if not message.author.id == 173237945149423619:
            return

        cmd = command.qualified_name.replace(" ", "_")
        self.bot.commands_used[cmd] += 1
        self.bot.counter["commands_ran"] += 1

        destination = "Private Message" if isinstance(ctx.channel, discord.DMChannel) else \
            f"#{message.channel.name} ({message.guild.name})"

        self.bot.log.info(f"{message.author} in {destination}: {message.content}")


def setup(bot):
    bot.add_cog(MessageHandler(bot))
