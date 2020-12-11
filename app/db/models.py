# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *

db = Database()



class Admin(db.Entity):
    user = PrimaryKey('User')


class User(db.Entity):
    id = PrimaryKey(int)
    senior_in_the_group = Optional('SeniorInTheGroup')
    groups = Optional('Group')
    name = Optional(str)
    password = Optional(str)
    email = Optional(str, unique=True)
    session_key_for_app = Optional(str)
    getting_time_session_key = Optional(datetime)
    admin = Optional(Admin)
    login_EIES = Optional(str)
    password_EIES = Optional(str)
    # verification_status = Required(bool, default='false')
    my_verification = Optional('NoneVerification', reverse='it_is_i')  # если поле пустое - то я верифицирован, если нет - то у меня нет доступа к информации группы
    i_verificate_thei = Set('NoneVerification', reverse='he_verificate_me')
    # те пользователи, которых я могу верифицировать
    # Это поле может быть не пустым только если я сам верифицирован
    curse_count = Optional(int)  # Счетчик мата


class DustbiningChat(db.Entity):
    """Флудилка, чат, где будут спрашивать домашку"""
    id = PrimaryKey(int)
    group = Optional('Group')


class ImportantChat(db.Entity):
    """Основная конфа, куда будут стекаться уведомления"""
    id = PrimaryKey(int)
    important_messages = Set('ImportantMessage')
    group = Set('Group')


class ImportantMessage(db.Entity):
    id = PrimaryKey(int, auto=True)
    important_chat = Optional(ImportantChat)
    text = Optional(str)


class Group(db.Entity):
    senior_in_the_group = Optional('SeniorInTheGroup')
    users = Set(User)
    dustbining_chats = Set(DustbiningChat)
    important_chats = Set(ImportantChat)
    subjects = Set('Subject')
    name = PrimaryKey(str)
    events = Set('Event')
    timesheet_update = Required(datetime, default=lambda: datetime.now())
    news = Set('News')


class HomeTask(db.Entity):
    id = PrimaryKey(int, auto=True)
    subject = Optional('Subject')
    deadline_date = Optional(date)
    deadline_time = Optional(time)
    text = Optional(str)
    files = Optional(Json)


class Subject(db.Entity):
    """Предмет для одной группы"""
    group = Required(Group)
    home_tasks = Set(HomeTask)
    weekday_and_time_subjects = Set('WeekdayAndTimeSubject')
    name = Required(str)
    teachers = Set('Teacher')
    PrimaryKey(group, name)


class WeekdayAndTimeSubject(db.Entity):
    """Так как предметы могут повторятся за две недели, то для каждого предмета введена вспомогательная таблица, в которой указываются день, номер недели и время предмета"""
    subject = Optional(Subject)
    number_week = Required(int)
    weekday = Required(str)
    time = Required(time, default="00:00")
    classroom_number = Optional(str)
    e_learning_url = Optional('ELearningUrl')
    update_time = Required(datetime, default=lambda: datetime.now())
    group_id = Required(int)
    PrimaryKey(number_week, weekday, time, group_id)


class ELearningUrl(db.Entity):
    id = PrimaryKey(int, auto=True)
    weekday_and_time_subject = Optional(WeekdayAndTimeSubject)
    url = Optional(str)
    login = Optional(str)
    password = Optional(str)
    additional_info = Optional(str)


class Event(db.Entity):
    id = PrimaryKey(int, auto=True)
    groups = Set(Group)
    name = Optional(str)
    date = Optional(date)
    time = Optional(time)


class Teacher(db.Entity):
    id = PrimaryKey(int, auto=True)
    subjects = Set(Subject)
    name = Required(str)
    email = Optional(str)
    phone_number = Optional(str)


class SeniorInTheGroup(db.Entity):
    user = Required(User)
    group = Required(Group)
    PrimaryKey(user, group)


class News(db.Entity):
    id = PrimaryKey(int, auto=True)
    group = Optional(Group)
    title = Optional(str)
    text = Optional(str)
    files = Optional(Json)
    some = Optional(str)


class NoneVerification(db.Entity):
    """представляет из себя не отдельно взятого пользователя, а поле верификации одного полльзователя другим (уже верифицированным пользователем)"""
    it_is_i = Required(User, reverse='my_verification')
    he_verificate_me = Required(User, reverse='i_verificate_thei')  # моя группа, которая должна подтвердить, что я с ними в одной группе
    confirmation = Optional(int, default=0)
    # 0 - пользователь ничего не ответил
    # 1 - ответил отрицательно
    # 2 - ответил положительно
    PrimaryKey(it_is_i, he_verificate_me)


def controller_migration_version(db_path=DB_PATH):
    """не работает, не использовать"""
    db.provider = db.schema = None
    db.migrate(
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


def make_migrate_file():
    """не работает, не использовать"""
    db.migrate(command='make',
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


def is_DB_created(db_path=DB_PATH, deep=0):
    from os.path import isfile
    if deep > 5:
        print('в коннекте с базой данных наблюдается большая рекурсия, значит что-то идет не так')
        import sys
        sys.exit()

    if not isfile(db_path):
        db.connect(allow_auto_upgrade=True,
                   create_tables=True,
                   create_db=True,
                   provider=cfg.get("db", "type"),
                   filename=db_path)
        # db.bind(provider=cfg.get("db", "type"), filename=db_path, create_db=True)
        # db.generate_mapping(create_tables=True)
        print('create db')
    else:

        try:
            # db.bind(provider=cfg.get("db", "type"), filename=db_path)
            # db.generate_mapping()
            db.connect(allow_auto_upgrade=True,
                       # create_tables=True,
                       # create_db=True,
                       provider=cfg.get("db", "type"),
                       filename=db_path)
        except Exception as e:
            print('при создании бд произошла какая-то ошибка (видимо, структура БД была изменена)\n', e)
            print('попытка исправить.....')
            try:
                db.connect(allow_auto_upgrade=True,
                           create_tables=True,
                           # create_db=True,
                           provider=cfg.get("db", "type"),
                           filename=db_path)
                print('получилось')
            except Exception as e:
                print("Начинаем миграцию")
                import shutil
                import os
                from os.path import split, join
                import time
                t = time.ctime().split()[1:]
                t[0], t[1], t[2] = t[2], t[1], t[0]
                copy_name = shutil.copy(db_path, DB_BACKUPS)
                new_name = join(split(copy_name)[0], '_'.join(t).replace(":", "-") + "_" + split(db_path)[1])
                os.rename(copy_name, new_name)
                print("создан бекап:", new_name)
                print("Удалена исходная база данных, создаём новую")
                os.remove(db_path)
                # controller_migration_version(db_path)
                print('\n---------------------------\n\nдля создания новой БД перезапустите код.....')
                import sys
                sys.exit()
                # is_DB_created(db_path=db_path, deep=deep + 1)


# is_DB_created()

if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)
    is_DB_created()
    # db.migrate(command='make',
    #            migration_dir=join(HOME_DIR, "db", 'migrations'),
    #            # allow_auto_upgrade=True,
    #            # create_tables=True,
    #            create_db=True,
    #            provider=cfg.get("db", "type"),
    #            filename=":memory:")

    # make_migrate_file()
    # controller_migration_version(TEST_DB)
    # is_DB_created(TEST_DB)
    # DB_PATH = ""
    # db.migrate(command='make',
    #            migration_dir=join(HOME_DIR, "db", 'migrations'),
    #            allow_auto_upgrade=True,
    #            # create_tables=True,
    #            # create_db=True,
    #            provider=cfg.get("db", "type"),
    #            filename=":memory:")  # join(HOME_DIR, "db", "tests", "test_" + cfg.get('db', "name"))
    # controller_migration_version()
    # is_DB_created()
    # db.connect(allow_auto_upgrade=True,
    #             create_tables=True,
    #             create_db=True,
    #            provider=cfg.get("db", "type"),
    #            filename=":memory:")

    with db_session():
        User.select().show()
