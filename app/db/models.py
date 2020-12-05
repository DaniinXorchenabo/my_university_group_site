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


class DustbiningChat(db.Entity):
    """Флудилка, чат, где будут спрашивать домашку"""
    id = PrimaryKey(int)
    groups = Optional('Group')


class ImportantChat(db.Entity):
    """Основная конфа, куда будут стекаться уведомления"""
    id = PrimaryKey(int)
    important_messages = Set('ImportantMessage')
    groups = Set('Group')


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


class HomeTask(db.Entity):
    id = PrimaryKey(int, auto=True)
    subjects = Optional('Subject')
    deadline_date = Optional(date)
    deadline_time = Optional(time)


class Subject(db.Entity):
    """Предмет для одной группы"""
    groups = Required(Group)
    home_tasks = Set(HomeTask)
    weekday_and_time_subjects = Set('WeekdayAndTimeSubject')
    name = Required(str)
    teachers = Set('Teacher')
    PrimaryKey(groups, name)


class WeekdayAndTimeSubject(db.Entity):
    """Так как предметы могут повторятся за две недели, то для каждого предмета введена вспомогательная таблица, в которой указываются день, номер недели и время предмета"""
    subject = Optional(Subject)
    id_group = Required(str)
    number_week = Required(int)
    weekday = Required(str)
    time = Required(time)
    classroom_number = Optional(str)
    e_learning_url = Optional('ELearningUrl')
    update_time = Required(datetime, default=lambda: datetime.now())
    PrimaryKey(id_group, number_week, weekday, time)


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



def is_DB_created():
    from os.path import isfile
    if not isfile(DB_PATH):
        db.bind(provider=cfg.get("db", "type"), filename=DB_PATH, create_db=True)
        db.generate_mapping(create_tables=True)
        print('create db')
    else:
        db.bind(provider=cfg.get("db", "type"), filename=DB_PATH)
        try:
            db.generate_mapping()
        except Exception as e:
            print('при создании бд произошла какая-то ошибка (видимо, структура БД была изменена)\n', e)
            print('попытка исправить.....')
            db.generate_mapping(create_tables=True)


# is_DB_created()

if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)

# string = input()
# arr = [string[i:i+2] for i in range(len(string)-1)]
# print({i: string.count(i) for i in arr})
# print((lambda word: ''.join([i.upper() if i.isalpha() and ind > 0 and (ind > 2 and word[ind-1] == ' ' and word[ind-2] == '.' or word[ind-1] == '.') else i for ind, i in enumerate(list(word))]))(' '.join(input().split())))