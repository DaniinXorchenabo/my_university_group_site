import asyncio
import sys
from itertools import chain as itertools_chain
from random import random
from time import sleep, time
from typing import Optional, Union

from arsenic import get_session, browsers, services
from arsenic.actions import Mouse, chain, Keyboard
from arsenic.session import Session, Element

from app.disk.a_exel.keyboard import Keys
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException, JavascriptException, ElementClickInterceptedException
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.remote.webdriver import WebDriver
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
from app.disk.exel.cells import Cell, BaseCell

if sys.platform.startswith('win'):
    GECKODRIVER = 'geckodriver.exe'
else:
    GECKODRIVER = './geckodriver'

try:

    class OldCellInYandexTable:
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


    class OldYandexTable:
        """Класс для работы с целоя яндекс таблицой"""

        def __init__(self, got_table: list[list[Union[str, Cell]]] = None, size: tuple[int, int] = None,
                     url="https://disk.yandex.ru/i/CUlgJ8bWhBvp7A"):
            """
            :param got_table: - материал для заполнения  таблицы
            :param size: size[0] - количество строк в таблице. size[1] - количество столбцов
            """
            assert got_table is not None or size is not None
            self.yandex_url = url
            # self._start_browser()
            if got_table is not None:
                size: tuple[int, int] = (len(got_table), max([len(i) for i in got_table]))
            self.table = [[CellInYandexTable(self.driver, i, j) for j in range(1, size[1] + 1)]
                          for i in range(1, size[0] + 1)]
            self.got_table = got_table
            self.service = services.Geckodriver(binary=GECKODRIVER)
            self.browser = browsers.Firefox()

        def _start_browser(self):
            """Запускаем коннект к таблице"""
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

except Exception:
    pass


class CellInYandexTable:
    how_to_move = ["teleport", "walk"][1]

    @classmethod
    async def go_to(cls, *args, how_to_move: str = None, **kwargs):
        """Общий метод перемещения. Зависит от настроек класса"""
        if how_to_move is None:
            how_to_move = cls.how_to_move
        if how_to_move == "teleport":
            return cls.go_as_teleport(*args, **kwargs)
        else:
            pass

    @classmethod
    async def go_as_teleport(cls, session: Session, where: str):
        table_name_el = await cls.get_cell_name_el(session)
        mouse = Mouse()
        keyboard = Keyboard()
        actions = chain(
            mouse.move_to(table_name_el),
            mouse.down(),
            mouse.up(),
            mouse.down(),
            mouse.up(),
            *itertools_chain(([keyboard.down(Keys.BACKSPACE),
                               keyboard.up(Keys.BACKSPACE)] * 10
                              ) + [func(i) for i in list(where)
                                   for func in [keyboard.down, keyboard.up]]
                             ),
            keyboard.down(Keys.ENTER), keyboard.up(Keys.ENTER)
        )

        await session.perform_actions(actions)
        return (await cls.get_cell_name(session)) == where

    @classmethod
    async def go_as_walk(cls, session: Session, where: str):
        *where_ind, _ = cls.name_to_ind(where)
        last_ind = (None, None)
        # reverse in [0, 2] - идем сначала вниз (или вверх),
        #                       а потом вправо (или влево)
        # reverse in [1, 3] - идем сначала влево (или вправо),
        #                       а потом вверх (или вниз)
        reverse: Union[int, str] = 0

        def how_key(now: str, finish: str, last: Optional[str] = None) -> Optional[str]:
            nonlocal where_ind, last_ind, reverse
            *now_ind, _ = cls.name_to_ind(now)

            def left_or_right():
                nonlocal where_ind, now_ind, last_ind
                return Keys.ARROW_RIGHT if now_ind[1] < where_ind[1] else Keys.ARROW_LEFT

            def up_or_down():
                nonlocal where_ind, now_ind, last_ind
                return Keys.ARROW_DOWN if now_ind[0] < where_ind[0] else Keys.ARROW_UP

            # key = ""
            # если выделенная ячейка
            # находится в одной строке с целевой ячецкой
            if reverse > 20:
                return None
            elif reverse > 3:
                if now_ind[0] == where_ind[0]:
                    key = left_or_right()
                elif now_ind[1] == where_ind[1]:
                    key = up_or_down()
                else:
                    if reverse % 2 == 0:
                        key = left_or_right()
                    else:
                        key = up_or_down()
                    reverse += 1
            if reverse % 2 == 1:
                if now_ind[1] == where_ind[1]:
                    key = up_or_down()
                else:
                    if last_ind[0] is None or \
                            last_ind[0] <= now_ind[0] < where_ind[0] or \
                            where_ind[0] < now_ind[0] <= last_ind[0]:

                        key = left_or_right()
                    else:
                        reverse += 1
                        return how_key(now, finish, last)
                last_ind = now_ind
            elif reverse % 2 == 0:
                if now_ind[0] == where_ind[0]:
                    key = left_or_right()
                else:
                    if last_ind[1] is None or \
                            last_ind[1] <= now_ind[1] < where_ind[1] or \
                            where_ind[1] < now_ind[1] <= last_ind[1]:
                        key = up_or_down()
                    else:
                        reverse += 1
                        return how_key(now, finish, last)
            last_ind = now_ind
            return key

        last_cell = None
        while True:
            now_cell = await cls.get_cell_name(session)
            if now_cell == where:
                last_ind = (None, None)
                last_cell = None
                # el = await cls.get_active_element(session)
                # return True
            elif (key := how_key(now_cell, where, last_cell)) is not None:
                print(key)
                el = await cls.get_active_element(session)
                await el.send_keys(key)
                last_cell = now_cell
                # await cls.send_keys_to_active_element(session, key)
            else:
                return await cls.go_as_teleport(session, where)


    @classmethod
    async def join_cells_to_names(cls, session: Session, top_left_cell: str, bottom_right_cell: str):
        element = await cls.go_as_teleport(session, top_left_cell)
        # session.

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
            print(char, char.isdigit())
            if char.isdigit():
                row_index = int(name[ind:])
                _chars = name[:ind - 1]
                break
            col_index.append(ord(char) - 64)
        col_index.reverse()
        print(col_index)
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

    # =======! Геттеры !=======

    @staticmethod
    async def get_cell_name_el(session: Session) -> Element:
        return await session.get_element("input[id=ce-cell-name]")

    @staticmethod
    async def get_cell_name(session: Session):
        return await session.execute_script("return document.getElementById('ce-cell-name').value;")

    @staticmethod
    async def get_active_element(session: Session) -> Element:
        element_id = await session.request("/element/active", "GET")
        print("**************************", element_id)
        return session.create_element(element_id)

    @classmethod
    async def send_keys_to_active_element(cls, session: Session, value: Union[str, list[str, Keys, int]]) -> Element:
        print([cls.keys_to_typing(value), value])
        return await session.request(
            "/keys", method="POST",
            data={"value": (_list := cls.keys_to_typing(value)),
                  "text": "".join(_list)})

    @staticmethod
    def keys_to_typing(value) -> list:
        """ Copy paste from Selenium

        Processes the values that will be typed in the element."""

        typing = []
        for val in value:
            if isinstance(val, Keys):
                typing.append(val)
            elif isinstance(val, int):
                val = str(val)
                for i in range(len(val)):
                    typing.append(val[i])
            else:
                for i in range(len(val)):
                    typing.append(val[i])
        return typing


class YandexTableTools:

    def __init__(self, session: Session):
        self.session = session
        self.url = None

    async def start(self, url):
        self.url = url
        await self.session.get(url)
        frame = await self.session.wait_for_element(10, 'iframe[name=frameEditor]')
        data = await self.session.request(
            url='/frame',
            method='POST',
            data={'id': {"ELEMENT": frame.id, "element-6066-11e4-a52e-4f735466cecf": frame.id}}
        )
        reload = False
        for i in range(5):
            try:
                cell_name = await self.session.wait_for_element(60, 'input[id=ce-cell-name]')
                canvas = await self.session.wait_for_element(60, "canvas[id=ws-canvas-graphic-overlay]")
                print(await self.session.execute_script("return document.getElementById('ce-cell-name').value;"))

                break
            except FileNotFoundError:
                reload = True
                for i in await self.session.get_elements('button[result=ok]'):
                    try:
                        await i.click()
                    except FileNotFoundError:
                        pass
                await asyncio.sleep(2)
        if reload is True:
            # Если в процессе работы высвечиваются окна
            # о некорректном завершении работы в прошлый раз - перезагружаемся
            return self.start(url)
        await (await CellInYandexTable.get_active_element(self.session)).send_keys(Keys.ENTER)
        return None

    async def write_table(self, table: list[list[CellInYandexTable]]):
        pass


async def write_table():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    async with get_session(service, browser) as session:
        y_table = YandexTableTools(session)
        await y_table.start("https://disk.yandex.ru/i/CUlgJ8bWhBvp7A")
        await CellInYandexTable.go_as_walk(y_table.session, "G10")
        # search_box = await session.wait_for_element(5, 'input[name=q]')
        # await search_box.send_keys('Cats')
        # await search_box.send_keys(keys.ENTER)
        print("------------------------")
        await asyncio.sleep(60)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(write_table())


if __name__ == '__main__':
    # 'C:\\Users\\Acer\\.wdm\\drivers\\geckodriver\\win64\\v0.29.1\\geckodriver.exe'
    main()
    # print(CellInYandexTable.name_to_ind("G10"))
