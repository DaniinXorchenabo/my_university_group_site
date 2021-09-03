import asyncio
import sys
from typing import Optional, Union

from arsenic import get_session, browsers, services
# from arsenic.actions import Mouse, chain, Keyboard
from arsenic.session import Session, Element

from app.disk.a_exel.utils.keyboard import Keys
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException, JavascriptException, ElementClickInterceptedException
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.remote.webdriver import WebDriver
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
from app.disk.exel.cells import Cell as ConstructCell, BaseCell, DataTaleType, CollCell
from app.disk.a_exel.utils.actions import ActionChainsSet
from app.disk.a_exel.yandex.table import Table as YandexTable
from app.disk.a_exel.yandex.cell import Cell


if sys.platform.startswith('win'):
    GECKODRIVER = 'geckodriver.exe'
else:
    GECKODRIVER = './geckodriver'


# class YandexTableTools:
#
#     async def start(self, url):
#         self.url = url
#         await self.session.get(url)
#         frame = await self.session.wait_for_element(10, 'iframe[name=frameEditor]')
#         data = await self.session.request(
#             url='/frame',
#             method='POST',
#             data={'id': {"ELEMENT": frame.id, "element-6066-11e4-a52e-4f735466cecf": frame.id}}
#         )
#         reload = False
#         for i in range(5):
#             try:
#                 cell_name = await self.session.wait_for_element(60, 'input[id=ce-cell-name]')
#                 canvas = await self.session.wait_for_element(60, "canvas[id=ws-canvas-graphic-overlay]")
#                 print(await self.session.execute_script("return document.getElementById('ce-cell-name').value;"))
#
#                 break
#             except FileNotFoundError:
#                 reload = True
#                 for i in await self.session.get_elements('button[result=ok]'):
#                     try:
#                         await i.click()
#                     except FileNotFoundError:
#                         pass
#                 await asyncio.sleep(2)
#         if reload is True:
#             # Если в процессе работы высвечиваются окна
#             # о некорректном завершении работы в прошлый раз - перезагружаемся
#             return self.start(url)
#         await (await CellTools.get_active_element(self.session)).send_keys(Keys.ENTER)
#         return None
#
#     async def write_table(self, table: list[list["CellTools"]]):
#         pass


# class VirtualTable(YandexTableTools):
#
#     def __init__(self, size: tuple[int, int] = None, table: DataTaleType = None):
#         assert size is None and table is None
#         if table is not None:
#             self.size = len(table), max([len(i) for i in table])
#             self.table: list[list[Cell]] = [[BaseCell(j, self.size) for j in i] for i in table]
#             self.matrix_size = len(self.table), max([sum([j.size[1] for j in i]) for i in self.table])
#             self.matrix_table: list[list[Cell]] = [[j for j in i for ind in range(j.size[1])] for i in self.table]
#         else:
#             self.table = self.matrix_table = [[""] * size[1] for i in range(size[0])]
#             self.size = self.matrix_size = size


# class YandexTable(VirtualTable):
#
#     def __init__(self, session: Session, size: tuple[int, int] = None, table: DataTaleType = None):
#         super().__init__(size=size, table=table)
#         self.session = session

    # def write_current_table(self):
    #     pass


# class CellTools:

    # @classmethod
    # async def _get_keys_to_cell(cls, session: Session, join_cell_button: Element,
    #                             top_left_cell: str, bottom_right_cell: str):
    #
    #     if (await cls.go_as_walk(session, top_left_cell)) in [False, None]:
    #         actions = ActionChainsSet.click_to_join_element_button(join_cell_button)
    #         await actions.run(session)
    #         await cls.go_as_walk(session, top_left_cell)
    #     keys = await cls.go_as_walk(session, bottom_right_cell)
    #     if keys in [False, None]:
    #         actions = ActionChainsSet.click_to_join_element_button(join_cell_button)
    #         await actions.run(session)
    #         await cls.go_as_walk(session, bottom_right_cell)
    #     reverse_keys = await cls.go_as_walk(session, top_left_cell)
    #     if keys in [False, None]:
    #         keys = await cls.go_as_walk(session, bottom_right_cell)
    #         keys, reverse_keys = reverse_keys, keys
    #         top_left_cell, bottom_right_cell = bottom_right_cell, top_left_cell
    #     return keys, reverse_keys, top_left_cell, bottom_right_cell
    #
    # @classmethod
    # async def rejoin_cells_to_names(cls, session: Session, top_left_cell: str, bottom_right_cell: str):
    #     """Разъеденить указанные ячейки"""
    #     join_cell_button = await cls.get_join_button(session)
    #     table_name_el = await cls.get_current_cell_name_el(session)
    #     keys, _, top_left_cell, bottom_right_cell = await cls._get_keys_to_cell(session, join_cell_button, top_left_cell, bottom_right_cell)
    #     actions1 = ActionChainsSet.join_cell(keys, join_cell_button)
    #     await actions1.run(session)
    #     [(await i.send_keys(Keys.ENTER)) for i in await session.get_elements("button[result=yes]")]
    #
    #     actions2 = ActionChainsSet.go_as_teleport(top_left_cell, table_name_el)
    #     actions2 = ActionChainsSet.click_to_join_element_button(join_cell_button, actions=actions2)
    #     actions2 = ActionChainsSet.go_as_teleport(top_left_cell, table_name_el, actions=actions2)
    #     actions2 += Keys.ENTER
    #     actions2 = ActionChainsSet.click_to_join_element_button(join_cell_button, actions=actions2)
    #     actions2 = ActionChainsSet.go_as_teleport(top_left_cell, table_name_el, actions=actions2)
    #     await actions2.run(session)
    #
    #     return join_cell_button, top_left_cell, bottom_right_cell
    #
    # @classmethod
    # async def join_cells_to_names(cls, session: Session, top_left_cell: str, bottom_right_cell: str):
    #     join_cell_button, top_left_cell, bottom_right_cell = await cls.rejoin_cells_to_names(session, top_left_cell, bottom_right_cell)
    #
    #     keys, _, top_left_cell, bottom_right_cell = await cls._get_keys_to_cell(session, join_cell_button,
    #                                                                             top_left_cell, bottom_right_cell)
    #     actions3 = ActionChainsSet.join_cell(keys, join_cell_button)
    #     await actions3.run(session)

    # @staticmethod
    # def name_to_ind(name: str) -> tuple[int, int, str]:
    #
    #     """ Преобразование имени ячейки форрмата A1 в индексы ячейки (1, 1)
    #     testing:
    #
    #     >>>from itertools import chain
    #     >>>
    #     >>>base = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    #     >>>base2 = [i + j for i in base for j in base]
    #     >>>base3 = [i + j + i1 for i in base for j in base for i1 in base]
    #     >>>for ind, i in enumerate(base + base2 + base3, 1):
    #     >>>    print(ind, i, CellTools.name_to_ind(str(i)))
    #     >>>    assert ind == CellTools.name_to_ind(str(i)[1])
    #
    #     :param name:
    #     :return: первый элемент - индекс по строке (тот, который циферками обозначается в таблице)
    #         Второй элемент - индекс по столбцу (порядковый номер буквы, начиная с единицы)
    #         Третий элемент - Буква (набор букв) ячейки
    #     """
    #
    #     row_index = 1
    #     col_index: list[int] = []
    #     _chars = ""
    #
    #     for ind, char in enumerate(name):
    #         print(char, char.isdigit())
    #         if char.isdigit():
    #             row_index = int(name[ind:])
    #             _chars = name[:ind - 1]
    #             break
    #         col_index.append(ord(char) - 64)
    #     col_index.reverse()
    #     print(col_index)
    #     col_index: int = sum([i * ((ord("Z") - ord("A") + 1) ** ind) for ind, i in enumerate(col_index)])
    #     return (row_index,  # Номер по столбцу. Аналогичен первому индексу в двумерном массиве
    #             col_index,  # Номер по строке. Аналогичен второму индексу в двумерном массиве
    #             _chars)
    #
    # @staticmethod
    # def ind_to_name(col_index: int) -> str:
    #     """Функция получения буквы ячейки по порядковому номеру столбца
    #
    #     testing:
    #     >>>from itertools import chain
    #     >>>
    #     >>>base = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    #     >>>base2 = [i + j for i in base for j in base]
    #     >>>base3 = [i + j + i1 for i in base for j in base for i1 in base]
    #     >>>for ind, i in enumerate(base + base2 + base3, 1):
    #     >>>    print(ind, i, CellTools.ind_to_name(ind))
    #     >>>    assert i == CellTools.ind_to_name(ind)
    #
    #     :param col_index: номер ячейки, начиная с единицы. Если ячейка A124, то number=1
    #     :return: буквенный номер ячейки. Если number=4, то return "D"
    #     """
    #
    #     res = []
    #     while True:
    #         d, m = divmod(col_index, 26)
    #         if m == 0:
    #             m = 26
    #             d -= 1
    #         res.append(m + 64)
    #         if d > 26:
    #             col_index = d
    #         elif 0 < d:  # 0 < d <= 26
    #             res.append(d + 64)
    #             break
    #         else:
    #             break
    #     res.reverse()
    #     return "".join([chr(i) for i in res])
    #
    # # =======! Геттеры !=======
    #
    # @staticmethod
    # async def get_current_cell_name_el(session: Session) -> Element:
    #     return await session.get_element("input[id=ce-cell-name]")
    #
    # @staticmethod
    # async def get_current_cell_name(session: Session):
    #     return await session.execute_script("return document.getElementById('ce-cell-name').value;")

    # @staticmethod
    # async def get_active_element(session: Session) -> Element:
    #     element_id = await session.request("/element/active", "GET")
    #     # print("**************************", element_id)
    #     return session.create_element(element_id)

    # @classmethod
    # async def write_in_clean_table(cls, session: Session, table):
    #     await cls.set_table_structure(session, table)
    #     await cls.write_in_formatted_table(session, table)
    #
    # @classmethod
    # async def set_table_structure(cls, session: Session, table: list[list[Cell]]):
    #     for coll in table:
    #         for cell in coll:
    #             if cell.size[1] > 1:
    #                 pass
    #                 # cls.join_cells_to_names()
    #
    # @classmethod
    # async def write_in_formatted_table(cls, session: Session, table):
    #     pass


# class CellInYandexTable(CellTools, BaseCell):
#     """
#     st_row_index - индекс первой ячейки (если ячейка состоит из некольких ячеек) по столбцу.
#         Аналогичен первому индексу в двумерном массиве.
#         Это та циферка, которая присутствует в номере ячецки
#         (начинается с единицы)
#     st_col_index - индекс первой ячейки (если ячейка состоит из некольких ячеек) в строке.
#         Аналогичен второму индексу в двумерном массиве.
#         Это порядковый номер букавки (начиная с единицы), который присутствует в ячейке
#     st_chars - буквенная часть номера первой ячейки (если ячейка состоит из некольких ячеек)
#     """

    # def __init__(self, names: Union[tuple[int, int], str, list[str]],
    #              session: Session, text="", coll_len=1, row_len=1,
    #              burned_obj: Cell = None):
    #
    #     """
    #
    #     :param names:
    #     :param session:
    #     :param text:
    #     :param coll_len:
    #     :param row_len:
    #     :param burned_obj:
    #     """
    #
    #     if isinstance(names, tuple):
    #         self.st_row_index: int = names[0]  # Номер столбца (тот, что буквами) с единицы
    #         self.st_col_index: int = names[1]  # Номер строки (цифрами) с единицы
    #         self.st_chars: str = self.ind_to_name(self.st_col_index)
    #         self.names: list[str] = [self.st_chars + str(self.st_col_index)]
    #
    #     elif isinstance(names, str):
    #         self.st_row_index, self.st_col_index, self.st_chars = self.name_to_ind(names)
    #         self.names: list[str] = [names]
    #     else:
    #         self.st_row_index, self.st_col_index, self.st_chars = self.name_to_ind(names[0])
    #         self.names = names
    #         self.names.sort(key=lambda i: self.name_to_ind(i)[:2])
    #
    #     self.session = session
    #
    #     if burned_obj is not None:
    #         text = burned_obj.text
    #         coll_len = burned_obj.size[1]
    #         row_len = burned_obj.size[0]
    #     super(BaseCell, self).__init__(text, coll_len, row_len)

    # @property
    # def name(self):
    #     return self.names[0]

    # def join(self):
        # finish_cell = self.ind_to_name(self.st_col_index + self.size[1] - 1) + str(self.st_row_index + self.size[0] - 1)
        # return self.join_cells_to_names(self.session, self.name, finish_cell)


async def write_table(writen_table: DataTaleType):
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    async with get_session(service, browser) as session:
        print("--------------------Session is started")
        y_table = YandexTable(session, size=(5, 5))
        # await y_table.start("https://disk.yandex.ru/i/CUlgJ8bWhBvp7A")
        # test_cell = Cell(session, BaseCell("Работает", (5, 5)), (1, 1))
        # print("------------------------------------------------------", (await test_cell.read()))

        # await CellTools.rejoin_cells_to_names(y_table.session, "A1", "G10")
        # await CellTools.write_in_clean_table(y_table.session, writen_table)
        # search_box = await session.wait_for_element(5, 'input[name=q]')
        # await search_box.send_keys('Cats')
        # await search_box.send_keys(keys.ENTER)
        print("------------------------")
        await asyncio.sleep(1)


def main():
    table = [
        ["С", "По", "Предмет", "Кабинет/Ссылка", "Идентификатор", "Код доступа", "Дата, время обновления ссылки"],
        [CollCell("Понидельник", ConstructCell.C.to_end)],
        ["8:00", "9:35", "Предмет1", "7a-308"],
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(write_table(table))


if __name__ == '__main__':
    # 'C:\\Users\\Acer\\.wdm\\drivers\\geckodriver\\win64\\v0.29.1\\geckodriver.exe'
    main()
    # print(CellTools.name_to_ind("G10"))
