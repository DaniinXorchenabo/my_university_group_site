from arsenic.session import Session, Element

from app.disk.a_exel.utils.actions import ActionChainsSet
from app.disk.a_exel.utils.keyboard import Keys
from app.disk.a_exel.yandex.base_utils import BaseUtils
from app.disk.a_exel.abstractions.cell_utils import AbcCellUtils


__all__ = ["CellUtils"]


class CellUtils(BaseUtils, AbcCellUtils):
    pass

