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

    # with db_session:
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


from typing import ForwardRef
from pydantic import BaseModel


Foo = ForwardRef('Foo')
Bar = ForwardRef('Bar')


class Foo(BaseModel):
    a: int = 7
    b: List[Bar] = None


class Bar(BaseModel):
    c: str = "__fgb"
    d: List[Foo] = None


Foo.update_forward_refs()
Bar.update_forward_refs()

print(Foo())
print(Bar(d=[Foo(b=[Bar()])]))