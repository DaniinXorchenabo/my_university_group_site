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
        return code

    @staticmethod
    def bracket_parser(string):
        print(string)
        values = ['']  # xdf
        flag = True
        for h in string:
            if h in '[,]':
                if (h == '[') and flag:
                    values[-1] = ''
                    flag = True
                elif (h == '[') and not flag:
                    values[-1] = ''
                    values.append('')
                    flag = True
                elif (h == ']') and flag:
                    values.append('')
                    flag = False
                elif (h == ',') and not flag:
                    values.append('')
                    flag = True
                elif (h == ']') and not flag:
                    values[-1] = ''
            else:
                values[-1] += h
        ans = tuple([i.replace('"', '').replace("'", '') for i in values[:-1] if bool(i)])
        return ans if len(ans) > 1 else ans[0]

    def __init__(self, obj: Any):

        meta_obj = type('MetaObject' + str(MyGetterDict.counter_metaclass), (), dict())()
        MyGetterDict.counter_metaclass += 1
        code = self.get_aributs(obj)
        [setattr(meta_obj, i, getattr(obj, i)) for i in code]
        [setattr(meta_obj, key, val(getattr(meta_obj, key))) for key, val in self.modif_type_rules.items()]
        db_obj_to_text_utils = {
            lambda i: type(i) == list and any((type(j) in db.entities.values() for j in i)):
                lambda i: [(self.bracket_parser(str(j)) if type(j) in db.entities.values() else j) for j in i],
            lambda i: type(i) != list and type(i) in db.entities.values(): lambda i: self.bracket_parser(str(i))
        }
        db_obj_to_text_run = lambda i: [setattr(meta_obj, str(i), val(getattr(meta_obj, str(i)))) for key, val in db_obj_to_text_utils.items() if key(getattr(meta_obj, str(i)))]
        [db_obj_to_text_run(i) for i in code]
        [print([getattr(meta_obj, i)]) for i in code]
        self._obj = meta_obj
        print('end init', obj)

    def get(self, key: Any, default: Any = None) -> Any:
        print(key, getattr(self._obj, key, default))
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