# -*- coding: utf-8 -*-

"""код, который собирает все зависимости, нужные для БД
Именно он применяется для импорта"""

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *
# from app.db.db_addition.user_addition import *
# from app.db.db_addition.Group_addition import *
#
# from app.db.db_addition.NoneVerification_additions import *
# from app.db.db_addition.Admin_additions import *
# from app.db.db_addition.SeniorInTheGroup_additions import *
# from app.db.db_addition.SeniorVerification_additions import *
from app.db.tests.create_test_db import *
from app.db.db_control_func import *
from app.db.pydantic_models_db.pydantic_models import *


if __name__ == '__main__':
    from os import chdir

    create_pydantic_models()

    chdir(HOME_DIR)
    is_DB_created()
    create_test_db_1()
    show_all()

    # def get_aributs(obj):
    #     from inspect import getsource
    #
    #     entity = obj.__class__
    #     code = getsource(entity).split('\n')
    #
    #     count_tabs = code[0].split('def')[0].count(' ') + 3
    #     code = (''.join(list(i.split('#')[0])[count_tabs:]) for i in code[1:])
    #     code = {i.split('=')[0].strip(): i for i in code if '=' in i}
    #     code = {i: [getattr(entity, i), val] for i, val in code.items()}
    #     to_list = ',\n'.join([f'"{i}": lambda i: i.select()[:]' for i, (t, c) in code.items() if 'Set' in c])
    #     to_list = 'modif_type_rules = {\n' + to_list + '\n}'
    #     print(to_list, sep='\n')
    # print(User.__dict__)
    with db_session:
        print(PdUser.from_orm(User[400]))
        # PdUser(login='Петя1', password="123")
        # User(id=400, name='Петя тестовый', login='Петя тестовый1')
        # commit()
        # obj = User[400]
        # print(getattr(User[400], 'id'))
        #
        # meta_obj = type('MetaObject' + str(MyGetterDict.counter_metaclass), (), dict())()
        # MyGetterDict.counter_metaclass += 1
        # self = MyGetterDictUser
        # code = self.get_aributs(obj)
        # [setattr(meta_obj, i, getattr(obj, i)) for i in code]
        # [setattr(meta_obj, key, val(getattr(meta_obj, key))) for key, val in self.modif_type_rules.items()]
        # [print(getattr(meta_obj, key)) for key, val in self.modif_type_rules.items()]
        # [print(i, [getattr(meta_obj, i)]) for i in code]
        #
        # class Test():
        #     id: int = 234
        #     name: str = 'dfg'
        #     login: str = 'dfgf'
        #     password: str = 'dfgsrf'
        #     email = None
        #     user_has_queues: list = []
        #     session_key_for_app: str = 'dsfs'
        #     getting_time_session_key = None
        #     admin = None
        #     login_EIES: str = 'dfsf'
        #     password_EIES: str = 'fgdsf'
        #     my_verification: list = []
        #     i_verificate_thei: list = []
        #     senior_in_the_group = None
        #     curse_count = None
        #     senior_verification = None
        #     groups = None
        # r = Test()

    #     print(User[100].__dict__)

    # with db_session:
    #     print(Group['20ВП1'].users)
    #     print(User[100].check_password('1234653'))
    #     print(len(User[100]._password), User[100]._password)
    #     print(len(User[100]._get_password), User[100]._get_password)
    #     print(len(User[100]._get_salt_password), User[100]._get_salt_password)
    #     print(len(User[100]._get_key_password), User[100]._get_key_password)
    # print(User[100].password)
    #     print(Group['20ВП1'].users)
    #     Group['20ВП1'].users |= {User[101], User[100]}
    #     print(Group['20ВП1'].users)
    #     print(Group['20ВП1'].no_verificated_users)
    #     commit()
