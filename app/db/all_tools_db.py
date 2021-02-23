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
        pass
