# -*- coding: utf-8 -*-

"""код, который собирает все зависимости, нужные для БД
Именно он применяется для импорта"""
from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *
from app.db.db_addition.Group_addition import *
from app.db.db_addition.user_addition import *
from app.db.db_addition.NoneVerification_additions import *
from app.db.db_addition.Admin_additions import *
from app.db.db_addition.SeniorInTheGroup_additions import *
from app.db.tests.create_test_db import *
from app.db.db_control_func import *

if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)
    is_DB_created()
    create_test_db_1()
    show_all()

    with db_session:
        print('&^')
        User[100].is_verificated = False
        print('$')
        # User[105].groups = None
        commit()
        # User[105].is_verificated = False
        # print(User[105].groups, User[105].is_verificated)
        # print('3')
        # User._groups = User.groups
        # User.groups = None
        # print(User[103]._groups, User[103].groups)
    #     print(User[103].is_verificated, User[103].groups, User[103].id)
    #     print(User[101].is_verificated, User[101].groups, User[101].id)
    #     print(User[105].is_verificated, User[105].groups, User[105].id)
        # print(Group['20ВП1'].get_teachers_data)