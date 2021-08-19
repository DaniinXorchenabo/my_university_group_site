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
from app.disk.exel.table import CellInYandexTable, YandexTable


table = YandexTable([
    ["С", "По", "Предмет", "Кабинет/Ссылка", "Идентификатор", "Код доступа", "Дата, время обновления ссылки"],
    [CollCell("Понидельник", Cell.C.to_end)],
    ["8:00", "9:35", "Предмет1", "7a-308"],
])
table.write_table()

# data = [
#            ["Расписание на понедельник"],
#            # ["С", "До", "Аудитория", "Предмет", "Препод", "Ссылка"],
#            # ["8:00", "9:35", "7a-308", "Предмет1", "Гурьянов", ""],
#            # ["9:50", "10:25", "7a-309", "Предмет2", "Гурьянов", ""],
#            # ["10:40", "11:15", "7a-306", "Предмет3", "Гурьянов", ""],
#            # ["11:35", "13:15", "7a-322", "Предмет4", "Гурьянов", ""],
#            # ["13:45", "15:15", "7a-323", "Предмет5", "Гурьянов", ""],
#            # ["15:35", "17:10", "лыжная база", "Предмет6", "Гурьянов", ""],
#        ] * 1
# table = YandexTable(size=(7, 7))
# canvas = table.driver.find_element_by_id('ws-canvas-graphic-overlay')
# print(table.driver.execute_script("""return document.activeElement.id ;"""))
# sleep(1)
# table.driver.switch_to.active_element.send_keys(Keys.ENTER)
# print(table.driver.execute_script("""return document.activeElement.id ;"""))
# sleep(1)
# table.driver.find_element_by_id("editor_sdk").click()

# CellInYandexTable.go_to_cell(None, table.driver, "D5")

# CellInYandexTable.join_cells([i[1:5] for i in table.table[1:4]])
# CellInYandexTable.join_cells(table.table, (1, 1), (3, 4))

