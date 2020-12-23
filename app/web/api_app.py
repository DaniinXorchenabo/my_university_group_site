# -*- coding: utf-8 -*-

"""Тут будут только роуты, предназначенные для API (взаимодействия с android)"""

import random

import uvicorn
from fastapi import FastAPI, APIRouter

from app.db.all_tools_db import *


api_app = APIRouter()

if __name__ == "__main__":
    is_DB_created()


@api_app.get("/")
def read_root():
    return {"Привет!": "World"}


@api_app.get("/api/log_in/{login}/{password}")
@db_session
def log_in(login: str, password: str):
    """Авторизация"""
    if User.exists(name=login):
        user = User.get(name=login)
        if user.password == password:
            session_key = random.random()
            user.session_key_for_app = str(session_key)
            User.select().show()
            return {
                'answer : True' + ', group_name : ' + 'user.groups' + ', name : ' + user.name + ', session_key : ' + str(
                    session_key)}
        return {"answer : False"}
    return {"answer : False"}


@api_app.get("/api/sign_in/{session_key}/news/{group_name}")
@db_session
def news(session_key: str, group_name: str):
    """Новости"""
    if User.exists(session_key_for_app=session_key):
        return {
            "first : Это новости, ты просто не видишь их,  second : Да-да, это именно так, не удивляйся, third : Именно так и должно быть"}
    return {"Ты накосячил с session_key. Взломать пытался, нехороший человек! Ухади!"}


@api_app.get("/api/{session_key}/homework/{group_name}/all")
@db_session
def all_homework(session_key: str, group_name: str):
    """Домашние задания (все)"""
    if User.exists(session_key_for_app=session_key):
        return {"Тут домашка"
                "<дд.мм.гггг> : { <Предмет1> : {домашка1, домашка2, ..., домашка}, <Предмет2> : {домашка1, домашка2, ..., домашка}, ... <Предмет> : {домашка1, домашка2, ..., домашка}"}
    return {"Ты накосячил с session_key. Взломать пытался, нехороший человек! Ухади!"}


@api_app.get("/api/{session_key}/homework/{group_name}/subject/{subject}")
@db_session
def subject_homework(session_key: str, group_name: str, subject: str):
    """Домашние задания (по предмету)"""
    if User.exists(session_key_for_app=session_key):
        if subject == "rus":
            return {
                "rus : <дд.мм.гггг> : {домашка1, домашка2, ..., домашка}, <дд.мм.гггг> : {домашка1, домашка2, ..., домашка},... <дд.мм.гггг> : {домашка1, домашка2, ..., домашка},"}
        elif subject == "sit":
            return {
                "sit : <дд.мм.гггг> : {домашка1, домашка2, ..., домашка}, <дд.мм.гггг> : {домашка1, домашка2, ..., домашка},... <дд.мм.гггг> : {домашка1, домашка2, ..., домашка},"}
        return {"У нас нет такого предмета"}
    return {"Ты накосячил с session_key. Взломать пытался, нехороший человек! Ухади!"}


@api_app.get("/api/{session_key}/homework/{group_name}/day/{data}")
@db_session
def data_homework(session_key: str, group_name: str, data: str):
    """Домашние задания (по дате)"""
    if User.exists(session_key_for_app=session_key):
        return {"Предмет1": ["домашка1", "домашка2", "домашка"],
                "Предмет2": ["домашка1", "домашка2", "домашка"],
                "Предмет3": ["домашка1", "домашка2", "домашка"], }
    return {"Ты накосячил с session_key. Взломать пытался, нехороший человек! Ухади!"}


@api_app.get("/api/{session_key}/teachers/{group_name}/")
@db_session
def teachers(session_key: str, group_name: str):
    """Информация о преподавателях"""
    if User.exists(session_key_for_app=session_key):
        return {
            "ФИО1": ["инфа1", "инфа2", 'инфа'],
            "ФИО2": ["инфа1", "инфа2", 'инфа'],
            "ФИО3": ["инфа1", "инфа2", 'инфа']
        }
    return {"Ты накосячил с session_key. Взломать пытался, нехороший человек! Ухади!"}


@api_app.get("/api/{session_key}/{group_name}/schedule/{change}")
@db_session
def schedule(session_key: str, group_name: str, change: str):
    """Расписание"""
    if User.exists(session_key_for_app=session_key):
        return {"Тут будет расписание на 2 недели"}
    return {"Ты накосячил с session_key. Взломать пытался, нехороший человек! Ухади!"}


@api_app.get("/api/{session_key}/educational_materials/{group_name}")
@db_session
def educational_materials(session_key: str, group_name: str):
    """Получает образовательные материалы"""
    if User.exists(session_key_for_app=session_key):
        return {
            "Файлы с учебниками: <предмет> : {инфа1, инфа2, ..., инфа}, <предмет> : {инфа1, инфа2, ..., инфа}, ... , <предмет> : {инфа1, инфа2, ..., инфа},"}
    return {"Ты накосячил с session_key. Взломать пытался, нехороший человек! Ухади!"}


@api_app.get("/api/{session_key}/log_out")
@db_session
def log_out(session_key: str):
    """Выход из пользователя"""
    if User.exists(session_key_for_app=session_key):
        k = 1
        if k == 1:
            return {"True"}
        return {"False"}
    return {"Ты накосячил с session_key. Взломать пытался, нехороший человек! Ухади!"}


@api_app.get("/api/sign_in/{login}/{password}/{_id}")
@db_session
def sign_in(login: str, password: str, _id: int):
    """Регистрация пользователя"""
    if User.exists(id=_id):
        return {"false"}
    else:
        User(id=_id, name=login, password=password)
    return {"true"}


@api_app.get("/api/reg_group/{group_name}")
@db_session
def reg_group(session_key: str):
    """Регистрация группы"""
    k = 1
    if k == 1:
        return {"True"}
    return {"Falseg"}


@api_app.get("/api/{session_key}/settings_user/get")
@db_session
def settings_user_get(session_key: str):
    """Получить настройки пользователя"""
    if User.exists(session_key_for_app=session_key):
        return {"<какой-то параметр> : <какое-то значение>"}
    return {"Ты накосячил с session_key. Взломать пытался, нехороший человек! Ухади!"}


# Установка настроек - не знаю, как сделать


@api_app.get("/api/{session_key}/settings_admin/get")
@db_session
def settings_user_admin(session_key: str):
    """Получить настройки для администратора"""
    if User.exists(session_key_for_app=session_key):
        return {"<какой-то параметр> : <какое-то значение>"}
    return {"Ты накосячил с session_key. Взломать пытался, нехороший человек! Ухади!"}


@api_app.get("/api/{session_key}/settings_bot/get")
@db_session
def settings_user_bot(session_key: str):
    """Получить настройки для бота (для личного пользования)"""
    if User.exists(session_key_for_app=session_key):
        return {"<какой-то параметр> : <какое-то значение>"}
    return {"Ты накосячил с session_key. Взломать пытался, нехороший человек! Ухади!"}


@api_app.get("/api/{session_key}/settings_group_senior/get")
@db_session
def settings_group_senior(session_key: str):
    """Получить настройки старосты"""
    if User.exists(session_key_for_app=session_key):
        return {"<какой-то параметр> : <какое-то значение>"}
    return {"Ты накосячил с session_key. Взломать пытался, нехороший человек! Ухади!"}


if __name__ == "__main__":
    # is_DB_created()
    show_all()
    uvicorn.run("main_web:api_app", host="127.0.0.1", port=8000, reload=True)