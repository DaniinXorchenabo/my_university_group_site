# -*- coding: utf-8 -*-

"""Код, который модифицирует БД,
   но должен выполняться после импорта pydantic-моделей"""

from typing import Union, Dict, Any, Tuple

from pony.orm.core import MultipleObjectsFoundError

from app.db.db_base_func import set, frozenset, change_field, AddArrtInDbClass, db_ent_to_dict
from app.db.models import *
from app.db.pydantic_models_db.pony_orm_to_pydantic_utils import MyGetterDict, get_p_k, check_model, BaseModel
# from app.db.pydantic_models_db.pydantic_models import *


def primary_key_to_entity(ent: db.Entity, param_name: str, value: Any,
                          entities: Dict[str, db.Entity],
                          entities_code: Dict[Union[str, db.Entity], Tuple[dict, dict]]):
    """
    Преобразует Сущности БД в кортеж с ключами

    :param ent: исходная сущность БД
    :param param_name: имя параметра у исходной сущности
    :param value: значение параметра у исходной сущности БД
    :param entities:type Dict[str, db.Entity]: Словарь со всеми сущностями БД
    :param entities_code: словарь, содержащий код и primaryKey для каждого класса БД
    :return: ключи сущности или список с ключами сущностей или изначальное значение
    """

    if type(value) == list:
        return [i for i in (primary_key_to_entity(ent, param_name, i, entities, entities_code) for i in value) if i]
    code, p_k = entities_code[ent]
    param_type = code[param_name].param_type

    if type(value) == dict and param_type in entities:
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
        value = get_p_k(value)

    if param_type not in entities:
        return value

    if param_type in entities:
        value = [value] if type(value) != tuple else value
        keys = {i: value[ind] for ind, i in enumerate(entities_code[param_type][1])}
        exists_keys = {key: val for key, val in keys.items() if val is not None}
        if not bool(exists_keys):
            return None
        if entities[param_type].exists(**exists_keys):
            return entities[param_type].get(**keys)
        try:
            return entities[param_type](**keys)
        except ValueError as e:
            print(e)
        return None
    return value


def pydantic_obj_parser(ent: db.Entity, args: tuple, kwargs: dict,
                        entities: Dict[str, db.Entity],
                        entities_code: Dict[Union[str, db.Entity], Tuple[dict, dict]]):
    """
    Преобразует входные аргументы в формат сущностей БД

    :param ent: сущность БД, объекты которой парсятся
    :param args: старые переданные аргументы (могут содержать модель )
    :param kwargs: старые переданные авргументы для работы с БД
    :param entities:type Dict[str, db.Entity]: Словарь со всеми сущностями БД
    :param entities_code: словарь, содержащий код и primaryKey для каждого класса БД
    :return: отредактированные args и kwargs
    """

    if args and bool(args):
        for ind, i in enumerate(args):
            if hasattr(i, '__class__') and hasattr(i.__class__, '__bases__') and BaseModel in i.__class__.__bases__:
                pd_values = {key: val for key, val in dict(i).items() if val and bool(val) and val != [None]}
                pd_values = {key: primary_key_to_entity(ent, key, val, entities, entities_code)
                             for key, val in pd_values.items()}
                kwargs.update(pd_values)
                args = list(args)
                del args[ind]
                args = tuple(args)
    return args, kwargs


def data_from_pydantic_decorator(base_init,
                                 entities: Dict[str, db.Entity],
                                 entities_code: Dict[Union[str, db.Entity], Tuple[dict, dict]]
                                 ):
    """
    Декорирует .__init__ сущности БД

    Декорирует __init__ метод сущности БД таким образом, чтобы
    было возможно передавать не только параметры в виде словаря, но и в виде
    модели pydantic. К примеру:
        User(PdUser(id=44524234, login='Петя', name='Вася'))
    или
        @app.get('/test')
        @db_session
        def create_user(user: PdUser):
            return User(user)

    :param base_init: __init__ метод сущности
    :param entities:type Dict[str, db.Entity]: Словарь со всеми сущностями БД
    :param entities_code: словарь, содержащий код и primaryKey для каждого класса БД
    :return: продекорированный __init__ метод сущности"""

    def decorator(self, *args, **kwargs):
        args, kwargs = pydantic_obj_parser(self.__class__, args, kwargs, entities, entities_code)
        base_init(self, *args, **kwargs)

    return decorator


def ent_get_decorator(base_init,
                      entities: Dict[str, db.Entity],
                      entities_code: Dict[Union[str, db.Entity], Tuple[dict, dict]]
                      ):
    """
    Декорирует .get

    Декорирует метод класса сущности БД таким образом, чтобы
    было возможно передавать не только параметры в виде словаря, но и в виде
    модели pydantic. К примеру:
        User.get(PdUser(login='Петя', name='Вася'))
    или
        @app.get('/test')
        @db_session
        def get_user(user: PdUser):
            return User.get(user)

    :param base_init: метод сущности .exists
    :param entities:type Dict[str, db.Entity]: Словарь со всеми сущностями БД
    :param entities_code: словарь, содержащий код и primaryKey для каждого класса БД
    :return: продекорированный метод сущности .get"""

    def decorator(cls, *args, **kwargs):
        args, kwargs = pydantic_obj_parser(cls, args, kwargs, entities, entities_code)
        try:
            return base_init(*args, **kwargs)
        except MultipleObjectsFoundError as e:
            if "Multiple objects were found" in str(e):
                ValueError("Недостаточно данных, чтобы идентифицировать пользователя!")
            MultipleObjectsFoundError(e)

    return decorator


def ent_set_decorator(base_init,
                      entities: Dict[str, db.Entity],
                      entities_code: Dict[Union[str, db.Entity], Tuple[dict, dict]]
                      ):
    """
    Декорирует .set

    Декорирует метод сущности БД таким образом, чтобы
    было возможно передавать не только параметры в виде словаря, но и в виде
    модели pydantic. К примеру:
        User.set(PdUser(login='Петя', name='Вася'))
    или
        @app.get('/test')
        @db_session
        def change_user(user: PdUser):
            values = dict(user)
            values.update(dict(mode='mode_of_operation'))
            user = PdUser(**values)  # Вызовет исключение, если пользователя не существует
            user.set(user)
            return {'ans': "Готово"}

    :param base_init: метод сущности .exists
    :param entities:type Dict[str, db.Entity]: Словарь со всеми сущностями БД
    :param entities_code: словарь, содержащий код и primaryKey для каждого класса БД
    :return: продекорированный метод сущности .exists"""

    def decorator(self, *args, **kwargs):
        args, kwargs = pydantic_obj_parser(self.__class__, args, kwargs, entities, entities_code)
        p_k = [j for i in entities_code[self.__class__][1] for j in ([i] if type(i) != tuple else i)]
        kwargs = {key: val for key, val in kwargs.items() if key not in p_k}
        base_init(self, *args, **kwargs)

    return decorator


def cl_set_creater(base_init,
                   entities: Dict[str, db.Entity],
                   entities_code: Dict[Union[str, db.Entity], Tuple[dict, dict]]):
    """
    Создаёт .cl_set на основе .set

    Создает метод класса, анолагичный методу .set сущности БД,
    который принемает не только ключевые слова или словарь,
    но и модель pydantic. К примеру
        User.cl_set(PdUser(login='Петя', name='Вася'))
    или
        @app.get('/test')
        @db_session
        def change_user(user: PdUser):
            User.cl_set(PdUser)
            return {'ans': "Готово"}

    :param base_init: метод сущности .set
    :param entities:type Dict[str, db.Entity]: Словарь со всеми сущностями БД
    :param entities_code: словарь, содержащий код и primaryKey для каждого класса БД
    :return: продекорированный метод сущности .set для создания метода класса"""

    def decorator(cls, *args, **kwargs):
        new_args = []
        for value in args:
            if hasattr(value, '__class__') and hasattr(  # Если значение является pydantic-объектом
                    value.__class__, '__bases__') and BaseModel in value.__class__.__bases__:
                d_value = dict(value)
                d_value.update(dict(upload_orm='min'))
                d_value = dict(value.__class__(**dict(d_value)))
                d_value.update({key: val for key, val in dict(value).items() if val is not None and val != [None]})
                value = value.__class__(**d_value)
            new_args.append(value)
        args = tuple(new_args)
        args, kwargs = pydantic_obj_parser(cls, args, kwargs, entities, entities_code)
        p_k = [j for i in entities_code[cls][1] for j in ([i] if type(i) != tuple else i)]
        if bool(p_k):
            p_k = {key: kwargs.get(key) for key in p_k}
            p_k = {key: val for key, val in p_k.items() if val}
            if bool(p_k) and cls.exists(**p_k):
                ent = cls.get(**p_k)
                kwargs = {key: val for key, val in kwargs.items() if key not in p_k}
                base_init(ent, *args, **kwargs)

    return decorator


def ent_exists_decorator(base_init,
                         entities: Dict[str, db.Entity],
                         entities_code: Dict[Union[str, db.Entity], Tuple[dict, dict]]):
    """
    Декорирует .exists

    Декорирует метод класса сущности БД таким образом, чтобы
    было возможно передавать не только параметры в виде словаря, но и в виде
    модели pydantic. К примеру:
        User.exists(PdUser(login='Петя', name='Вася'))
    или
        @app.get('/test')
        @db_session
        def is_user(user: PdUser):
            if User.exists(user):
                return {'ans': "да"}

    :param base_init: метод сущности .exists
    :param entities:type Dict[str, db.Entity]: Словарь со всеми сущностями БД
    :param entities_code: словарь, содержащий код и primaryKey для каждого класса БД
    :return: продекорированный метод сущности .exists
    """

    def decorator(cls, *args, **kwargs):
        args, kwargs = pydantic_obj_parser(cls, args, kwargs, entities, entities_code)
        kwargs = {key: val for key, val in kwargs.items() if type(val) != list}
        assert bool(kwargs), 'Ненайдено параметров, необходимых для  однозначной идентификации'
        return base_init(*args, **kwargs)

    return decorator


def change_to_dict_method(base_metod):
    """
    .to_dict() выдает значения с учетом переопределения полей в БД

    Делает так, чтобы метод сущностей .to_dict() возвращал
    значения с учетом переопределения типов в файлах папки app/db/db_addition
    К примеру, вместо хеша пароля будет возвращены "***"
    """

    def is_iter(i) -> bool:
        """ Вернёт True, если объект нужно перебирать циклом"""

        return (hasattr(i, '__iter__') and not type(i) == str) or hasattr(i, 'select')

    def is_ent(i) -> bool:
        """ Вернёт True, если объект принадлежит Pony ORM"""
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

            if is_iter(_dict[key]) and any((i in ents for i in _dict[key])):
                _dict[key] = [(i.get_pk() if i in ents else i) for i in _dict[key]]

        return _dict

    return decorator
