# -*- coding: utf-8 -*-

"""Место для настроек, которые нельзя записать в .ini"""

from app.settings.config_control import *
from os.path import split, dirname, abspath, join
from os import chdir

HOME_DIR = split(dirname(abspath(__file__)))[0]
SETTINGS_DIR = join(HOME_DIR, "settings")
SETTINGS_FILE = "settings.ini"
EXAMPLE_SETTINGS_FILE = f"example_{SETTINGS_FILE}"

SETTINGS_FILE = join(HOME_DIR, SETTINGS_DIR, SETTINGS_FILE)
EXAMPLE_SETTINGS_FILE = join(HOME_DIR, SETTINGS_DIR, EXAMPLE_SETTINGS_FILE)
print(SETTINGS_FILE, EXAMPLE_SETTINGS_FILE)
cfg = create_cfg(SETTINGS_FILE, EXAMPLE_SETTINGS_FILE)
DB_PATH = join(HOME_DIR, "db", cfg.get('db', "name"))

if __name__ == '__main__':
    chdir(HOME_DIR)