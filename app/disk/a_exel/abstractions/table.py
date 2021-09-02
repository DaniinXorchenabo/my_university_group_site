from abc import ABC, abstractmethod
from typing import Type

from app.disk.exel.cells import Cell as PCell, BaseCell, DataTaleType, CollCell
from app.disk.a_exel.utils.actions import ActionChainsSet
from app.disk.a_exel.abstractions.cell import AbcCell


__all__ = ["AbcTable"]


class AbcTable(ABC):

    def __init__(self, size: tuple[int, int] = None, table: DataTaleType = None, target_cell_class: Type[AbcCell] = None):
        assert size is None and table is None
        if table is not None:
            self.size = len(table), max([len(i) for i in table])
            self.table: list[list[AbcCell]] = [[target_cell_class(BaseCell(j, self.size)) for j in i] for i in table]
            self.matrix_size = len(self.table), max([sum([j.size[1] for j in i]) for i in self.table])
            self.matrix_table: list[list[AbcCell]] = [[j for j in i for ind in range(j.size[1])] for i in self.table]
        else:
            self.table = self.matrix_table = [[""] * size[1] for i in range(size[0])]
            self.size = self.matrix_size = size

    @abstractmethod
    async def start(self, *a, **k):
        pass

    @abstractmethod
    async def write_table(self, *a, **k):
        pass

    @abstractmethod
    async def read_table(self, *a, **k):
        pass


