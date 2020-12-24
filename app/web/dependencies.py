# -*- coding: utf-8 -*-

"""Это файл,
где объявляются все зависимости нашего web-приложения"""

import random

import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from app.db.all_tools_db import *


def checking_session_key(session_key1: str = "None"):
    """Проверка на то, что session_key правильный"""
    """Будет реализована как-нибудь потом"""
    pass


connect_with_db()