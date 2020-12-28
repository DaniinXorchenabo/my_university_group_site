# -*- coding: utf-8 -*-

"""Этот код генерируется автоматически,ни одно изменение не сохранится в этом файле.Тут объявляются pydantic-модели, в которых присутствуют все сущности БДи все атрибуты сущностей"""

from typing import Set as PdSet

from datetime import date, datetime, time
from pony.orm import *
from typing import Optional as PdOptional
from pydantic import BaseModel, Json as PdJson
from app.db.models import *


class PdAdmin(BaseModel): pass


class PdUser(BaseModel): pass


class PdDustbiningChat(BaseModel): pass


class PdImportantChat(BaseModel): pass


class PdImportantMessage(BaseModel): pass


class PdGroup(BaseModel): pass


class PdHomeTask(BaseModel): pass


class PdSubject(BaseModel): pass


class PdWeekdayAndTimeSubject(BaseModel): pass


class PdELearningUrl(BaseModel): pass


class PdEvent(BaseModel): pass


class PdTeacher(BaseModel): pass


class PdSeniorInTheGroup(BaseModel): pass


class PdNews(BaseModel): pass


class PdNoneVerification(BaseModel): pass


class PdQueue(BaseModel): pass


class PdUserHasQueue(BaseModel): pass


class PdReminder(BaseModel): pass


class PdSeniorVerification(BaseModel): pass


class PdAdmin(BaseModel):
    user: PdUser = ...


class PdUser(BaseModel):
    id: int
    name: PdOptional[str] = None
    login: str
    password: PdOptional[str] = None
    email: PdOptional[str] = None
    user_has_queues: PdOptional[PdSet[PdUserHasQueue]] = ...
    session_key_for_app: PdOptional[str] = None
    getting_time_session_key: PdOptional[datetime] = None
    admin: PdOptional[PdAdmin] = ...
    login_EIES: PdOptional[str] = None
    password_EIES: PdOptional[str] = None
    my_verification: PdOptional[PdSet[PdNoneVerification]] = ...
    i_verificate_thei: PdOptional[PdSet[PdNoneVerification]] = ...
    senior_in_the_group: PdOptional[PdSeniorInTheGroup] = ...
    curse_count: PdOptional[int] = None
    senior_verification: PdOptional[PdSeniorVerification] = ...
    groups: PdOptional[PdGroup] = ...


class PdDustbiningChat(BaseModel):
    id: int
    group: PdOptional[PdGroup] = ...
    reminders: PdOptional[PdSet[PdReminder]] = ...


class PdImportantChat(BaseModel):
    id: int
    important_messages: PdOptional[PdSet[PdImportantMessage]] = ...
    group: PdOptional[PdSet[PdGroup]] = ...


class PdImportantMessage(BaseModel):
    id: int
    important_chat: PdOptional[PdImportantChat] = ...
    text: PdOptional[str] = None


class PdGroup(BaseModel):
    senior_in_the_group: PdOptional[PdSeniorInTheGroup] = ...
    users: PdOptional[PdSet[PdUser]] = ...
    dustbining_chats: PdOptional[PdSet[PdDustbiningChat]] = ...
    important_chats: PdOptional[PdSet[PdImportantChat]] = ...
    subjects: PdOptional[PdSet[PdSubject]] = ...
    name: str
    events: PdOptional[PdSet[PdEvent]] = ...
    timesheet_update: datetime = lambda: datetime.now
    news: PdOptional[PdSet[PdNews]] = ...
    queues: PdOptional[PdSet[PdQueue]] = ...


class PdHomeTask(BaseModel):
    id: int
    subject: PdOptional[PdSubject] = ...
    deadline_date: PdOptional[date] = None
    deadline_time: PdOptional[time] = None
    text: PdOptional[str] = None
    files: PdOptional[PdJson] = None


class PdSubject(BaseModel):
    group: PdGroup = ...
    home_tasks: PdOptional[PdSet[PdHomeTask]] = ...
    name: str
    queues: PdOptional[PdSet[PdQueue]] = ...
    teachers: PdOptional[PdSet[PdTeacher]] = ...
    weekday_and_time_subjects: PdOptional[PdSet[PdWeekdayAndTimeSubject]] = ...


class PdWeekdayAndTimeSubject(BaseModel):
    subject: PdOptional[PdSubject] = ...
    number_week: int
    weekday: int
    u_time: PdOptional[time] = lambda: time(00, 00)
    classroom_number: PdOptional[str] = None
    e_learning_url: PdOptional[PdELearningUrl] = ...
    update_time: datetime = lambda: datetime.now
    type: PdOptional[str] = None


class PdELearningUrl(BaseModel):
    id: int
    weekday_and_time_subject: PdOptional[PdWeekdayAndTimeSubject] = ...
    url: PdOptional[str] = None
    login: PdOptional[str] = None
    password: PdOptional[str] = None
    additional_info: PdOptional[str] = None


class PdEvent(BaseModel):
    id: int
    groups: PdOptional[PdSet[PdGroup]] = ...
    name: PdOptional[str] = None
    u_date: PdOptional[date] = None
    u_time: PdOptional[time] = None


class PdTeacher(BaseModel):
    id: int
    subjects: PdOptional[PdSet[PdSubject]] = ...
    name: str
    email: PdOptional[str] = None
    phone_number: PdOptional[str] = None
    vk_url: PdOptional[str] = None


class PdSeniorInTheGroup(BaseModel):
    user: PdUser = ...
    senior_verifications: PdOptional[PdSet[PdSeniorVerification]] = ...
    group: PdGroup = ...
    is_verification: PdOptional[bool] = None


class PdNews(BaseModel):
    id: int
    group: PdOptional[PdGroup] = ...
    title: PdOptional[str] = None
    text: PdOptional[str] = None
    files: PdOptional[PdJson] = None


class PdNoneVerification(BaseModel):
    it_is_i: PdUser = ...
    he_verificate_me: PdUser = ...
    confirmation: PdOptional[int] = 0


class PdQueue(BaseModel):
    id: int
    user_has_queues: PdOptional[PdSet[PdUserHasQueue]] = ...
    group: PdGroup = ...
    name: PdOptional[str] = None
    subject: PdOptional[PdSubject] = ...


class PdUserHasQueue(BaseModel):
    user: PdUser = ...
    queue: PdQueue = ...
    number: int = -1
    id: int


class PdReminder(BaseModel):
    id: int
    title: PdOptional[str] = "Вы просили о чем-то напомнить"
    text: PdOptional[str] = " "
    reminder_time: datetime
    dustbining_chat: PdDustbiningChat = ...


class PdSeniorVerification(BaseModel):
    senior_in_the_group: PdSeniorInTheGroup = ...
    user: PdUser = ...
    confirmation: int = 0


if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)
