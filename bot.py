import logging
import sys

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import AutoShardedBot as DiscordBot

from config import config
from utils.ctx import Context


def get_banner():
    banner = open("utils/assets/banner.txt")
    return banner.read()


class Bot(DiscordBot):
    async def get_context(self, message, *, cls=Context):
        return await super().get_context(message, cls=cls)

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        logging.info("Cleaning up and logging out...")
        await super().close()
        await self.session.close()

    def __init__(self):
        super().__init__(
            intents=config.intents,
            command_prefix=commands.when_mentioned

        )

        # Argument Handling
        self.session = None
        self.debug: bool = any("debug" in arg.lower() for arg in sys.argv)

        # Commands/extensions
        self.initial_extensions = [
            "modules.events.ready"
        ]

        # Logging
        discord_log = logging.getLogger("discord")
        discord_log.setLevel(logging.CRITICAL if not self.debug else logging.INFO)
        self.log: logging.Logger = logging.getLogger("bot")
        self.log.info(f"\n{get_banner()}\nLoading....")

        # Config
        self.config = config
        self.version = {
            "bot": config.version,
            "python": sys.version.split(" ")[0],
            "discord.py": discord.__version__
        }
