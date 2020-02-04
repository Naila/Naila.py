from asyncio import tasks
from discord.ext import commands
import os

__author__ = "Kanin"
__date__ = "02/03/2020"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"


class Heartbeat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session
        self.heartbeat.start()

    def cog_unload(self):
        self.heartbeat.stop()

    @tasks.loop(minutes=1)
    async def heartbeat(self):
        try:
            self.bot.log.info("[UptimeRobot HeartBeat] - Sending heartbeat Request")
            req = await self.session.get(os.getenv("UPTIMEROBOT_URL"))
            response = await req.json()
            self.bot.log.info(f"[UptimeRobot Heartbeat] - UptimeRobot says: {response['msg']}")
        except Exception as e:
            self.bot.sentry.capture_exception(e)

    @heartbeat.before_loop
    async def before_update_loop(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Heartbeat(bot))
