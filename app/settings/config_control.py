# -*- coding: utf-8 -*-

if __name__ == '__main__':
    print('-------------')
    from os import chdir
    from app.settings.config import HOME_DIR, SETTINGS_FILE, EXAMPLE_SETTINGS_FILE

    chdir(HOME_DIR)


def create_new_settings(config_path, example_settings_filename):

    from configparser import ConfigParser

    example_cfg = ConfigParser(allow_no_value=True, converters={'list': lambda x: [i.strip() for i in x.split(',')]})
    example_cfg.read(example_settings_filename)
    user_input_tag = example_cfg.get("settings_ini_file", "user_input_tag")
    print("Config file not found!")
    print(f"I am trying to create {config_path}...")
    print(f"I am coping {example_settings_filename} and rename this to {config_path}")
    with open(f"{example_settings_filename}", "r", encoding="utf-8") as file, open(config_path, 'w',
                                                                                   encoding='utf-8') as wtiten_file:
        print(
            '\n'.join([(''.join([i + input(f"\nВведите пожалуйста {i.replace('=', '').strip()} для своей программы:\n")
                                 for i in filter(bool, string.split(user_input_tag))])
                        if user_input_tag in string and not string.startswith("user_input_tag") else string)
                       for string in iter(file.read().split('\n'))]), file=wtiten_file)


def create_cfg(config_path='',
               example_settings_filename=''):
    import sys
    from configparser import ConfigParser
    from os.path import exists

    if not exists(config_path) and not exists(example_settings_filename):
        print(f"Config file ({config_path}) not found! Exiting!")
        sys.exit(0)
    if not exists(config_path):
        create_new_settings(config_path, example_settings_filename)
    if exists(config_path):
        cfg = ConfigParser(allow_no_value=True, converters={'list': lambda x: [i.strip() for i in x.split(',')]})
        cfg.read(config_path)
    else:
        print("Config not found! Exiting!")
        print(f"I can't create {SETTINGS_FILE}...")
        print(f"You can try cloning {EXAMPLE_SETTINGS_FILE} to {SETTINGS_FILE} and edit params into this")
        sys.exit(0)
    return cfg


def save_change_in_cinfig_file(cfg=None):
    if not cfg:
        cfg = create_cfg(SETTINGS_FILE, EXAMPLE_SETTINGS_FILE)
    with open(SETTINGS_FILE, "w") as config_file:
        cfg.write(config_file)
    return cfg


if __name__ == '__main__':
    print('---------------')
    print(EXAMPLE_SETTINGS_FILE)
    cfg = create_cfg(SETTINGS_FILE, EXAMPLE_SETTINGS_FILE)
