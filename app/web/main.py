# -*- coding: utf-8 -*-

"""Главный файл нашего web-приложения"""

from fastapi import FastAPI

from app.web.routers.api_app import *


app = FastAPI()

app.include_router(api_app)

if __name__ == "__main__":
    is_DB_created()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
