# -*- coding: utf-8 -*-

""" В этом файле содержится код, необходимый для работы
автоматически сгенерированных pydantic-моделей, который не генерируется автоматически"""

from typing import Set as PdSet, Union, List, Dict, Tuple, ForwardRef
from typing import Optional as PdOptional, Callable, Generator
from datetime import date, datetime, time

from pony.orm import *
from pydantic import BaseModel, Json as PdJson, validator, root_validator, Field
from pydantic.utils import GetterDict, display_as_type

from app.db.models import *


class MyGetterDict(GetterDict):
    counter_metaclass = 0
    modif_type_rules = dict()

    @staticmethod
    def get_aributs(obj):
        from inspect import getsource

        entity = obj.__class__
        code = getsource(entity).split('\n')

        count_tabs = code[0].split('def')[0].count(' ') + 3
        code = (''.join(list(i.split('#')[0])[count_tabs:]) for i in code[1:])
        code = {i.split('=')[0].strip(): i for i in code if '=' in i}
        code = {i: [getattr(entity, i), val] for i, val in code.items()}
        to_list = ',\n'.join([f'"{i}": lambda i: i.select()[:]' for i, (t, c) in code.items() if 'Set' in c])
        to_list = 'modif_type_rules = {\n' + to_list + '\n}'
        # print(to_list, sep='\n')
        return code

    def __init__(self, obj: Any):
        meta_obj = type('MetaObject' + str(MyGetterDict.counter_metaclass), (), dict())()
        MyGetterDict.counter_metaclass += 1
        # self = MyGetterDictUser
        code = self.get_aributs(obj)
        [setattr(meta_obj, i, getattr(obj, i)) for i in code]
        [setattr(meta_obj, key, val(getattr(meta_obj, key))) for key, val in self.modif_type_rules.items()]
        # [print(getattr(meta_obj, key)) for key, val in self.modif_type_rules.items()]
        # [print(i, [getattr(meta_obj, i)]) for i in code]
        self._obj = meta_obj

    def get(self, key: Any, default: Any = None) -> Any:
        return getattr(self._obj, key, default)


"""
    # @validator('id')
    # def check_db_id(cls, param):
    # 	assert User.exists(id=param), 'Пользователя с таким id нет в БД'
    # 	return param
    # 	raise ValueError('Пользователя с таким id нет в БД')

    @root_validator
    def check_model(cls, values: dict):
        # print(values)
        values = {key: val for key, val in values.items() if val is not None and val != [None]}
        # print(values)
        # assert User.exists(**values), "Такого пользователя нат в БД"
        return values
"""