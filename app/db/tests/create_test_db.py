# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *


@db_session
def create_test_db_1():
    """создает тестовую БД для того, чтобы можно было поиграться с ней"""
    try:
        User(name='Петя', id=100, password="123")
    except Exception as e:
        print('произошла ошибка при заполнении БД', e)
        print('похоже, что БД уже содержит данное заполнение')
    User(name='Вася', id=101, password="123")
    User(name='Ваня', id=102, password="123")
    User(name='Вася Админ', id=103, password="123")
    User(name='Вася Староста', id=104, password="123")
    commit()
    admin = User[103]
    Admin(user=admin)
    Group(name='20ВП1', users={admin, User[100], User[101], User[102], User[104]})
    # non_verivicared = {User[100], User[101], User[102]}
    # verivicared = {User[104], User[103]}
    NoneVerification(it_is_i=User[100], he_verificate_me=User[104])
    NoneVerification(it_is_i=User[101], he_verificate_me=User[104])
    NoneVerification(it_is_i=User[102], he_verificate_me=User[104])
    commit()
    NoneVerification(it_is_i=User[100], he_verificate_me=User[103])
    NoneVerification(it_is_i=User[101], he_verificate_me=User[103])
    NoneVerification(it_is_i=User[102], he_verificate_me=User[103])
    # [NoneVerification(it_is_i=non_verif_user, he_verificate_me=verificates_user) for non_verif_user in non_verivicared
    #  for verificates_user in verivicared]
    commit()
    gr = Group['20ВП1']
    DustbiningChat(id=30000001, group=gr)
    DustbiningChat(id=30000002, group=gr)
    ImportantChat(id=30000001, group=gr)
    Subject(name="ППО", group=gr)
    Subject(name="СИТ", group=gr)
    Subject(name="Прога", group=gr)
    News(group=gr, title='Мату нет!', text="в беседах мат будет запрещен")
    News(group=gr, title='неужели без дурки?', text="на совещании представителей группы было высказано предложение о запрете мемов про дурку")
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
    HomeTask(subject=PPO)
    HomeTask(subject=PPO)
    HomeTask(subject=PROGA)
    commit()

@db_session
def show_all():
    """Показывает все сущьности все сущности всех БД"""
    [(print('\n', key), val.select().show()) for key, val in db.entities.items()]

if __name__ == '__main__':
    # db.bind(provider=cfg.get("db", "type"), filename=join(HOME_DIR, "db", "tests", "test_" + cfg.get('db', "name")))
    # db.generate_mapping(create_tables=True)
    # make_migrate_file()
    is_DB_created()
    create_test_db_1()
    # with db_session:
    #     NoneVerification(it_is_i=User[102], he_verificate_me=User[103])
    show_all()
    from pprint import pprint
    # pprint(db.entities)