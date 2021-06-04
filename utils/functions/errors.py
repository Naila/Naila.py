from discord.ext.commands import CheckFailure, UserInputError, BadArgument

from utils.functions.text import readable_list


class BotMissingPermissions(CheckFailure):
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


class TooManyPrefixes(UserInputError):
    pass


class PrefixTooLong(BadArgument):
    pass


class PrefixNotFound(BadArgument):
    pass


class DuplicatePrefix(BadArgument):
    pass


class UsedOnSelf(BadArgument):
    pass
