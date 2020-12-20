# -*- coding: utf-8 -*-

"""код, который собирает все зависимости, нужные для БД
Именно он применяется для импорта"""
from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *
from app.db.db_addition.user_addition import *
from app.db.db_addition.Group_addition import *

from app.db.db_addition.NoneVerification_additions import *
from app.db.db_addition.Admin_additions import *
from app.db.db_addition.SeniorInTheGroup_additions import *
from app.db.tests.create_test_db import *
from app.db.db_control_func import *

# setattr(property, '__iadd__', lambda *a, **k: None)
if __name__ == '__main__':
    from os import chdir



    # class Test:
    #     _ggg = set({1, 2})
    #
    #     @property
    #     def ggg(self):
    #         print('---', self._ggg)
    #         return frozenset(self._ggg)
    #
    #     @ggg.setter
    #     def ggg(self, val):
    #         print('val', val)
    #         print('_ggg', self._ggg)
    #         self._ggg = set(val)
    #         print(self._ggg)

        # def my_iadd(self, val):
        #     print(val)
        #
        # print('^%%%%')
        # setattr(ggg, '__iadd__', my_iadd)
        # print('^%%%%')
        # @ggg.__iadd__
        # def ggg(self, val):
        #     self._ggg |= val

    # test = Test()
    # # test.ggg
    # # test.ggg = {3, 5}
    # test.ggg |= {6, 7}
    chdir(HOME_DIR)
    is_DB_created()
    create_test_db_1()
    show_all()

    with db_session:
        print(Group['20ВП1'].users)
        Group['20ВП1'].users |= {User[101], User[100]}
        print(Group['20ВП1'].users)
        print(Group['20ВП1'].no_verificated_users)
        commit()
        # User[100].is_verificated = False
        print('$')
        # User[105].groups = None
        # commit()
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