import asyncio
import logging
import os
import shutil
from logging.handlers import RotatingFileHandler

import coloredlogs
import yaml
from dotenv import load_dotenv
import platform

log = logging.getLogger("bot")


def validate_config():
    env_exists = True
    if not os.path.exists("config/.env"):
        env_exists = False
        shutil.copy("config/.env.example", "config/.env")
        log.info("Copied config/.env.example to config/.env")

    if not os.path.exists("config/config.py"):
        shutil.copy("config/config.example.py", "config/config.py")
        log.info("Copied config/config.example.py to config/config.py")

    if not os.path.exists("config/emojis.yml"):
        shutil.copy("config/emojis.example.yml", "config/emojis.yml")
        log.info("Copied config/emojis.example.yml to config/emojis.yml")

    if not os.path.exists("utils/assets/banner.txt"):
        shutil.copy("utils/assets/banner.example.txt", "utils/assets/banner.txt")
        log.info("Moved utils/assets/banner.example.txt to utils/assets/banner.txt")
    return env_exists


def setup_logger():
    logger = logging.getLogger()

    created = []
    if not os.path.exists("config/logging.yml"):
        shutil.copy("config/logging.example.yml", "config/logging.yml")
        created.append("config/logging.yml")

    if not os.path.exists("logs/bot.log"):
        if not os.path.exists("logs"):
            os.mkdir("logs")
        open("logs/bot.log", "x")
        created.append("logs/bot.log")

    with open("config/logging.yml", "r") as log_config:
        config = yaml.safe_load(log_config)

    coloredlogs.install(
        level="INFO",
        logger=logger,
        fmt=config["formats"]["console"],
        datefmt=config["formats"]["datetime"],
        level_styles=config["levels"],
        field_styles=config["fields"],
        milliseconds=True
    )

    max_bytes = int(config["file"]["max_MiB"]) * 1024 * 1024
    file = RotatingFileHandler(
        filename=f"logs/bot.log",
        encoding="utf-8",
        maxBytes=max_bytes,
        backupCount=int(config["file"]["backup_count"])
    )
    file.setFormatter(logging.Formatter(config["formats"]["file"]))
    file.setLevel(logging.WARNING)
    logger.addHandler(file)

    msg = "Successfully setup the logger"
    if created:
        msg = "Created " + ", ".join(created) + " and " + msg
    log.info(msg)
    return logger


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    setup_logger()
    ready = validate_config()
    if not ready:
        log.error("Please fill out config/.env before starting the bot")
        exit(1)
    load_dotenv(os.path.join(os.path.dirname(__file__), "config/.env"))
    if not os.getenv("TOKEN"):
        log.error("Please fill out config/.env before starting the bot")
        exit(1)

    from bot import Bot
    bot = Bot()
    try:
        bot.run(os.getenv("TOKEN"), log_handler=None)
    except Exception as e:
        log.error(e)
