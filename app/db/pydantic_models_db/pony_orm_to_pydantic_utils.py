# -*- coding: utf-8 -*-

""" В этом файле содержится код, необходимый для работы
автоматически сгенерированных pydantic-моделей, который не генерируется автоматически
и должен быть импортирован перед импортом автоматически созданных pydantic-моделей"""

from typing import Set as PdSet, Union, List, Dict, Tuple, ForwardRef
from typing import Optional as PdOptional, Callable, Generator, Any
from datetime import date, datetime, time

from pony.orm import *
from pydantic import BaseModel, Json as PdJson, validator, root_validator, Field
from pydantic.utils import GetterDict, display_as_type

from app.db.models import *


class MyGetterDict(GetterDict):
    """Родительский класс для превращения объектов Pony ORM в pydantic-модели"""

    def __init__(self, obj: Any):
        print(obj)
        self._obj = obj.to_dict(with_collections=True)
        self._obj['primary_key'] = obj.get_pk()
        print(self._obj)

    def get(self, key: Any, default: Any = None) -> Any:
        if type(self._obj) == dict:
            print(key, self._obj.get(key, default))
            return self._obj.get(key, default)
        return getattr(self._obj, key, default)


def get_p_k(pd_obj):
    if type(pd_obj) == list:
        return [get_p_k(i) for i in pd_obj]
    if not hasattr(pd_obj, 'Config') or not hasattr(pd_obj.Config, 'my_primaty_key_field'):
        return pd_obj
    pd_obj_dict = dict(pd_obj)
    p_k = [[pd_obj_dict.get(j) for j in (i if type(i) == tuple else [i])] for i in pd_obj.Config.my_primaty_key_field]
    p_k = [i for i in p_k if all((j is not None for j in i))]
    p_k = p_k if bool(p_k) else [[None]]
    p_k = p_k[0]
    return p_k[0] if len(p_k) == 1 else tuple(p_k)


def check_model(cls, values: dict, ent, pk=[], unique=[]):
    """
    Валидатор для проверки наличия такой сущности в БД
    :param values:
    :param ent:
    :param pk:
    :param unique:
    :return:
    """

    def test_p_k(errors=True, val_mode=False, pk=pk, values=values, ent=ent):
        """
        Проверяет, есть ли пользователь с таким(и) Primary key
        :param errors: Если True, то будут подниматься исключения, указанные в assert
        :type errors: bool
        :param val_mode: Если True, то будет возвращен словарь с допустимыми ключами
        :param pk:
        :param values:
        :param ent:
        :returns: bool или dict (смотри :param val_mode:)
        :rtype: list
        """

        data = {i: values[i] for i in pk if (all((j in values for j in i)) and ent.exists(**{j: values[j] for j in i})
                                             if type(i) == tuple else i in values and ent.exists(**{i: values[i]}))}
        assert not errors or bool(data), '''Невозможно получить данные, потому что либо не указан ни один PrimaryKey,
         либо указанного PrimaryKey нет в БД'''
        assert not errors or (len(data) == 1 and not ent.exists(**data)), 'Такого пользователя нет в БД'
        # Данные принадлежат разным пользователям
        assert not errors or (len(data) > 1 and not ent.exists(**data)), 'В БД нет такого пользователя...'
        return data if val_mode else bool(data)

    def test_unique_params(errors=True, unique=unique, values=values, ent=ent):
        """
         Проверяет, есть ли пользователь с такими уникальными параметрами
        :param errors: Если True, то будут подниматься исключения, указанные в assert
        :param unique:
        :param values:
        :param ent:
        :return:
        """

        data = {i: values[i] for i in unique if i in values and ent.exists(**{i: values[i]})}
        assert not errors or bool(data), '''Невозможно получить данные, потому что либо не указан ни один
         парамерт для поиска, либо указанных параметров нет в БД'''
        assert not errors or (len(data) == 1 and not ent.exists(**data)), 'Такого пользователя нет в БД'
        # Данные принадлежат разным пользователям
        assert not errors or (len(data) > 1 and not ent.exists(**data)), 'В БД нет такого пользователя...'
        return bool(data)

    mode_of_operation = values.pop('mode', None)
    upload_orm = values.pop('upload_orm', None)
    p_k = values.pop('primary_key', None)
    p_k = [{j: values.get(j, None) for j in (i if type(i) == tuple else [i])} for i in cls.Config.my_primaty_key_field]
    print('-^^----------------', [p_k], upload_orm, mode_of_operation)

    values = {key: ([] if val == [None] else val) for key, val in values.items()}
    values = {key: val for key, val in values.items()}
    my_required_fields = cls.Config.my_required_fields

    if mode_of_operation == 'new':  # проверяет, можно ли создать такого пользователя
        data = [{param: get_p_k(values[param]) for param in ([i] if type(i) != tuple else i)}
                for i in pk + unique
                if all((p in values for p in ([i] if type(i) != tuple else i)))]
        print('--------')
        values = {key: get_p_k(val) for key, val in values.items()}
        print(values)
        assert all((i in values for i in my_required_fields)), 'Не все обязательные поля заполнены'
        assert all((not ent.exists(**i) for i in data)), \
            f'Следующие параметры уже заняты:' + ', '.join([', '.join(i.keys()) for i in data if ent.exists(**i)])

    elif mode_of_operation == 'edit':  # проверяет, можно ли отредактировать пользователя
        # TODO: Проверить проверку на существование сущностей
        # Поиск в переданных значениях PrimaryKey
        data = [{param: get_p_k(values[param]) for param in ([i] if type(i) != tuple else i)}
                for i in pk
                if all((p in values for p in ([i] if type(i) != tuple else i)))]
        if bool(data):  # Если PrimaryKey был передан
            # Указанные PrimaryKey принадлежат разным сущностям
            assert ent.exists(**{key: val for i in data for key, val in i.items()}), 'Невозможно внести изменения'
            data1 = [{i: get_p_k(values[i])} for i in unique if i in values]
            # Уникальные параметры, которые уже заняты другими пользователями
            no_unique = [i for i in data1 if ent.exists(**i)]

            text = ''
            if len(no_unique) == 1 and len(no_unique[0]) == 1:
                text = f'Такой {list(no_unique[0].keys())[0]} уже занят'
            elif bool(no_unique):
                text = f'Такие {", ".join([", ".join(list(i.keys())) for i in no_unique])} уже заняты'
            assert not bool(no_unique), text
        else:
            # Если PrimaryKey не были переданы,
            # то осуществляем поиск по уникальным параметрам
            data = [{i: get_p_k(values[i])} for i in unique if i in values]
            # не указан ни один из уникальных параметров или PrimaryKey
            assert bool(data), "Невозможность идентификации"
            # Указанные уникальные параметры принадлежат разным сущностям
            assert ent.exists(**{key: val for i in data for key, val in i.items()}), 'Невозможно внести изменения'

    elif mode_of_operation == 'find':
        data = {key: val for key, val in values.items() if val is not None and val != [None] and val != []}
        #  ent.exists почему-то не работает с параметром типа Set
        data = {key: get_p_k(val) for key, val in data.items() if type(val) != list}
        assert ent.exists(**data), 'Данный человек отсутствует в БД'

    elif mode_of_operation == 'strict_find':
        values = {key: ([] if val == [None] else val) for key, val in values.items()}
        #  ent.exists почему-то не работает с параметром типа Set
        data = {key: val for key, val in values.items() if type(val) != list}
        print({key: get_p_k(val) for key, val in data.items()})
        assert ent.exists(**{key: get_p_k(val) for key, val in data.items()}), 'Данный человек отсутствует в БД'

    if upload_orm == 'min':
        # Если хоть один обязательный параметр (или хоть один надор ключей)
        # указан верно, то пользователь будет найден
        # Если указанные уникальные значения принадлежат разным пользователям, то ошибка
        data = {key: val for key, val in values.items() if val is not None and val != [None] and val != []}
        #  ent.exists почему-то не работает с параметром типа Set
        data = {key: get_p_k(val) for key, val in data.items() if type(val) != list}
        print('-@@@@')
        if bool(p_k) and any((all((j is not None for j in i.values())) for i in p_k)):
            # Если был указан primary key
            print('-******')
            p_k = [i for i in p_k if all((j is not None for j in i.values()))]

            testing = [i for i in p_k if ent.exists(**i)]
            # Не удалось найти пользователя, ибо его нет в БД
            assert len(testing) != 0, 'Пользователь не найден'
            # Ошибка, если уникальные параметры принадлежат разным пользователям
            assert len(testing) == 1, 'Пользователь не найден'
            values = dict(cls.from_orm(ent.get(**testing[0])))
            return values
        unique = {i: values.get(i) for i in unique}
        unique = [{key: val} for key, val in unique.items() if val is not None]
        print('---&&&&&&&&&&&&&')
        if bool(unique):
            print('--**&^%', data, unique)
            # Если был указан хоть один уникальный параметр
            testing = [i for i in unique if ent.exists(**i)]
            print(testing)
            # Не удалось найти пользователя, ибо его нет в БД
            assert len(testing) != 0, 'Пользователь не найден'
            if not ent.exists(**reduce(lambda i, j: (i.update(j), i)[1], testing)):
                # Ошибка, если уникальные параметры принадлежат разным пользователям
                assert len(testing) == 1, 'Пользователь не найден'
            print('-8*****')
            values = dict(cls.from_orm(ent.get(**reduce(lambda i, j: (i.update(j), i)[1], testing))))
            print('**&&&&&&&&&&&&&', values)
            return values

    if upload_orm:
        print('upload_orm')
        # Если хоть один параметр указан не верно - ошибка
        print('-----&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        data = {key: val for key, val in values.items() if val is not None and val != [None] and val != []}
        #  ent.exists почему-то не работает с параметром типа Set
        data = {key: get_p_k(val) for key, val in data.items() if type(val) != list}
        assert ent.exists(**data), "Такого пользователя нет в БД"
        values = dict(cls.from_orm(ent.get(**data)))

    print(upload_orm, mode_of_operation)

    return values


def new_init_pydantic(base_init):
    def decorator(self, *args, **kwargs):
        print('BaseModel.__init__')
        new_args = []
        for i in args:
            if hasattr(i, '__class__') and hasattr(i.__class__, '__name__') and i.__class__.__name__ in db.entities:
                kwargs.update(dict(self.__class__.from_orm(i)))
            else:
                new_args.append(i)
        args = new_args
        base_init(self, *args, **kwargs)

    return decorator


BaseModel.__init__ = new_init_pydantic(BaseModel.__init__)