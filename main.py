import asyncio
import atexit
import os
import sys
from os.path import join, dirname

import discord
from discord.ext.commands import AutoShardedBot as DiscordBot
from dotenv import load_dotenv

from utils.Database.Prefix import get_prefixes
from utils.config.setup_bot import setup_bot, setup_logger
from utils.ctx import CustomContext

description = "Naila Bot"

test = any("test" in arg.lower() for arg in sys.argv)


class Bot(DiscordBot):
    def __init__(self):
        load_dotenv(join(dirname(__file__), 'env/.env'))
        atexit.register(lambda: asyncio.ensure_future(self.logout()))
        super().__init__(command_prefix=get_prefixes, description=description, case_insensitive=True)
        setup_bot(self)
        try:
            self.loop.run_until_complete(self.start(os.getenv("TOKEN")))
        except discord.errors.LoginFailure or discord.errors.HTTPException as e:
            self.log.error(f"Shit: {repr(e)}", exc_info=False)
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.pool.close())
            self.loop.run_until_complete(self.logout())

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or CustomContext)

    if __name__ != "__main__":
        if not test:
            setup_logger()


if __name__ == "__main__":
    if not test:
        setup_logger()
    Bot()
