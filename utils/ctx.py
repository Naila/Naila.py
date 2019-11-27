import discord
import yaml
from discord.ext import commands
from dictor import dictor

from modules.Cogs.Help import command_signature


class CustomContext(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session(self):
        return self.bot.session

    @property
    def pool(self):
        return self.bot.pool

    @property
    def log(self):
        return self.bot.log

    async def guildcolor(self):
        if not self.guild:
            return self.bot.color
        return await self.pool.fetchval("SELECT color FROM guilds WHERE guild_id=$1", self.guild.id)

    def emojis(self, emoji: str):
        with open("config/emojis.yml", "r") as emojis:
            emojis = yaml.safe_load(emojis)
        return self.bot.get_emoji(dictor(emojis, emoji))

    async def missing_argument(self):
        channel = self.channel
        prefix = self.prefix.replace(self.bot.user.mention, '@' + self.bot.user.display_name)
        command = self.invoked_subcommand if self.invoked_subcommand else self.command
        em = discord.Embed(color=self.bot.error_color)
        em.title = "Missing required argument ❌"
        em.description = f"{prefix}{command.qualified_name} {command_signature(command)}\n{command.description}"
        await channel.send(embed=em)

    async def send_error(self, content):
        channel = self.channel
        em = discord.Embed(color=self.bot.error_color, title="Error ❌")
        em.description = str(content)
        await channel.send(embed=em)

    async def bad_argument(self, content):
        channel = self.channel
        em = discord.Embed(color=self.bot.error_color, title="Invalid argument ❌")
        em.description = str(content)
        await channel.send(embed=em)
