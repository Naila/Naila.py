from discord.ext import commands, tasks

from utils.APIs.BotLists import BotListSpace, DiscordBots
from utils.database.Reminders import Reminders

__author__ = "Kanin"
__date__ = "01/13/2020"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"


class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ten_second_loop.start()
        self.botlists.start()

    def cog_unload(self):
        self.ten_second_loop.stop()
        self.botlists.stop()

    @tasks.loop(seconds=10)
    async def ten_second_loop(self):
        await Reminders.check(self.bot)

    @tasks.loop(minutes=30)
    async def botlists(self):
        self.bot.log.info(
            f"Posting to all bot lists... | Shards: {self.bot.shard_count} | Guilds: {len(self.bot.guilds)}"
        )
        await BotListSpace().post_bot_stats(self.bot)
        await DiscordBots().post_bot_stats(self.bot)
        self.bot.log.info("Done posting")


def setup(bot):
    bot.add_cog(Loops(bot))
