# -*- coding: utf-8 -*-

"""Тут Объявляются все сущности БД"""

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.db_base_func import *


db = Database()


class Admin(db.Entity):
    user = PrimaryKey('User')


class User(db.Entity):
    id = PrimaryKey(int)
    name = Optional(str)
    login = Required(str, unique=True)
    password = Optional(str)
    email = Optional(str, unique=True)
    user_has_queues = Set('UserHasQueue')
    session_key_for_app = Optional(str)
    getting_time_session_key = Optional(datetime)
    admin = Optional(Admin)
    login_EIES = Optional(str)
    password_EIES = Optional(str)
    my_verification = Set('NoneVerification', reverse='it_is_i')  # если поле пустое - то я верифицирован, если нет - то у меня нет доступа к информации группы
    i_verificate_thei = Set('NoneVerification', reverse='he_verificate_me')
    # те пользователи, которых я могу верифицировать
    # Это поле может быть не пустым только если я сам верифицирован
    senior_in_the_group = Optional('SeniorInTheGroup')
    curse_count = Optional(int)  # Счетчик мата
    senior_verification = Optional('SeniorVerification')
    groups = Optional('Group')




class DustbiningChat(db.Entity):
    """Флудилка, чат, где будут спрашивать домашку"""
    id = PrimaryKey(int)
    group = Optional('Group')
    reminders = Set('Reminder')


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
    queues = Set('Queue')


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
    name = Required(str)
    queues = Set('Queue')
    teachers = Set('Teacher')
    weekday_and_time_subjects = Set('WeekdayAndTimeSubject')
    PrimaryKey(group, name)


class WeekdayAndTimeSubject(db.Entity):
    """Так как предметы могут повторятся за две недели, то для каждого предмета введена вспомогательная таблица, в которой указываются день, номер недели и время предмета"""
    id = PrimaryKey(int, auto=True)
    subject = Optional(Subject)
    number_week = Required(int)
    weekday = Required(int)  # Номер дня недели, начиная с 1
    time = Optional(time, default="00:00")
    classroom_number = Optional(str)
    e_learning_url = Optional('ELearningUrl')
    update_time = Required(datetime, default=lambda: datetime.now())
    type = Optional(str)  # лекция, практика и т.д.


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
    vk_url = Optional(str)


class SeniorInTheGroup(db.Entity):
    """Это сущность старосты"""
    user = Required(User)
    senior_verifications = Set('SeniorVerification')
    group = Required(Group)
    is_verification = Optional(bool)
    PrimaryKey(user, group)


class News(db.Entity):
    id = PrimaryKey(int, auto=True)
    group = Optional(Group)
    title = Optional(str)
    text = Optional(str)
    files = Optional(Json)


class NoneVerification(db.Entity):
    """представляет из себя не отдельно взятого пользователя, а поле верификации одного полльзователя другим (уже верифицированным пользователем)"""
    it_is_i = Required(User, reverse='my_verification')
    he_verificate_me = Required(User, reverse='i_verificate_thei')  # моя группа, которая должна подтвердить, что я с ними в одной группе
    confirmation = Optional(int, default=0)
    # 0 - пользователь ничего не ответил
    # -1 - ответил отрицательно
    # 1 - ответил положительно
    PrimaryKey(it_is_i, he_verificate_me)


class Queue(db.Entity):
    """Сущность очереди. Реализует механизм кто что и за кем занял"""
    id = PrimaryKey(int, auto=True)
    user_has_queues = Set('UserHasQueue')
    group = Required(Group)
    name = Optional(str)
    subject = Optional(Subject)


class UserHasQueue(db.Entity):
    """Это вспомогательная сущность очереди,  олицетворяет какой пользователь в какой очереди занял какой место. По идее, не должна использоваться вне кода БД"""
    user = Required(User)
    queue = Required(Queue)
    number = Required(int, default="-1")
    id = PrimaryKey(int, auto=True)


class Reminder(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Optional(str, default="Вы просили о чем-то напомнить")
    text = Optional(str, default=" ")
    reminder_time = Required(datetime)
    dustbining_chat = Required(DustbiningChat)


class SeniorVerification(db.Entity):
    """Сущность, нужная для верификации старосты (для каждой пары староста- верифицированный пользователь группы)"""
    senior_in_the_group = Required(SeniorInTheGroup)
    user = PrimaryKey(User)
    confirmation = Required(int, default=0)
    # 0 - пользователь ничего не ответил
    # -1 - ответил отрицательно
    # 1 - ответил положительно


for name, ent in db.entities.items():
    ent.__bases__ = tuple(list(ent.__bases__) + [AddArrtInDbClass])\
        if AddArrtInDbClass not in list(ent.__bases__) else tuple(list(ent.__bases__))


# is_DB_created()

if __name__ == '__main__':
    from app.db.db_control_func import *
    is_DB_created()
    with db_session:
        User[103].is_verificated = True
        print(User[103].is_verificated)
        # User[105].groups = None
        commit()
    from os import chdir

    chdir(HOME_DIR)
    # is_DB_created()

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

    # with db_session():
    #     User.select().show()
