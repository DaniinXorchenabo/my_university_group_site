# -*- coding: utf-8 -*-

"""Тут находятся функции для работы с .ini файлом"""

from os.path import exists

from configparser import ConfigParser


def create_new_settings(config_path, example_settings_filename):
    """
    Создаёт файл конфига из примера конфига

    Недостабщие данные запрашиваются у пользователя через терминал.
    Эта функция не должна вызываться за пределами этого файла
    """

    example_cfg = ConfigParser(allow_no_value=True, converters={'list': lambda x: [i.strip() for i in x.split(',')]})
    example_cfg.read(example_settings_filename)
    user_input_tag = example_cfg.get("settings_ini_file", "user_input_tag")
    print("Config file not found!")
    print(f"I am trying to create {config_path}...")
    print(f"I am coping {example_settings_filename} and rename this to {config_path}")

    # =======! Получение данных от пользователя !=======
    with open(f"{example_settings_filename}", "r", encoding="utf-8") as file:
        data = []
        for string in iter(file.read().split('\n')):
            if user_input_tag in string and not string.startswith("user_input_tag"):
                user_data = input(f"\nВведите пожалуйста {string.replace('=', '').strip()} для своей программы:\n")
                user_data = string.replace(user_input_tag, user_data.strip())
                data.append(user_data)
            else:
                data.append(string)

    # =======! Запись данных в файл !=======
    with open(config_path, 'w', encoding='utf-8') as writen_file:
        data = '\n'.join(data)
        print(data, file=writen_file)


def create_cfg(config_file: str, example_settings_filename: str) -> ConfigParser:
    """ Создаёт объект конфига (привязанный к файлу конфига)"""

    if not exists(config_file) and not exists(example_settings_filename):
        print(f"Config file ({config_file}) not found! Exiting!")
        exit()
    if not exists(config_file):
        create_new_settings(config_file, example_settings_filename)

    cfg = ConfigParser(allow_no_value=True, converters={'list': lambda x: [i.strip() for i in x.split(',')]})
    cfg.read(config_file)
    return cfg


def save_change_in_config_file(config_file: str, example_settings_filename: str,
                               config: ConfigParser = None) -> ConfigParser:
    """ Сохраняет изменения в конфиг-файле"""

    if not config:
        config = create_cfg(config_file, example_settings_filename)
    with open(config_file, "w") as config_file:
        config.write(config_file)
    return config
