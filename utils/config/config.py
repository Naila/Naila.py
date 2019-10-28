import yaml


def get_icon():
    file = open("res/banner.txt")
    return file.read()


def get_config():
    with open("config/config.yml", "r") as config:
        return yaml.safe_load(config)
