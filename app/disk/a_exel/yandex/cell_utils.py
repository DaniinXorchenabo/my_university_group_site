from arsenic.session import Session, Element

from app.disk.a_exel.utils.actions import ActionChainsSet
from app.disk.a_exel.utils.keyboard import Keys
from app.disk.a_exel.yandex.base_utils import BaseUtils
from app.disk.a_exel.abstractions.cell_utils import AbcCellUtils


__all__ = ["CellUtils"]


class CellUtils(BaseUtils, AbcCellUtils):

    # =======! Геттеры !=======

    @staticmethod
    async def get_cell_name_el(session: Session) -> Element:
        return await session.get_element("input[id=ce-cell-name]")

    @staticmethod
    async def get_cell_name(session: Session):
        return await session.execute_script("return document.getElementById('ce-cell-name').value;")

