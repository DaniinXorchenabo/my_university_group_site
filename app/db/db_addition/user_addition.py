# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *


if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)



@User.getter_and_classmethod
def is_verificated(self):
    """Возвращает True, если пользователь верифицирован
    False - в противном случае"""
    pass


@User.only_setter
def is_verificated(self, value: bool):
    """устанавлмвает значение верификации
    True - пользователь верифицирован
    False - пользователь не верифицирован"""
    if value:
        self.my_verification = set()
        self.i_verificate_thei = set()
        commit()
        [NoneVerification(**params) for params in
         (dict(it_is_i=u, he_verificate_me=self) for u in User.select(lambda u: not u.is_verificated))
         if not NoneVerification.exists(**params)]
        commit()
    else:
        self.my_verification = set()
        commit()
        self.i_verificate_thei = set()
        commit()
        delete(i for i in NoneVerification if i.he_verificate_me == self)
        commit()
        delete(i for i in NoneVerification if i.it_is_i == self)
        commit()
        [NoneVerification(**params) for params in
         (dict(it_is_i=self, he_verificate_me=u) for u in User.select(lambda u: u.is_verificated and u != self))
         if not NoneVerification.exists(**params)]
        commit()


@User.getter_and_classmethod
def check_verificated(self):
    """если по большинству голосов за пользователя он получается веривицированным, то функция верифицирует его"""
    if bool(self.my_verification):
        num, count, *_ = zip(*((i.confirmation, 1) for i in self.my_verification.select()))
        if sum(count) // 2 <= sum(num):
            self.is_verificated = True
            return True
        return False
    return self.groups is not None


@User.getter_and_classmethod
def is_verificated(self):
    """Возвращает True, если пользователь верифицирован
    False - в противном случае"""
    return self.check_verificated


@User.only_func
def __init__(self, *args, **kwargs):
    # print(self, args, kwargs)
    """при инициализации пользователя делаем его неверифицированным, если не указано иное"""
    init_kw = kwargs.copy()
    super(User, self).__init__(*args, **kwargs)
    commit()
    if "my_verification" not in init_kw and "i_verificate_thei" not in init_kw:
        if User.exists(**init_kw):
            print('существует')
            self_user = User.get(**init_kw)
            if "groups" in init_kw:
                my_group = init_kw.get('groups', '')
                my_group_friends = set(select(i for i in User if i.groups == my_group and i.is_verificated)[:]) - {self}
                print(my_group_friends)
                [NoneVerification(it_is_i=self, he_verificate_me=u) for u in my_group_friends]
                commit()
        else:
            print('не существует')


@User.func_and_classmethod
def add_group(self, *args, **params):
    """Функция для добавления пользователю группы
    =======! Внимание !=======
    никаким образом больше добавлять группы нельзя!!!!!"""
    """Использование:
    User.add_group('20ВП1', id=123078234)
    User.add_group(Group['20ВП1'], id=123078234)
    User.add_group('20ВП1', id=123078234, name='Billy' <и другие параметры пользователя>)
    User.add_group(Group['20ВП1'], id=123078234, name='Billy' <и другие параметры пользователя>)
    User[123078234].add_group('20ВП1')
    User[123078234].add_group(Group['20ВП1'])
    User[123078234].add_group('20ВП1', name='Billy' <и другие параметры пользователя>)
    User[123078234].add_group(Group['20ВП1'], name='Billy' <и другие параметры пользователя>)
    """

    if bool(args) and type(args[0]) in [str, Group]:
        if bool(params):
            self.set(**params)
            commit()
        self.groups = Group[args[0]] if type(args[0]) == str else args[0]
        commit()
        self.is_verificated = False
        return True
    elif bool(params):
        flag = False
        if "groups" in params and self.groups is None:
            flag = True
        self.set(**params)
        commit()
        if flag:
            self.is_verificated = False
        return True
    return False

