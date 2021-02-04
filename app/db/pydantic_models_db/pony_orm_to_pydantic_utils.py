# -*- coding: utf-8 -*-

""" В этом файле содержится код, необходимый для работы
автоматически сгенерированных pydantic-моделей, который не генерируется автоматически
и должен быть импортирован перед импортом автоматически созданных pydantic-моделей"""

from typing import Set as PdSet, Union, List, Dict, Tuple, ForwardRef
from typing import Optional as PdOptional, Callable, Generator
from datetime import date, datetime, time

from pony.orm import *
from pydantic import BaseModel, Json as PdJson, validator, root_validator, Field
from pydantic.utils import GetterDict, display_as_type

from app.db.models import *


class MyGetterDict(GetterDict):
    """Родительский класс для превращения объектов Pony ORM в pydantic-модели"""

    def __init__(self, obj: Any):
        self._obj = obj.to_dict(with_collections=True)

    def get(self, key: Any, default: Any = None) -> Any:
        if type(self._obj) == dict:
            # print(key, self._obj.get(key, default))
            return self._obj.get(key, default)
        return getattr(self._obj, key, default)


def check_model(values: dict, ent, pk=[], unique=[]):
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
    values = {key: ([] if val == [None] else val) for key, val in values.items()}
    values = {key: val for key, val in values.items()}

    if mode_of_operation == 'new':  # проверяет, можно ли создать такого пользователя
        data = [{param: values[param] for param in ([i] if type(i) != tuple else i)}
                for i in pk + unique
                if all((p in values for p in ([i] if type(i) != tuple else i)))]
        assert all((not ent.exists(**i) for i in data)),\
            f'Следующие параметры уже заняты:' + ', '.join([', '.join(i.keys()) for i in data if ent.exists(**i)])

    elif mode_of_operation == 'edit':  # проверяет, можно ли отредактировать пользователя
        # Поиск в переданных значениях PrimaryKey
        data = [{param: values[param] for param in ([i] if type(i) != tuple else i)}
                for i in pk
                if all((p in values for p in ([i] if type(i) != tuple else i)))]
        if bool(data):  # Если PrimaryKey был передан
            # Указанные PrimaryKey принадлежат разным сущностям
            assert ent.exists(**{key: val for i in data for key, val in i.items()}), 'Невозможно внести изменения'
            data1 = [{i: values[i]} for i in unique if i in values]
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
            data = [{i: values[i]} for i in unique if i in values]
            # не указан ни один из уникальных параметров или PrimaryKey
            assert bool(data), "Невозможность идентификации"
            # Указанные уникальные параметры принадлежат разным сущностям
            assert ent.exists(**{key: val for i in data for key, val in i.items()}), 'Невозможно внести изменения'

    elif mode_of_operation == 'find':
        data = {key: val for key, val in values.items() if val is not None and val != [None] and val != []}
        #  ent.exists почему-то не работает с параметром типа Set
        data = {key: val for key, val in data.items() if type(val) != list}
        assert ent.exists(**data), 'Данный человек отсутствует в БД'

    elif mode_of_operation == 'strict_find':
        values = {key: ([] if val == [None] else val) for key, val in values.items()}
        #  ent.exists почему-то не работает с параметром типа Set
        data = {key: val for key, val in values.items() if type(val) != list}
        assert ent.exists(**{key: val for key, val in data.items()}), 'Данный человек отсутствует в БД'

    if upload_orm:
        assert ent.exists(**values), "Такого пользователя нет в БД"
        values = ent.get(**values)

    return values

