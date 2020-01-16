from discord.ext import commands

__author__ = "Kanin"
__date__ = "11/22/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"


class TooManyPrefixes(commands.UserInputError):
    pass


class PrefixTooLong(commands.BadArgument):
    pass


class PrefixNotFound(commands.BadArgument):
    pass


class DuplicatePrefix(commands.BadArgument):
    pass


class UsedOnSelf(commands.BadArgument):
    pass


class TooManyUsers(commands.BadArgument):
    pass


class CheckFailure(commands.CheckFailure):
    pass
