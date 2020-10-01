import json
import os
import re
from datetime import datetime

import discord
from discord.ext import commands


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        ws = json.loads(self.bot._connection._get_websocket(shard_id=0)._trace[0])
        self.bot.gateway_server_name = ws[0]
        self.bot.session_server_name = ws[1]["calls"][0]

    @commands.Cog.listener()
    async def on_resumed(self):
        ws = json.loads(self.bot._connection._get_websocket(shard_id=0)._trace[0])
        self.bot.gateway_server_name = ws[0]
        self.bot.session_server_name = ws[1]["calls"][0]

    @commands.Cog.listener()
    async def on_ready(self):
        ws = json.loads(self.bot._connection._get_websocket(shard_id=0)._trace[0])
        self.bot.gateway_server_name = ws[0]
        self.bot.session_server_name = ws[1]["calls"][0]

        info = f"\n**Connected** ⚡\n" \
               f"**Gateway server:** {self.bot.gateway_server_name}\n" \
               f"**Session server:** {self.bot.session_server_name}\n" \
               f"\n**Logged in** 📡\n" \
               f"**User:** {self.bot.user} ({self.bot.user.id})\n" \
               f"**Avatar:** {self.bot.user.avatar_url_as(static_format='png', size=512)}\n" \
               f"\n**Information** ℹ\n" \
               f"**Bot version:** {self.bot.version['bot']}\n" \
               f"**Lib version:** {self.bot.version['discord.py']}\n" \
               f"**Python version:** {self.bot.version['python']}"
        self.bot.log.info(re.sub("\*", "", info))
        await self.bot.change_presence(
            activity=discord.Game(
                name="n!help | discord.gg/WXGHfHH | Mid rewrite.. please be patient",
                type=discord.ActivityType.playing
            ),
            status=discord.Status.online
        )
        if len(self.bot.cogs) == 1:
            self.starter_modules()
        webhook = discord.Webhook.from_url(os.getenv("READY"), adapter=discord.AsyncWebhookAdapter(self.bot.session))
        em = discord.Embed(description=info, color=self.bot.color)
        em.set_author(name=f'{self.bot.user.name} Ready')
        em.timestamp = datetime.utcnow()
        await webhook.send(embed=em, username="Ready", avatar_url=self.bot.user.avatar_url)
        self.bot.log.info("Logged in and ready!")

    async def on_shard_ready(self, shard_id: int):
        ws = json.loads(self.bot._connection._get_websocket(shard_id=shard_id)._trace[0])

        em = discord.Embed(color=self.bot.color)
        em.description = f"**Gateway server:** {ws[0]}\n**Session server:** {ws[1]['calls'][0]}"
        em.set_author(name=f"Shard {shard_id}/{self.bot.shard_count - 1} ready")
        webhook = discord.Webhook.from_url(os.getenv("READY"), adapter=discord.AsyncWebhookAdapter(self.bot.session))
        await webhook.send(embed=em, username="Shard ready/restarted", avatar_url=self.bot.user.avatar_url)

    def starter_modules(self):
        paths = ["modules/Events", "modules/Cogs"]
        blacklist = ["modules/Events/Ready", "modules/Cogs/Music", "modules/Cogs/MusicRewrite"]
        if self.bot.debug:
            blacklist.append("modules/Events/Loops")
        for path in paths:
            loaded, failed = 0, 0
            name = path.split("/")[-1]
            for file in os.listdir(path):
                try:
                    if file.endswith(".py"):
                        to_load = f"{path}/{file[:-3]}"
                        if to_load not in blacklist:
                            self.bot.load_extension(to_load.replace("/", "."))
                            loaded += 1
                except Exception as e:
                    failed += 1
                    self.bot.log.error(f"Failed to load {path}/{file}: {repr(e)}")
            message = f"Loaded {loaded} {name}"
            if failed > 0:
                message += f" | Failed to load {failed} {name}"
            self.bot.log.info(message)


def setup(bot):
    bot.add_cog(Ready(bot))
