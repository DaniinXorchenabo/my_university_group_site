# -*- coding: utf-8 -*-

"""Функции, нужные для тестирования БД"""

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
        Group(name='20ВП1')
        commit()

    except Exception as e:
        print('произошла ошибка при заполнении БД', e)
        print('похоже, что БД уже содержит данное заполнение')
        return

    gr = Group['20ВП1']
    User(name='Петя', id=100, password="123", groups=gr, login='Петя1')
    User(name='Вася', id=101, password="123", groups=gr, login='Вася1')
    User(name='Ваня', id=102, password="123", groups=gr, login='Ваня')
    User(name='Вася Админ', id=103, password="123", groups=gr, login='Вася2')
    User(name='Вася Староста', id=104, password="123", groups=gr, login='Вася3')
    User(name='Настя', id=105, password="123", groups=gr, login='Настя1')
    User(name='Наташа', id=106, password="123", groups=gr, login='Наташа1')
    User(name='Алиса', id=107, password="123", groups=gr, login='Алиса1')
    commit()

    admin = User[103]
    Admin(user=admin)

    commit()
    User[104].is_verificated = True
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
    Reminder(dustbining_chat=DustbiningChat[30000001], title="С днем рождения, дорогая А.",
             text='Желаем тебе от всей души всего-всего-всего!, твоя группа!', reminder_time="2020-11-15 00:00:00")

    SeniorInTheGroup(group=gr, user=User[104])
    chat = ImportantChat[30000001]
    ImportantMessage(important_chat=chat, text='всем срочно пройти опрос!')
    ImportantMessage(important_chat=chat, text='всем прочитать этот документ!')
    PPO = Subject[gr, "ППО"]
    SIT = Subject[gr, "СИТ"]
    PROGA = Subject[gr, "Прога"]
    Queue(group=gr, name='очередь на 11 лабу по ППО', subject=PPO)
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
    ppo_queue = Queue.get(group=gr, name='очередь на 11 лабу по ППО', subject=PPO)
    UserHasQueue(queue=ppo_queue, user=User[104], number=1)
    UserHasQueue(queue=ppo_queue, user=User[103], number=2)
    UserHasQueue(queue=ppo_queue, user=User[102], number=3)

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
    connect_with_db()
