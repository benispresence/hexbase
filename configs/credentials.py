import configparser

PATH_CONFIG = '~/global_config.ini'


def get_config():
    """
    :return: credentials from global_config.ini
    """
    config = configparser.ConfigParser()
    config.read(PATH_CONFIG)
    return config
