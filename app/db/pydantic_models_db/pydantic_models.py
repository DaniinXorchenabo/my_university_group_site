# -*- coding: utf-8 -*-

"""Этот код генерируется автоматически,ни одно изменение не сохранится в этом файле.Тут объявляются pydantic-модели, в которых присутствуют все сущности БДи все атрибуты сущностей"""

from typing import Set as PdSet, Union, List, Dict

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
	user: Union[int, str, PdUser, Dict, List]

	class Config:
		orm_mode = True


class PdUser(BaseModel):
	id: int
	name: PdOptional[str]
	login: str
	password: PdOptional[str]
	email: PdOptional[str]
	user_has_queues: PdOptional[List[Union[int, str, PdUserHasQueue, Dict, List]]]
	session_key_for_app: PdOptional[str]
	getting_time_session_key: PdOptional[datetime]
	admin: PdOptional[Union[int, str, PdAdmin, Dict, List]]
	login_EIES: PdOptional[str]
	password_EIES: PdOptional[str]
	my_verification: PdOptional[List[Union[int, str, PdNoneVerification, Dict, List]]]
	i_verificate_thei: PdOptional[List[Union[int, str, PdNoneVerification, Dict, List]]]
	senior_in_the_group: PdOptional[Union[int, str, PdSeniorInTheGroup, Dict, List]]
	curse_count: PdOptional[int]
	senior_verification: PdOptional[Union[int, str, PdSeniorVerification, Dict, List]]
	groups: PdOptional[Union[int, str, PdGroup, Dict, List]]

	class Config:
		orm_mode = True


class PdDustbiningChat(BaseModel):
	id: int
	group: PdOptional[Union[int, str, PdGroup, Dict, List]]
	reminders: PdOptional[List[Union[int, str, PdReminder, Dict, List]]]

	class Config:
		orm_mode = True


class PdImportantChat(BaseModel):
	id: int
	important_messages: PdOptional[List[Union[int, str, PdImportantMessage, Dict, List]]]
	group: PdOptional[List[Union[int, str, PdGroup, Dict, List]]]

	class Config:
		orm_mode = True


class PdImportantMessage(BaseModel):
	id: int
	important_chat: PdOptional[Union[int, str, PdImportantChat, Dict, List]]
	text: PdOptional[str]

	class Config:
		orm_mode = True


class PdGroup(BaseModel):
	senior_in_the_group: PdOptional[Union[int, str, PdSeniorInTheGroup, Dict, List]]
	users: PdOptional[List[Union[int, str, PdUser, Dict, List]]]
	dustbining_chats: PdOptional[List[Union[int, str, PdDustbiningChat, Dict, List]]]
	important_chats: PdOptional[List[Union[int, str, PdImportantChat, Dict, List]]]
	subjects: PdOptional[List[Union[int, str, PdSubject, Dict, List]]]
	name: str
	events: PdOptional[List[Union[int, str, PdEvent, Dict, List]]]
	timesheet_update: datetime = lambda: datetime.now
	news: PdOptional[List[Union[int, str, PdNews, Dict, List]]]
	queues: PdOptional[List[Union[int, str, PdQueue, Dict, List]]]

	class Config:
		orm_mode = True


class PdHomeTask(BaseModel):
	id: int
	subject: PdOptional[Union[int, str, PdSubject, Dict, List]]
	deadline_date: PdOptional[date]
	deadline_time: PdOptional[time]
	text: PdOptional[str]
	files: PdOptional[PdJson]

	class Config:
		orm_mode = True


class PdSubject(BaseModel):
	group: Union[int, str, PdGroup, Dict, List]
	home_tasks: PdOptional[List[Union[int, str, PdHomeTask, Dict, List]]]
	name: str
	queues: PdOptional[List[Union[int, str, PdQueue, Dict, List]]]
	teachers: PdOptional[List[Union[int, str, PdTeacher, Dict, List]]]
	weekday_and_time_subjects: PdOptional[List[Union[int, str, PdWeekdayAndTimeSubject, Dict, List]]]

	class Config:
		orm_mode = True


class PdWeekdayAndTimeSubject(BaseModel):
	subject: PdOptional[Union[int, str, PdSubject, Dict, List]]
	number_week: int
	weekday: int
	u_time: PdOptional[time] = lambda: time(00, 00)
	classroom_number: PdOptional[str]
	e_learning_url: PdOptional[Union[int, str, PdELearningUrl, Dict, List]]
	update_time: datetime = lambda: datetime.now
	type: PdOptional[str]

	class Config:
		orm_mode = True


class PdELearningUrl(BaseModel):
	id: int
	weekday_and_time_subject: PdOptional[Union[int, str, PdWeekdayAndTimeSubject, Dict, List]]
	url: PdOptional[str]
	login: PdOptional[str]
	password: PdOptional[str]
	additional_info: PdOptional[str]

	class Config:
		orm_mode = True


class PdEvent(BaseModel):
	id: int
	groups: PdOptional[List[Union[int, str, PdGroup, Dict, List]]]
	name: PdOptional[str]
	u_date: PdOptional[date]
	u_time: PdOptional[time]

	class Config:
		orm_mode = True


class PdTeacher(BaseModel):
	id: int
	subjects: PdOptional[List[Union[int, str, PdSubject, Dict, List]]]
	name: str
	email: PdOptional[str]
	phone_number: PdOptional[str]
	vk_url: PdOptional[str]

	class Config:
		orm_mode = True


class PdSeniorInTheGroup(BaseModel):
	user: Union[int, str, PdUser, Dict, List]
	senior_verifications: PdOptional[List[Union[int, str, PdSeniorVerification, Dict, List]]]
	group: Union[int, str, PdGroup, Dict, List]
	is_verification: PdOptional[bool]

	class Config:
		orm_mode = True


class PdNews(BaseModel):
	id: int
	group: PdOptional[Union[int, str, PdGroup, Dict, List]]
	title: PdOptional[str]
	text: PdOptional[str]
	files: PdOptional[PdJson]

	class Config:
		orm_mode = True


class PdNoneVerification(BaseModel):
	it_is_i: Union[int, str, PdUser, Dict, List]
	he_verificate_me: Union[int, str, PdUser, Dict, List]
	confirmation: PdOptional[int] = 0

	class Config:
		orm_mode = True


class PdQueue(BaseModel):
	id: int
	user_has_queues: PdOptional[List[Union[int, str, PdUserHasQueue, Dict, List]]]
	group: Union[int, str, PdGroup, Dict, List]
	name: PdOptional[str]
	subject: PdOptional[Union[int, str, PdSubject, Dict, List]]

	class Config:
		orm_mode = True


class PdUserHasQueue(BaseModel):
	user: Union[int, str, PdUser, Dict, List]
	queue: Union[int, str, PdQueue, Dict, List]
	number: int = -1
	id: int

	class Config:
		orm_mode = True


class PdReminder(BaseModel):
	id: int
	title: PdOptional[str] = "Вы просили о чем-то напомнить"
	text: PdOptional[str] = " "
	reminder_time: datetime
	dustbining_chat: Union[int, str, PdDustbiningChat, Dict, List]

	class Config:
		orm_mode = True


class PdSeniorVerification(BaseModel):
	senior_in_the_group: Union[int, str, PdSeniorInTheGroup, Dict, List]
	user: Union[int, str, PdUser, Dict, List]
	confirmation: int = 0

	class Config:
		orm_mode = True


if __name__ == '__main__':
	from os import chdir

	chdir(HOME_DIR)
