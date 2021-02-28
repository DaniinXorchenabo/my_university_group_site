# -*- coding: utf-8 -*-

"""документация к коду"""

if __name__ == '__main__':
    from os.path import split as os_split
    import sys

    sys.path += [os_split(os_split(os_split(__file__)[0])[0])[0]]

import random
import json
import os

from flask import Flask, request
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from app.db.all_tools_db import *
from app.bot.data import *


def write_json(data, file):
    with open("app/bot/" + file, "w", encoding="utf-8") as write_file:
        json.dump(data, write_file)


def read_json(file):
    with open("app/bot/" + file, "r", encoding="utf-8") as read_file:
        data = json.load(read_file)
    return data


def get_week(tomorrow=False):
    if tomorrow:
        return int(not bool(datetime.utcnow().isocalendar()[1] % 2))
    return datetime.utcnow().isocalendar()[1] % 2 - 1


def get_today():
    return (datetime.utcnow().isocalendar()[2] - 1) % 6


def get_raspisanie_on_week(tomorrow=False):
    week = get_week(tomorrow)
    raspisanie = ""
    if week == 0:
        raspisanie = raspisanie_first_week
    else:
        raspisanie = raspisanie_second_week
    return raspisanie


def get_raspisanie_on_today():
    day = get_today()
    s = get_raspisanie_on_week().split("\n")[1:]
    raspisanie = s[day]
    return raspisanie


def get_raspisanie_on_tomorrow():
    day = get_today()
    if day > 4:
        s = get_raspisanie_on_week(True).split("\n")[1:]
        raspisanie = s[0]
    else:
        s = get_raspisanie_on_week().split("\n")[1:]
        raspisanie = s[day]
    return raspisanie


token = cfg.get('vk', 'token')
vk = vk_api.VkApi(token=token).get_api()

keyboard = VkKeyboard(one_time=False)
keyboard.add_button("Расписание на неделю", color=VkKeyboardColor.POSITIVE, payload='{"payload":"week"}')
keyboard.add_line()
keyboard.add_button("Расписание на сегодня", color=VkKeyboardColor.POSITIVE, payload='{"payload":"today"}')
keyboard.add_line()
keyboard.add_button("Расписание на завтра", color=VkKeyboardColor.POSITIVE, payload='{"payload":"tomorrow"}')
keyboard.add_line()
keyboard.add_button("Расписание пар", color=VkKeyboardColor.POSITIVE, payload='{"payload":"timetable"}')
keyboard.add_line()
keyboard.add_button("ФИО преподавателей", color=VkKeyboardColor.POSITIVE, payload='{"payload":"prepody"}')
keyboard.add_openlink_button("Ссылка на диск", "https://yadi.sk/d/0W7wTf29wwaOYw")

subjects_keyboard = VkKeyboard(one_time=False)
app = Flask(__name__)


def reply(**kwargs):
    general = dict(random_id=random.randint(0, 343439483948), keyboard=keyboard.get_keyboard())
    kwargs.update(general)
    vk.messages.send(**kwargs)


@app.route('/', methods=["GET", "POST"])
def bot():
    def homework(text, from_id, peer_id):
        temp = text.split()  # для разделения команда параметры
        if len(temp) < 2:
            return
        all_hw = read_json("homework.json")
        s = ""
        ids = read_json("ids.json")["ids"]
        if str(from_id) in list(map(str, ids)):
            if temp[0] == "/добавить_дз":
                dl, subject, hw = temp[1:]
                try:
                    all_hw['homework'][0][dl].append([subject, hw])
                except KeyError:
                    all_hw['homework'][0].update({dl: []})
                    all_hw['homework'][0][dl].append([subject, hw])
                write_json(all_hw, "homework.json")
                reply(peer_id=peer_id, message=f"Добавил Дз на {dl}")
                if temp[0] == "/очистить_дз":
                    dl = temp[1:]
                    all_hw['homework'][0][dl] = []
                    write_json(all_hw, "homework.json")
                    reply(peer_id=peer_id, message=f"Дз на {dl} успешно удалено")
        if temp[0] == "/получить_дз":
            dl = temp[1]
            for i in all_hw["homework"][0][dl]:
                s += i[0] + " " + i[1] + '\n'
            reply(peer_id=peer_id, message=f"Дз на {dl}\n {s}")

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
            if text == "/showkb":
                reply(peer_id=peer_id, message="keyboard on", keyboard=keyboard.get_keyboard())
            if "payload" in message.keys():
                payload = message["payload"]["payload"]
                if payload == "start":
                    responce = "Привет. У меня ты можешь узнать расписание, фио преподовов и дз"
                    reply(peer_id=peer_id, message=responce)
                elif payload == "week":
                    reply(peer_id=peer_id, message=get_raspisanie_on_week())
                elif payload == "today":
                    reply(peer_id=peer_id, message=get_raspisanie_on_today())
                elif payload == "tomorrow":
                    reply(peer_id=peer_id, message=get_raspisanie_on_tomorrow())
                elif payload == "timetable":
                    reply(peer_id=peer_id, message=raspisanie_par)
                elif payload == "prepody":
                    reply(peer_id=peer_id, keyboard=subjects_keyboard.get_keyboard())
            homework(text, from_id, peer_id)
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
