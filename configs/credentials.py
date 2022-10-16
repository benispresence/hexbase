import configparser

PATH_CONFIG = '/Users/benjaminharmat/global_config.ini'


def get_config():
    config = configparser.ConfigParser()
    config.read(PATH_CONFIG)
    return config
