# -*- coding: utf-8 -*-

"""Дополнения к сущности верификации старосты группы"""

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *
from app.db.db_addition.User_addition import *


if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)


@SeniorVerification.only_func
def __init__(self, *args, **kwargs):
    if kwargs.get('senior_in_the_group') and kwargs.get('user', '') == kwargs.get('senior_in_the_group')._user:
        # староста не может верифицировать сам сабя
        del self
        return
    super(SeniorVerification, self).__init__(*args, **kwargs)