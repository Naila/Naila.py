import logging
from logging.handlers import RotatingFileHandler
from os.path import join, dirname

import coloredlogs
import yaml
from dotenv import load_dotenv

from bot import Bot

load_dotenv(join(dirname(__file__), "config/.env"))


def setup_logger():
    logger = logging.getLogger()

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
    return logger


if __name__ == "__main__":
    setup_logger()
    Bot()
