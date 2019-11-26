import json

import discord
from discord.ext import commands


class ReadyHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        self.bot.gateway_server_name = json.loads(self.bot.shards[0].ws._trace[0])[0]
        self.bot.session_server_name = json.loads(self.bot.shards[0].ws._trace[0])[1]["calls"][0]

    @commands.Cog.listener()
    async def on_resumed(self):
        self.bot.gateway_server_name = json.loads(self.bot.shards[0].ws._trace[0])[0]
        self.bot.session_server_name = json.loads(self.bot.shards[0].ws._trace[0])[1]["calls"][0]

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.gateway_server_name = json.loads(self.bot.shards[0].ws._trace[0])[0]
        self.bot.session_server_name = json.loads(self.bot.shards[0].ws._trace[0])[1]["calls"][0]
        info = f"\nConnected ⚡\n" \
               f"Gateway server: {self.bot.gateway_server_name}\n" \
               f"Session server: {self.bot.session_server_name}\n" \
               f"\nLogged in 📡\n" \
               f"User: {self.bot.user} ({self.bot.user.id})\n" \
               f"Avatar: {self.bot.user.avatar_url_as(static_format='png', size=512)}\n" \
               f"\nInformation ℹ\n" \
               f"Bot version: {self.bot.version['bot']}\n" \
               f"Lib version: {self.bot.version['discord.py']}\n" \
               f"Python version: {self.bot.version['python']}"
        self.bot.log.info(info)
        await self.bot.change_presence(
            activity=discord.Game(name="n!help | Mid rewrite.. please be patient", type=discord.ActivityType.playing,
                                  status=discord.Status.dnd))
        self.bot.log.info("Logged in and ready!")


def setup(bot):
    bot.add_cog(ReadyHandler(bot))
