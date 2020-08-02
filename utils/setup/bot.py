import datetime
import json
import logging
import os
import sys
from collections.__init__ import Counter

import aiohttp
import asyncpg
import discord
import psutil
import sentry_sdk as sentry
import spotipy
# from ksoftapi.client import Client as KClient
from spotipy.oauth2 import SpotifyClientCredentials

from utils.config.config import get_banner, get_config

__author__ = "Kanin"
__date__ = "07/10/2020"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"


def init_sentry(bot):
    sentry.init(
        os.getenv("SENTRY_URL"),
        attach_stacktrace=True,
        max_breadcrumbs=50,
        environment="Development" if bot.debug else "Production"
    )


async def init_connection(conn):
    await conn.set_type_codec(
        'json',
        encoder=json.dumps,
        decoder=json.loads,
        schema='pg_catalog'
    )


def setup_bot(bot):
    # Argument Handling
    bot.debug = any("debug" in arg.lower() for arg in sys.argv)

    # Logging
    init_sentry(bot)
    bot.sentry = sentry
    discord_log = logging.getLogger("discord")
    discord_log.setLevel(logging.CRITICAL if not bot.debug else logging.INFO)
    log = logging.getLogger("bot")
    bot.log = log
    log.info(f"\n{get_banner()}\nLoading....")

    # Load modules
    bot.session = aiohttp.ClientSession(loop=bot.loop)
    bot.load_extension("modules.Events.Ready")

    # Database
    credentials = {
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASS"),
        "database": os.getenv("POSTGRES_DATABASE"),
        "host": os.getenv("POSTGRES_HOST"),
        "init": init_connection
    }
    bot.pool = bot.loop.run_until_complete(asyncpg.create_pool(**credentials))
    bot.log.info(f"Postgres connected to database ({bot.pool._working_params.database})"
                 f" under the ({bot.pool._working_params.user}) user")

    # Config
    bot.config = get_config
    # bot.kclient = KClient(api_key=os.getenv("KSOFT"))
    bot.spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=os.getenv("SPOTIFY_ID"),
            client_secret=os.getenv("SPOTIFY_SECRET")
        )
    )
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
