# -*- coding: utf-8 -*-

"""Главный файл нашего web-приложения"""

from app.web.dependencies import *
from app.web.routers.api_app import *


app = FastAPI()


@app.get("/")
@db_session
def read_root():
    print(User[100])
    return {"Привет!": "World"}


app.include_router(api_app)
app.include_router(session_keyless_api)

if __name__ == "__main__":
    create_test_db_1()
    show_all()
    print(db)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
