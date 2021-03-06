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
keyboard_my.add_callback_button("Расписание на завтра", color=VkKeyboardColor.POSITIVE,
                                payload='{"payload":"tomorrow"}')
keyboard_my.add_line()
keyboard_my.add_callback_button("Расписание пар", color=VkKeyboardColor.POSITIVE, payload='{"payload":"timetable"}')
keyboard_my.add_line()
keyboard_my.add_callback_button("Defend", color=VkKeyboardColor.NEGATIVE, payload={"payload": "defend"})
keyboard_my.add_line()
# keyboard.add_callback_button("ФИО преподавателей", color=VkKeyboardColor.POSITIVE, payload='{"payload":"prepody"}')
# keyboard.add_line()
keyboard_my.add_openlink_button("Ссылка на диск", "https://yadi.sk/d/0W7wTf29wwaOYw")

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


def delete_last_message(peer_id_):
    message_id = vk.messages.getHistory(count=1, peer_id=peer_id_)["items"][0]["id"]
    # reply(peer_id=peer_id_, message=str(message_id))
    # [0]["response"]["items"][0]["id"]
    vk.messages.delete(message_ids=message_id, delete_for_all=True)


def smart_msg_creator(text, send_method, type_param="show_snackbar"):
    if send_method == vk.messages.sendMessageEventAnswer:
        data = dict(event_data=json.dumps({
            "type": type_param,
            "text": text
        }))
    else:
        data = dict(message=text)
    return data


def processing_msg(command: str, data: dict, send_method=vk.messages.sendMessageEventAnswer):
    if send_method == vk.messages.sendMessageEventAnswer:
        user_id = data["object"]["user_id"]
        peer_id = data["object"]["peer_id"]
        print(data["object"])
        payload = command = data["object"]["payload"]
        print(payload)
        basic_data_msg = dict(
            peer_id=peer_id,
            event_id=data["object"]["event_id"],
            user_id=user_id,
        )
    else:
        message = data['object']["message"]
        from_id = message["from_id"]
        peer_id = message['peer_id']
        basic_data_msg = dict()
        command = command.split()[0].lstrip('/')

    if command == "start":
        ans = "Привет. У меня ты можешь узнать расписание, фио преподовов и дз"
        send_method = reply
        basic_data_msg = dict(peer_id=peer_id, message=ans)

    elif command == "week":
        send_method = reply
        basic_data_msg = dict(peer_id=peer_id, message=get_raspisanie_on_week())

    elif command == "today":
        basic_data_msg.update(smart_msg_creator(get_raspisanie_on_today(), send_method))
    elif command == "tomorrow":
        basic_data_msg.update(smart_msg_creator(get_raspisanie_on_tomorrow(), send_method))

    elif command == "timetable":
        basic_data_msg.update(smart_msg_creator(raspisanie_par, send_method))

    elif command == "prepody":
        send_method = reply
        basic_data_msg = dict(
            peer_id=peer_id,
            message="Выберете предмет",
            keyboard=subjects_keyboard.get_keyboard()
        )
    elif command == "mainmenu":
        send_method = reply
        basic_data_msg = dict(
            peer_id=peer_id,
            message="Вы вернулись в главное меню",
            keyboard=keyboard.get_keyboard()
        )

    # преподы предметов
    # мне хочется плакать, когда я вижу этот код
    elif command == "english":
        basic_data_msg.update(smart_msg_creator(
            "Английский\n"
            "Данкова Наталья Станиславовна n.s.dankova@mail.ru\n"
            "Юрасова Ольга Николаевна ol.iurasova@yandex.ru",
            send_method
        ))

    elif command == "defend":
        send_method = reply
        basic_data_msg = dict(peer_id=peer_id, attachment="photo379254977_457239134")
    elif command == "itvpd":
        basic_data_msg.update(smart_msg_creator("ИТвПД\nГолобокова Елена Михайловна", send_method))

    elif command == "math":
        basic_data_msg.update(smart_msg_creator("Математика\nКупряшина Лилия Александровна", send_method))

    elif command == "mlita":
        basic_data_msg.update(smart_msg_creator("МЛиТА\nКазакова Ирина Анатольевна", send_method))

    elif command == "pravo":
        basic_data_msg.update(smart_msg_creator("Правоведение\nДанилова Валерия Александровна", send_method))

    elif command == "proga":
        basic_data_msg.update(smart_msg_creator("Программирование\nГурьянов Лев Вячеславович", send_method))

    elif command == "trir":
        basic_data_msg.update(smart_msg_creator("ТРИР\nТакташкин Денис Витальевич", send_method))

    elif command == "phisic":
        basic_data_msg.update(smart_msg_creator(
            "Физика\nКостина Наталья Владимировна\nСуровичкая Галина Владимировна",
            send_method
        ))
    else:
        return
    send_method(**basic_data_msg)


@app.route('/', methods=["GET", "POST"])
def bot():
    def homework(text, from_id, peer_id):
        temp = text.split()  # для разделения команда параметры
        if len(temp) < 2:
            return
        all_hw = read_json("homework.json")

        ids = read_json("ids.json")["ids"]
        if str(from_id) in list(map(str, ids)):
            if temp[0] == "/добавить_дз":
                _, dl, subject, *hw = temp
                all_hw['homework'][0][dl] = all_hw['homework'][0].get(dl, []) + [[subject, ' '.join(hw)]]
                write_json(all_hw, "homework.json")
                reply(peer_id=peer_id, message=f"Добавил Дз на {dl}")
                if temp[0] == "/очистить_дз":
                    dl = temp[1:]
                    all_hw['homework'][0][dl] = []
                    write_json(all_hw, "homework.json")
                    reply(peer_id=peer_id, message=f"Дз на {dl} успешно удалено")
        if temp[0] == "/получить_дз":
            dl = temp[1]
            msg = f"Дз на {dl}\n" + '-' * 10 + '\n'
            for i in all_hw["homework"][0][dl]:
                msg += i[0] + " - " + i[1] + '\n\n'
            reply(peer_id=peer_id, message=msg)

    if request.data:
        data = json.loads(request.data)
        request_type = data['type']

        if request_type == 'confirmation':
            return cfg.get('vk', 'confirmation')

        elif request_type == "message_event":
            print('!!!!__________________', data["object"])
            payload = data["object"]["payload"].get(['payload'], '-')
            processing_msg(payload, data)

        elif request_type == 'message_new':
            print('-------------------------------', data)
            message = data['object']["message"]
            from_id = message["from_id"]
            peer_id = message['peer_id']
            text = message["text"].lower()

            if text == "/show_kb":
                if str(from_id) in ["159526068", "285983191"]:
                    reply(user_id=from_id, message="keyboard on", keyboard=keyboard_my.get_keyboard())
                else:
                    reply(peer_id=peer_id, message="keyboard on", keyboard=keyboard.get_keyboard())
                delete_last_message(peer_id)

            elif text == "/test_msg_with_timer":
                reply(
                    user_id=from_id,
                    message="Какой-то текст",
                    keyboard=keyboard_my.get_keyboard(),
                    expire_ttl=18000
                )
            elif processing_msg(text, data, send_method=reply):
                pass
            else:
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
