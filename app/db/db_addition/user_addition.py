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
def is_verificated(self): return None


@User.getter_and_classmethod
def check_verificated(self):
    """если по большинству голосов за пользователя он получается веривицированным, то функция верифицирует его"""
    if bool(self.my_verification):
        num, count, *_ = zip(*((i.confirmation, 1) for i in self.my_verification.select()))
        # print(self, num, count, sum(count) // 2 <= sum(num),  not (sum(num) == 1 and sum(count) == 0))
        if sum(count) // 2 <= sum(num) and not (sum(num) == 0 and sum(count) == 1):
            self._is_verificated = True
            # print('-----True')
            return True
        # print('-----False')
        return False
    # User._expanded_white_list.add('groups')
    gr = self._groups
    # print('------', [gr])
    return gr is not None and type(gr) != str


@User.getter_and_classmethod
def _is_verificated(self):
    """Возвращает True, если пользователь верифицирован
    False - в противном случае"""
    # return self.check_verificated
    return not bool(self.my_verification)


@User.getter_and_classmethod
def is_verificated(self):
    """Проверяет, верифицирован ли пользователь
    Возвращает True, если пользователь верифицирован
    False - в противном случае"""
    return self.check_verificated


@User.only_setter
def _is_verificated(self, value: bool):
    """устанавлмвает значение верификации
    True - пользователь верифицирован
    False - пользователь не верифицирован"""
    print('&&6')
    if value:
        self.my_verification = set()
        self.i_verificate_thei = set()
        commit()
        [NoneVerification(**params) for params in
         (dict(it_is_i=u, he_verificate_me=self) for u in self._groups._users.select(lambda u: not u._is_verificated and u != self))
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
        if self._groups:
            [NoneVerification(**params) for params in
             (dict(it_is_i=self, he_verificate_me=u) for u in self._groups._users.select(
                 lambda u: u._is_verificated and u != self)) if not NoneVerification.exists(**params)]
            commit()


@User.only_setter
def is_verificated(self, value: bool):
    print(self._is_verificated)
    if not(self._is_verificated == value == True):
        [u.check_verificated for u in self._groups._users.select()]
        # self.check_verificated
        commit()
        self._is_verificated = value


@User.only_func
def __init__(self, *args, **kwargs):
    """при инициализации пользователя делаем его неверифицированным, если не указано иное"""
    init_kw = kwargs.copy()
    super(User, self).__init__(*args, **kwargs)
    commit()
    if "my_verification" not in init_kw and "i_verificate_thei" not in init_kw:
        if User.exists(**init_kw):
            print('существует')
            if init_kw.get("groups", None):
                my_group_friends = set(select(i for i in self._groups._users if i._is_verificated)[:]) - {self}
                print(my_group_friends)
                [NoneVerification(it_is_i=self, he_verificate_me=u) for u in my_group_friends
                 if not NoneVerification.exists(it_is_i=self, he_verificate_me=u)]
                commit()
        else:
            print('не существует')


# @User.only_func
# def __getattribute__(self, item, ):
#     # print(super(User.__bases__[0], self))
#     if item in User._expanded_white_list or item[0] == '_':
#         User._expanded_white_list = User._white_list.copy()
#         return super(User.__bases__[0], self).__getattribute__(item)
#     # self.my_verification
#     # print(item, User.my_verification, item in {'senior_in_the_group': None, 'groups': "вы не авторизированы"})
#     block_attr = {'senior_in_the_group': None, 'groups': 'Вы не выбрали группу'}
#     # print("*****", item, not self.is_verificated,  item in block_attr)
#     if item in block_attr and not self.is_verificated:
#         if item == 'groups':
#             # print('*************')
#             User._expanded_white_list.add(item)
#             block_attr['groups'] = super(User.__bases__[0], self).__getattribute__(item) or block_attr['groups']
#             block_attr['groups'] = (type(block_attr['groups']) == str and block_attr['groups']) or block_attr['groups'].name
#         return block_attr[item]
#     else:
#         User._expanded_white_list.add(item)
#         return super(User.__bases__[0], self).__getattribute__(item)

# @User.only_getter
# def groups(self):
#     if

# @User.func_and_classmethod
# def add_group(self, *args, **params):
#     """Функция для добавления пользователю группы
#     =======! Внимание !=======
#     никаким образом больше добавлять группы нельзя!!!!!"""
#     """Использование:
#     User.add_group('20ВП1', id=123078234)
#     User.add_group(Group['20ВП1'], id=123078234)
#     User.add_group('20ВП1', id=123078234, name='Billy' <и другие параметры пользователя>)
#     User.add_group(Group['20ВП1'], id=123078234, name='Billy' <и другие параметры пользователя>)
#     User[123078234].add_group('20ВП1')
#     User[123078234].add_group(Group['20ВП1'])
#     User[123078234].add_group('20ВП1', name='Billy' <и другие параметры пользователя>)
#     User[123078234].add_group(Group['20ВП1'], name='Billy' <и другие параметры пользователя>)
#     """
#
#     if bool(args) and type(args[0]) in [str, Group]:
#         if bool(params):
#             self.set(**params)
#             commit()
#         self.groups = Group[args[0]] if type(args[0]) == str else args[0]
#         commit()
#         self.is_verificated = False
#         return True
#     elif bool(params):
#         flag = False
#         if "groups" in params and self.groups is None:
#             flag = True
#         self.set(**params)
#         commit()
#         if flag:
#             self.is_verificated = False
#         return True
#     return False
#

def protect_attr(attr_name='groups'):
    new_attr_name = '_' + attr_name

    def decorator(cls):
        print('!!!!!!!!!!')

        @property
        def attr(self):
            if self._is_verificated:
                return self._groups
            return getattr(self, new_attr_name) and getattr(self, new_attr_name).name

        @attr.setter
        def attr(self, val):
            if type(val) == Group or val is None:
                setattr(self, new_attr_name, val)
            elif Group.exists(name=str(val)):  # если указанная група (в строковом формате) существует
                setattr(self, new_attr_name, Group.get(name=val))
            else:
                return False
            self.is_verificated = False
            return True

        last_attr = getattr(cls, attr_name)
        setattr(cls, new_attr_name, last_attr)
        setattr(cls, attr_name, attr)
        return cls

    return decorator


User = protect_attr(attr_name='groups')(User)
