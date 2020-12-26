# -*- coding: utf-8 -*-

"""Дополнения к группе"""

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *
from app.db.db_addition.user_addition import *


if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)
    from app.db.models import *


@Group.getter_and_classmethod
def get_subject(self):
    """возвращает сущности всех предметов"""
    """Для всех штук, обладающих декоратором @<Entity>.getter_and_classmethod есть 2 варианта вызова:
    Примеры:
    Group.cl_get_subject(**params)
    и 
    gr = Group.get(**params)
    gr.get_subject
    где params - те параметры (в нашем случае, name='20ВП1'),
    по которым можно найти интересующую группу"""
    return self.subjects.select()[:]


@Group.getter_and_classmethod
def get_subject_name(self):
    """Возвращает названия всех предметов"""
    return self.subjects.select()[:]


@Group.getter_and_classmethod
def get_time_list(self):
    """Возвращает сущности расписания группы"""
    return (i[0] for i in select((j, j.number_week, j.weekday, j.time)
                                 for i in self.subjects for j in i.weekday_and_time_subjects).sort_by(2, 3, 4)[:])


@Group.getter_and_classmethod
def get_time_list_data(self):
    """Возвращает расписания группы в формате"
    [((номер_недели, номер_дня_недели, время, название предмета), (препод1, препод2, ...)), (...), ...]"""
    return [(i[:-1], select(j.name for j in i[-1].teachers)[:]) for i in
            select((j.number_week, j.weekday, j.time, i.name, i) for i in self.subjects
                   for j in i.weekday_and_time_subjects).sort_by(1, 2, 3)]


@Group.getter_and_classmethod
def get_hometask(self):
    """возвращает сущности всего домашнего задания в порядке возрастания даты
    (от старого к новому)
    если дата или время не указано, то считается, что это меньше всего"""
    return (i[0] for i in select((j, j.deadline_date, j.deadline_time)
                                 for i in self.subjects for j in i.home_tasks).sort_by(2, 3, )[:])


@Group.getter_and_classmethod
def get_hometask_data(self):
    """возвращает данные всего домашнего задания в порядке возрастания даты
    (от старого к новому)
    если дата или время не указано, то считается, что это меньше всего
    формат:
    [((дата дедлайна, время дедлайна, название предмета, текст задания), [препод1, препод2, ...]) (...), ...]"""
    return [(i[:-1], select(j.name for j in i[-1].teachers)[:])
            for i in select((j.deadline_date, j.deadline_time, i.name, j.text, i)
                            for i in self.subjects for j in i.home_tasks).sort_by(1, 2)]


@Group.getter_and_classmethod
def get_teachers(self):
    """Возвращает сущности учителей"""
    return select(t for i in self.subjects for t in i.teachers)[:]


@Group.getter_and_classmethod
def get_teachers_data(self):
    """Возвращает словарь с ключем - имя учителя и значением:
    - список предметов, которые он ведет (у этой группы)
    - емеил
    - номер телефона"""
    ans = dict()
    for [name, sub, em, num] in select(
            (t.name, i.name, t.email, t.phone_number) for i in self.subjects for t in i.teachers):
        ans[name] = ans.get(name, [[sub], em, num])
        ans[name][0].append(sub)
    return ans
    # return [(j.name, j.email, j.phone_number, select(sub.name for sub in j.subjects)[:]) for j in select(t for i in self.subjects for t in i.teachers)[:]]


def protect_attr(attr_name='users'):
    new_attr_name = '_' + attr_name

    def decorator(cls):
        print('!!!!!!!!!!')

        @property
        def attr(self):
            return frozenset(filter(lambda i: i.is_verificated, getattr(self, new_attr_name).select()))

        @attr.setter
        def attr(self, val):
            val = frozenset(val)
            old_val = frozenset(self._users.select()[:])
            print('val', val)
            print('old_val', old_val)
            self._users = val
            for u in ((val - old_val) | (old_val - val)):  # новые пользователи и удалённые пользователи
                u._is_verificated = False
                print('u', u)
            return True

        last_attr = getattr(cls, attr_name)
        setattr(cls, new_attr_name, last_attr)
        setattr(cls, attr_name, attr)
        return cls

    return decorator


def protect_senior(attr_name='senior_in_the_group'):
    new_attr_name = '_' + attr_name

    def decorator(cls):
        print('!!!!!!!!!!')

        @property
        def attr(self):
            senior = getattr(self, new_attr_name)
            return 'Староста не назначен' if senior is None else \
                (senior.user if senior.is_verification else 'Староста не верифицирован')

        @attr.setter
        def attr(self, val):
            if val is None:
                senior = getattr(self, new_attr_name)
                if senior:
                    senior.is_verification = False
                    senior.delite()
                    commit()
            elif type(val) == User and not SeniorInTheGroup.exists(user=val, group=self):
                SeniorInTheGroup(user=val, group=self)
                commit()
            elif type(val) == SeniorInTheGroup:
                setattr(self, new_attr_name, val)
            else:
                return False
            return True

        last_attr = getattr(cls, attr_name)
        setattr(cls, new_attr_name, last_attr)
        setattr(cls, attr_name, attr)
        return cls

    return decorator


Group = protect_attr(attr_name='users')(Group)
Group = protect_senior(attr_name='senior_in_the_group')(Group)


@Group.getter_and_classmethod
def all_group(self):
    """Возвращает как верифицированных пользователей, так и не верифицированных"""
    return self._users


@Group.getter_and_classmethod
def no_verificated_users(self):
    """Возвращает только неверифицированных пользователей"""
    return frozenset(filter(lambda i: not i.is_verificated, self._users.select()))


@User.only_func
def __init__(self, *args, **kwargs):
    """при инициализации делаем всех доступных пользователей верифицированными"""
    super(User, self).__init__(*args, **kwargs)  # создание пользователя
    for u in kwargs.get('users', []):
        u.is_verificated = True
    commit()