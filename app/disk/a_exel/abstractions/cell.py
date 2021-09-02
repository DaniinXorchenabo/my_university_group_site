from abc import ABC, abstractmethod
from typing import Union, Any

from app.disk.exel.cells import BaseCell
from app.disk.a_exel.abstractions.cell_utils import AbcCellUtils
# from app.disk.a_exel

__all__ = ["AbcCell"]


class AbcCell(ABC, AbcCellUtils):

    def __init__(self, abc_cell: BaseCell, names: Union[tuple[int, int], str, list[str]]):
        self.size = abc_cell.size
        self.text = abc_cell.text
        self.table_size = abc_cell.table_size
        [setattr(self, i, getattr(abc_cell, i)) for i in abc_cell.__slots__]

        if isinstance(names, tuple):
            self.st_row_index: int = names[0]  # Номер столбца (тот, что буквами) с единицы
            self.st_col_index: int = names[1]  # Номер строки (цифрами) с единицы
            self.st_chars: str = self.ind_to_name(self.st_col_index)
            self.names: list[str] = [self.st_chars + str(self.st_col_index)]

        elif isinstance(names, str):
            self.st_row_index, self.st_col_index, self.st_chars = self.name_to_ind(names)
            self.names: list[str] = [names]
        else:
            self.st_row_index, self.st_col_index, self.st_chars = self.name_to_ind(names[0])
            self.names = names
            self.names.sort(key=lambda i: self.name_to_ind(i)[:2])

    @abstractmethod
    async def go_to(self, *a, **k):
        pass

    @abstractmethod
    async def read(self, *a, **k):
        pass

    @abstractmethod
    async def write(self, *a, **k):
        pass

    @property
    def name(self):
        return self.names[0]


