import json
import logging
import os
import sys
from collections import Counter
from datetime import datetime

import aiohttp
import asyncpg
from discord import Embed as DefaultEmbed, __version__ as LibVersion, Game, ActivityType, Status
import psutil
import sentry_sdk as sentry
from discord.ext.commands import AutoShardedBot
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from config import config
from utils.ctx import Context
from utils.functions.prefix import Prefixes


def get_banner():
    banner = open("utils/assets/banner.txt")
    return banner.read()


def init_sentry(bot):
    sentry.init(
        os.getenv("SENTRY_URL"),
        integrations=[AioHttpIntegration()],
        attach_stacktrace=True,
        max_breadcrumbs=50,
        environment="Development" if bot.debug else "Production"
    )


async def init_connection(conn):
    await conn.set_type_codec(
        "json",
        encoder=json.dumps,
        decoder=json.loads,
        schema="pg_catalog"
    )


class Bot(AutoShardedBot):
    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or Context)

    class Embed(DefaultEmbed):
        def __init__(self, **kwargs):
            color = kwargs.pop("color", config.colors["main"])
            super().__init__(**kwargs, color=color)

    def __init__(self):
        super().__init__(
            intents=config.intents,
            command_prefix=Prefixes.get,
            description=config.description,
            case_insensitive=True,
            activity=Game(
                name="Booting...",
                type=ActivityType.playing
            ),
            status=Status.dnd
        )

        # Argument Handling
        self.debug: bool = any("debug" in arg.lower() for arg in sys.argv)

        # Logging
        init_sentry(self)
        discord_log = logging.getLogger("discord")
        discord_log.setLevel(logging.CRITICAL if not self.debug else logging.INFO)
        log = logging.getLogger("bot")
        self.log: logging.Logger = log
        log.info(f"\n{get_banner()}\nLoading....")

        # Load modules
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(loop=self.loop)
        self.load_extension("modules.Events.Ready")

        # Database
        credentials = {
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASS"),
            "database": os.getenv("POSTGRES_DATABASE"),
            "host": os.getenv("POSTGRES_HOST"),
            "init": init_connection
        }
        self.pool: asyncpg.Pool = self.loop.run_until_complete(asyncpg.create_pool(**credentials))
        self.log.info(
            f"Postgres connected to database ({self.pool._working_params.database})"
            f" under the ({self.pool._working_params.user}) user"
        )

        # Config
        self.config = config
        self.uptime = datetime.utcnow()
        self.version = {
            "bot": config.bot_version,
            "python": sys.version.split(" ")[0],
            "discord.py": LibVersion
        }
        self.counter: Counter = Counter()
        self.commands_used: Counter = Counter()
        self.process = psutil.Process()
        self.color = config.colors["main"]
        self.error_color = config.colors["error"]

        # Run the bot
        self.run(os.getenv("TOKEN"))
