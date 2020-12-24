# -*- coding: utf-8 -*-

"""В этом коде пишется и объявляется то, что нужно еще до объявления сущностей БД"""

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *


class AddArrtInDbClass(object):
    _white_list = {'_white_list'}
    _expanded_white_list = _white_list

    @classmethod
    def get_into_white_list(cls, name):
        if not hasattr(cls, '_white_list'):
            cls._white_list = {'_white_list'}
        cls._white_list.add(name)
        cls._expanded_white_list = cls._white_list.copy()

    @classmethod
    def getter_and_classmethod(cls, func):
        """добавляет одноимянный атрибут и метод сласса"""
        """"Это означает, что можно так:
        Group['20ВП1'].func
        и Group.cl_func(name='20ВП1')
        вместо name='20ВП1' могут быть любые параметры, идентифицирующие сущность
        """
        setattr(cls, func.__name__, property(func))  # types.MethodType(func, cls)
        cls.get_into_white_list(func.__name__)

        def w(*arfs, **kwargs):
            if cls.exists(**kwargs):
                ent = cls.get(**kwargs)
                return getattr(ent, func.__name__)
            return None

        setattr(cls, 'cl_' + func.__name__, classmethod(w))
        cls.get_into_white_list('cl_' + func.__name__)

    @classmethod
    def only_func(cls, func):
        """добавляет к классу одноимянную функцию"""
        """Это означает, что можно так:
        Group['20ВП1'].func(ваши параметры, которые требует функция)"""
        setattr(cls, func.__name__, func)  # types.MethodType(func, cls)
        cls.get_into_white_list(func.__name__)

    @classmethod
    def func_and_classmethod(cls, func):
        """добавляет к классу одноимянную функцию и метод класса"""
        """Это означает, что можно так:
        Group['20ВП1'].func(ваши параметры, которые требует функция)
        и так 
        Group['20ВП1'].func(ваши параметры, которые требует функция)"""
        setattr(cls, func.__name__, func)  # types.MethodType(func, cls)
        cls.get_into_white_list(func.__name__)

        def w(*arfs, **kwargs):
            if cls.exists(id=kwargs.get('id', -1234)):
                ent = cls.get(id=kwargs.get('id', -1234))
                return getattr(ent, func.__name__)(*arfs, **kwargs)
            return None

        setattr(cls, 'cl_' + func.__name__, classmethod(w))
        cls.get_into_white_list('cl_' + func.__name__)

    @classmethod
    def only_setter(cls, func):
        """добавляет к классу одноимянный сеттер"""
        """Это означает, что можно так:
        Group['20ВП1'].func = ваше значение"""
        print(getattr(cls, func.__name__), func.__name__)
        setattr(cls, func.__name__, getattr(cls, func.__name__).setter(func))  # types.MethodType(func, cls)
        print('-0-0-0-0-')

    @classmethod
    def only_getter(cls, func):
        """добавляет одноимянный геттер"""
        """"Это означает, что можно так:
        Group['20ВП1'].func"""
        setattr(cls, func.__name__, property(func))  # types.MethodType(func, cls)


    @classmethod
    def only_classmetod(cls, func):
        """добавляет к классу метод класса"""
        """Это означает, что можно так:
        Group.func()"""
        cls.get_into_white_list(func.__name__)
        setattr(cls, func.__name__, classmethod(func))


if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)
