import uvicorn
from fastapi import FastAPI

from app.db.models import *


# is_DB_created()
app = FastAPI()

#-----------------
@app.get("/")
def read_root():
    return {"Привет!": "World"}

@app.get("/api/log_in/{login}/{password}/{_id}")
@db_session
def login(login: str, password: str, _id: int):

    if User.exists(id=_id):
        return {"Вы уже зарегестрировались!"}
    else:
        user1 = User(id=_id, name=login, password=password)
    return {"Привет, дорогой пользовватель,    ты зарегестрирован как " + login + " "}


@app.get("/api/sign_in/{login}/{password}")
@db_session
def login(login: str, password: str):
    try:
        if User.exists(name=login):
            user = User.get(name=login)
            if user.password == password:
                return {"вы авторизированы!"}
            return {"неверный!"}
        return {"введены не верно логин или пароль"}
    except Exception as e:
        print(e)
    return {"все словано!"}


if __name__ == "__main__":
    uvicorn.run("main_web:app", host="127.0.0.1", port=8000, reload=True)





