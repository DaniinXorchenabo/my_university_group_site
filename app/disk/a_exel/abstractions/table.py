from abc import ABC, abstractmethod
from typing import Type, Callable, Union

from app.disk.exel.cells import Cell as PCell, BaseCell, DataTaleType, CollCell
from app.disk.a_exel.utils.actions import ActionChainsSet
from app.disk.a_exel.abstractions.cell import AbcCell


__all__ = ["AbcTable"]


class AbcTable(ABC):

    def __init__(self, size: tuple[int, int] = None,
                 table: DataTaleType = None,
                 target_cell_class: Union[Callable[[BaseCell, tuple[int, int]], AbcCell], Type[AbcCell]] = None):
        print("^^111111", size is None,  table is None, )
        assert size is None or table is None, "размер или таблица должны быть заданы явно!"
        print("^^222")
        if table is not None:
            print("^^33")
            self.size = len(table), max([len(i) for i in table])
            self.table: list[list[AbcCell]] = [[target_cell_class(BaseCell(j, self.size), (ind_i, ind_j)) for ind_j, j in enumerate(i, 1)] for ind_i, i in enumerate(table, 1)]
            self.matrix_size = len(self.table), max([sum([j.size[1] for j in i]) for i in self.table])
            self.matrix_table: list[list[AbcCell]] = [[j for j in i for ind in range(j.size[1])] for i in self.table]
        else:
            self.size = self.matrix_size = size
            print("^^44")
            self.table = self.matrix_table = [
                [target_cell_class(BaseCell("", size), (i, j))
                 for j in range(1, size[1] + 1)] for i in range(1, size[0] + 1)]


    @abstractmethod
    async def start(self, *a, **k):
        pass

    # @abstractmethod
    # async def write_table(self, *a, **k):
    #     pass
    #
    # @abstractmethod
    # async def read_table(self, *a, **k):
    #     pass


