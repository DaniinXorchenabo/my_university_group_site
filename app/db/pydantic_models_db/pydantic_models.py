# -*- coding: utf-8 -*-

""" Этот код генерируется автоматически,
ни одно изменение не сохранится в этом файле.
Тут объявляются pydantic-модели, в которых присутствуют все сущности БД
и все атрибуты сущностей"""

from typing import Set as PdSet, Union, List, Dict, Tuple, ForwardRef
from typing import Optional as PdOptional
from datetime import date, datetime, time

from pony.orm import *
from pydantic import BaseModel, Json as PdJson

from app.db.models import *


PdAdmin = ForwardRef("PdAdmin")
PdUser = ForwardRef("PdUser")
PdDustbiningChat = ForwardRef("PdDustbiningChat")
PdImportantChat = ForwardRef("PdImportantChat")
PdImportantMessage = ForwardRef("PdImportantMessage")
PdGroup = ForwardRef("PdGroup")
PdHomeTask = ForwardRef("PdHomeTask")
PdSubject = ForwardRef("PdSubject")
PdWeekdayAndTimeSubject = ForwardRef("PdWeekdayAndTimeSubject")
PdELearningUrl = ForwardRef("PdELearningUrl")
PdEvent = ForwardRef("PdEvent")
PdTeacher = ForwardRef("PdTeacher")
PdSeniorInTheGroup = ForwardRef("PdSeniorInTheGroup")
PdNews = ForwardRef("PdNews")
PdNoneVerification = ForwardRef("PdNoneVerification")
PdQueue = ForwardRef("PdQueue")
PdUserHasQueue = ForwardRef("PdUserHasQueue")
PdReminder = ForwardRef("PdReminder")
PdSeniorVerification = ForwardRef("PdSeniorVerification")


class PdAdmin(BaseModel):
	user: Union[Dict, int, PdUser, Dict]

	class Config:
		orm_mode = True


class PdUser(BaseModel):
	id: int
	name: PdOptional[str]
	login: str
	password: PdOptional[str]
	email: PdOptional[str]
	user_has_queues: PdOptional[List[Union[Dict, int, PdUserHasQueue, Dict, None]]] = [None]
	session_key_for_app: PdOptional[str]
	getting_time_session_key: PdOptional[datetime]
	admin: PdOptional[Union[Dict, Union[Dict, int, PdUser, Dict], PdAdmin, Dict]]
	login_EIES: PdOptional[str]
	password_EIES: PdOptional[str]
	my_verification: PdOptional[List[Union[Dict, Tuple[Union[Dict, int, PdUser, Dict], Union[Dict, int, PdUser, Dict]], PdNoneVerification, Dict, None]]] = [None]
	i_verificate_thei: PdOptional[List[Union[Dict, Tuple[Union[Dict, int, PdUser, Dict], Union[Dict, int, PdUser, Dict]], PdNoneVerification, Dict, None]]] = [None]
	senior_in_the_group: PdOptional[Union[Dict, Tuple[Union[Dict, int, PdUser, Dict], Union[Dict, str, PdGroup, Dict]], PdSeniorInTheGroup, Dict]]
	curse_count: PdOptional[int]
	senior_verification: PdOptional[Union[Dict, Union[Dict, int, PdUser, Dict], PdSeniorVerification, Dict]]
	groups: PdOptional[Union[Dict, str, PdGroup, Dict]]

	class Config:
		orm_mode = True


class PdDustbiningChat(BaseModel):
	id: int
	group: PdOptional[Union[Dict, str, PdGroup, Dict]]
	reminders: PdOptional[List[Union[Dict, int, PdReminder, Dict, None]]] = [None]

	class Config:
		orm_mode = True


class PdImportantChat(BaseModel):
	id: int
	important_messages: PdOptional[List[Union[Dict, int, PdImportantMessage, Dict, None]]] = [None]
	group: PdOptional[List[Union[Dict, str, PdGroup, Dict, None]]] = [None]

	class Config:
		orm_mode = True


class PdImportantMessage(BaseModel):
	id: int
	important_chat: PdOptional[Union[Dict, int, PdImportantChat, Dict]]
	text: PdOptional[str]

	class Config:
		orm_mode = True


class PdGroup(BaseModel):
	senior_in_the_group: PdOptional[Union[Dict, Tuple[Union[Dict, int, PdUser, Dict], Union[Dict, str, PdGroup, Dict]], PdSeniorInTheGroup, Dict]]
	users: PdOptional[List[Union[Dict, int, PdUser, Dict, None]]] = [None]
	dustbining_chats: PdOptional[List[Union[Dict, int, PdDustbiningChat, Dict, None]]] = [None]
	important_chats: PdOptional[List[Union[Dict, int, PdImportantChat, Dict, None]]] = [None]
	subjects: PdOptional[List[Union[Dict, Tuple[Union[Dict, str, PdGroup, Dict], str], PdSubject, Dict, None]]] = [None]
	name: str
	events: PdOptional[List[Union[Dict, int, PdEvent, Dict, None]]] = [None]
	timesheet_update: datetime = lambda: datetime.now
	news: PdOptional[List[Union[Dict, int, PdNews, Dict, None]]] = [None]
	queues: PdOptional[List[Union[Dict, int, PdQueue, Dict, None]]] = [None]

	class Config:
		orm_mode = True


class PdHomeTask(BaseModel):
	id: int
	subject: PdOptional[Union[Dict, Tuple[Union[Dict, str, PdGroup, Dict], str], PdSubject, Dict]]
	deadline_date: PdOptional[date]
	deadline_time: PdOptional[time]
	text: PdOptional[str]
	files: PdOptional[PdJson]

	class Config:
		orm_mode = True


class PdSubject(BaseModel):
	group: Union[Dict, str, PdGroup, Dict]
	home_tasks: PdOptional[List[Union[Dict, int, PdHomeTask, Dict, None]]] = [None]
	name: str
	queues: PdOptional[List[Union[Dict, int, PdQueue, Dict, None]]] = [None]
	teachers: PdOptional[List[Union[Dict, int, PdTeacher, Dict, None]]] = [None]
	weekday_and_time_subjects: PdOptional[List[Union[Dict, int, PdWeekdayAndTimeSubject, Dict, None]]] = [None]

	class Config:
		orm_mode = True


class PdWeekdayAndTimeSubject(BaseModel):
	id: int
	subject: PdOptional[Union[Dict, Tuple[Union[Dict, str, PdGroup, Dict], str], PdSubject, Dict]]
	number_week: int
	weekday: int
	u_time: PdOptional[time] = lambda: time(00, 00)
	classroom_number: PdOptional[str]
	e_learning_url: PdOptional[Union[Dict, int, PdELearningUrl, Dict]]
	update_time: datetime = lambda: datetime.now
	type: PdOptional[str]

	class Config:
		orm_mode = True


class PdELearningUrl(BaseModel):
	id: int
	weekday_and_time_subject: PdOptional[Union[Dict, int, PdWeekdayAndTimeSubject, Dict]]
	url: PdOptional[str]
	login: PdOptional[str]
	password: PdOptional[str]
	additional_info: PdOptional[str]

	class Config:
		orm_mode = True


class PdEvent(BaseModel):
	id: int
	groups: PdOptional[List[Union[Dict, str, PdGroup, Dict, None]]] = [None]
	name: PdOptional[str]
	u_date: PdOptional[date]
	u_time: PdOptional[time]

	class Config:
		orm_mode = True


class PdTeacher(BaseModel):
	id: int
	subjects: PdOptional[List[Union[Dict, Tuple[Union[Dict, str, PdGroup, Dict], str], PdSubject, Dict, None]]] = [None]
	name: str
	email: PdOptional[str]
	phone_number: PdOptional[str]
	vk_url: PdOptional[str]

	class Config:
		orm_mode = True


class PdSeniorInTheGroup(BaseModel):
	user: Union[Dict, int, PdUser, Dict]
	senior_verifications: PdOptional[List[Union[Dict, Union[Dict, int, PdUser, Dict], PdSeniorVerification, Dict, None]]] = [None]
	group: Union[Dict, str, PdGroup, Dict]
	is_verification: PdOptional[bool]

	class Config:
		orm_mode = True


class PdNews(BaseModel):
	id: int
	group: PdOptional[Union[Dict, str, PdGroup, Dict]]
	title: PdOptional[str]
	text: PdOptional[str]
	files: PdOptional[PdJson]

	class Config:
		orm_mode = True


class PdNoneVerification(BaseModel):
	it_is_i: Union[Dict, int, PdUser, Dict]
	he_verificate_me: Union[Dict, int, PdUser, Dict]
	confirmation: PdOptional[int] = 0

	class Config:
		orm_mode = True


class PdQueue(BaseModel):
	id: int
	user_has_queues: PdOptional[List[Union[Dict, int, PdUserHasQueue, Dict, None]]] = [None]
	group: Union[Dict, str, PdGroup, Dict]
	name: PdOptional[str]
	subject: PdOptional[Union[Dict, Tuple[Union[Dict, str, PdGroup, Dict], str], PdSubject, Dict]]

	class Config:
		orm_mode = True


class PdUserHasQueue(BaseModel):
	user: Union[Dict, int, PdUser, Dict]
	queue: Union[Dict, int, PdQueue, Dict]
	number: int = -1
	id: int

	class Config:
		orm_mode = True


class PdReminder(BaseModel):
	id: int
	title: PdOptional[str] = "Вы просили о чем-то напомнить"
	text: PdOptional[str] = " "
	reminder_time: datetime
	dustbining_chat: Union[Dict, int, PdDustbiningChat, Dict]

	class Config:
		orm_mode = True


class PdSeniorVerification(BaseModel):
	senior_in_the_group: Union[Dict, Tuple[Union[Dict, int, PdUser, Dict], Union[Dict, str, PdGroup, Dict]], PdSeniorInTheGroup, Dict]
	user: Union[Dict, int, PdUser, Dict]
	confirmation: int = 0

	class Config:
		orm_mode = True


PdAdmin.update_forward_refs()
PdUser.update_forward_refs()
PdDustbiningChat.update_forward_refs()
PdImportantChat.update_forward_refs()
PdImportantMessage.update_forward_refs()
PdGroup.update_forward_refs()
PdHomeTask.update_forward_refs()
PdSubject.update_forward_refs()
PdWeekdayAndTimeSubject.update_forward_refs()
PdELearningUrl.update_forward_refs()
PdEvent.update_forward_refs()
PdTeacher.update_forward_refs()
PdSeniorInTheGroup.update_forward_refs()
PdNews.update_forward_refs()
PdNoneVerification.update_forward_refs()
PdQueue.update_forward_refs()
PdUserHasQueue.update_forward_refs()
PdReminder.update_forward_refs()
PdSeniorVerification.update_forward_refs()


if __name__ == '__main__':
	from os import chdir

	chdir(HOME_DIR)
