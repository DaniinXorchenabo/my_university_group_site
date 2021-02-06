# -*- coding: utf-8 -*-

""" Содержит функции, позволяющие удобнее работать
с автоматически генерируемыми pydantic-моделями"""

from typing import Set as PdSet, Union, List, Dict, Tuple, ForwardRef
from typing import Optional as PdOptional
from datetime import date, datetime, time

from pony.orm import *
from pydantic import BaseModel, Json as PdJson

from app.db.models import *
from app.db.pydantic_models_db.pony_orm_to_pydantic_utils import *
from app.db.pydantic_models_db.pydantic_models import *


def from_orm(ent: db.Entity):
    """Создает из сущности Pony ORM pydantic-модель"""
    return eval('Pd' + ent.__class__.__name__).from_orm(ent)