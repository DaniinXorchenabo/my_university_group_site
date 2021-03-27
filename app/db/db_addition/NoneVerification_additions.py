# -*- coding: utf-8 -*-

"""Дополнения к сущности верифификации"""

from datetime import date
from datetime import datetime
from datetime import time

from pony.orm import *

from app.settings.config import *
from app.db.models import NoneVerification


@NoneVerification.only_func
def __init__(self, *args, **kwargs):
    if kwargs['it_is_i'] == kwargs['he_verificate_me']:
        del self
        return
    super(NoneVerification, self).__init__(*args, **kwargs)