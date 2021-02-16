# -*- coding: utf-8 -*-

"""Код, который модифицирует БД,
   но должен выполняться после импорта pydantic-моделей"""

from pony.orm.core import MultipleObjectsFoundError


from app.db.db_base_func import *
from app.db.models import *
from app.db.pydantic_models_db.pony_orm_to_pydantic_utils import *
from app.db.pydantic_models_db.pydantic_models import *


def primary_key_to_entity(ent, param_name: str, value, entities, entities_code):
    # print(value)
    if type(value) == list:
        return [i for i in (primary_key_to_entity(ent, param_name, i, entities, entities_code) for i in value) if i]
    code, p_k = entities_code[ent]
    param_type = code[param_name].param_type

    if type(value) == dict and param_type in entities:
        # print('1---*****------')
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
        # print('2---*****------')
        value = get_p_k(value)

    if param_type not in entities:
        # print('3---*****------', param_type)
        return value

    if param_type in entities:
        # print('4---*****------')
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


def pydantic_obj_parser(ent, args, kwargs, entities, entities_code):
    if args and bool(args):
        # print(args)
        for ind, i in enumerate(args):
            if hasattr(i, '__class__') and hasattr(i.__class__, '__bases__') and BaseModel in i.__class__.__bases__:
                pd_values = {key: val for key, val in dict(i).items() if val and bool(val) and val != [None]}
                pd_values = {key: primary_key_to_entity(ent, key, val, entities, entities_code)
                             for key, val in pd_values.items()}
                # print(pd_values)
                kwargs.update(pd_values)
                args = list(args)
                del args[ind]
                args = tuple(args)
    return args, kwargs


def data_from_pydantic_decorator(base_init, entities, entities_code):
    """Позволяет создавать новую сущность БД из модели pydantic"""

    def decorator(self, *args, **kwargs):
        args, kwargs = pydantic_obj_parser(self.__class__, args, kwargs, entities, entities_code)

        base_init(self, *args, **kwargs)

    return decorator


def data_from_pydantic_decorator2(base_init, entities, entities_code):
    """Позволяет создавать новую сущность БД из модели pydantic"""

    def decorator(cls, *args, **kwargs):
        # print('-----------$$$$$$$$$$$$$$$$$$$$$$$$$$$', args)
        args, kwargs = pydantic_obj_parser(cls, args, kwargs, entities, entities_code)
        # print(*args, kwargs)
        # print(base_init)
        try:
            return base_init(*args, **kwargs)
        except MultipleObjectsFoundError as e:
            if "Multiple objects were found" in str(e):
                ValueError("Недостаточно данных, чтобы идентифицировать пользователя!")
            MultipleObjectsFoundError(e)

    return decorator


def data_from_pydantic_decorator3(base_init, entities, entities_code):
    """Позволяет создавать новую сущность БД из модели pydantic"""

    def decorator(self, *args, **kwargs):
        # print('-----------$$$$$$$$$$$$$$$$$$$$$$$$$$$', args)
        args, kwargs = pydantic_obj_parser(self.__class__, args, kwargs, entities, entities_code)
        p_k = [j for i in entities_code[self.__class__][1] for j in ([i] if type(i) != tuple else i)]
        kwargs = {key: val for key, val in kwargs.items() if key not in p_k}
        # print(*args, kwargs)
        # print(base_init)
        base_init(self, *args, **kwargs)

    return decorator


def data_from_pydantic_decorator4(base_init, entities, entities_code):
    """Позволяет создавать новую сущность БД из модели pydantic"""

    def decorator(cls, *args, **kwargs):
        # print('-----------$$$$$$$$$$$$$$$$$$$$$$$$$$$', args)
        new_args = []
        # print(args)
        for value in args:
            if hasattr(value, '__class__') and hasattr(  # Если значение является pydantic-объектом
                    value.__class__, '__bases__') and BaseModel in value.__class__.__bases__:
                d_value = dict(value)
                d_value.update(dict(upload_orm='min'))
                d_value = dict(value.__class__(**dict(d_value)))
                d_value.update({key: val for key, val in dict(value).items() if val is not None and val != [None]})
                value = value.__class__(**d_value)
                # print('----------------')
            new_args.append(value)
        args = tuple(new_args)
        # print('--**&&&&&$$##@@', args)

        args, kwargs = pydantic_obj_parser(cls, args, kwargs, entities, entities_code)
        # print('-*&&&&&&&&&&&&&???????', args, kwargs)
        p_k = [j for i in entities_code[cls][1] for j in ([i] if type(i) != tuple else i)]
        if bool(p_k):
            p_k = {key: kwargs.get(key) for key in p_k}
            p_k = {key: val for key, val in p_k.items() if val}
            if bool(p_k) and cls.exists(**p_k):
                ent = cls.get(**p_k)
                kwargs = {key: val for key, val in kwargs.items() if key not in p_k}
                # print('!!!!!!!!!', *args, kwargs)
                # print(base_init)
                base_init(ent, *args, **kwargs)

    return decorator


def data_from_pydantic_decorator5(base_init, entities, entities_code):
    """Позволяет создавать новую сущность БД из модели pydantic"""

    def decorator(cls, *args, **kwargs):
        # print('-----------$$$$$$$$$$$$$$$$$$$$$$$$$$$', args)
        args, kwargs = pydantic_obj_parser(cls, args, kwargs, entities, entities_code)
        kwargs = {key: val for key, val in kwargs.items() if type(val) != list}
        # print(*args, kwargs)
        # print(base_init)
        return base_init(*args, **kwargs)

    return decorator


def change_to_dict_method(base_metod):

    """
    .to_dict() выдает значения с учетом переопределения полей в БД

    Делает так, чтобы метод сущностей .to_dict() возвращал
    значения с учетом переопределения типов в файлех папки app/db/db_addition
    К примеру, вместо хеша пароля будет возвращены "***"
    """

    def is_iter(i) -> bool:
        return (hasattr(i, '__iter__') and not type(i) == str) or hasattr(i, 'select')

    def is_ent(i) -> bool:
        return hasattr(i, 'select') or type(i) in db.entities.values()

    def decorator(self, *args, **kwargs):

        _dict = base_metod(self, *args, **kwargs)
        change_args = {}
        for key, val in _dict.items():
            db_val = getattr(self, key)
            if db_val != val:
                change_args[key] = val, db_val

        for key, [d_val, db_val] in change_args.items():
            ents = db.entities.values()
            t_db, t_d = type(db_val), type(d_val)
            if not is_iter(d_val) and not is_iter(db_val):
                # Если и то и то не списки
                if not is_ent(d_val) and is_ent(db_val):
                    _dict[key] = d_val
                elif not is_ent(d_val) and not is_ent(db_val):
                    _dict[key] = db_val
            elif is_iter(d_val) and is_iter(db_val):
                # Если и то и то списки
                db_val = [(i.get_pk() if is_ent(i) else i) for i in
                          (db_val.select()[:] if hasattr(db_val, 'select') else db_val)]
                _dict[key] = db_val

            elif not is_iter(d_val) and is_iter(db_val):
                pass
            elif is_iter(d_val) and not is_iter(db_val):
                pass


            # if type(db_val) != list and type(db_val) not in db.entities.values() and type(d_val) not in db.entities.values():
            #     _dict[key] = db_val
            #
            # elif type(db_val) == list and all(
            #         (type(i) not in db.entities.values() for i in d_val + db_val)):
            #     _dict[key] = db_val
            #
            # elif type(db_val) != list and type(db_val) in db.entities.values() and type(d_val) not in db.entities.values():
            #     _dict[key] = d_val
            #
            # elif type(db_val) == list and all((type(i) in db.entities.values() for i in db_val)) and all((type(i) not in db.entities.values() for i in d_val)):
            #     _dict[key] = d_val

            if is_iter(_dict[key]) and any((i in ents for i in _dict[key])):
                _dict[key] = [(i.get_pk() if i in ents else i) for i in _dict[key]]

        return _dict

    return decorator