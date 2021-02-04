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

    modif_type_rules = dict()

    @staticmethod
    def get_aributs(obj):
        """ На основе класса сущности БД делает словарь вида
        Dict[имя поля: нолноя строка этого поля]"""
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
        """ Выделение из строки вида SeniorInTheGroup[User[104],Group['20ВП1']]
        значений PrimaryKey"""
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
        meta_obj = type('MetaObject', (), dict())()
        code = self.get_aributs(obj)
        [setattr(meta_obj, i, getattr(obj, i)) for i in code]
        [setattr(meta_obj, key, val(getattr(meta_obj, key))) for key, val in self.modif_type_rules.items()]

        db_obj_to_text_utils = {
            lambda i: type(i) == list and any((type(j) in db.entities.values() for j in i)):
                lambda i: [(self.bracket_parser(str(j)) if type(j) in db.entities.values() else j) for j in i],
            lambda i: type(i) != list and type(i) in db.entities.values(): lambda i: self.bracket_parser(str(i))
        }

        def db_obj_to_text_run(i):
            return [setattr(meta_obj, str(i), val(getattr(meta_obj, str(i))))
                    for key, val in db_obj_to_text_utils.items() if key(getattr(meta_obj, str(i)))]

        [db_obj_to_text_run(i) for i in code]
        self._obj = meta_obj

    def get(self, key: Any, default: Any = None) -> Any:
        # print(key, getattr(self._obj, key, default))
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
        print(Group.exists(name='20ВП1'))
        print(data,ent, ent.exists(**data))
        assert ent.exists(**data), 'Данный человек отсутствует в БД'

    elif mode_of_operation == 'strict_find':
        values = {key: ([] if val == [None] else val) for key, val in values.items()}
        assert ent.exists(**values), 'Данный человек отсутствует в БД'

    # if mode_of_operation == 'check':
    #     values = {key: ([] if val == [None] else val) for key, val in values.items()}
    #     assert ent.exists(**values), "Такого пользователя нет в БД"

    # if mode_of_operation == 'pk':  # PrimaryKey
    #     values = {param: values[param] for i in pk if all((p in values for p in ([i] if type(i) != tuple else i))) for param in ([i] if type(i) != tuple else i)}
    #     assert bool(values) and ent.exists(**values), "Такого пользователя нет в БД"  # проверка только по primaryKey

    # if mode_of_operation == 'unique':
    #     # Проверка по всем уникальным параметрам, в том числе и по PrimaryKey, если они есть в наличии
    #     values = {param: values[param] for i in pk + unique if all((p in values for p in ([i] if type(i) != tuple else i))) for
    #               param in ([i] if type(i) != tuple else i)}
    #     assert bool(values) and ent.exists(**values), "Такого пользователя нет в БД"

    # if mode_of_operation == 'any':  # проверяет по всем параметрам, которые не None или [None]
    #     values = {key: val for key, val in values.items() if val is not None and val != [None]}
    #     assert ent.exists(**values), "Такого пользователя нет в БД"



        # assert bool(values), 'Укажите опознавательные знаки'
        # assert not ent.exists(**values), 'Уже существует в БД'
        # assert all((not ent.exists({key: val}) for key, val in values.items())), "Такого пользователя нет в БД"

    # if mode_of_operation == 'edit':
    #     params = {param: values[param] for i in pk if all((p in values for p in ([i] if type(i) != tuple else i))) for
    #               param in ([i] if type(i) != tuple else i)}
    #     params = params if bool(params) else {param: values[param] for i in unique if all((p in values for p in ([i] if type(i) != tuple else i))) for
    #               param in ([i] if type(i) != tuple else i)}
    #     assert bool(params), 'Неудалось найти пользователя для редактирования'
    #     assert all((not ent.exists({key: val}) for key, val in params.items())), "Такого пользователя нет в БД"

    if upload_orm:
        assert ent.exists(**values), "Такого пользователя нет в БД"
        values = ent.get(**values)
    print('456')
    return values


"""
    @root_validator
    def check_orm_correcting_model(cls, values):
        primary_keys = []
        unique_params = []
        return check_model(values, User, pk=primary_keys, unique=unique_params)
"""


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