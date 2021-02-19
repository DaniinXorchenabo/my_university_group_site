from flask import Flask, request
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import json
import datetime
from app.db.all_tools_db import *
from app.bot.base.libs import *

raspisanie_par = """1 Пара - 8:00-9:35
2 Пара - 9:50-11:25
3 Пара - 11:40-13:15
4 Пара - 13:45-15:20
5 Пара - 15:35-17:10
"""
raspisanie = [
    ["Понедельник\n11:40 Физика пр Костина Н.В. 8-507\n15:35 Математика пр. Купряшина Л.А. 8-216",
                "Понедельник\n9:50 Кураторский час 7а-307\n11:40 Физика пр Костина Н.В. 8-507\n13:45Математика пр. Купряшина Л.А. 8-216"],
    ["Вторник\n9:50 Математика пр. Купряшина Л. А. 7б-205\n11:40 Элективные дисциплины по физической культуре и спорту\n13:45 ИТ в ПД лб Голобокова Е.М. Тюразова Ю.В. Лб 7а-405а",
                          "Вторник\n9:50 Математика практика Купряшина Л.А. 7б-205\n11:40 Элективные дисциплины по физической культуре и спорту\n13:45 ИТ в ПД лб Голобокова Е.М. Терякова Ю.В. Лб 7а-405а"],
    ["Среда\n9:50 Технология разработки И-Р лек. Такташкин Д.В. 7а-425\n11:40 Программирование лб Гуряьнов Л.В. Самуйлов С.А. 7а-108\n13:45 Программирование лек. Гурьянов Л.В. 7а-503\n15:35 ",
                "Среда\n11:40 Программирование лб Гуряьнов Л.В. Самуйлов С.А. 7а-108\n13:45 Программирование лек. Гурьянов Л.В. 7а-503\n15:35 Правоведение пр. данилова В.А. 7а-425"],
    ["Четверг\n8:00 Физика лек. Суровичкая Г.В. ДО дома сидим\n9:50 Математика пр. Купряшина Л.А. ДО дома сидим\n11:40 МЛ и ТА лб Казакова И. Ю. Казаков Б. В. ДО дома сидим",
                "Четверг\n8:00 Физика лек. Суровичкая Г.В. ДО дома сидим\n9:50 Математика пр. Купряшина Л.А. ДО дома сидим"],
    ["Пятница\n8:00 Технология разработки Интернет-ресурсов лб Такташкин Д.В. Попова Н.А. 7а-108\n9:40 Иностранный язык Данкова 8-807 Юрасова 8-807б\n11:40 Элективные дисциплины по физической культуре и спорту",
                "Пятница\n8:00 Технология разработки Интернет-ресурсов лб Такташкин Д.В. Попова Н.А. 7а-108\n9:50 Иностранный язык Данкова 8-807 Юрасова 8-807б\n11:40 Элективные дисциплины по физической культуре и спорту"],
    ["Суббота\n8:00 Правоведение лек. Данилова В.А. ДО сидим дома\n9:50 Математическая логика и ТА лек. Казакова И.А. ДО сидим дома",
                "Суббота\nКрутяк, пар нет!"],
    ["В воскресень пар нет, ты что ку-ку?","В воскресень пар нет, ты что ку-ку?"]
                ]

keyboard = VkKeyboard(one_time=False)
keyboard.add_button("Расписание на неделю", color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button("Расписание на сегодня", color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button("Расписание на завтра", color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button("Расписание пар", color=VkKeyboardColor.POSITIVE)
keyboard.add_openlink_button("Ссылка на диск", "https://yadi.sk/d/0W7wTf29wwaOYw")
app = Flask(__name__)

token = cfg.get("vk", "token")

def get_week(tomorrow=False):
    if tomorrow:
        if datetime.datetime.utcnow().isocalendar()[2] - 1 < 6:pass
        else:return int(not bool(datetime.datetime.utcnow().isocalendar()[1] % 2 - 1))
    return datetime.datetime.utcnow().isocalendar()[1] % 2 - 1
def get_today():
    return (datetime.datetime.utcnow().isocalendar()[2] - 1) % 6

token = "8a9c94c201e8f0b1e9af4ebf74bbc1b4d81a0c60e8f21e454b8f23ea61c6d04b9d7b375bec85723bd7158"
vk = vk_api.VkApi(token=token).get_api()
app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def bot():
    def reply(message, responce, text, peer_id, attachment=""):
        if message in text.lower():
            vk.messages.send(peer_id=str(peer_id), message=responce, random_id=random.getrandbits(64), attachment=attachment, keyboard=keyboard.get_keyboard())
    if(request.data):
        data = json.loads(request.data)
        if data['type'] == 'message_new':
            peer_id = data['object']['peer_id']
            text = data['object']["text"]
            reply("привет", "привет", text, peer_id)
            reply("начать", "Привет. У меня ты можешь узнать расписание на неделю и в дальнейшем домашнее задание)", text, peer_id)
            reply("расписание на неделю", "", text, peer_id, "photo-201379365_457239017")
            reply("расписание на сегодня", raspisanie[get_today()][get_week()], text, peer_id)
            reply("расписание на завтра", raspisanie[get_today()+1][get_week(True)], text, peer_id)
            reply("расписание пар", raspisanie_par, text, peer_id)
    return "ok"
if __name__ == "__main__":
    app.run()