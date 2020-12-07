import uvicorn
from fastapi import FastAPI

from app.db.models import *


# is_DB_created()
app = FastAPI()

#-----------------
@app.get("/")
def read_root():
    return {"Привет!": "World"}

#Авторизация
@app.get("/api/sign_in/{login}/{password}")
@db_session
def login(login: str, password: str):

    if User.exists(name=login):
        user = User.get(name=login)
        if user.password == password:
            return {"вы авторизированы!"}
        return {"неверный!"}
    return {"введены не верно логин или пароль"}

#answer: json{
#answer : true,
#group_name : "имя группы или None, в случае, если такого пользователя нет",
#name : "ФИО пользователя",
#photo : "ну а что, а вдруг, а пусть будет",
#session_key : "большой набор из цифорок и букавок, который будет отправляться каждый раз для подтверждения авторизации пользователя."
#}

#Новости
@app.get("/api/sign_in/{session_key}/news/{group_name}")
@db_session
def news(session_key: str, group_name: str):
    return {"first : Это новости, ты просто не видишь их  second : Да-да, это именно так, не удивляйся third : Именно так и должно быть"}

#Домашние задания (все)
@app.get("/api/{session_key}/homework/{group_name}/all")
@db_session
def all_homework(session_key: str, group_name: str):
    return {"Тут домашка"
            "<дд.мм.гггг> : { <Предмет1> : {домашка1, домашка2, ..., домашка}, <Предмет2> : {домашка1, домашка2, ..., домашка}, ... <Предмет> : {домашка1, домашка2, ..., домашка}"}

#Домашние задания (по предмету)
@app.get("/api/{session_key}/homework/{group_name}/subject/{subject}")
@db_session
def subject_homework(session_key: str, group_name: str, subject: str):
    if subject == "rus":
        return {"rus : <дд.мм.гггг> : {домашка1, домашка2, ..., домашка}, <дд.мм.гггг> : {домашка1, домашка2, ..., домашка},... <дд.мм.гггг> : {домашка1, домашка2, ..., домашка},"}
    elif subject == "sit":
        return {"sit : <дд.мм.гггг> : {домашка1, домашка2, ..., домашка}, <дд.мм.гггг> : {домашка1, домашка2, ..., домашка},... <дд.мм.гггг> : {домашка1, домашка2, ..., домашка},"}
    return {"У нас нет такого предмета"}

#Домашние задания (по дате)
@app.get("/api/{session_key}/homework/{group_name}/day/{data}")
@db_session
def data_homework(session_key: str, group_name: str, data: str):
    return {"<Предмет1> : {домашка1, домашка2, ..., домашка}, <Предмет2> : {домашка1, домашка2, ..., домашка}, ... <Предмет> : {домашка1, домашка2, ..., домашка},"}

#Информация о преподавателях
@app.get("/api/{session_key}/teachers/{group_name}/")
@db_session
def teachers(session_key: str, group_name: str):
    return {"<ФИО> : {инфа1, инфа2, ..., инфа}, <ФИО> : {инфа1, инфа2, ..., инфа}, ... , <ФИО> : {инфа1, инфа2, ..., инфа},"}

#Расписание
@app.get("/api/{session_key}/{group_name}/schedule/{change}")
@db_session
def schedule(session_key: str, group_name: str, change: str):
    return {"Тут будет расписание на 2 недели"}

#Получает образовательные материалы
@app.get("/api/{session_key}/educational_materials/{group_name}")
@db_session
def educational_materials(session_key: str, group_name: str):
    return {"Файлы с учебниками: <предмет> : {инфа1, инфа2, ..., инфа}, <предмет> : {инфа1, инфа2, ..., инфа}, ... , <предмет> : {инфа1, инфа2, ..., инфа},"}

#Выход из пользователя
@app.get("/api/{session_key}/log_out")
@db_session
def log_out(session_key: str):
    if True:
        return {"true"}
    return {"false"}

#Регистрация пользователя
@app.get("/api/sign_in/{login}/{password}/{_id}")
@db_session
def sign_in(login: str, password: str, _id: int):
    if User.exists(id = _id):
        return {"false"}
    else:
        user1 = User(id = _id, name = login, password = password)
    return {"true"}

#Регистрация группы
@app.get("/api/reg_group/{group_name}")
@db_session
def reg_group(session_key: str):
    if True:
        return {"true"}
    return {"false"}

#Получить настройки пользователя
@app.get("/api/{session_key}/settings_user/get")
@db_session
def settings_user_get(session_key: str):
    return {"<какой-то параметр> : <какое-то значение>"}

#Установка настроек - не знаю, как сделать

#Получить настройки для администратора
@app.get("/api/{session_key}/settings_admin/get")
@db_session
def settings_user_admin(session_key: str):
    return {"<какой-то параметр> : <какое-то значение>"}

#Получить настройки для бота (для личного пользования)
@app.get("/api/{session_key}/settings_bot/get")
@db_session
def settings_user_bot(session_key: str):
    return {"<какой-то параметр> : <какое-то значение>"}

#Получить настройки старосты
@app.get("/api/{session_key}/settings_group_senior/get")
@db_session
def settings_group_senior(session_key: str):
    return {"<какой-то параметр> : <какое-то значение>"}



if __name__ == "__main__":
    uvicorn.run("main_web:app", host="127.0.0.1", port=8000, reload=True)





