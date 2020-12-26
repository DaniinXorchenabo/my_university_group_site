# -*- coding: utf-8 -*-

"""Дополнение к пользователю"""

import uuid
import hashlib
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
    if value:  # если мы делаем пользователя верифицированным
        self.my_verification = set()
        self.i_verificate_thei = set()
        commit()
        [NoneVerification(**params) for params in
         (dict(it_is_i=u, he_verificate_me=self) for u in
          self._groups._users.select(lambda u: not u._is_verificated and u != self))
         if not NoneVerification.exists(**params)]
        if self._groups and type(self._groups.senior_in_the_group) == SeniorInTheGroup and\
                not self._groups.senior_in_the_group.is_verification:
            # если в группе пользователя есть неверифицированный староста,
            # то добавляем пользователя в верифиувторы старосты
            senior = self._groups.senior_in_the_group
            if not SeniorVerification.exists(user=self, senior_in_the_group=senior):
                SeniorVerification(user=self, senior_in_the_group=senior)
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
            if type(self._groups.senior_in_the_group) == SeniorInTheGroup and \
                not self._groups.senior_in_the_group.is_verification:
                # если в группе пользователя есть неверифицированный староста,
                # то убираем пользователя из верификаторов старосты
                senior = self._groups.senior_in_the_group
                if SeniorVerification.exists(user=self, senior_in_the_group=senior):
                    SeniorVerification.get(user=self, senior_in_the_group=senior).delite()


@User.only_setter
def is_verificated(self, value: bool):
    print(self._is_verificated)
    if not (self._is_verificated == value == True):
        [u.check_verificated for u in self._groups._users.select()]
        # self.check_verificated
        commit()
        self._is_verificated = value


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

@User.only_staticmethod
def create_hash(string, salt):
    from hashlib import pbkdf2_hmac
    from binascii import unhexlify

    if type(salt) == str:
        if len(salt) % 2 != 0:
            salt = salt + 'a'
        salt = unhexlify(salt)
    return pbkdf2_hmac('sha256', str(string).encode('utf-8'), salt, 100000, dklen=32)


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


def protect_password(attr_name='groups'):
    from hashlib import pbkdf2_hmac
    from binascii import unhexlify, hexlify
    from os import urandom

    new_attr_name = '_' + attr_name
    get_system_atr_name = '_get_' + attr_name
    get_salt_name = '_get_salt_' + attr_name
    get_key_password_name = '_get_key_' + attr_name

    def decorator(cls):
        print('!!!!!!!!!!')

        @property
        def attr(self):
            """Будет возвращаться при попытке получить значение атрибута attr_name"""
            return "***"

        @attr.setter
        def attr(self, new_password):
            """Будет выполнятся при присваивании нового значения атрибуту attr_name"""
            salt = urandom(32)  # размер строки - 64
            key = self.create_hash(new_password, salt)  # размер строки - 64
            # print(len(str(binascii.hexlify(key), encoding="utf-8")))
            # print(len(str(binascii.hexlify(salt), encoding="utf-8")))
            storage = salt + key
            setattr(self, new_attr_name, str(hexlify(storage), encoding="utf-8"))
            commit()

        @property
        def get_all_password(self):
            """Получить весь пароль (захешированный)"""
            if getattr(self, new_attr_name):
                password_hash = getattr(self, new_attr_name)
                return password_hash if type(password_hash) == str \
                    else str(hexlify(password_hash), encoding="utf-8")
            return getattr(self, new_attr_name) or ""

        @property
        def get_salt(self):
            """Получить соль захешированного пароля"""
            if getattr(self, new_attr_name):
                salt_from_storage = getattr(self, new_attr_name)[:64]  # 32 является длиной соли
                return salt_from_storage if type(salt_from_storage) == str \
                    else str(hexlify(salt_from_storage), encoding="utf-8")
            return getattr(self, new_attr_name) or ""

        @property
        def get_key(self):
            """получить только ключ захешированного пароля"""
            if getattr(self, new_attr_name):
                key_from_storage = getattr(self, new_attr_name)[64:]
                return key_from_storage if type(key_from_storage) == str \
                    else str(hexlify(key_from_storage), encoding="utf-8")
            return getattr(self, new_attr_name) or ""

        last_attr = getattr(cls, attr_name)
        setattr(cls, new_attr_name, last_attr)
        setattr(cls, attr_name, attr)
        setattr(cls, get_system_atr_name, get_all_password)
        setattr(cls, get_salt_name, get_salt)
        setattr(cls, get_key_password_name, get_key)
        return cls

    return decorator


def protect_senior(attr_name='senior_in_the_group'):
    new_attr_name = '_' + attr_name

    def decorator(cls):
        print('!!!!!!!!!!')

        @property
        def attr(self):
            senior = getattr(self, new_attr_name)
            return senior if senior is None else 'Вы не староста'

        @attr.setter
        def attr(self, val):
            if val is None or not val:
                senior = getattr(self, new_attr_name)
                if senior:  # если пользователь был старостой, но теперь больше не староста
                    senior.is_verification = False
                    senior.delite()
                    commit()
            elif val == True:  # если человека назначили старостой
                if self.is_verificated and not SeniorInTheGroup.exists(user=self, group=self._groups):
                    # и он им не был, то создаем неверифицированного старосту
                    SeniorInTheGroup(user=self, group=self._groups)
                    commit()
            elif type(val) == SeniorInTheGroup and self.is_verificated and val.group == self.groups:
                setattr(self, new_attr_name, val)
            else:
                return False
            return True

        last_attr = getattr(cls, attr_name)
        setattr(cls, new_attr_name, last_attr)
        setattr(cls, attr_name, attr)
        return cls

    return decorator


User = protect_attr(attr_name='groups')(User)
User = protect_password(attr_name='password')(User)
User = protect_senior(attr_name='senior_in_the_group')(User)


@User.func_and_classmethod
def check_password(self, password: str = ""):
    """Выполняет проверку пароля пользователя"""
    from binascii import hexlify

    salt = self._get_salt_password
    testing_password_hash = self.create_hash(password, salt)
    testing_password_hash = str(hexlify(testing_password_hash), encoding="utf-8")
    count = 0
    print(testing_password_hash, self._get_key_password)
    for ch1, ch2 in zip(testing_password_hash, self._get_key_password):
        count += 1 if ch1 == ch2 else 2
    return count == len(self._get_key_password) and len(testing_password_hash) == len(self._get_key_password)


@User.only_func
def __init__(self, *args, **kwargs):
    """при инициализации пользователя делаем его неверифицированным, если не указано иное"""
    init_kw = kwargs.copy()
    is_verificated_user = kwargs.pop('is_verificated', None)
    verificate_bool = (is_verificated_user is None and
                       ("my_verification" not in init_kw and "i_verificate_thei" not in init_kw)) \
                      or is_verificated_user == False  # True, если пользователь неверифицирован
    if verificate_bool:  # если пользователь не верифицирован
        kwargs.pop('senior_in_the_group', None)  # то он не может быть старостой
    super(User, self).__init__(*args, **kwargs)  # создание пользователя
    if verificate_bool:  # если пользователь не верифицирован
        if User.exists(**init_kw):
            print('существует')
            if init_kw.get("groups", None):  # и имеет группу
                my_group_friends = set(select(i for i in self._groups._users if i._is_verificated)[:]) - {self}
                print(my_group_friends)
                [NoneVerification(it_is_i=self, he_verificate_me=u) for u in my_group_friends
                 if not NoneVerification.exists(it_is_i=self, he_verificate_me=u)]
                commit()  # то дабовляем ему тех, кто будет верифицировать его
        else:
            print('не существует')
    elif is_verificated_user:  # если при создании явно указано, что пользователь верифицирован
        my_no_verificated_friends = set(select(i for i in self._groups._users if not i._is_verificated)[:]) - {self}
        print(my_no_verificated_friends)
        [NoneVerification(it_is_i=u, he_verificate_me=self) for u in my_no_verificated_friends
         if not NoneVerification.exists(it_is_i=u, he_verificate_me=self)]
        commit()  # то добавляем ему тех, кого он должен верифицировать

    if 'password' in kwargs:  # хешируем пероль
        self.password = kwargs['password']
    commit()
