# -*- coding: utf-8 -*-

"""Собирает все файлы (которые нужны
   для модификации БД), и модифицирует БД"""

from app.settings.config import *
from app.db.db_base_func import *
from app.db.models import *


entities_code = {}  # Тут будет находиться код сущностей БД в удобном виде
for name, ent in db.entities.items():
    ent.__bases__ = (tuple(list(ent.__bases__) + [AddArrtInDbClass])
                     if AddArrtInDbClass not in list(ent.__bases__)
                     else tuple(list(ent.__bases__)))
    entities_code[ent] = db_ent_to_dict(ent)
    entities_code[name] = entities_code[ent]


from app.db.db_addition.user_addition import *
from app.db.db_addition.Group_addition import *
from app.db.db_addition.NoneVerification_additions import *
from app.db.db_addition.Admin_additions import *
from app.db.db_addition.SeniorInTheGroup_additions import *
from app.db.db_addition.SeniorVerification_additions import *


from app.db.pydantic_models_db.pony_orm_to_pydantic_utils import *
from app.db.pydantic_models_db.pydantic_models import *
from app.db.pydantic_models_db.pydantic_utils import *
from app.db.entities_modification_utils import *


for name, ent in db.entities.items():
    # ent.__bases__[0].__init__ = data_from_pydantic_decorator(ent.__bases__[0].__init__, db.entities, entities_code)
    ent.__init__ = data_from_pydantic_decorator(ent.__init__, db.entities, entities_code)

    ent.get = classmethod(ent_get_decorator(ent.get, db.entities, entities_code))
    ent.exists = classmethod(ent_exists_decorator(ent.exists, db.entities, entities_code))
    ent.set = ent_set_decorator(ent.set, db.entities, entities_code)
    ent.to_dict = change_to_dict_method(ent.to_dict)
    setattr(ent, 'cl_set', classmethod(cl_set_creater(ent.set, db.entities, entities_code)))