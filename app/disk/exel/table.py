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
from app.disk.exel.cells import Cell, CollCell, BigCell, BaseCell


__all__ = [
    "CellInYandexTable",
    "YandexTable",
]


class CellInYandexTable:
    """Работа с конкретной ячецкой в таблице"""

    def __init__(self, driver: WebDriver, i: int = None, j: int = None, name: Union[list[str], str] = None):
        """

        :param driver: драйвер
        :param i: порядковый номер ячейки по вертикали начиная с единицы
        :param j: порядковый номер ячейки по горизонтали начиная с единицы
            (в таблице это обозначается буквой, например: A это 1, F это 6, BD это 56, AAA это 703)
        :param name: Имя ячейки в таблице (Пример: A1, B8, AC13)
        """
        self.driver = driver
        if name is None:
            assert i is not None and j is not None
            self.row_index: int = j  # Номер столбца (тот, что буквами) с единицы
            self.col_index: int = i  # Номер строки (цифрами) с единицы
            self.chars: str = self.ind_to_name(j)
            self.name: list[str] = [self.chars + str(self.col_index)]
        else:
            if isinstance(name, str):
                name = [name]
            self.col_index, self.row_index, self.chars = self.name_to_ind(name[0])
            self.name: list[str] = name

    def read(self, current_driver: WebDriver) -> Union[None, str]:
        """Перейти в ячейку и прочитать данные"""
        correct_cell: bool = self.go_to_cell(current_driver)
        if correct_cell is True:
            return self._read(current_driver)
        return None

    @staticmethod
    def _read(current_driver: WebDriver) -> str:
        """Процесс чтения из текущей ячецки"""
        return CellInYandexTable.get_current_text(None, current_driver)

    def write(self, current_driver: WebDriver, text: str) -> bool:
        """Перейти в ячецку и записать что-то и проверить, что это записалось

        Если не удалось перейти в ячейку - ничего не записываем,
        возвращаем False"""
        correct_cell: bool = self.go_to_cell(current_driver)
        if correct_cell is True:
            self._write(current_driver, text)
            correct_cell_2: bool = self.go_to_cell(current_driver)
            return correct_cell_2 and self.get_current_text(current_driver) == text
        return correct_cell

    @staticmethod
    def _write(current_driver: WebDriver, text: str) -> None:
        """Процесс записи в ячейку"""
        current_driver.switch_to.active_element.send_keys(Keys.BACKSPACE)
        sleep(0.2 + random() * 0.1)
        current_driver.switch_to.active_element.send_keys(text)
        sleep(0.2 + random() * 0.1)
        current_driver.switch_to.active_element.send_keys(Keys.ENTER)

    def go_to_cell(self: Optional['CellInYandexTable'],
                   current_driver: WebDriver = None,
                   cell: Union[str, list[str]] = None):
        """Перейти в ячейку через поле ввода ячейки"""
        if current_driver is None:
            current_driver = self.driver
        if cell is None:
            cell: list[str] = self.name
        elif isinstance(cell, str):
            cell: list[str] = [cell]
        if current_driver.execute_script("""return document.activeElement.id ;""") != "area_id":
            current_driver.find_element_by_id("editor_sdk").click()

        actions = ActionChains(current_driver)
        actions.move_to_element(current_driver.find_elements_by_class_name("ce-group-name")[0])
        actions.click(current_driver.find_element_by_id("ce-cell-name"))
        actions.click(current_driver.find_element_by_id("ce-cell-name"))
        actions.send_keys_to_element(current_driver.find_element_by_id("ce-cell-name"),
                                     *([Keys.BACKSPACE] * 10),
                                     cell[0], Keys.ENTER)
        actions.perform()
        return cell[0] == CellInYandexTable.get_current_cell(self, current_driver)
        # print(driver.execute_script(f'document.getElementById("ce-cell-name").click();'
        #                             f'document.getElementById("ce-cell-name").click();'
        #                             f'document.getElementById("ce-cell-name").value = "{cell}";' +
        #                         '''return (() => {
        #                             var evt = document.createEvent('HTMLEvents');
        #                             evt.initEvent("change", true, true);
        #                             document.getElementById("ce-cell-name").dispatchEvent(evt);
        #                             // document.getElementById("ce-cell-name").submit();
        #                             document.getElementById("ce-cell-name").dispatchEvent(
        #                             new KeyboardEvent("keypress", {view: window, keyCode: 13,
        #                             bubbles: true, cancelable: true}));
        #                             return "done";
        #                             })()}''' + ""
        #                       # '''document.getElementById("ce-cell-name").dispatchEvent(
        #                       #  new KeyboardEvent("keypress", {view: window, keyCode: 13,
        #                       #  bubbles: true, cancelable: true}));'''))
        # exit()
        # driver.switch_to.active_element.send_keys(Keys.ENTER)

    def get_current_cell(self: Optional['CellInYandexTable'], driver: WebDriver) -> str:
        """Функция получения текущей ячейки"""
        if driver is None:
            driver = self.driver
        return driver.execute_script('return document.getElementById("ce-cell-name").value ;')

    def get_current_text(self: Optional['CellInYandexTable'], driver: WebDriver) -> str:
        """Функйия получения текста в текущей ячецке"""
        if driver is None:
            driver = self.driver
        return driver.execute_script('return document.getElementById("ce-cell-content").value ;')

    @staticmethod
    def name_to_ind(name: str) -> tuple[int, int, str]:

        """ Преобразование имени ячейки форрмата A1 в индексы ячейки (1, 1)
        testing:

        >>>from itertools import chain
        >>>
        >>>base = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
        >>>base2 = [i + j for i in base for j in base]
        >>>base3 = [i + j + i1 for i in base for j in base for i1 in base]
        >>>for ind, i in enumerate(base + base2 + base3, 1):
        >>>    print(ind, i, CellInYandexTable.name_to_ind(str(i)))
        >>>    assert ind == CellInYandexTable.name_to_ind(str(i)[1])

        :param name:
        :return: первый элемент - индекс по строке
            Второй элемент - индекс по столбцу (порядковый номер буквы, начиная с единицы)
            Третий элемент - Буква (набор букв) ячейки
        """

        row_index = 1
        col_index: list[int] = []
        _chars = ""
        for ind, char in enumerate(name):
            if char.isdigit():
                row_index = int(name[ind:])
                _chars = name[:ind - 1]
            col_index.append(ord(char) - 64)
        col_index.reverse()
        col_index: int = sum([i * ((ord("Z") - ord("A") + 1) ** ind) for ind, i in enumerate(col_index)])
        return (row_index,  # Номер по столбцу. Аналогичен первому индексу в двумерном массиве
                col_index,  # Номер по строке. Аналогичен второму индексу в двумерном массиве
                _chars)

    @staticmethod
    def ind_to_name(col_index: int) -> str:
        """Функция получения букыф ячейки по порядковому номеру столбца

        testing:
        >>>from itertools import chain
        >>>
        >>>base = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
        >>>base2 = [i + j for i in base for j in base]
        >>>base3 = [i + j + i1 for i in base for j in base for i1 in base]
        >>>for ind, i in enumerate(base + base2 + base3, 1):
        >>>    print(ind, i, CellInYandexTable.ind_to_name(ind))
        >>>    assert i == CellInYandexTable.ind_to_name(ind)

        :param col_index: номер ячейки, начиная с единицы. Если ячейка A124, то number=1
        :return: буквенный номер ячейки. Если number=4, то return "D"
        """

        res = []
        while True:
            d, m = divmod(col_index, 26)
            if m == 0:
                m = 26
                d -= 1
            res.append(m + 64)
            if d > 26:
                col_index = d
            elif 0 < d:  # 0 < d <= 26
                res.append(d + 64)
                break
            else:
                break
        res.reverse()
        return "".join([chr(i) for i in res])

    @classmethod
    def join_cells(cls, cells: list[list['CellInYandexTable']],
                   start: tuple[int, int] = None,
                   end: tuple[int, int] = None) -> list[list['CellInYandexTable']]:
        """Соеденить, слепить, объеденить несколько ячеек в одну.

        :param cells: Весь массив ячеек, который используется в программе
        :param start: индексы в массиве первой ячейки (верхняя левая), которую нужно объеденить
        :param end: индексы в массиве последней ячейки (нижняя правая), которую нужно объеденить
        :return: изменённая таблица. Теперь все объеденённые элементы
            матрицы ячеек ссылаются на левую правую
        """
        assert (start is None and end is None) or (start is not None and end is not None)

        if start is None and end is None:
            start_cell = cells[0][0]
            end_cell = cells[-1][-1]
            for i, coll in enumerate(cells):
                for j, cell in enumerate(coll):
                    if cell.go_to_cell() is False:
                        cell._click_to_join_cell()
                        cells[i][j] = start_cell + cells[i][j]
        else:
            start_cell = cells[start[0]][start[1]]
            end_cell = cells[end[0]][end[1]]
            for i, coll in filter(lambda i: start[0] <= i[0] < end[0], enumerate(cells)):
                for j, cell in filter(lambda i: start[1] <= i[0] < end[1], enumerate(coll)):
                    if cell.go_to_cell() is False:
                        cell._click_to_join_cell()
                        cells[i][j] = start_cell + cells[i][j]
        cls._join_cells(start_cell, end_cell)
        return cells

    def _click_to_join_cell(self):
        """Кликнуть по ячейке кнопкой объеденить

         с целью удостовериться, чтоячецка не была объеденина с другими яцейками.
         Если она была объеденена, то ячейки разъеденятся"""
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element_by_id("id-toolbar-rtn-merge"))
        actions.click(self.driver.find_element_by_id("id-toolbar-rtn-merge"))
        actions.perform()

    @classmethod
    def _join_cells(cls, top_left: "CellInYandexTable", bottom_right: "CellInYandexTable"):
        """Сам процесс объединения ячеек

        :param top_left:
        :param bottom_right:
        :return:
        """

        top_left.go_to_cell()
        top_left._click_to_join_cell()
        top_left.go_to_cell()
        actions = ActionChains(top_left.driver)
        actions.key_down(Keys.SHIFT).send_keys(
            *([Keys.ARROW_RIGHT] * (bottom_right.row_index - top_left.row_index)),
            *([Keys.ARROW_DOWN] * (bottom_right.col_index - top_left.col_index))
        ).key_up(Keys.SHIFT).move_to_element(top_left.driver.find_element_by_id("id-toolbar-rtn-merge"))
        actions.click(top_left.driver.find_element_by_id("id-toolbar-rtn-merge"))
        actions.perform()
        [i.find_element_by_xpath('//button[@result="yes"]').click() for i in
         top_left.driver.find_elements_by_class_name("asc-window")]

    def __add__(self, other: "CellInYandexTable"):
        """ Переопределение метода складывания ячеек"""
        self.name.extend(other.name)
        return self


class YandexTable:
    """Класс для работы с целоя яндекс таблицой"""

    def __init__(self, got_table: list[list[Union[str, Cell]]] = None, size: tuple[int, int] = None):
        """
        :param got_table: - материал для заполнения  таблицы
        :param size: size[0] - количество строк в таблице. size[1] - количество столбцов
        """
        assert got_table is not None or size is not None
        self._start_browser()
        if got_table is not None:
            size: tuple[int, int] = (len(got_table), max([len(i) for i in got_table]))
        self.table = [[CellInYandexTable(self.driver, i, j) for j in range(1, size[1] + 1)]
                      for i in range(1, size[0] + 1)]
        self.got_table = got_table
        # if got_table is not None:
        #     for i, coll in enumerate(got_table):
        #         for j, cell in enumerate(coll):
        #             ob = BaseCell(cell, (len(self.table), len(self.table[0])))
        #             if ob.size != (1, 1):
        #                 CellInYandexTable.join_cells(self.table, (i, j), (i + ob.size[0] - 1, j + ob.size[1] - 1))
        #                 # self.table[i][j]

    def _start_browser(self):
        """Запускаем коннект к таблице"""
        self.yandex_url = "https://disk.yandex.ru/i/CUlgJ8bWhBvp7A"
        self.driver: WebDriver = webdriver.Firefox(GeckoDriverManager().install())
        # driver.implicitly_wait(10) # seconds
        self.driver.get(self.yandex_url)
        self._wait_loaded()
        working_frame = self.driver.find_elements_by_name("frameEditor")[0]
        self.driver.switch_to.frame(working_frame)

    def _wait_loaded(self):
        """Ждём загрузки таблицы"""
        start_time = time()
        for i in range(120):
            try:
                _working_frame = self.driver.find_elements_by_name("frameEditor")[0]
                self.driver.switch_to.frame(_working_frame)
                print(i, round(time() - start_time, 2))
                self.driver.execute_script(
                    f"""return document.getElementById("ce-cell-name").value  + "{i}";""")
                # canvas = driver.find_element_by_id('ws-canvas-graphic-overlay')
                self.driver.switch_to.default_content()
                sleep(5)
                break
            except (NoSuchElementException, IndexError, JavascriptException):  # IndexError
                sleep(0.5)
                self.driver.switch_to.default_content()
        else:
            self.driver.quit()

        _working_frame = self.driver.find_elements_by_name("frameEditor")[0]
        self.driver.switch_to.frame(_working_frame)
        reload = False
        for i in range(5):
            try:
                self.driver.find_element_by_id('ws-canvas-graphic-overlay')
                break
            except NoSuchElementException:
                reload = True
                for i in self.driver.find_elements_by_xpath('//button[@result="ok"]'):
                    try:
                        i.click()
                    except ElementClickInterceptedException:
                        pass
                sleep(2)
        self.driver.switch_to.default_content()
        if reload is True:
            # Если в процессе работы высвечиваются окна
            # о некорректном завершении работы в прошлый раз - перезагружаемся
            self.driver.refresh()
            return self._wait_loaded()

    def write_table(self):
        """Записать таблицу"""
        if self.got_table is not None:
            for i, coll in enumerate(self.got_table):
                for j, cell in enumerate(coll):
                    ob = BaseCell(cell, (len(self.table), len(self.table[0])))
                    if ob.size != (1, 1):
                        self.table = CellInYandexTable.join_cells(self.table, (i, j),
                                                                  (i + ob.size[0] - 1, j + ob.size[1] - 1))
                    # if self.table[i][j].get_current_cell(self.driver) not in self.table[i][j].name:
                    #     self.table[i][j]._click_to_join_cell()
                    self.table[i][j].write(self.driver, ob.text)
                    # self.table[i][j]