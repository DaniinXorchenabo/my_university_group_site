# -*- coding: utf-8 -*-



if __name__ == '__main__':
    from os import chdir, getcwd
    from os.path import split
    print("*"*100)
    dir_ = split(split(getcwd())[0])[0]
    print(dir_)
    print("*" * 100)
    chdir(dir_)
from app.db.all_tools_db import *
from app.bot.base.libs import *
if __name__ == '__main__':
    connect_with_db()
    create_test_db_1()
    #show_all()
    token = cfg.get("vk", "token")
    print(token)
