# -*- coding: utf-8 -*-

"""Функции для контроля, соединения, миграции БД"""

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *



def controller_migration_version(db_path=DB_PATH, db_l=db):
    """не работает, не использовать"""
    db_l.provider = db_l.schema = None
    db_l.migrate(
        # command='apply --fake-initial',
        migration_dir=MIGRATIONS_DIR,
        allow_auto_upgrade=True,
        # create_tables=True,
        # create_db=True,
        provider=cfg.get("db", "type"),
        filename=db_path)
    print('миграция прошла успешно')
    print('перезапустите программу для дальнейшего использования')
    import sys
    sys.exit()
    # from os.path import isfile
    # version = None
    # if not isfile(join(MIGRATIOMS_DIR, 'controller.txt')):
    #     version = 1
    # else:
    #     with open(join(MIGRATIOMS_DIR, 'controller.txt'), 'r', encoding='utf-8') as f:
    #         version = int(f.read().split()[0])


def make_migrate_file(db_l=db):
    """не работает, не использовать"""
    db_l.migrate(command='make',
                 migration_dir=MIGRATIONS_DIR,
                 # allow_auto_upgrade=True,
                 # create_tables=True,
                 create_db=True,
                 provider=cfg.get("db", "type"),
                 filename=":memory:")
    print('файл миграции создан, осуществляю выход из системы')
    print('чтобы применить миграцию, используйте controller_migration_version()')
    print("""Для этого вам также будет необходимо использовать аргумент командной строки
     apply --fake-initial при запуске кода""")
    import sys
    sys.exit()


def connect_with_db(db_path=DB_PATH, deep=0, db_l=db):
    """
    Создает соединение с БД для Pony ORM версии 0.8
    :param db_path: путь к БД
    :param deep: глубина рекурсии
    :param db_l: объект БД
    :return:
    """
    from os.path import isfile, split, join
    from os import remove, rename
    from sys import exit
    from time import ctime
    from shutil import copy as shutil_copy

    if deep > 5:
        print('в коннекте с базой данных наблюдается большая рекурсия, значит что-то идет не так')
        exit()

    if not isfile(db_path):
        db_l.connect(allow_auto_upgrade=True,
                     create_tables=True,
                     create_db=True,
                     provider=cfg.get("db", "type"),
                     filename=db_path)
        print('create db')
    else:

        try:
            db_l.connect(allow_auto_upgrade=True,
                         provider=cfg.get("db", "type"),
                         filename=db_path)
        except Exception as e:
            print('при создании бд произошла какая-то ошибка (видимо, структура БД была изменена)\n', e)
            print('попытка исправить.....')
            try:
                db_l.connect(allow_auto_upgrade=True,
                             create_tables=True,
                             # create_db=True,
                             provider=cfg.get("db", "type"),
                             filename=db_path)
                print('получилось')
            except Exception as e:
                print("Начинаем миграцию")
                t = ctime().split()[1:]
                t[0], t[1], t[2] = t[2], t[1], t[0]
                copy_name = shutil_copy(db_path, DB_BACKUPS)
                new_name = join(split(copy_name)[0], '_'.join(t).replace(":", "-") + "_" + split(db_path)[1])
                rename(copy_name, new_name)
                print("создан бекап:", new_name)
                print("Удалена исходная база данных, создаём новую")
                remove(db_path)
                # controller_migration_version(db_path)
                print('\n=========================================\n\n\t\tдля создания новой БД перезапустите код.....')
                print('\n=========================================')
                exit()
                # connect_with_db(db_path=db_path, deep=deep + 1)


is_DB_created = connect_with_db


def old_connect_with_db(db_path=DB_PATH, deep=0, db_l=db):
    """
    Создает соединение с БД для Pony ORM версии 0.73
    :param db_path: путь к БД
    :param deep: глубина рекурсии
    :param db_l: объект БД
    :return:
    """
    from os.path import isfile, split, join
    from os import remove, rename
    from sys import exit
    from time import ctime
    from shutil import copy as shutil_copy

    if deep > 5:
        print('в коннекте с базой данных наблюдается большая рекурсия, значит что-то идет не так')
        exit()

    if not isfile(db_path):
        db.bind(provider=cfg.get("db", "type"), filename=db_path, create_db=True)
        db.generate_mapping(create_tables=True)
        print('create db')
    else:

        try:
            db.bind(provider=cfg.get("db", "type"), filename=db_path)
            db.generate_mapping()
        except Exception as e:
            print('при создании бд произошла какая-то ошибка (видимо, структура БД была изменена)\n', e)
            print('попытка исправить.....')
            try:
                db.bind(provider=cfg.get("db", "type"), filename=db_path, create_tables=True, )
                db.generate_mapping()
                print('получилось')
            except Exception as e:
                print("Создаём бекап а затем удаляем БД")
                t = ctime().split()[1:]
                t[0], t[1], t[2] = t[2], t[1], t[0]
                copy_name = shutil_copy(db_path, DB_BACKUPS)
                new_name = join(split(copy_name)[0], '_'.join(t).replace(":", "-") + "_" + split(db_path)[1])
                rename(copy_name, new_name)
                print("создан бекап:", new_name)
                print("Удалена исходная база данных, создаём новую")
                remove(db_path)
                print('\n=========================================\n\n\t\tдля создания новой БД перезапустите код.....')
                print('\n=========================================')
                exit()


def create_pydantic_models(create_file=AUTO_PYDANTIC_MODELS):
    """Генерирует модель pydantic на основе модели Pony ORM"""

    from inspect import getsource
    from typing import Optional, List, Dict, Union, Any, Tuple, ForwardRef
    from pydantic import BaseModel, validator
    from functools import reduce

    CreatePdModels = ForwardRef('CreatePdModels')

    class CreatePdModels(BaseModel):
        """ Олицетворяет одну строку будущего кода"""
        name: Optional[str] = None  # Название параметра
        type_db_param: Optional[str] = None  # Тип параметра, который Optional, PrimaryKey, Required, Set
        type_param: Optional[str] = None  # Настоящий тип параметра (int, str, User, ...)
        default: Optional[str] = None  # Значение по умоолчанию
        code: Union[str, Dict[str, str], None] = ''  # Сгенерированный код строки
        is_primary_key: Optional[bool] = None  # Является ли данный параметр PrimaryKey
        # Неотформатированный тип параметра (int, str, User, ...)
        raw_type_param: Union[str, list, CreatePdModels, None] = None
        raw_name: Optional[str] = None  # Неотформатированное имя параметра
        entity_name: Union[str, list, None] = None  # Имя сущности из БД, тип которой имеет параметр (если имеет)

    class PydanticModel(BaseModel):
        """ Олицетворяет один класс будущего кода"""
        prefix: str = ''  # То, что перед телом класса (к примеру, его имя)
        body: List[Any] = []  # Тело класса (то, что мы создаём)
        postfix: str = ''  # То, что статично в классе и идет после тела (к примеру, класс конфагурации)
        primary_key: Any = None  # Ключевые слова сущности из БД

    def get_aributs(entity, blanks):
        from inspect import getsource

        print([entity])
        code = getsource(entity).split('\n')
        count_tabs = code[0].split('def')[0].count(' ') + 3
        code = (''.join(list(i.split('#')[0])[count_tabs:]) for i in code[1:])
        code = {i.split('=')[0].strip(): i for i in code if '=' in i}
        to_list = [f'"{i}": lambda i: list(i.select()[:]),' for i, c in code.items() if 'Set' in c]
        to_list = blanks + 'modif_type_rules = {' + (('\n' + ('\n' + ' ' * 4 + blanks).join(to_list) + '\n' + blanks)
                                                     if bool(to_list) else '') + '}'
        return to_list

    def create_const_params(work_modes: list) -> str:
        """Возвращает строку с параметрами, одинаковыми для каждой модели"""

        string = '\n\tmode: PdOptional[Union[' + ', '.join(['Literal["' + i + '"]' for i in work_modes]) + ']] = None\n'
        string += '\tupload_orm: PdOptional[Union[bool, Literal["min"]]] = None\n'
        string += '\tprimary_key: Any = None'
        return string

    CreatePdModels.update_forward_refs()
    all_module_code = {}  # Код всего создаваемого модуля
    pr_key_str = []  # тут будут строки с PrimaryKey одного класса
    code = []  # Строки одного класса
    work_modes = ['new', 'edit', 'find', "strict_find"]
    required_fields = dict()

    # Правила обработки типа параметра из модели Pony
    rules_type_param = {
        lambda i: True: lambda i: setattr(i, 'type_param', i.type_param.replace(',', "").strip()),
        lambda i: i.name in ["date", "time"]: lambda i: setattr(i, 'name', 'u_' + i.name),
        lambda i: i.type_param.count("'") > 0 or i.type_param.count('"') > 0:
            lambda i: setattr(i, 'type_param', i.type_param.replace('"', "").replace("'", "")),
    }

    # Правила обработки обязательности или не обязательнояти параметра из модели Pony
    rules_type = {
        lambda i: i.type_db_param == "PrimaryKey":
            lambda i: (setattr(i, 'type_db_param', "Required"), setattr(i, 'is_primary_key', True)),
        lambda i: True: lambda i: setattr(i, 'type_db_param', str(i.type_db_param))
        # lambda i: i.type_db_param == "Optional": lambda i: setattr(i, 'type_db_param', "PdOptional"),
        # lambda i: i.type_db_param == "Set": lambda i: setattr(i, 'type_db_param', "PdSet"),
    }

    # Правила обработки значения по умолчанию из модели Pony
    rules_default = {
        # lambda i: i.type_param in db.entities: lambda i: setattr(i, 'default', None),
        lambda i: i.type_param == "int" and i.default and i.default.replace(
            '"', "").replace("'", "").replace("-", "").isdigit():
            lambda i: setattr(i, 'default', i.default.replace('"', "").replace("'", "")),

        lambda i: i.type_param == "time" and i.default and all(
            (i.isdigit() for i in i.default.replace('"', "").replace("'", "").split(':'))):
            lambda i: setattr(i, 'default',
                              f'''lambda: time({", ".join(i.default.replace('"', "").replace("'", "").split(":"))})'''),
        lambda i: i.type_param in db.entities and i.type_db_param == 'Set': lambda i: setattr(i, 'default', '[None]')

    }

    # Правила превращения в код имени параметра
    name_to_text = {
        lambda i: True: lambda i: setattr(i, 'raw_name', str(i.name)),
        lambda i: True: lambda i: setattr(i, 'name', str(i.name) + ": ")
    }

    # Правила превращения параметра в текст
    type_param_to_text = {
        lambda i: True: lambda i: setattr(i, "raw_type_param", i.raw_type_param or i.type_param),
        lambda i: i.type_param in db.entities: lambda i: (
            setattr(i, 'entity_name', "Pd" + i.type_param), setattr(
                i, 'type_param',
                f"""Union[{'Dict, ' if i.type_param != 'Set'
                else ''}*, Pd{i.type_param}, Dict{', None' if i.type_db_param == 'Set' else ''}]""")),
        lambda i: i.type_param == "Json": lambda i: setattr(i, 'type_param', "PdJson"),
    }

    # Правила превращения в код имени обязательности параметра
    type_db_param_to_text = {
        lambda i: i.type_db_param == "Required" and i.default is None: lambda i: required_fields.update({i.name: i}),
        lambda i: i.type_db_param == "Required": lambda i: setattr(i, 'type_db_param', f'PdOptional[{i.type_param}]'),
        lambda i: i.type_db_param == "Optional": lambda i: setattr(i, 'type_db_param', f'PdOptional[{i.type_param}]'),
        lambda i: i.type_db_param == "Set": lambda i: setattr(i, 'type_db_param', f'PdOptional[List[{i.type_param}]]'),
        # lambda i: i.type_db_param == "Required": lambda
        #     i: f'{i.type_param}{" = " + str(i.default) if i.default else ""}',
        # lambda i: i.type_db_param == "PdOptional": lambda i: f'{i.type_db_param}[{i.type_param}] = {i.default}',
    }

    # Правила превращения в код значения по умолчанию
    default_to_text = {
        lambda i: i.type_param in db.entities: lambda i: setattr(i, 'default', ''),
        lambda i: i.default and bool(i.default): lambda i: setattr(i, 'default', ' = ' + str(i.default)),
        lambda i: i.default is None: lambda i: setattr(i, 'default', ''),
    }

    # Правила превращения PrimaryKey в объекты CreatePdModels
    create_p_k_obj = {
        lambda i: type(i) == list and len(i) > 1: lambda i: [CreatePdModels(type_param=j, raw_type_param=j) for j in i],
        lambda i: type(i) != list: lambda i: CreatePdModels(type_param=i, raw_type_param=i),
        lambda i: type(i) == list and len(i) == 1: lambda i: CreatePdModels(type_param=i[0], raw_type_param=i[0])
    }

    # Обработка PrimaryKey
    rules_p_k = {
        lambda i: type(i) == list: lambda j: [[val(i) for key, val in rules_type_param.items() if key(i)] for i in j],
        lambda i: type(i) != list: lambda i: [val(i) for key, val in rules_type_param.items() if key(i)]
    }

    # Правила обработки PrimaryKey правилами для типа параметра (rules_type_param)
    p_k_to_text = {
        lambda i: type(i) == list: lambda i: CreatePdModels(
            type_param=f'Tuple[' + ", ".join(
                [next(filter(lambda i: i.raw_name == j.type_param, code)).type_param for j in i]) + ']',
            raw_type_param=[j.raw_type_param or j.type_param for j in i]
        ),
        lambda i: type(i) != list and type(i.type_param) == str and '*' not in i.type_param: lambda i: i,
        lambda i: type(i) != list and type(i.type_param) == str and '*' in i.type_param:
            lambda i: CreatePdModels(
                type_param=f'Tuple[' + ", ".join(
                    [j1 for j in i.raw_type_param for j1 in code if j1.raw_name == j]
                ) or ', '.join(i.raw_type_param) + ']',
                raw_type_param=i.raw_type_param
            )
    }

    # Правила формирования типа параметра для элементов сложного типа (к примеру, тип User)
    postcreated_rules = {
        lambda i: i.type_param.count('*') == 1: lambda i: (
            setattr(
                i, 'type_param',
                i.type_param.replace('*', ', '.join(
                    [j.type_param for j in all_module_code['Pd' + i.raw_type_param].primary_key
                     if '*' not in j.type_param]) or '*')
            ),
            [setattr(j, 'type_param', i.type_param) for j in pr_key_str if j.raw_type_param == i.raw_type_param]
            if i.is_primary_key else None),
        lambda i: i.type_param.count('*') > 1: lambda i: print(i)
    }

    # Правила обновления PrimaryKey со сложными параметрами (к примеру, тип User)
    update_p_k = {
        lambda i: '*' in i.type_param and type(i.raw_type_param) == list and not i.entity_name:
            lambda i: setattr(i, 'entity_name', [j.entity_name or j.raw_name for pr in i.raw_type_param
                                                 for j in code if pr.strip() == j.raw_name]),

        lambda i: '*' in i.type_param and type(i.raw_type_param) == list:
            lambda i: (setattr(i, 'type_param', (
                reduce(lambda param, edit: param.replace('*', edit, 1),
                       [i.type_param] + [', '.join([j.type_param for j in (
                           all_module_code[ent].primary_key
                           if ent in all_module_code
                           else [j1 for j1 in code if j1.raw_name == ent]
                       ) if '*' not in j.type_param]) for ent in i.entity_name]
                       )
                if all((
                    '*' not in j.type_param for ent in i.entity_name for j in (
                    all_module_code[ent].primary_key
                    if ent in all_module_code
                    else [j1 for j1 in code if j1.raw_name == ent])))
                else '*'))),
        lambda i: '*' in i.type_param and type(i.raw_type_param) != list:
            lambda i: setattr(i, 'type_param',
                              i.type_param.replace('*', (', '.join(
                                  [j.type_param for j in all_module_code[i.entity_name].primary_key
                                   if '*' not in j.type_param]
                              ) or '*' if all(('*' not in j.type_param for j in
                                               all_module_code[i.entity_name].primary_key)) else '*')))
    }

    code_module = """# -*- coding: utf-8 -*-\n\n\"\"\" Этот код генерируется автоматически,\n"""
    code_module += """ни одно изменение не сохранится в этом файле.\n"""
    code_module += """Тут объявляются pydantic-модели, в которых присутствуют все сущности БД\n"""
    code_module += """и все атрибуты сущностей\"\"\"\n\n"""
    code_module += """from typing import Set as PdSet, Union, List, Dict, Tuple, ForwardRef\n"""
    code_module += """from typing import Optional as PdOptional, Literal, Any\n"""
    code_module += """from datetime import date, datetime, time\n\n"""
    code_module += """from pony.orm import *\n"""
    code_module += """from pydantic import BaseModel, Json as PdJson\n\nfrom app.db.models import *\n\n"""
    code_module += """from app.db.pydantic_models_db.pony_orm_to_pydantic_utils import *\n\n\n"""

    for entity in db.entities:
        code_module += f'Pd{entity} = ForwardRef("Pd{entity}")\n'

    code_module += '\n\n'
    for entity_name, entity in db.entities.items():
        code_module += f"class MyGetterDict{entity_name}(MyGetterDict):\n"
        code_module += get_aributs(entity, '    ') + '\n\n\n'

    for entity_nane, entity in db.entities.items():
        # =======! Парсинг кода из моделей Pony ORM !=======
        pr_key_str = []  # тут будут строки с PrimaryKey
        required_fields = dict()  # Тут будут обязвтельные поля

        code = getsource(entity).split('\n')

        count_tabs = code[0].split('def')[0].count(' ') + 3
        code = [''.join(list(i.split('#')[0])[count_tabs:]) for i in code[1:]]
        unique_params = ["'" + i.split('=')[0].strip() + "'" for i in code if 'unique=True' in i]
        code = (j.split('=') for j in code if bool(j) and (('PrimaryKey' in j and pr_key_str.append(j)) or '=' in j))

        code = (([i[0].strip()] +
                 list((j1.strip() for j in '='.join(i[1:]).strip().replace('(', '#').replace(')', '#').split('#')
                       if bool(j) for j1 in j.split(',')))) for i in code)
        code = (({key: val for key, val in zip(['name', 'type_db_param', 'type_param'], i[:3])},
                 {j[0].strip(): j[1].strip() for j in (j1.split('=') for j1 in i[3:])}) for i in code)
        code = [CreatePdModels(**i[0], **i[1]) for i in code if not print(i)]
        # print(pr_key_str, entity_nane)

        # =======! Обработка кода (к примеру, удаление пробелов) !=======
        [[val(i) for key, val in rules_type_param.items() if key(i)] for i in code]
        [[val(i) for key, val in rules_default.items() if key(i)] for i in code]
        [[val(i) for key, val in rules_type.items() if key(i)] for i in code]

        names_p_k = [('"' + i.split('=')[0].strip() + '"' if '=' in i
                      else ('(' + ', '.join(['"' + j.strip() + '"'
                                             for j in i.split('(')[1].replace(')', '').split(',')]) + ')'))
                     for i in pr_key_str]
        pr_key_str = (list(filter(lambda j: '=' not in j, i.replace(')', '').split('PrimaryKey(')[-1].split(',')))
                      for i in pr_key_str)
        pr_key_str = [[val(i) for key, val in create_p_k_obj.items() if key(i)][0] for i in pr_key_str]

        [[val(i) for key, val in rules_p_k.items() if key(i)] for i in pr_key_str]

        # =======! Превращение кода в текст !=======
        [[val(i) for key, val in name_to_text.items() if key(i)] for i in code]
        [[val(i) for key, val in type_param_to_text.items() if key(i)] for i in code]
        [[val(i) for key, val in default_to_text.items() if key(i)] for i in code]

        pr_key_str = [[val(i) for key, val in p_k_to_text.items() if key(i)][0] for i in pr_key_str]
        [[val(i) for key, val in type_param_to_text.items() if key(i)] for i in pr_key_str]
        # print(pr_key_str)

        postfix = '\n\n'
        postfix += '\t@root_validator\n'
        postfix += "\tdef check_orm_correcting_model(cls, values):\n"
        postfix += f"\t\tprimary_keys = [{', '.join(names_p_k)}]\n"
        postfix += f"\t\tunique_params = [{', '.join(unique_params)}]\n"
        postfix += f"\t\treturn check_model(cls, values, {entity_nane}, pk=primary_keys, unique=unique_params)\n\n"
        postfix += "\tclass Config:\n"
        postfix += "\t\torm_mode = True\n"
        postfix += f"\t\tgetter_dict = MyGetterDict{entity_nane}\n"
        postfix += f"\t\tmy_primaty_key_field = [{', '.join(names_p_k)}]\n"
        postfix += f"\t\tmy_required_fields = [{', '.join(list(required_fields.keys()))}]\n"

        all_module_code['Pd' + entity_nane] = PydanticModel(
            prefix=f'\n\nclass Pd{entity_nane}(BaseModel):\n',
            body=code,
            postfix=postfix,
            primary_key=pr_key_str
        )

    # =======! Обработка сложных типов (к примеру, User) !=======
    for _ in range(10):
        for name_class, body_class in all_module_code.items():
            code = body_class.body
            pr_key_str = body_class.primary_key
            [[val(i) for key, val in postcreated_rules.items() if key(i)] for i in code]
            [[val(i) for key, val in update_p_k.items() if key(i)] for i in pr_key_str]

    # =======! Сборка всего кода в единую строку !=======
    for name_class, body_class in all_module_code.items():
        code = body_class.body
        pr_key_str = body_class.primary_key
        [[val(i) for key, val in type_db_param_to_text.items() if key(i)] for i in code]
        [setattr(i, 'code', f'\t' + i.name + i.type_db_param + i.default) for i in code]

        code_class = body_class.prefix
        code_class += '\n'.join([i.code for i in code])
        code_class += create_const_params(work_modes)
        code_class += body_class.postfix
        code_module += code_class

    code_module += '\n\n'
    for entity in db.entities:
        code_module += f'Pd{entity}.update_forward_refs()\n'
    code_module += "\n\nif __name__ == '__main__':\n\tfrom os import chdir\n\n\tchdir(HOME_DIR)"

    # =======! Запись кода в файл !=======
    with open(create_file, "w", encoding='utf-8') as f:
        print(code_module, file=f)


if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)
    is_DB_created()
