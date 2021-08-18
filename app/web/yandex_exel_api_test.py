from time import sleep, time
from random import random
from typing import Optional, Union

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, JavascriptException, ElementClickInterceptedException, \
ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


# def __wait_loaded(driver):
#     start_time = time()
#     for i in range(120):
#         try:
#             _working_frame = driver.find_elements_by_name("frameEditor")[0]
#             driver.switch_to.frame(_working_frame)
#             print(i, round(time() - start_time, 2))
#             driver.execute_script(
#                 f"""return document.getElementById("ce-cell-name").value  + "{i}";""")
#             # canvas = driver.find_element_by_id('ws-canvas-graphic-overlay')
#             driver.switch_to.default_content()
#             sleep(5)
#             break
#         except (NoSuchElementException, IndexError, JavascriptException):  # IndexError
#             sleep(0.5)
#             driver.switch_to.default_content()
#     else:
#         driver.quit()
#
#     _working_frame = driver.find_elements_by_name("frameEditor")[0]
#     driver.switch_to.frame(_working_frame)
#     for i in range(5):
#         try:
#             driver.find_element_by_id('ws-canvas-graphic-overlay')
#             break
#         except NoSuchElementException:
#             print(len([i.click() for i in driver.find_elements_by_xpath('//button[@result="ok"]')]))
#             # driver.switch_to.active_element.send_key(Keys.ENTER)
#             sleep(5)
#
#     driver.switch_to.default_content()

# yandex_url = "https://disk.yandex.ru/i/CUlgJ8bWhBvp7A"
# driver = webdriver.Chrome(ChromeDriverManager().install())
# # driver.implicitly_wait(10) # seconds
# driver.get(yandex_url)
# __wait_loaded(driver)
# working_frame = driver.find_elements_by_name("frameEditor")[0]
# driver.switch_to.frame(working_frame)


class CellInYandexTable:

    def __init__(self, driver: WebDriver, i: int = None, j: int = None, name: Union[list[str], str] = None):
        self.driver = driver
        if name is None:
            assert i is not None and j is not None
            self.row_index: int = j  # Номер столбца (тот, что буквами) с единицы
            self.col_index: int = i  # Номер строки (цифрами) с единицы
            self.chars: str = self.ind_to_name(j)
            self.name = [self.chars + str(self.col_index)]
        else:
            if isinstance(name, str):
                name = [name]
            self.col_index, self.row_index, self.chars = self.name_to_ind(name[0])
            self.name: list[str] = name

    def read(self, current_driver: WebDriver) -> Union[None, str]:
        correct_cell: bool = self.go_to_cell(current_driver)
        if correct_cell is True:
            return self._read(current_driver)
        return None

    @staticmethod
    def _read(current_driver: WebDriver) -> str:
        return CellInYandexTable.get_current_text(None, current_driver)

    def write(self, current_driver: WebDriver, text: str) -> bool:
        correct_cell: bool = self.go_to_cell(current_driver)
        if correct_cell is True:
            self._write(current_driver, text)
            correct_cell_2: bool = self.go_to_cell(current_driver)
            return correct_cell_2 and self.get_current_text(current_driver) == text
        return correct_cell

    @staticmethod
    def _write(current_driver: WebDriver, text: str) -> None:
        current_driver.switch_to.active_element.send_keys(Keys.BACKSPACE)
        sleep(0.2 + random() * 0.1)
        current_driver.switch_to.active_element.send_keys(text)
        sleep(0.2 + random() * 0.1)
        current_driver.switch_to.active_element.send_keys(Keys.ENTER)

    def go_to_cell(self: Optional['CellInYandexTable'],
                   current_driver: WebDriver = None,
                   cell: Union[str, list[str]] = None):
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
        if driver is None:
            driver = self.driver
        return driver.execute_script('return document.getElementById("ce-cell-name").value ;')

    def get_current_text(self: Optional['CellInYandexTable'], driver: WebDriver) -> str:
        if driver is None:
            driver = self.driver
        return driver.execute_script('return document.getElementById("ce-cell-content").value ;')

    @staticmethod
    def name_to_ind(name: str) -> tuple[int, int, str]:

        """
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
        :return:
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
        return row_index, col_index, _chars

    @staticmethod
    def ind_to_name(number: int) -> str:
        """
        testing:
        >>>from itertools import chain
        >>>
        >>>base = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
        >>>base2 = [i + j for i in base for j in base]
        >>>base3 = [i + j + i1 for i in base for j in base for i1 in base]
        >>>for ind, i in enumerate(base + base2 + base3, 1):
        >>>    print(ind, i, CellInYandexTable.ind_to_name(ind))
        >>>    assert i == CellInYandexTable.ind_to_name(ind)

        :param number: номер ячейки, начиная с единицы. Если ячейка A124, то number=1
        :return: буквенный номер ячейки. Если number=4, то return "D"
        """

        res = []
        while True:
            d, m = divmod(number, 26)
            if m == 0:
                m = 26
                d -= 1
            res.append(m + 64)
            if d > 26:
                number = d
            elif 0 < d:  # 0 < d <= 26
                res.append(d + 64)
                break
            else:
                break
        res.reverse()
        return "".join([chr(i) for i in res])

    @classmethod
    def join_cells(cls, cells: list[list['CellInYandexTable']]):
        return cls._join_cells(cells[0][0], cells[-1][-1])

    def _click_to_join_cell(self, old_actions: ActionChains = None):
        if old_actions is None:
            actions = ActionChains(self.driver)
        else:
            actions = old_actions
        actions.move_to_element(self.driver.find_element_by_id("id-toolbar-rtn-merge"))
        actions.click(self.driver.find_element_by_id("id-toolbar-rtn-merge"))
        if old_actions is None:
            actions.perform()

    @classmethod
    def _join_cells(cls, top_left: "CellInYandexTable", bottom_right: "CellInYandexTable"):
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


class YandexTable:

    def __init__(self, got_table: list[list[str]] = None, size: tuple[int, int] = None):
        """

        :param size: size[0] - количество строк в таблице. size[1] - количество столбцов
        """
        assert got_table is not None or size is not None
        self._start_browser()
        if got_table is not None:
            size: tuple[int, int] = (len(got_table), max([len(i) for i in got_table]))
        self.table = [[CellInYandexTable(self.driver, i, j) for j in range(1, size[1] + 1)] for i in range(1, size[0] + 1)]

    def _start_browser(self):
        self.yandex_url = "https://disk.yandex.ru/i/CUlgJ8bWhBvp7A"
        self.driver: WebDriver = webdriver.Chrome(ChromeDriverManager().install())
        # driver.implicitly_wait(10) # seconds
        self.driver.get(self.yandex_url)
        self._wait_loaded()
        working_frame = self.driver.find_elements_by_name("frameEditor")[0]
        self.driver.switch_to.frame(working_frame)

    def _wait_loaded(self):
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
        for i in range(5):
            try:
                self.driver.find_element_by_id('ws-canvas-graphic-overlay')
                break
            except NoSuchElementException:
                for i in self.driver.find_elements_by_xpath('//button[@result="ok"]'):
                    try:
                        i.click()
                    except ElementClickInterceptedException:
                        pass
                sleep(5)

        self.driver.switch_to.default_content()


table = YandexTable(size=(7, 7))

data = [
           ["Расписание на понедельник"],
           # ["С", "До", "Аудитория", "Предмет", "Препод", "Ссылка"],
           # ["8:00", "9:35", "7a-308", "Предмет1", "Гурьянов", ""],
           # ["9:50", "10:25", "7a-309", "Предмет2", "Гурьянов", ""],
           # ["10:40", "11:15", "7a-306", "Предмет3", "Гурьянов", ""],
           # ["11:35", "13:15", "7a-322", "Предмет4", "Гурьянов", ""],
           # ["13:45", "15:15", "7a-323", "Предмет5", "Гурьянов", ""],
           # ["15:35", "17:10", "лыжная база", "Предмет6", "Гурьянов", ""],
       ] * 1

canvas = table.driver.find_element_by_id('ws-canvas-graphic-overlay')
print(table.driver.execute_script("""return document.activeElement.id ;"""))
# sleep(1)
table.driver.switch_to.active_element.send_keys(Keys.ENTER)
print(table.driver.execute_script("""return document.activeElement.id ;"""))
# sleep(1)
table.driver.find_element_by_id("editor_sdk").click()

CellInYandexTable.go_to_cell(None, table.driver, "D5")

CellInYandexTable.join_cells([i[2:5] for i in table.table[1:4]])

