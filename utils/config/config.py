import yaml

__author__ = "Kanin"
__date__ = "11/19/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"


def get_banner():
    banner = open("utils/assets/banner.txt")
    return banner.read()


def get_config():
    with open("config/config.yml", "r") as config:
        return yaml.safe_load(config)
