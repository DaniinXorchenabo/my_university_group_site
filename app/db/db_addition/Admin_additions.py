# -*- coding: utf-8 -*-

"""Дополнения к админу"""

from datetime import date
from datetime import datetime
from datetime import time

from pony.orm import *

from app.settings.config import *
from app.db.models import Admin
from app.db.db_addition.User_addition import User


if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)


@Admin.only_func
def __init__(self, *args, **kwargs):
    """
        Переопределяем инициализацию админа

        Если пользователя назначили админом, то он автоматически
        становится верифицированным в своей группе
    """
    kwargs['user'].is_verificated = True
    super(Admin, self).__init__(*args, **kwargs)