import yaml


def get_banner():
    banner = open("res/banner.txt")
    return banner.read()


def get_config():
    with open("config/config.yml", "r") as config:
        return yaml.safe_load(config)
