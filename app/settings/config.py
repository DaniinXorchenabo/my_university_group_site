# -*- coding: utf-8 -*-

"""Место для настроек, которые нельзя записать в .ini"""

from os.path import split, dirname, abspath, join
from os import chdir

from app.settings.config_control import *


HOME_DIR = split(dirname(abspath(__file__)))[0]
SETTINGS_DIR = join(HOME_DIR, "settings")
SETTINGS_FILE = "settings.ini"
EXAMPLE_SETTINGS_FILE = f"example_{SETTINGS_FILE}"

SETTINGS_FILE = join(HOME_DIR, SETTINGS_DIR, SETTINGS_FILE)
EXAMPLE_SETTINGS_FILE = join(HOME_DIR, SETTINGS_DIR, EXAMPLE_SETTINGS_FILE)
print(SETTINGS_FILE, EXAMPLE_SETTINGS_FILE)
cfg = create_cfg(SETTINGS_FILE, EXAMPLE_SETTINGS_FILE)
DB_PATH = join(HOME_DIR, "db", cfg.get('db', "name"))
MIGRATIONS_DIR = join(HOME_DIR, "db", 'migrations')
TEST_DB = join(HOME_DIR, "db", "tests", "test_" + cfg.get('db', "name"))
DB_BACKUPS = join(HOME_DIR, "db", "backups")

weekdays_num = {1: "Понидельник",
                2: "Вторник",
                3: "Среда",
                4: "Четверг",
                5: "Пятница",
                6: "Суббота",
                7: "Воскресенье"}

weekdays = {val: key for key, val in weekdays_num.items()}

if __name__ == '__main__':
    chdir(HOME_DIR)
