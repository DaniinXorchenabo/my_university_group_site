# -*- coding: utf-8 -*-

"""
    Место для настроек, которые нельзя записать в .ini

    Этот файл должен быть импортирован (со *) в любой другой файл проекта
    Сам по себе файл запускаться не должен
"""

from os.path import split, dirname, abspath, join
from pathlib import Path
from os import chdir

from app.settings.config_control import create_cfg


SETTINGS_DIR = 'settings'
SETTINGS_FILE = 'settings.ini'

HOME_DIR = split(dirname(abspath(__file__)))[0]

SETTINGS_DIR = join(HOME_DIR, SETTINGS_DIR)
EXAMPLE_SETTINGS_FILE = f"example_{SETTINGS_FILE}"
SETTINGS_FILE = join(HOME_DIR, SETTINGS_DIR, SETTINGS_FILE)
EXAMPLE_SETTINGS_FILE = join(HOME_DIR, SETTINGS_DIR, EXAMPLE_SETTINGS_FILE)

cfg = create_cfg(SETTINGS_FILE, EXAMPLE_SETTINGS_FILE)

AUTO_PYDANTIC_MODELS = Path(HOME_DIR, cfg.get('paths', 'auto_pydantic_models'))
DB_PATH = Path(HOME_DIR, cfg.get('paths', "db_path"), cfg.get('db', "name"))
MIGRATIONS_DIR = Path(HOME_DIR, cfg.get('paths', "migration_dir"))
TEST_DB = Path(HOME_DIR, cfg.get('paths', "test_db"), cfg.get('db', "test_db_name"))
DB_BACKUPS = Path(HOME_DIR, cfg.get('paths', "db_backups"))

if __name__ == '__main__':
    chdir(HOME_DIR)
