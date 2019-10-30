import discord
from discord.ext import commands
from rethinkdb import r

from modules.Cogs.Help import command_signature


class CustomContext(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session(self):
        return self.bot.session

    async def guildcolor(self, gid: str):
        color = await r.table("guilds").get(gid).get_field("color").run(self.bot.conn)
        return color

    async def missing_argument(self):
        channel = self.channel
        prefix = self.prefix.replace(self.bot.user.mention, '@' + self.bot.user.display_name)
        command = self.invoked_subcommand if self.invoked_subcommand else self.command
        em = discord.Embed(color=discord.Color.red())
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

    async def group_help(self):
        message = self.message
        prefix = await self.bot.get_prefix(message)
        message.content = f"{prefix}help {self.command.name}"
        await self.bot.invoke(await self.bot.get_context(message, cls=CustomContext))
