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
	user: Union[PdUser, str, List, Dict, PdSet]

	class Config:
		orm_mode = True


class PdUser(BaseModel):
	id: int
	name: PdOptional[str]
	login: str
	password: PdOptional[str]
	email: PdOptional[str]
	user_has_queues: PdOptional[PdSet[Union[PdUserHasQueue, str, List, Dict, PdSet]]]
	session_key_for_app: PdOptional[str]
	getting_time_session_key: PdOptional[datetime]
	admin: PdOptional[Union[PdAdmin, str, List, Dict, PdSet]]
	login_EIES: PdOptional[str]
	password_EIES: PdOptional[str]
	my_verification: PdOptional[PdSet[Union[PdNoneVerification, str, List, Dict, PdSet]]]
	i_verificate_thei: PdOptional[PdSet[Union[PdNoneVerification, str, List, Dict, PdSet]]]
	senior_in_the_group: PdOptional[Union[PdSeniorInTheGroup, str, List, Dict, PdSet]]
	curse_count: PdOptional[int]
	senior_verification: PdOptional[Union[PdSeniorVerification, str, List, Dict, PdSet]]
	groups: PdOptional[Union[PdGroup, str, List, Dict, PdSet]]

	class Config:
		orm_mode = True


class PdDustbiningChat(BaseModel):
	id: int
	group: PdOptional[Union[PdGroup, str, List, Dict, PdSet]]
	reminders: PdOptional[PdSet[Union[PdReminder, str, List, Dict, PdSet]]]

	class Config:
		orm_mode = True


class PdImportantChat(BaseModel):
	id: int
	important_messages: PdOptional[PdSet[Union[PdImportantMessage, str, List, Dict, PdSet]]]
	group: PdOptional[PdSet[Union[PdGroup, str, List, Dict, PdSet]]]

	class Config:
		orm_mode = True


class PdImportantMessage(BaseModel):
	id: int
	important_chat: PdOptional[Union[PdImportantChat, str, List, Dict, PdSet]]
	text: PdOptional[str]

	class Config:
		orm_mode = True


class PdGroup(BaseModel):
	senior_in_the_group: PdOptional[Union[PdSeniorInTheGroup, str, List, Dict, PdSet]]
	users: PdOptional[PdSet[Union[PdUser, str, List, Dict, PdSet]]]
	dustbining_chats: PdOptional[PdSet[Union[PdDustbiningChat, str, List, Dict, PdSet]]]
	important_chats: PdOptional[PdSet[Union[PdImportantChat, str, List, Dict, PdSet]]]
	subjects: PdOptional[PdSet[Union[PdSubject, str, List, Dict, PdSet]]]
	name: str
	events: PdOptional[PdSet[Union[PdEvent, str, List, Dict, PdSet]]]
	timesheet_update: datetime = lambda: datetime.now
	news: PdOptional[PdSet[Union[PdNews, str, List, Dict, PdSet]]]
	queues: PdOptional[PdSet[Union[PdQueue, str, List, Dict, PdSet]]]

	class Config:
		orm_mode = True


class PdHomeTask(BaseModel):
	id: int
	subject: PdOptional[Union[PdSubject, str, List, Dict, PdSet]]
	deadline_date: PdOptional[date]
	deadline_time: PdOptional[time]
	text: PdOptional[str]
	files: PdOptional[PdJson]

	class Config:
		orm_mode = True


class PdSubject(BaseModel):
	group: Union[PdGroup, str, List, Dict, PdSet]
	home_tasks: PdOptional[PdSet[Union[PdHomeTask, str, List, Dict, PdSet]]]
	name: str
	queues: PdOptional[PdSet[Union[PdQueue, str, List, Dict, PdSet]]]
	teachers: PdOptional[PdSet[Union[PdTeacher, str, List, Dict, PdSet]]]
	weekday_and_time_subjects: PdOptional[PdSet[Union[PdWeekdayAndTimeSubject, str, List, Dict, PdSet]]]

	class Config:
		orm_mode = True


class PdWeekdayAndTimeSubject(BaseModel):
	subject: PdOptional[Union[PdSubject, str, List, Dict, PdSet]]
	number_week: int
	weekday: int
	u_time: PdOptional[time] = lambda: time(00, 00)
	classroom_number: PdOptional[str]
	e_learning_url: PdOptional[Union[PdELearningUrl, str, List, Dict, PdSet]]
	update_time: datetime = lambda: datetime.now
	type: PdOptional[str]

	class Config:
		orm_mode = True


class PdELearningUrl(BaseModel):
	id: int
	weekday_and_time_subject: PdOptional[Union[PdWeekdayAndTimeSubject, str, List, Dict, PdSet]]
	url: PdOptional[str]
	login: PdOptional[str]
	password: PdOptional[str]
	additional_info: PdOptional[str]

	class Config:
		orm_mode = True


class PdEvent(BaseModel):
	id: int
	groups: PdOptional[PdSet[Union[PdGroup, str, List, Dict, PdSet]]]
	name: PdOptional[str]
	u_date: PdOptional[date]
	u_time: PdOptional[time]

	class Config:
		orm_mode = True


class PdTeacher(BaseModel):
	id: int
	subjects: PdOptional[PdSet[Union[PdSubject, str, List, Dict, PdSet]]]
	name: str
	email: PdOptional[str]
	phone_number: PdOptional[str]
	vk_url: PdOptional[str]

	class Config:
		orm_mode = True


class PdSeniorInTheGroup(BaseModel):
	user: Union[PdUser, str, List, Dict, PdSet]
	senior_verifications: PdOptional[PdSet[Union[PdSeniorVerification, str, List, Dict, PdSet]]]
	group: Union[PdGroup, str, List, Dict, PdSet]
	is_verification: PdOptional[bool]

	class Config:
		orm_mode = True


class PdNews(BaseModel):
	id: int
	group: PdOptional[Union[PdGroup, str, List, Dict, PdSet]]
	title: PdOptional[str]
	text: PdOptional[str]
	files: PdOptional[PdJson]

	class Config:
		orm_mode = True


class PdNoneVerification(BaseModel):
	it_is_i: Union[PdUser, str, List, Dict, PdSet]
	he_verificate_me: Union[PdUser, str, List, Dict, PdSet]
	confirmation: PdOptional[int] = 0

	class Config:
		orm_mode = True


class PdQueue(BaseModel):
	id: int
	user_has_queues: PdOptional[PdSet[Union[PdUserHasQueue, str, List, Dict, PdSet]]]
	group: Union[PdGroup, str, List, Dict, PdSet]
	name: PdOptional[str]
	subject: PdOptional[Union[PdSubject, str, List, Dict, PdSet]]

	class Config:
		orm_mode = True


class PdUserHasQueue(BaseModel):
	user: Union[PdUser, str, List, Dict, PdSet]
	queue: Union[PdQueue, str, List, Dict, PdSet]
	number: int = -1
	id: int

	class Config:
		orm_mode = True


class PdReminder(BaseModel):
	id: int
	title: PdOptional[str] = "Вы просили о чем-то напомнить"
	text: PdOptional[str] = " "
	reminder_time: datetime
	dustbining_chat: Union[PdDustbiningChat, str, List, Dict, PdSet]

	class Config:
		orm_mode = True


class PdSeniorVerification(BaseModel):
	senior_in_the_group: Union[PdSeniorInTheGroup, str, List, Dict, PdSet]
	user: Union[PdUser, str, List, Dict, PdSet]
	confirmation: int = 0

	class Config:
		orm_mode = True


if __name__ == '__main__':
	from os import chdir

	chdir(HOME_DIR)
