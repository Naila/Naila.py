import asyncio
import atexit
import os
from os.path import join, dirname

import discord
from discord.utils import oauth_url
from discord.ext.commands import AutoShardedBot as DiscordBot
from dotenv import load_dotenv

from utils.database.GuildSettings import Prefixes
from utils import setup
from utils.ctx import CustomContext
from config import config

__author__ = "Kanin"
__date__ = "11/19/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"

load_dotenv(join(dirname(__file__), "config/.env"))

description = f"**Support server**: {config.support_invite}\n" \
              f"**Bot invite**:" \
              f" [Recommended perms]({oauth_url(config.client_id, permissions=config.permissions)}) |" \
              f" [No perms]({oauth_url(config.client_id)})"


class Bot(DiscordBot):
    def __init__(self):
        atexit.register(lambda: asyncio.ensure_future(self.logout()))
        super().__init__(
            command_prefix=Prefixes.get,
            description=description,
            case_insensitive=True,
            activity=discord.Game(
                name="Booting...",
                type=discord.ActivityType.playing
            ),
            status=discord.Status.dnd
        )
        setup.bot(self)
        try:
            self.loop.run_until_complete(self.start(os.getenv("TOKEN")))
        except (discord.errors.LoginFailure, discord.errors.HTTPException) as e:
            self.log.error(f"Shit: {repr(e)}", exc_info=False)
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.pool.close())
            self.loop.run_until_complete(self.logout())

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or CustomContext)

    if __name__ != "__main__":
        setup.logger()


if __name__ == "__main__":
    setup.logger()
    Bot()
