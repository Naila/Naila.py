import asyncio
import logging
import os
import sys

import aiohttp
import asyncpg
import discord
from discord.ext import commands
from discord.ext.commands import AutoShardedBot as DiscordBot
# from utils.Database import async_session

from config import config
from utils.ctx import Context


def get_banner():
    banner = open("utils/assets/banner.txt")
    return banner.read()


class Bot(DiscordBot):
    async def get_context(self, message, *, cls=Context):
        return await super().get_context(message, cls=cls)

    async def setup_hook(self):
        # self.background_task.start()
        self.session = aiohttp.ClientSession()
        credentials = {
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASS"),
            "database": os.getenv("POSTGRES_DATABASE"),
            "host": os.getenv("POSTGRES_HOST", "127.0.0.1"),
            "port": os.getenv("POSTGRES_PORT", "5432")
            # "init": init_connection
        }
        self.pool: asyncpg.Pool = await asyncpg.create_pool(**credentials)
        self.log.info(
            f"Postgres connected to database ({self.pool._working_params.database})"
            f" under the ({self.pool._working_params.user}) user"
        )
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
        self.pool = None
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
