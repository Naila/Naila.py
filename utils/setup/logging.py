import logging

import coloredlogs
import yaml

__author__ = "Kanin"
__date__ = "07/10/2020"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "0.0.1"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Development"


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

    file = logging.FileHandler(filename=f"logs/bot.log", encoding="utf-8", mode="w")
    file.setFormatter(logging.Formatter(config["formats"]["file"]))
    logger.addHandler(file)
    return logger
