# -*- coding: utf-8 -*-

if __name__ == '__main__':
    from os.path import split as os_split
    import sys
    sys.path += [os_split(os_split(os_split(__file__)[0])[0])[0]]

from app.db.all_tools_db import *
from app.bot.base.libs import *
if __name__ == '__main__':
    connect_with_db()
    create_test_db_1()
    #show_all()
    token = cfg.get("vk", "token")
    print(token)
