"""
@author: ravi
"""
import configparser
from os import path
import time

config = None
last_fallback_path = path.dirname(path.dirname(path.realpath(__file__))) + '/appconfig.ini'


def get_config():
    global config
    config_paths = ['/etc/config/stockit/appconfig.ini', '/stockit/config/appconfig.ini', last_fallback_path]
    config = configparser.ConfigParser()
    config_file_found = False
    for file_path in config_paths:
        if path.isfile(file_path):
            config.read(file_path)
            config_file_found = True
            break
    if not config_file_found:
        raise Exception("Config file should be present at one of the locations {}".format(config_paths))


get_config()


class Methods(object):
    """
    Place to store generic methods/utilities
    """
    @staticmethod
    def is_file_older_than_x_days(file, days=1):
        if days < 1:
            raise Exception("Invalid days {}".format(days))
        file_time = path.getmtime(file)
        # Check against 24 hours
        return (time.time() - file_time) > 3600 * 24 * days
