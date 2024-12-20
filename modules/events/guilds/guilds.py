import discord
from discord.ext import commands

from bot import Bot


class Guilds(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.bot.log.info(f"Joined {guild}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self.bot.log.info(f"Left {guild}")
