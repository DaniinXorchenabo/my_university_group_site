# -*- coding: utf-8 -*-

import random

import uvicorn
from fastapi import FastAPI

from app.db.all_tools_db import *
from app.web.api_app import *


app = FastAPI()

app.include_router(api_app)

if __name__ == "__main__":
    is_DB_created()
    uvicorn.run("main_web:app", host="127.0.0.1", port=8000, reload=True)
