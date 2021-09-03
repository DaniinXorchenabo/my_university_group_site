from enum import Enum
from random import random
from time import sleep, time
from typing import Optional, Union

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, JavascriptException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

__all__ = [
    "Cell",
    "CollCell",
    "BigCell",
    "BaseCell",
    "DataTaleType",
    "DataCellType"
]

# class CellFields(object):
#     __slots__ = ["text"]


class Cell(object):
    """Базовый класс для создания схемы таблицы.

    Просто ячейка таблицы, которая может содержать какой-то текст.
    Возможно сюда же будут добавлены стили ячейки, ее размеры и т.д.
    """

    # __slots__ = ()

    class C(Enum):
        """Набор констант для динамического вычисления размера ячеек"""
        to_end = "to_end"  # ячейка длится до конца таблицы

    def __init__(self, text: str):
        self.text = text
        self.size: tuple[Union[int, Cell.C], Union[int, Cell.C]] = (1, 1)


class CollCell(Cell):
    """Класс, который задаёт одну ячейку как объединение нескольких ячеек в линию
    """

    def __init__(self, text: str, coll_len: Union[int, Cell.C]):
        """

        :param text:
        :param coll_len: сколько ячеек в строчку надо объединить
        """
        self.text = text
        self.size: tuple[Union[int, Cell.C], Union[int, Cell.C]] = (1, coll_len)


class BigCell(CollCell):
    """Класс, который задаёт ячейку как объединение нескольких ячеек как в линию, так и в столбец."""

    def __init__(self, text: str,
                 coll_len: Union[int, Cell.C],
                 row_len: Union[int, Cell.C]):
        """

        :param text:
        :param coll_len: сколько ячеек в строчку надо объединить
        :param row_len: сколько ячеек в по столбцу надо объединить
        """
        self.text = text
        self.size: tuple[Union[int, Cell.C], Union[int, Cell.C]] = (row_len, coll_len)


DataTaleType = list[list[Union[str, Cell, tuple[str, int], tuple[str, int, int]]]]
DataCellType = Union[str, Cell, tuple[str, int], tuple[str, int, int]]


class BaseCell(BigCell, CollCell, Cell):
    """Класс-конструктор

    для автоматического преобразования разных типов входных данных
    в единую форму.
    """

    __slots__ = ("table_size", "size", "text")

    def __init__(self, data: DataCellType,
                 table_size: tuple[int, int]):
        """
        :param data: строка, экземпляр класса Cell или его потомков,
            кортеж из строки и размера ячейки по горизонтали
            (сколько ячеек надо будет объединить по горизонтали)
            кортеж из строки и размеров ячейки по горизонтали и по вертикали соответственно
            (сколько ячеек надо будет объединить по горизонтали и по вертикали)
        :param table_size: размер итоговой таблицы
            для вычисления динамических констант из  Cell.C
        """
        print("$$ начал")
        self.table_size = table_size
        if isinstance(data, str):
            Cell.__init__(self, data)
        elif isinstance(data, tuple):
            if len(data) == 2:
                CollCell.__init__(self, *data)
            elif len(data) == 3:
                BigCell.__init__(self, *data)
        if isinstance(self.size[0], Cell.C):
            if self.size[0] == Cell.C.to_end:
                self.size = (table_size[0], self.size[1])
        if isinstance(self.size[1], Cell.C):
            if self.size[1] == Cell.C.to_end:
                self.size = (self.size[0], table_size[1])
        self.size: tuple[int, int]
        print("$$99--------- ок")

