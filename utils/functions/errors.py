from discord.ext import commands


class BotMissingPermissions(commands.CheckFailure):
    def __init__(self, missing_perms, *args):
        self.missing_perms = missing_perms

        missing = [perm.replace("_", " ").replace("guild", "server").title() for perm in missing_perms]

        permissions = f"{', '.join(missing[:-1])}, and {missing[-1]}" if len(missing) > 2 else " and ".join(missing)
        message = f"I need permissions to `{permissions}` for this command to work!"
        super().__init__(message, *args)


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
