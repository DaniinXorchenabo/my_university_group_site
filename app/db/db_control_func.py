# -*- coding: utf-8 -*-

"""Функции для контроля, соединения, миграции БД"""

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *


def controller_migration_version(db_path=DB_PATH, db_l=db):
    """не работает, не использовать"""
    db_l.provider = db_l.schema = None
    db_l.migrate(
        # command='apply --fake-initial',
        migration_dir=MIGRATIONS_DIR,
        allow_auto_upgrade=True,
        # create_tables=True,
        # create_db=True,
        provider=cfg.get("db", "type"),
        filename=db_path)
    print('миграция прошла успешно')
    print('перезапустите программу для дальнейшего использования')
    import sys
    sys.exit()
    # from os.path import isfile
    # version = None
    # if not isfile(join(MIGRATIOMS_DIR, 'controller.txt')):
    #     version = 1
    # else:
    #     with open(join(MIGRATIOMS_DIR, 'controller.txt'), 'r', encoding='utf-8') as f:
    #         version = int(f.read().split()[0])


def make_migrate_file(db_l=db):
    """не работает, не использовать"""
    db_l.migrate(command='make',
                 migration_dir=MIGRATIONS_DIR,
                 # allow_auto_upgrade=True,
                 # create_tables=True,
                 create_db=True,
                 provider=cfg.get("db", "type"),
                 filename=":memory:")
    print('файл миграции создан, осуществляю выход из системы')
    print('чтобы применить миграцию, используйте controller_migration_version()')
    print("""Для этого вам также будет необходимо использовать аргумент командной строки
     apply --fake-initial при запуске кода""")
    import sys
    sys.exit()


def connect_with_db(db_path=DB_PATH, deep=0, db_l=db):
    """
    Создает соединение с БД для Pony ORM версии 0.8
    :param db_path: путь к БД
    :param deep: глубина рекурсии
    :param db_l: объект БД
    :return:
    """
    from os.path import isfile, split, join
    from os import remove, rename
    from sys import exit
    from time import ctime
    from shutil import copy as shutil_copy

    if deep > 5:
        print('в коннекте с базой данных наблюдается большая рекурсия, значит что-то идет не так')
        exit()

    if not isfile(db_path):
        db_l.connect(allow_auto_upgrade=True,
                     create_tables=True,
                     create_db=True,
                     provider=cfg.get("db", "type"),
                     filename=db_path)
        print('create db')
    else:

        try:
            db_l.connect(allow_auto_upgrade=True,
                         provider=cfg.get("db", "type"),
                         filename=db_path)
        except Exception as e:
            print('при создании бд произошла какая-то ошибка (видимо, структура БД была изменена)\n', e)
            print('попытка исправить.....')
            try:
                db_l.connect(allow_auto_upgrade=True,
                             create_tables=True,
                             # create_db=True,
                             provider=cfg.get("db", "type"),
                             filename=db_path)
                print('получилось')
            except Exception as e:
                print("Начинаем миграцию")
                t = ctime().split()[1:]
                t[0], t[1], t[2] = t[2], t[1], t[0]
                copy_name = shutil_copy(db_path, DB_BACKUPS)
                new_name = join(split(copy_name)[0], '_'.join(t).replace(":", "-") + "_" + split(db_path)[1])
                rename(copy_name, new_name)
                print("создан бекап:", new_name)
                print("Удалена исходная база данных, создаём новую")
                remove(db_path)
                # controller_migration_version(db_path)
                print('\n=========================================\n\n\t\tдля создания новой БД перезапустите код.....')
                print('\n=========================================')
                exit()
                # connect_with_db(db_path=db_path, deep=deep + 1)


is_DB_created = connect_with_db


def old_connect_with_db(db_path=DB_PATH, deep=0, db_l=db):
    """
    Создает соединение с БД для Pony ORM версии 0.73
    :param db_path: путь к БД
    :param deep: глубина рекурсии
    :param db_l: объект БД
    :return:
    """
    from os.path import isfile, split, join
    from os import remove, rename
    from sys import exit
    from time import ctime
    from shutil import copy as shutil_copy

    if deep > 5:
        print('в коннекте с базой данных наблюдается большая рекурсия, значит что-то идет не так')
        exit()

    if not isfile(db_path):
        db.bind(provider=cfg.get("db", "type"), filename=db_path, create_db=True)
        db.generate_mapping(create_tables=True)
        print('create db')
    else:

        try:
            db.bind(provider=cfg.get("db", "type"), filename=db_path)
            db.generate_mapping()
        except Exception as e:
            print('при создании бд произошла какая-то ошибка (видимо, структура БД была изменена)\n', e)
            print('попытка исправить.....')
            try:
                db.bind(provider=cfg.get("db", "type"), filename=db_path, create_tables=True,)
                db.generate_mapping()
                print('получилось')
            except Exception as e:
                print("Создаём бекап а затем удаляем БД")
                t = ctime().split()[1:]
                t[0], t[1], t[2] = t[2], t[1], t[0]
                copy_name = shutil_copy(db_path, DB_BACKUPS)
                new_name = join(split(copy_name)[0], '_'.join(t).replace(":", "-") + "_" + split(db_path)[1])
                rename(copy_name, new_name)
                print("создан бекап:", new_name)
                print("Удалена исходная база данных, создаём новую")
                remove(db_path)
                print('\n=========================================\n\n\t\tдля создания новой БД перезапустите код.....')
                print('\n=========================================')
                exit()


if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)
    is_DB_created()
