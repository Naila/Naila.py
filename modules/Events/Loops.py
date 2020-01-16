from discord.ext import commands, tasks

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

    def cog_unload(self):
        self.ten_second_loop.stop()

    @tasks.loop(seconds=10)
    async def ten_second_loop(self):
        if not self.bot.is_ready():
            return
        await Reminders.check(self.bot)


def setup(bot):
    bot.add_cog(Loops(bot))
