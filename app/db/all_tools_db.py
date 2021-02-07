# -*- coding: utf-8 -*-

"""код, который собирает все зависимости, нужные для БД
Именно он применяется для импорта"""

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.entities_modification import *

from app.db.tests.create_test_db import *
from app.db.db_control_func import *

if __name__ == '__main__':
    from os import chdir

    create_pydantic_models()

    chdir(HOME_DIR)
    is_DB_created()
    create_test_db_1()
    show_all()

    with db_session:
        # m = PdUser(User[100])
        # print(m)
        User(PdUser(id=201, login='201', password='32'))
        print(PdUser(User[201]))
        # print(m.check_verificated)
        # print(Group['20ВП1'].all_group)
        # print(type(m))
        # print(m.__class__)
        # print(m.__class__.__bases__)
        # users = [PdUser.from_orm(User.get(id=i, login=str(i))) for i in range(161, 165)]
        # print(Group(PdGroup(name='20ВП6', users=users)))
        # print(*entities_code.items(), sep='\n\n\n')


        # print(User.get(PdUser(id=125, login='125')))
        # {1: 2}.update()
        # print(reduce(lambda i, j: (i.update(j), i)[1], [{1: 2}]))
        # print(User.cl_set(PdUser(login='Петя1', email='12------58@mail.ru')))
        # print(User[100].email)
        # print(from_orm(m))
        # print(Group.exists(PdGroup(name='20П1', users=Group['20ВП1'].users)))


        # print(Subject(PdSubject(name='ППО_34', group='20ВП1')))
        # print(Subject.get(name='ППО', group='20ВП1'))
        # User(login=130)
        # print(Group.exists(name='20ВП1', users=Group["20ВП1"].users.select()[:]))
        # print(dict(Group["20ВП1"]))
        # print(Group["20ВП1"].senior_in_the_group)
        # print(SeniorInTheGroup[104, '20ВП1'])
        # print(SeniorInTheGroup[User[104], Group['20ВП1']])
        # User(id=120, login='120')
        # new_users = [
        #     User.get(id=i, login=str(i)) for i in range(110, 115)
        # ]
        # print(Group(**dict(PdGroup(
        #     name='20ВП3',
        #     # senior_in_the_group=SeniorInTheGroup[User[104], Group['20ВП1']],  # .get_pk(),
        #     mode='new',
        #     users=new_users,
        #
        #     # upload_orm=True
        # ))))  #
        # print(PdGroup.from_orm(Group['20ВП1']))
        # print(Group['20ВП1'].subjects.select()[:][0].get_pk())
    #     print(PdGroup.from_orm(Group['20ВП1']))
    # print(PdUser.from_orm(User[100]))
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
