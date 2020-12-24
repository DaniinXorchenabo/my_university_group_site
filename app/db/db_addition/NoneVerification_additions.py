# -*- coding: utf-8 -*-

"""Дополнения к сущности верифификации"""

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *


if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)


@NoneVerification.only_func
def __init__(self, *args, **kwargs):
    if kwargs['it_is_i'] == kwargs['he_verificate_me']:
        print('----------------------------------------------')
        del self
        return
    super(NoneVerification, self).__init__(*args, **kwargs)