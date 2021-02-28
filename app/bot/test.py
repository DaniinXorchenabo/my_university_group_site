from datetime import datetime

with open("raspisanie_par.txt", encoding="utf-8") as f:
    raspisanie_par = f.read()
with open("raspisanie_first_week.txt", encoding="utf-8") as f:
    raspisanie_first_week = f.read()
with open("raspisanie_second_week.txt", encoding="utf-8") as f:
    raspisanie_second_week = f.read()

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
        raspisanie = s[day]
    return raspisanie

print(get_raspisanie_on_tomorrow())