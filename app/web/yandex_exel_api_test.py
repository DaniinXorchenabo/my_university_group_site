from time import sleep
from random import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

yandex_url = "https://disk.yandex.ru/i/CUlgJ8bWhBvp7A"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(yandex_url)
print(888888888)
sleep(10)
print("i write")
print(len(_l := driver.find_elements_by_name("frameEditor")), _l)
driver.switch_to.frame(_l[0])
data = [
           ["Расписание на понедельник"],
           ["С", "До", "Аудитория", "Предмет", "Препод", "Ссылка"],
           # ["8:00", "9:35", "7a-308", "Предмет1", "Гурьянов", ""],
           # ["9:50", "10:25", "7a-309", "Предмет2", "Гурьянов", ""],
           # ["10:40", "11:15", "7a-306", "Предмет3", "Гурьянов", ""],
           # ["11:35", "13:15", "7a-322", "Предмет4", "Гурьянов", ""],
           # ["13:45", "15:15", "7a-323", "Предмет5", "Гурьянов", ""],
           # ["15:35", "17:10", "лыжная база", "Предмет6", "Гурьянов", ""],
       ] * 1
# canvas = driver.find_element_by_id('ws-canvas-graphic-overlay')
[([(
    driver.switch_to.active_element.send_keys(Keys.BACKSPACE), sleep(0.2 + random() * 0.1),
    driver.switch_to.active_element.send_keys(cell), sleep(0.2 + random() * 0.1),
    driver.switch_to.active_element.send_keys(Keys.ENTER),
    driver.switch_to.active_element.send_keys(Keys.ARROW_UP),
    # print([driver.find_element_by_id("ce-cell-content").text]),
    print(driver.execute_script("""return document.getElementById("ce-cell-name").value ;"""), end="\t\t"),

    print(driver.execute_script("""return document.getElementById("ce-cell-content").value ;""")),
    driver.switch_to.active_element.send_keys(Keys.ARROW_RIGHT)
) for cell in string],
  driver.switch_to.active_element.send_keys(Keys.ARROW_DOWN),
  driver.switch_to.active_element.send_keys(Keys.HOME)
) for string in data]

driver.switch_to.active_element.send_keys(Keys.ENTER)
