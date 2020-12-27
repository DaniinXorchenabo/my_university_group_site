# -*- coding: utf-8 -*-

"""Этот код генерируется автоматически,
ни одно изменение не сохранится в этом файле.
Тут объявляются pydantic-модели, в которых присутствуют все сущности БД и все атрибуты сущностей"""


from datetime import date, datetime, time
from pony.orm import *
from typing import Optional

from pydantic import BaseModel
from app.db.models import *

class Admin(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class User(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class DustbiningChat(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class ImportantChat(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class ImportantMessage(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class Group(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class HomeTask(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class Subject(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class WeekdayAndTimeSubject(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class ELearningUrl(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class Event(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class Teacher(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class SeniorInTheGroup(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class News(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class NoneVerification(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class Queue(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class UserHasQueue(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class Reminder(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


class SeniorVerification(BaseModel):
	id: int
	name: Optional[str] = None
	login: str
	password: Optional[str] = None
	email: Optional[str] = None
	user_has_queues: Set[UserHasQueue] = None
	session_key_for_app: Optional[str] = None
	getting_time_session_key: Optional[datetime] = None
	admin: Optional[Admin] = None
	login_EIES: Optional[str] = None
	password_EIES: Optional[str] = None
	my_verification: Set[NoneVerification] = None
	i_verificate_thei: Set[NoneVerification] = None
	senior_in_the_group: Optional[SeniorInTheGroup] = None
	curse_count: Optional[int] = None
	senior_verification: Optional[SeniorVerification] = None
	groups: Optional[Group] = None


if __name__ == '__main__':
	from os import chdir

	chdir(HOME_DIR)
