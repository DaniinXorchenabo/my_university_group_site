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
    News(group=gr, title='неужели без дурки?',
         text="на совещании представителей группы было высказано предложение о запрете мемов про дурку")
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
    HomeTask(subject=PPO, deadline_date="2020-11-15", deadline_time="12:00:00", text='сдать 10 лабу')
    HomeTask(subject=PPO, deadline_date="2020-11-15", deadline_time="12:30:00", text='срочно сдать 10 лабу!')
    HomeTask(subject=PPO, deadline_date="2020-11-15", text='показать конспект лекций')
    HomeTask(subject=PPO, text='сделать хоть что-нибудь')
    HomeTask(subject=PROGA, deadline_date="2020-12-15", text="починить интернет Гурьянову")
    HomeTask(subject=PROGA, text="сдать работу по динамическим стрктурам")
    [WeekdayAndTimeSubject(subject=PROGA, number_week=i, weekday=j, type=k, time=t) for i in range(1, 3) for j, [k, t]
     in
     {1: ["лекция", '11:40'], 4: ["консультация", '17:00'],
      6: ["практика", '9:50']}.items()]
    a = WeekdayAndTimeSubject(subject=PPO, number_week=1, weekday=6, type="лекция", time="15:35")
    a1 = WeekdayAndTimeSubject(subject=PPO, number_week=2, weekday=6, type="практика", time="11:40",
                               update_time="2020-11-15 00:00:00")  #
    a2 = [WeekdayAndTimeSubject(subject=PPO, number_week=i, weekday=4, type="консультация", time="15:35") for i
          in range(1, 3)]
    commit()
    print(a1.update_time)
    ELearningUrl(url="https://us05web.zoom.us/j/86213813841?pwd=eXVPZjhoajNsUW9HemlkWER2ZG16Zz09#success",
                 login='86 213 813 841', password='0wFSjb', weekday_and_time_subject=a)
    ELearningUrl(url="https://us05web.zoom.us/j/82781947757?pwd=S2VKTW9CSmFqbHIwdkJNTXpFaWhFdz09#success",
                 login='82 781 947 757', password='8ezXfd', weekday_and_time_subject=a1)
    [ELearningUrl(url="https://us05web.zoom.us/j/88911176462?pwd=ZDU0RjI1bnBHWnhOajFXS2xqUDFSdz09#success",
                  login='88 911 176 462', password='5hyAg4', weekday_and_time_subject=i) for i in a2]
    a3 = WeekdayAndTimeSubject.get(subject=PROGA, number_week=1, weekday=1)
    ELearningUrl(url="https://us05web.zoom.us/j/85655737563?pwd=LzFqUlQ1cy9FMlZidDhwY0J3NjFwUT09#success",
                 login='85655737563', password='3TxTxb', weekday_and_time_subject=a3)
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
    # create_test_db_1()
    show_all()
    with db_session:
    #     gr = Group['20ВП1']
        u = User(name='Вася Тестовый-Второй', id=105, password="123")
    #     commit()
    #     NoneVerification[User[106], User[104]].confirmation = 1
        print(User[105].check_verificated)
    #     print(User[106].i_verificate_thei)
    from pprint import pprint
    # pprint(db.entities)
