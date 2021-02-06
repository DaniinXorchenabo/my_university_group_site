# -*- coding: utf-8 -*-

"""Код, который модифицирует БД,
   но должен выполняться после импорта pydantic-моделей"""

from app.db.db_base_func import *
from app.db.models import *
from app.db.pydantic_models_db.pony_orm_to_pydantic_utils import *
from app.db.pydantic_models_db.pydantic_models import *


def init_decorator(base_init, entities, entities_code):
    """Позволяет создавать новую сущность БД из модели pydantic"""

    def primary_key_to_entity(ent, param_name: str, value):
        print(value)
        if type(value) == list:
            return [i for i in (primary_key_to_entity(ent, param_name, i) for i in value) if i]
        code, p_k = entities_code[ent.__class__]
        param_type = code[param_name].param_type

        if type(value) == dict and param_type in entities:
            print('1---*****------')
            try:
                value = eval('Pd' + entities[param_type].__name__)(**value)
            except ValueError as e:
                print('init_decorator.primary_key_to_entity: произошла ошибка', e)
                value = None
            except TypeError as e:
                print('init_decorator.primary_key_to_entity: произошла ошибка', e)
                value = None
            except AssertionError as e:
                print('init_decorator.primary_key_to_entity: произошла ошибка', e)
                value = None

        if hasattr(value, '__class__') and hasattr(  # Если значение является pydantic-объектом
                value.__class__, '__bases__') and BaseModel in value.__class__.__bases__:
            print('2---*****------')
            value = get_p_k(value)

        if param_type not in entities:
            print('3---*****------', param_type)
            return value

        if param_type in entities:
            print('4---*****------')
            value = [value] if type(value) != tuple else value
            keys = {i: value[ind] for ind, i in enumerate(entities_code[param_type][1])}
            if entities[param_type].exists(**keys):
                return entities[param_type].get(**keys)
            try:
                return entities[param_type](**keys)
            except ValueError as e:
                print(e)
            return None
        return value


    def new_init(self, *args, **kwargs):
        if args and bool(args):
            for ind, i in enumerate(args):
                if hasattr(i, '__class__') and hasattr(i.__class__, '__bases__') and BaseModel in i.__class__.__bases__:
                    pd_values = {key: val for key, val in dict(i).items() if val and bool(val) and val != [None]}
                    pd_values = {key: primary_key_to_entity(self, key, val) for key, val in pd_values.items()}
                    print(pd_values)
                    kwargs.update(pd_values)
                    args = list(args)
                    del args[ind]
                    args = tuple(args)

        base_init(self, *args, **kwargs)
    return new_init