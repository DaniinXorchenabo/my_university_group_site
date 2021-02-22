# -*- coding: utf-8 -*-

"""документация к коду"""

if __name__ == '__main__':
    from os.path import split as os_split
    import sys

    sys.path += [os_split(os_split(os_split(__file__)[0])[0])[0]]

import random
import json
import datetime
import os

from flask import Flask, request
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from app.db.all_tools_db import *
from app.bot.base.libs import *

token = cfg.get('vk', 'token')
vk = vk_api.VkApi(token=token).get_api()


def write_json(data, file):
    with open("mysite/" + file, "w", encoding="utf-8") as write_file:
        json.dump(data, write_file)


def read_json(file):
    with open("mysite/" + file, "r", encoding="utf-8") as read_file:
        data = json.load(read_file)
    return data


raspisanie_par = """1 Пара - 8:00-9:35
2 Пара - 9:50-11:25
3 Пара - 11:40-13:15
4 Пара - 13:45-15:20
5 Пара - 15:35-17:10
"""
raspisanie = [
    ["Понедельник\n11:40 Физика пр Костина Н.В. 8-507\n15:35 Математика пр. Купряшина Л.А. 8-216",
     "Понедельник\n9:50 Кураторский час 7а-307\n11:40 Физика пр Костина Н.В. 8-507\n13:45Математика пр. Купряшина Л.А. 8-216"],
    [
        "Вторник\n9:50 Математика пр. Купряшина Л. А. 7б-205\n11:40 Элективные дисциплины по физической культуре и спорту\n13:45 ИТ в ПД лб Голобокова Е.М. Тюразова Ю.В. Лб 7а-405а",
        "Вторник\n9:50 Математика практика Купряшина Л.А. 7б-205\n11:40 Элективные дисциплины по физической культуре и спорту\n13:45 ИТ в ПД лб Голобокова Е.М. Терякова Ю.В. Лб 7а-405а"],
    [
        "Среда\n9:50 Технология разработки И-Р лек. Такташкин Д.В. 7а-425\n11:40 Программирование лб Гуряьнов Л.В. Самуйлов С.А. 7а-108\n13:45 Программирование лек. Гурьянов Л.В. 7а-503\n15:35 ",
        "Среда\n11:40 Программирование лб Гуряьнов Л.В. Самуйлов С.А. 7а-108\n13:45 Программирование лек. Гурьянов Л.В. 7а-503\n15:35 Правоведение пр. данилова В.А. 7а-425"],
    [
        "Четверг\n8:00 Физика лек. Суровичкая Г.В. ДО дома сидим\n9:50 Математика пр. Купряшина Л.А. ДО дома сидим\n11:40 МЛ и ТА лб Казакова И. Ю. Казаков Б. В. ДО дома сидим",
        "Четверг\n8:00 Физика лек. Суровичкая Г.В. ДО дома сидим\n9:50 Математика пр. Купряшина Л.А. ДО дома сидим"],
    [
        "Пятница\n8:00 Технология разработки Интернет-ресурсов лб Такташкин Д.В. Попова Н.А. 7а-108\n9:40 Иностранный язык Данкова 8-807 Юрасова 8-807б\n11:40 Элективные дисциплины по физической культуре и спорту",
        "Пятница\n8:00 Технология разработки Интернет-ресурсов лб Такташкин Д.В. Попова Н.А. 7а-108\n9:50 Иностранный язык Данкова 8-807 Юрасова 8-807б\n11:40 Элективные дисциплины по физической культуре и спорту"],
    [
        "Суббота\n8:00 Правоведение лек. Данилова В.А. ДО сидим дома\n9:50 Математическая логика и ТА лек. Казакова И.А. ДО сидим дома",
        "Суббота\nКрутяк, пар нет!"],
    ["В воскресень пар нет, ты что ку-ку?", "В воскресень пар нет, ты что ку-ку?"]
]
prepody = "Английский Юрасова Ольга Николаевна Данкова Наталья Станиславовна\nИТ в ПД Голобокова Елена Михайловна\nМатематика Купряшина Лилия Александровна\nМатематическая логика и теория алгоритмов Казакова Ирина Анатольевна\nПравоведение Данилова Валерия Александровна\nПрограммирование Гурьянов Лев Вячеславович\nТРИР Такташкин Денис Витальевич\nФизика Лекция Суровицкая Галина Владимировна Практика Костина Наталья Владимировна\n"

keyboard = VkKeyboard(one_time=False)
keyboard.add_button("Расписание на неделю", color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button("Расписание на сегодня", color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button("Расписание на завтра", color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button("Расписание пар", color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button("ФИО преподавателей", color=VkKeyboardColor.POSITIVE)
keyboard.add_openlink_button("Ссылка на диск", "https://yadi.sk/d/0W7wTf29wwaOYw")


def get_week(tomorrow=False):
    if tomorrow:
        if datetime.datetime.utcnow().isocalendar()[2] - 1 < 6:
            pass
        else:
            return int(not bool(datetime.datetime.utcnow().isocalendar()[1] % 2 - 1))
    return datetime.datetime.utcnow().isocalendar()[1] % 2 - 1


def get_today():
    return (datetime.datetime.utcnow().isocalendar()[2] - 1) % 6


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def bot():
    def homework(text, from_id, peer_id):
        ids = read_json("ids.json")["ids"]
        all_hw = read_json("homework.json")
        s = ""
        if str(from_id) in list(map(str, ids)):
            text = text.lower()
            if "добавить_дз" in text:
                dl, subject, hw = text.split("добавить_дз")[1].split()
                try:
                    all_hw['homework'][0][dl].append([subject, hw])
                except KeyError:
                    all_hw['homework'][0].update({dl: []})
                    all_hw['homework'][0][dl].append([subject, hw])
                write_json(all_hw, "homework.json")
                vk.messages.send(peer_id=str(peer_id), message="получил", random_id=random.getrandbits(64),
                                 keyboard=keyboard.get_keyboard())
            elif "получить_дз" in text:
                m = text.split("получить_дз ")
                if len(m) == 2:
                    _, dl = m
                    for i in all_hw["homework"][0][dl]:
                        s += i[0] + " " + i[1] + '\n'
                    vk.messages.send(peer_id=str(peer_id), message=s, random_id=random.getrandbits(64),
                                     keyboard=keyboard.get_keyboard())
            elif "очистить_дз" in text:
                m = text.split("очистить_дз ")
                if len(m) == 2:
                    _, dl = m
                    all_hw['homework'][0][dl] = []
                    write_json(all_hw, "homework.json")
                    vk.messages.send(peer_id=str(peer_id), message="Дз " + dl + "очищено",
                                     random_id=random.getrandbits(64), keyboard=keyboard.get_keyboard())

    if request.data:
        data = json.loads(request.data)
        request_type = data['type']
        if data['type'] == 'confirmation':
            return cfg.get('vk', 'confirmation')
        if request_type == 'message_new':
            message = data['object']["message"]
            from_id = message["from_id"]
            peer_id = message['peer_id']
            text = message["text"].lower()
            if peer_id == from_id:
                if "начать" in text:
                    responce = "Привет. У меня ты можешь узнать расписание на неделю и в дальнейшем домашнее задание)"
                    vk.messages.send(user_id=str(from_id), message=responce, random_id=random.getrandbits(64),
                                     keyboard=keyboard.get_keyboard())
                elif "расписание на неделю" in text:
                    vk.messages.send(user_id=str(from_id), random_id=random.getrandbits(64),
                                     attachment="photo-201379365_457239017", keyboard=keyboard.get_keyboard())
                elif "расписание на сегодня" in text:
                    vk.messages.send(user_id=str(from_id), message=raspisanie[get_today()][get_week()],
                                     random_id=random.getrandbits(64), keyboard=keyboard.get_keyboard())
                elif "расписание на завтра" in text:
                    vk.messages.send(user_id=str(from_id), message=raspisanie[get_today() + 1][get_week(True)],
                                     random_id=random.getrandbits(64), keyboard=keyboard.get_keyboard())
                elif "расписание пар" in text:
                    vk.messages.send(user_id=str(from_id), message=raspisanie[get_today() + 1][get_week(True)],
                                     random_id=random.getrandbits(64), keyboard=keyboard.get_keyboard())
                elif "getcwd" in text:
                    vk.messages.send(user_id=str(from_id), message=os.getcwd(), random_id=random.getrandbits(64),
                                     keyboard=keyboard.get_keyboard())
                elif "фио преподавателей" in text:
                    vk.messages.send(user_id=str(from_id), message=prepody, random_id=random.getrandbits(64),
                                     keyboard=keyboard.get_keyboard())
            elif "[club201379365|@20vp1helper] " in text:
                if "начать" in text:
                    responce = "Привет. У меня ты можешь узнать расписание на неделю и в дальнейшем домашнее задание)"
                    vk.messages.send(peer_id=str(peer_id), message=responce, random_id=random.getrandbits(64),
                                     keyboard=keyboard.get_keyboard())
                elif "расписание на неделю" in text:
                    vk.messages.send(peer_id=str(peer_id), random_id=random.getrandbits(64),
                                     attachment="photo-201379365_457239017", keyboard=keyboard.get_keyboard())
                elif "расписание на сегодня" in text:
                    vk.messages.send(peer_id=str(peer_id), message=raspisanie[get_today()][get_week()],
                                     random_id=random.getrandbits(64), keyboard=keyboard.get_keyboard())
                elif "расписание на завтра" in text:
                    vk.messages.send(peer_id=str(peer_id), message=raspisanie[get_today() + 1][get_week(True)],
                                     random_id=random.getrandbits(64), keyboard=keyboard.get_keyboard())
                elif "расписание пар" in text:
                    vk.messages.send(peer_id=str(peer_id), message=raspisanie_par, random_id=random.getrandbits(64),
                                     keyboard=keyboard.get_keyboard())
                elif "getcwd" in text:
                    vk.messages.send(peer_id=str(peer_id), message=os.getcwd(), random_id=random.getrandbits(64),
                                     keyboard=keyboard.get_keyboard())
                elif "фио преподавателей" in text:
                    vk.messages.send(peer_id=str(peer_id), message=prepody, random_id=random.getrandbits(64),
                                     keyboard=keyboard.get_keyboard())
            homework(text, from_id, peer_id)
        # elif type == "confirmation":
        #     return "b6750942"
    return "ok"


# @app.route('/update', methods=["GET", "POST"])
# def webhook():
#     if request.method == 'POST':
#         repo = git.Repo('path/to/git_repo')
#         origin = repo.remotes.origin
#         origin.pull()
#         return 'Updated PythonAnywhere successfully', 200
#     else:
#         return 'Wrong event type', 400


if __name__ == "__main__":
    app.run()
