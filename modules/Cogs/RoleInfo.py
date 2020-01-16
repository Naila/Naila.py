from discord.ext import commands

__author__ = "Kanin"
__date__ = "11/22/2019"
__copyright__ = "Copyright 2019, Naila"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"


class RoleInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(RoleInfo(bot))
