import requests

url = "http://homeworkbot1.pythonanywhere.com/"

q_week = """{
    "type": "message_new",
    "object": {
        "message": {
            "date": 1614518187,
            "from_id": 159526068,
            "id": 373,
            "out": 0,
            "peer_id": 159526068,
            "text": "Расписание на неделю",
            "conversation_message_id": 310,
            "fwd_messages": [],
            "important": false,
            "random_id": 0,
            "attachments": [],
            "is_hidden": false
        },
        "client_info": {
            "button_actions": [
                "text",
                "vkpay",
                "open_app",
                "location",
                "open_link",
                "intent_subscribe",
                "intent_unsubscribe"
            ],
            "keyboard": true,
            "inline_keyboard": true,
            "carousel": false,
            "lang_id": 0
        }
    },
    "group_id": 202767654,
    "event_id": "784b44b575d586f164d80745ac223eb4b991039c"
}"""
q_today = """{
    "type": "message_new",
    "object": {
        "message": {
            "date": 1614518187,
            "from_id": 159526068,
            "id": 373,
            "out": 0,
            "peer_id": 159526068,
            "text": "Расписание на сегодня",
            "conversation_message_id": 310,
            "fwd_messages": [],
            "important": false,
            "random_id": 0,
            "attachments": [],
            "is_hidden": false
        },
        "client_info": {
            "button_actions": [
                "text",
                "vkpay",
                "open_app",
                "location",
                "open_link",
                "intent_subscribe",
                "intent_unsubscribe"
            ],
            "keyboard": true,
            "inline_keyboard": true,
            "carousel": false,
            "lang_id": 0
        }
    },
    "group_id": 202767654,
    "event_id": "784b44b575d586f164d80745ac223eb4b991039c"
}"""
requests.post(url, data=q_today.encode("utf-8"))