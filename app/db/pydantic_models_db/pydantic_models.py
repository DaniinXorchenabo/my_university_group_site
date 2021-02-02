# -*- coding: utf-8 -*-

"""Этот код генерируется автоматически,ни одно изменение не сохранится в этом файле.Тут объявляются pydantic-модели, в которых присутствуют все сущности БДи все атрибуты сущностей"""

from typing import Set as PdSet, Union, List, Dict, Tuple

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
	user: Union[int, Dict]

	class Config:
		orm_mode = True




class PdUser(BaseModel):
	id: int
	name: PdOptional[str]
	login: str
	password: PdOptional[str]
	email: PdOptional[str]
	user_has_queues: PdOptional[List[Union[int, Dict]]]
	session_key_for_app: PdOptional[str]
	getting_time_session_key: PdOptional[datetime]
	admin: PdOptional[Union[Union[int, Dict], Dict]]
	login_EIES: PdOptional[str]
	password_EIES: PdOptional[str]
	my_verification: PdOptional[List[Union[Tuple[Union[int, Dict], Union[int, Dict]], Dict]]]
	i_verificate_thei: PdOptional[List[Union[Tuple[Union[int, Dict], Union[int, Dict]], Dict]]]
	senior_in_the_group: PdOptional[Union[Tuple[Union[int, Dict], Union[str, Dict]], Dict]]
	curse_count: PdOptional[int]
	senior_verification: PdOptional[Union[Union[int, Dict], Dict]]
	groups: PdOptional[Union[str, Dict]]

	class Config:
		orm_mode = True




class PdDustbiningChat(BaseModel):
	id: int
	group: PdOptional[Union[str, Dict]]
	reminders: PdOptional[List[Union[int, Dict]]]

	class Config:
		orm_mode = True




class PdImportantChat(BaseModel):
	id: int
	important_messages: PdOptional[List[Union[int, Dict]]]
	group: PdOptional[List[Union[str, Dict]]]

	class Config:
		orm_mode = True




class PdImportantMessage(BaseModel):
	id: int
	important_chat: PdOptional[Union[int, Dict]]
	text: PdOptional[str]

	class Config:
		orm_mode = True




class PdGroup(BaseModel):
	senior_in_the_group: PdOptional[Union[Tuple[Union[int, Dict], Union[str, Dict]], Dict]]
	users: PdOptional[List[Union[int, Dict]]]
	dustbining_chats: PdOptional[List[Union[int, Dict]]]
	important_chats: PdOptional[List[Union[int, Dict]]]
	subjects: PdOptional[List[Union[Tuple[Union[str, Dict], str], Dict]]]
	name: str
	events: PdOptional[List[Union[int, Dict]]]
	timesheet_update: datetime = lambda: datetime.now
	news: PdOptional[List[Union[int, Dict]]]
	queues: PdOptional[List[Union[int, Dict]]]

	class Config:
		orm_mode = True




class PdHomeTask(BaseModel):
	id: int
	subject: PdOptional[Union[Tuple[Union[str, Dict], str], Dict]]
	deadline_date: PdOptional[date]
	deadline_time: PdOptional[time]
	text: PdOptional[str]
	files: PdOptional[PdJson]

	class Config:
		orm_mode = True




class PdSubject(BaseModel):
	group: Union[str, Dict]
	home_tasks: PdOptional[List[Union[int, Dict]]]
	name: str
	queues: PdOptional[List[Union[int, Dict]]]
	teachers: PdOptional[List[Union[int, Dict]]]
	weekday_and_time_subjects: PdOptional[List[Union[int, Dict]]]

	class Config:
		orm_mode = True




class PdWeekdayAndTimeSubject(BaseModel):
	id: int
	subject: PdOptional[Union[Tuple[Union[str, Dict], str], Dict]]
	number_week: int
	weekday: int
	u_time: PdOptional[time] = lambda: time(00, 00)
	classroom_number: PdOptional[str]
	e_learning_url: PdOptional[Union[int, Dict]]
	update_time: datetime = lambda: datetime.now
	type: PdOptional[str]

	class Config:
		orm_mode = True




class PdELearningUrl(BaseModel):
	id: int
	weekday_and_time_subject: PdOptional[Union[int, Dict]]
	url: PdOptional[str]
	login: PdOptional[str]
	password: PdOptional[str]
	additional_info: PdOptional[str]

	class Config:
		orm_mode = True




class PdEvent(BaseModel):
	id: int
	groups: PdOptional[List[Union[str, Dict]]]
	name: PdOptional[str]
	u_date: PdOptional[date]
	u_time: PdOptional[time]

	class Config:
		orm_mode = True




class PdTeacher(BaseModel):
	id: int
	subjects: PdOptional[List[Union[Tuple[Union[str, Dict], str], Dict]]]
	name: str
	email: PdOptional[str]
	phone_number: PdOptional[str]
	vk_url: PdOptional[str]

	class Config:
		orm_mode = True




class PdSeniorInTheGroup(BaseModel):
	user: Union[int, Dict]
	senior_verifications: PdOptional[List[Union[Union[int, Dict], Dict]]]
	group: Union[str, Dict]
	is_verification: PdOptional[bool]

	class Config:
		orm_mode = True




class PdNews(BaseModel):
	id: int
	group: PdOptional[Union[str, Dict]]
	title: PdOptional[str]
	text: PdOptional[str]
	files: PdOptional[PdJson]

	class Config:
		orm_mode = True




class PdNoneVerification(BaseModel):
	it_is_i: Union[int, Dict]
	he_verificate_me: Union[int, Dict]
	confirmation: PdOptional[int] = 0

	class Config:
		orm_mode = True




class PdQueue(BaseModel):
	id: int
	user_has_queues: PdOptional[List[Union[int, Dict]]]
	group: Union[str, Dict]
	name: PdOptional[str]
	subject: PdOptional[Union[Tuple[Union[str, Dict], str], Dict]]

	class Config:
		orm_mode = True




class PdUserHasQueue(BaseModel):
	user: Union[int, Dict]
	queue: Union[int, Dict]
	number: int = -1
	id: int

	class Config:
		orm_mode = True




class PdReminder(BaseModel):
	id: int
	title: PdOptional[str] = "Вы просили о чем-то напомнить"
	text: PdOptional[str] = " "
	reminder_time: datetime
	dustbining_chat: Union[int, Dict]

	class Config:
		orm_mode = True




class PdSeniorVerification(BaseModel):
	senior_in_the_group: Union[Tuple[Union[int, Dict], Union[str, Dict]], Dict]
	user: Union[int, Dict]
	confirmation: int = 0

	class Config:
		orm_mode = True


if __name__ == '__main__':
	from os import chdir

	chdir(HOME_DIR)
