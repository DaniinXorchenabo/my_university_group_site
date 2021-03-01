# -*- coding: utf-8 -*-

"""документация к коду"""

# TODO: Добавить список команд для бота в кнопку

if __name__ == '__main__':
    from os.path import split as os_split
    import sys

    sys.path += [os_split(os_split(os_split(__file__)[0])[0])[0]]

import json
import random

import vk_api
from flask import Flask, request
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from app.bot.data import *
from app.db.all_tools_db import *


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
    return datetime.utcnow().isocalendar()[1] % 2


def get_today():
    return ((datetime.utcnow().isocalendar()[2]) % 8) - 1


def get_raspisanie_on_week(tomorrow=False):
    day = get_today()
    print(day)
    week = get_week(tomorrow)
    print(week)
    if not tomorrow:
        if day > 5:
            week = int(not bool(week))
    raspisanie = ""
    if week == 1:
        raspisanie = raspisanie_first_week
    else:
        raspisanie = raspisanie_second_week
    return raspisanie


def get_raspisanie_on_today():
    day = get_today()
    if day > 5:
        day = 0
    s = get_raspisanie_on_week().split("*****")[1:]
    raspisanie = s[day]
    return raspisanie


def get_raspisanie_on_tomorrow():
    day = get_today()
    if day > 4:
        s = get_raspisanie_on_week(True).split("*****")[1:]
        raspisanie = s[0]
    else:
        s = get_raspisanie_on_week().split("*****")[1:]
        raspisanie = s[day + 1]
    return raspisanie


token = cfg.get('vk', 'token')
vk = vk_api.VkApi(token=token).get_api()

keyboard = VkKeyboard(one_time=False)
keyboard.add_callback_button("Расписание на сегодня", color=VkKeyboardColor.POSITIVE, payload='{"payload":"today"}')
keyboard.add_line()
keyboard.add_callback_button("Расписание на завтра", color=VkKeyboardColor.POSITIVE, payload='{"payload":"tomorrow"}')
keyboard.add_line()
keyboard.add_callback_button("Расписание пар", color=VkKeyboardColor.POSITIVE, payload='{"payload":"timetable"}')
keyboard.add_line()
# keyboard.add_callback_button("ФИО преподавателей", color=VkKeyboardColor.POSITIVE, payload='{"payload":"prepody"}')
# keyboard.add_line()
keyboard.add_openlink_button("Ссылка на диск", "https://yadi.sk/d/0W7wTf29wwaOYw")

keyboard_my = VkKeyboard(one_time=False)
keyboard_my.add_callback_button("Расписание на сегодня", color=VkKeyboardColor.POSITIVE, payload='{"payload":"today"}')
keyboard_my.add_line()
keyboard_my.add_callback_button("Расписание на завтра", color=VkKeyboardColor.POSITIVE, payload='{"payload":"tomorrow"}')
keyboard_my.add_line()
keyboard_my.add_callback_button("Расписание пар", color=VkKeyboardColor.POSITIVE, payload='{"payload":"timetable"}')
keyboard_my.add_line()
keyboard_my.add_callback_button("Defend", color=VkKeyboardColor.NEGATIVE, payload='{"payload":"defend"}')
keyboard_my.add_line()
# keyboard.add_callback_button("ФИО преподавателей", color=VkKeyboardColor.POSITIVE, payload='{"payload":"prepody"}')
# keyboard.add_line()
keyboard.add_openlink_button("Ссылка на диск", "https://yadi.sk/d/0W7wTf29wwaOYw")

subjects_keyboard = VkKeyboard(inline=True)
subjects_keyboard.add_callback_button("Английский", payload={"payload": "english"})
subjects_keyboard.add_callback_button("ИТвПД", payload={"payload": "itvpd"})
subjects_keyboard.add_callback_button("Математика", payload={"payload": "math"})
subjects_keyboard.add_callback_button("МЛиТА", payload={"payload": "mlita"})
subjects_keyboard.add_line()
subjects_keyboard.add_callback_button("Правоведение", payload={"payload": "pravo"})
subjects_keyboard.add_callback_button("Программирование", payload={"payload": "proga"})
subjects_keyboard.add_callback_button("ТРИР", payload={"payload": "trir"})
subjects_keyboard.add_callback_button("Физика", payload={"payload": "phisic"})
subjects_keyboard.add_line()
subjects_keyboard.add_callback_button("Назад", payload={"payload": "mainmenu"})
app = Flask(__name__)


def reply(**kwargs):
    general = dict(random_id=random.randint(0, 343439483948), keyboard=keyboard.get_keyboard())
    general.update(kwargs)
    vk.messages.send(**general)


def reply_with_event(peer_id, event_id, user_id, text):
    vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                       event_data=json.dumps(
                                           '{"type": "show_snackbar", "text": ' + text + ' }'))


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
        if request_type == "message_event":
            event_id = data["object"]["event_id"]
            user_id = data["object"]["user_id"]
            peer_id = data["object"]["peer_id"]
            payload = data["object"]["payload"]

            if len(payload) < 85:
                payload = payload["payload"]
            else:
                payload = list(payload)[85:]

                for i in range(-5, -1 + 1, -1):
                    payload[i] = ''
                ''.join(payload)
            if payload == "start":
                responce = "Привет. У меня ты можешь узнать расписание, фио преподовов и дз"
                reply(peer_id=peer_id, message=responce)
            elif payload == "week":
                reply(peer_id=peer_id, message=get_raspisanie_on_week())
            elif payload == "today":
                vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                   event_data=json.dumps(
                                                       {"type": "show_snackbar", "text": get_raspisanie_on_today()}))
            elif payload == "tomorrow":
                vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                   event_data=json.dumps(
                                                       {"type": "show_snackbar", "text": get_raspisanie_on_tomorrow()}))
            elif payload == "timetable":
                vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                   event_data=json.dumps(
                                                       {"type": "show_snackbar",
                                                        "text": ''.join(list(raspisanie_par)[:80])}))
                vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                   event_data=json.dumps(
                                                       {"type": "show_snackbar",
                                                        "text": ''.join(list(raspisanie_par)[81:])}))
            elif payload == "prepody":
                reply(peer_id=peer_id, message="Выберете предмет", keyboard=subjects_keyboard.get_keyboard())
            elif payload == "mainmenu":
                reply(peer_id=peer_id, message="Вы вернулись в главное меню", keyboard=keyboard.get_keyboard())
            # преподы предметов
            elif payload == "english":
                vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                   text=json.dumps(
                                                       {"type": "show_snackbar",
                                                        "text": "Английский\nДанкова Наталья Станиславовна n.s.dankova@mail.ru\nЮрасова Ольга Николаевна ol.iurasova@yandex.ru"}))
            elif payload == "defend":
                reply(peer_id=peer_id, attachment="photo379254977_457239134")
            elif payload == "itvpd":
                vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                   text=json.dumps(
                                                       {"type": "show_snackbar",
                                                        "text": "ИТвПД\nГолобокова Елена Михайловна"}))
            elif payload == "math":
                vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                   text=json.dumps(
                                                       {"type": "show_snackbar",
                                                        "text":"Математика\nКупряшина Лилия Александровна"}))
            elif payload == "mlita":
                vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                   text=json.dumps(
                                                       {"type": "show_snackbar",
                                                        "text":"МЛиТА\nКазакова Ирина Александровна"}))
            elif payload == "pravo":
                vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                   text=json.dumps(
                                                       {"type": "show_snackbar",
                                                        "text":"Правоведение\nДанилова Валерия Александровна"}))
            elif payload == "proga":
                vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                   text=json.dumps(
                                                       {"type": "show_snackbar",
                                                        "text":"Программирование\nГурьянов Лев Вячеславович"}))
            elif payload == "trir":
                vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                   text=json.dumps(
                                                       {"type": "show_snackbar",
                                                        "text":"ТРИР\nТакташкин Денис Витальевич"}))
            elif payload == "phisic":
                vk.messages.sendMessageEventAnswer(peer_id=peer_id, event_id=event_id, user_id=user_id,
                                                   text=json.dumps(
                                                       {"type": "show_snackbar",
                                                        "text":"Физика\nКостина Наталья Владимировна\nСуровичкая Галина Владимировна"}))

        elif request_type == 'message_new':
            message = data['object']["message"]
            from_id = message["from_id"]
            peer_id = message['peer_id']
            text = message["text"].lower()
            if text == "/showkb":
                if from_id == "159526068":
                    reply(user_id=from_id, message="keyboard on", keyboard=keyboard_my.get_keyboard())
                else:
                    reply(peer_id=peer_id, message="keyboard on", keyboard=keyboard.get_keyboard())


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
