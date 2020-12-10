# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *


@db_session
def create_test_db_1():
    User(name='Петя', id=100, password="123")
    User(name='Вася', id=101, password="123")
    User(name='Ваня', id=102, password="123")
    User(name='Вася Админ', id=103, password="123")
    User(name='Вася Староста', id=104, password="123")
    commit()
    admin = User[103]
    Admin(user=admin)
    Group(name='20ВП1', users={admin, User[100], User[101], User[102], User[104]})
    commit()
    gr = Group['20ВП1']
    DustbiningChat(id=30000001, groups=gr)
    DustbiningChat(id=30000002, groups=gr)
    ImportantChat(id=30000001, groups=gr)
    Subject(name="ППО", groups=gr)
    Subject(name="СИТ", groups=gr)
    Subject(name="Прога", groups=gr)
    commit()
    SeniorInTheGroup(group=gr, user=User[104])
    chat = ImportantChat[30000001]
    ImportantMessage(important_chat=chat, text='всем срочно пройти опрос!')
    ImportantMessage(important_chat=chat, text='всем прочитать этот документ!')
    PPO = Subject[gr, "ППО"]
    SIT = Subject[gr, "СИТ"]
    PROGA = Subject[gr, "Прога"]
    Teacher(name="Самуйлов", subjects={PPO, PROGA})
    Teacher(name="Такташкин", subjects={SIT})
    Teacher(name="Второй препод по СИТу", subjects={SIT})
    Teacher(name="Гурьянов", subjects={PROGA})
    HomeTask(subjects=PPO)
    HomeTask(subjects=PPO)
    HomeTask(subjects=PROGA)
    commit()

@db_session
def create_users_1():
    pass

if __name__ == '__main__':
    db.bind(provider=cfg.get("db", "type"), filename=join(HOME_DIR, "db", "tests", "test_" + cfg.get('db', "name")), create_db=True)
    db.generate_mapping(create_tables=True)
    create_test_db_1()