from discord.ext import commands

from utils.functions.text import readable_list


class BotMissingPermissions(commands.CheckFailure):
    def __init__(self, missing_perms, *args):
        # from utils.ctx import CustomContext
        # _ = CustomContext.translator
        self.missing_perms = missing_perms

        # missing = [_("permissions", perm) for perm in missing_perms]
        missing = [perm.replace("guild", "server").title() for perm in missing_perms]

        permissions = readable_list(missing)
        # message = _("errors", "bot_missing_perms", permissions=permissions)
        message = f"I need the `{permissions}` permissions for this command to work!"
        super().__init__(message, *args)


class UserMissingPermissions(BotMissingPermissions):
    pass


class TranslationError(Exception):
    def __init__(self, error):
        self.error = error
        super().__init__(error)


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
