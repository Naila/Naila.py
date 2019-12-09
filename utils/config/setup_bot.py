import datetime
import logging
import os
import sys
import json
from collections.__init__ import Counter

import aiohttp
import asyncpg
import coloredlogs
import discord
import psutil
import sentry_sdk as sentry
import yaml

from utils.config.config import get_banner, get_config

logger = logging.getLogger()


def init_sentry():
    sentry.init(
        os.getenv("SENTRY_URL"),
        attach_stacktrace=True,
        max_breadcrumbs=50
    )


async def init_connection(conn):
    await conn.set_type_codec(
        'json',
        encoder=json.dumps,
        decoder=json.loads,
        schema='pg_catalog'
    )


def setup_logger():
    with open("config/logging.yml", "r") as log_config:
        config = yaml.safe_load(log_config)

    coloredlogs.install(
        level="INFO",
        logger=logger,
        fmt=config["formats"]["console"],
        datefmt=config["formats"]["datetime"],
        level_styles=config["levels"],
        field_styles=config["fields"]
    )

    file = logging.FileHandler(filename=f"logs/bot.log", encoding="utf-8", mode="w")
    file.setFormatter(logging.Formatter(config["formats"]["file"]))
    logger.addHandler(file)
    return logger


def setup_bot(bot):
    # Argument Handling
    bot.debug = any("debug" in arg.lower() for arg in sys.argv)

    # Logging
    init_sentry()
    bot.sentry = sentry
    discord_log = logging.getLogger("discord")
    discord_log.setLevel(logging.CRITICAL if not bot.debug else logging.INFO)
    log = logging.getLogger("bot")
    bot.log = log
    log.info(f"\n{get_banner()}\nLoading....")

    # Load modules
    bot.session = aiohttp.ClientSession(loop=bot.loop)
    starter_modules(bot)

    # Database
    credentials = {
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASS"],
        "database": os.environ["POSTGRES_DATABASE"],
        "host": os.environ["POSTGRES_HOST"],
        "init": init_connection
    }
    bot.pool = bot.loop.run_until_complete(asyncpg.create_pool(**credentials))
    bot.log.info(f"Postgres connected to database ({bot.pool._working_params.database})"
                 f" under the ({bot.pool._working_params.user}) user")

    # Config
    bot.config = get_config
    bot.uptime = datetime.datetime.utcnow()
    bot.version = {
        "bot": bot.config()["version"],
        "python": sys.version.split(" ")[0],
        "discord.py": discord.__version__
    }
    bot.counter = Counter()
    bot.commands_used = Counter()
    bot.process = psutil.Process()
    bot.color = bot.config()["colors"]["main"]
    bot.error_color = bot.config()["colors"]["error"]


def starter_modules(bot):
    paths = ["modules/Events", "modules/Cogs"]
    for path in paths:
        loaded, failed = 0, 0
        name = path.split('/')[1]
        for file in os.listdir(path):
            try:
                if file.endswith(".py"):
                    bot.load_extension(f"{path.replace('/', '.')}.{file[:-3]}")
                    loaded += 1
            except Exception as e:
                failed += 1
                bot.log.error(f"Failed to load {path}/{file}: {repr(e)}")
        if failed > 0:
            bot.log.info(f"Loaded {loaded} {name} | Failed to load {failed} {name}")
        else:
            bot.log.info(f"Loaded {loaded} {name}")
