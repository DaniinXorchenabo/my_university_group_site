# -*- coding: utf-8 -*-

"""Дополнения к админу"""

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *
from app.db.db_addition.user_addition import *


if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)


@Admin.only_func
def __init__(self, *args, **kwargs):
    kwargs['user'].is_verificated = True
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    super(Admin, self).__init__(*args, **kwargs)
