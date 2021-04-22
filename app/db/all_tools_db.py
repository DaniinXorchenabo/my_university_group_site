# -*- coding: utf-8 -*-

"""код, который собирает все зависимости, нужные для БД
Именно он применяется для импорта"""

if __name__ == '__main__':
    from os.path import split as os_split
    import sys

    sys.path += [os_split(os_split(os_split(__file__)[0])[0])[0]]


from datetime import date
from datetime import datetime
from datetime import time

from pony.orm import *

from app.settings.config import *
from app.db.entities_modification import (
    Admin, User, DustbiningChat, ImportantChat,
    ImportantMessage, Group, HomeTask, Subject,
    WeekdayAndTimeSubject, ELearningUrl, Event,
    Teacher, SeniorInTheGroup, News, NoneVerification,
    Queue, UserHasQueue, Reminder, SeniorVerification
)
from app.db.pydantic_models_db.pony_orm_to_pydantic_utils import (
    MyGetterDict, BaseModel, check_model
)
from app.db.pydantic_models_db.pydantic_models import (
    PdAdmin, PdUser, PdDustbiningChat, PdImportantChat,
    PdImportantMessage, PdGroup, PdHomeTask, PdSubject,
    PdWeekdayAndTimeSubject, PdELearningUrl, PdEvent,
    PdTeacher, PdSeniorInTheGroup, PdNews, PdNoneVerification,
    PdQueue, PdUserHasQueue, PdReminder, PdSeniorVerification
)
from app.db.pydantic_models_db.pydantic_utils import from_orm
from app.db.tests.create_test_db import create_test_db_1, show_all
from app.db.db_control_func import create_pydantic_models, connect_with_db


if __name__ == '__main__':
    from os import chdir

    create_pydantic_models()

    connect_with_db()
    create_test_db_1()
    show_all()
