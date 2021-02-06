# -*- coding: utf-8 -*-

"""В этом коде пишется и объявляется то, что нужно еще до объявления сущностей БД"""

from datetime import date
from datetime import datetime
from datetime import time
from typing import Any, List, Iterator, Tuple
from functools import reduce

from pony.orm import *
from pydantic import BaseModel

from app.settings.config import *
from app.db.pydantic_models_db.pony_orm_to_pydantic_utils import get_p_k

class AddArrtInDbClass(object):
    # _white_list = {'_white_list'}
    # _expanded_white_list = _white_list

    # @classmethod
    # def get_into_white_list(cls, name):
    #     if not hasattr(cls, '_white_list'):
    #         cls._white_list = {'_white_list'}
    #     cls._white_list.add(name)
    #     cls._expanded_white_list = cls._white_list.copy()

    @classmethod
    def getter_and_classmethod(cls, func):
        """добавляет одноимянный атрибут и метод сласса"""
        """"Это означает, что можно так:
        Group['20ВП1'].func
        и Group.cl_func(name='20ВП1')
        вместо name='20ВП1' могут быть любые параметры, идентифицирующие сущность
        """
        setattr(cls, func.__name__, property(func))  # types.MethodType(func, cls)

        # cls.get_into_white_list(func.__name__)

        def w(*arfs, **kwargs):
            if cls.exists(**kwargs):
                ent = cls.get(**kwargs)
                return getattr(ent, func.__name__)
            return None

        setattr(cls, 'cl_' + func.__name__, classmethod(w))
        # cls.get_into_white_list('cl_' + func.__name__)

    @classmethod
    def only_func(cls, func):
        """добавляет к классу одноимянную функцию"""
        """Это означает, что можно так:
        Group['20ВП1'].func(ваши параметры, которые требует функция)"""
        setattr(cls, func.__name__, func)  # types.MethodType(func, cls)
        # cls.get_into_white_list(func.__name__)

    @classmethod
    def func_and_classmethod(cls, func):
        """добавляет к классу одноимянную функцию и метод класса"""
        """Это означает, что можно так:
        Group['20ВП1'].func(ваши параметры, которые требует функция)
        и так 
        Group['20ВП1'].func(ваши параметры, которые требует функция)"""
        setattr(cls, func.__name__, func)  # types.MethodType(func, cls)

        # cls.get_into_white_list(func.__name__)

        def w(*arfs, **kwargs):
            if cls.exists(id=kwargs.get('id', -1234)):
                ent = cls.get(id=kwargs.get('id', -1234))
                return getattr(ent, func.__name__)(*arfs, **kwargs)
            return None

        setattr(cls, 'cl_' + func.__name__, classmethod(w))
        # cls.get_into_white_list('cl_' + func.__name__)

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
        # cls.get_into_white_list(func.__name__)
        setattr(cls, func.__name__, classmethod(func))

    @classmethod
    def only_staticmethod(cls, func):
        """добавляет к классу статический метод"""
        """Это означает, что можно так:
        Group.func(<параметры>)
        Group['20ВП1'].func(<параметры>)"""
        # cls.get_into_white_list(func.__name__)
        setattr(cls, func.__name__, staticmethod(func))


def db_ent_to_dict(ent):
    """
    Генерирует представление класса БД в виде кода

    На выход поступает словарь {имя_атрибута: объект_StringDB}
    и {имя_primary_key: тип_primary_key_в_БД}
    """

    class StringDB(BaseModel):
        """Олицетворяет одну строку в классе сузности Pony"""
        name: str
        db_type: str
        param_type: str
        default: Any
        other_params: dict
        is_primary_key: bool = False

    code = [i.strip() for i in ent.describe().split('\n')]
    p_k = [i for i in code if 'PrimaryKey' in i]
    code = (i.split('=') for i in code if '=' in i)
    code = ((i[0].strip(), '='.join(i[1:]).split('(')) for i in code)
    code = ((i[0], i[1][0].strip(), i[1][1].strip(')').split(',')) for i in code)
    code = ((i[0], i[1], i[2][0], [j.strip().split('=') for j in i[2][1:]]) for i in code)
    code = ((i[0], i[1], i[2], {j[0].strip(): j[1].strip() for j in i[3]}) for i in code)
    code = {i[0]: StringDB(
        name=i[0],
        db_type=i[1],
        param_type=reduce(lambda string, ch: string.replace(ch, ''), [i[2], '"', "'"]),
        default=i[3].pop('default', None),
        other_params=i[3],
        is_primary_key=i[1] == 'PrimaryKey'
    ) for i in code}

    simple_p_k = [i.split('=')[0].strip() for i in p_k if '=' in i]
    simple_p_k = {i: code[i].param_type for i in simple_p_k}
    complex_p_k = [i.split('(')[1].strip(')').strip().split(',') for i in p_k if '=' not in i]
    complex_p_k = {tuple([j.strip() for j in i]): [code[j.strip()].param_type for j in i] for i in complex_p_k}
    simple_p_k.update(complex_p_k)
    return code, simple_p_k


if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)
