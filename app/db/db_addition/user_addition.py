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
            # print('-----True')
            return True
        # print('-----False')
        return False
    User._expanded_white_list.add('groups')
    gr = self.groups
    # print('------', [gr])
    return gr is not None and type(gr) != str


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


@User.only_func
def __getattribute__(self, item, ):
    # print(super(User.__bases__[0], self))
    if item in User._expanded_white_list or item[0] == '_':
        User._expanded_white_list = User._white_list.copy()
        return super(User.__bases__[0], self).__getattribute__(item)
    # self.my_verification
    # print(item, User.my_verification, item in {'senior_in_the_group': None, 'groups': "вы не авторизированы"})
    block_attr = {'senior_in_the_group': None, 'groups': 'Вы не выбрали группу'}
    # print("*****", item, not self.is_verificated,  item in block_attr)
    if item in block_attr and not self.is_verificated:
        if item == 'groups':
            # print('*************')
            User._expanded_white_list.add(item)
            block_attr['groups'] = super(User.__bases__[0], self).__getattribute__(item) or block_attr['groups']
            block_attr['groups'] = (type(block_attr['groups']) == str and block_attr['groups']) or block_attr['groups'].name
        return block_attr[item]
    else:
        User._expanded_white_list.add(item)
        return super(User.__bases__[0], self).__getattribute__(item)
    # ans = super(User, self).__getattribute__(item)
    # if callable(ans):
    #     return super(User, self).__getattribute__(item)

    # bloking = dict() if self.is_verificated else {'senior_in_the_group': None, 'groups': "вы не авторизированы"}
    # if item == 'groups':
    #     bloking['groups'] = Group[self.group]
    #     bloking['groups'] = bloking['groups'] and bloking['groups'].name
    # return bloking.get(item, super(User.__bases__[0], self).__getattribute__(item))


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

