# -*- coding: utf-8 -*-

""" Этот код генерируется автоматически,
функцией create_pydantic_models файла app/db/bd_control_func.py
Ни одно изменение не сохранится в этом файле.
Тут объявляются pydantic-модели, в которых присутствуют все сущности БД
и все атрибуты сущностей"""

from typing import Set as PdSet, Union, List, Dict, Tuple, ForwardRef
from typing import Optional as PdOptional, Literal, Any
from datetime import date, datetime, time

from pony.orm import *
from pydantic import BaseModel, Json as PdJson

from app.db.models import *

from app.db.pydantic_models_db.pony_orm_to_pydantic_utils import *


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


class MyGetterDictAdmin(MyGetterDict):
    modif_type_rules = {}


class MyGetterDictUser(MyGetterDict):
    modif_type_rules = {
"user_has_queues": lambda i: list(i.select()[:]),
        "my_verification": lambda i: list(i.select()[:]),
        "i_verificate_thei": lambda i: list(i.select()[:]),
    }


class MyGetterDictDustbiningChat(MyGetterDict):
    modif_type_rules = {
"reminders": lambda i: list(i.select()[:]),
    }


class MyGetterDictImportantChat(MyGetterDict):
    modif_type_rules = {
"important_messages": lambda i: list(i.select()[:]),
        "group": lambda i: list(i.select()[:]),
    }


class MyGetterDictImportantMessage(MyGetterDict):
    modif_type_rules = {}


class MyGetterDictGroup(MyGetterDict):
    modif_type_rules = {
"users": lambda i: list(i.select()[:]),
        "dustbining_chats": lambda i: list(i.select()[:]),
        "important_chats": lambda i: list(i.select()[:]),
        "subjects": lambda i: list(i.select()[:]),
        "events": lambda i: list(i.select()[:]),
        "news": lambda i: list(i.select()[:]),
        "queues": lambda i: list(i.select()[:]),
    }


class MyGetterDictHomeTask(MyGetterDict):
    modif_type_rules = {}


class MyGetterDictSubject(MyGetterDict):
    modif_type_rules = {
"home_tasks": lambda i: list(i.select()[:]),
        "queues": lambda i: list(i.select()[:]),
        "teachers": lambda i: list(i.select()[:]),
        "weekday_and_time_subjects": lambda i: list(i.select()[:]),
    }


class MyGetterDictWeekdayAndTimeSubject(MyGetterDict):
    modif_type_rules = {}


class MyGetterDictELearningUrl(MyGetterDict):
    modif_type_rules = {}


class MyGetterDictEvent(MyGetterDict):
    modif_type_rules = {
"groups": lambda i: list(i.select()[:]),
    }


class MyGetterDictTeacher(MyGetterDict):
    modif_type_rules = {
"subjects": lambda i: list(i.select()[:]),
    }


class MyGetterDictSeniorInTheGroup(MyGetterDict):
    modif_type_rules = {
"senior_verifications": lambda i: list(i.select()[:]),
    }


class MyGetterDictNews(MyGetterDict):
    modif_type_rules = {}


class MyGetterDictNoneVerification(MyGetterDict):
    modif_type_rules = {}


class MyGetterDictQueue(MyGetterDict):
    modif_type_rules = {
"user_has_queues": lambda i: list(i.select()[:]),
    }


class MyGetterDictUserHasQueue(MyGetterDict):
    modif_type_rules = {}


class MyGetterDictReminder(MyGetterDict):
    modif_type_rules = {}


class MyGetterDictSeniorVerification(MyGetterDict):
    modif_type_rules = {}




class PdAdmin(BaseModel):
	user: PdOptional[Union[Dict, int, PdUser, Dict]]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["user"]
		unique_params = []
		return check_model(cls, values, Admin, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictAdmin
		my_primaty_key_field = ["user"]
		my_required_fields = []


class PdUser(BaseModel):
	id: PdOptional[int]
	name: PdOptional[str]
	login: PdOptional[str]
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
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = ['login', 'email']
		return check_model(cls, values, User, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictUser
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdDustbiningChat(BaseModel):
	id: PdOptional[int]
	group: PdOptional[Union[Dict, str, PdGroup, Dict]]
	reminders: PdOptional[List[Union[Dict, int, PdReminder, Dict, None]]] = [None]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = []
		return check_model(cls, values, DustbiningChat, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictDustbiningChat
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdImportantChat(BaseModel):
	id: PdOptional[int]
	important_messages: PdOptional[List[Union[Dict, int, PdImportantMessage, Dict, None]]] = [None]
	group: PdOptional[List[Union[Dict, str, PdGroup, Dict, None]]] = [None]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = []
		return check_model(cls, values, ImportantChat, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictImportantChat
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdImportantMessage(BaseModel):
	id: PdOptional[int]
	important_chat: PdOptional[Union[Dict, int, PdImportantChat, Dict]]
	text: PdOptional[str]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = []
		return check_model(cls, values, ImportantMessage, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictImportantMessage
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdGroup(BaseModel):
	senior_in_the_group: PdOptional[Union[Dict, Tuple[Union[Dict, int, PdUser, Dict], Union[Dict, str, PdGroup, Dict]], PdSeniorInTheGroup, Dict]]
	users: PdOptional[List[Union[Dict, int, PdUser, Dict, None]]] = [None]
	dustbining_chats: PdOptional[List[Union[Dict, int, PdDustbiningChat, Dict, None]]] = [None]
	important_chats: PdOptional[List[Union[Dict, int, PdImportantChat, Dict, None]]] = [None]
	subjects: PdOptional[List[Union[Dict, Tuple[Union[Dict, str, PdGroup, Dict], str], PdSubject, Dict, None]]] = [None]
	name: PdOptional[str]
	events: PdOptional[List[Union[Dict, int, PdEvent, Dict, None]]] = [None]
	timesheet_update: PdOptional[datetime] = lambda: datetime.now
	news: PdOptional[List[Union[Dict, int, PdNews, Dict, None]]] = [None]
	queues: PdOptional[List[Union[Dict, int, PdQueue, Dict, None]]] = [None]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["name"]
		unique_params = []
		return check_model(cls, values, Group, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictGroup
		my_primaty_key_field = ["name"]
		my_required_fields = []


class PdHomeTask(BaseModel):
	id: PdOptional[int]
	subject: PdOptional[Union[Dict, Tuple[Union[Dict, str, PdGroup, Dict], str], PdSubject, Dict]]
	deadline_date: PdOptional[date]
	deadline_time: PdOptional[time]
	text: PdOptional[str]
	files: PdOptional[PdJson]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = []
		return check_model(cls, values, HomeTask, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictHomeTask
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdSubject(BaseModel):
	group: PdOptional[Union[Dict, str, PdGroup, Dict]]
	home_tasks: PdOptional[List[Union[Dict, int, PdHomeTask, Dict, None]]] = [None]
	name: PdOptional[str]
	queues: PdOptional[List[Union[Dict, int, PdQueue, Dict, None]]] = [None]
	teachers: PdOptional[List[Union[Dict, int, PdTeacher, Dict, None]]] = [None]
	weekday_and_time_subjects: PdOptional[List[Union[Dict, int, PdWeekdayAndTimeSubject, Dict, None]]] = [None]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = [("group", "name")]
		unique_params = []
		return check_model(cls, values, Subject, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictSubject
		my_primaty_key_field = [("group", "name")]
		my_required_fields = []


class PdWeekdayAndTimeSubject(BaseModel):
	id: PdOptional[int]
	subject: PdOptional[Union[Dict, Tuple[Union[Dict, str, PdGroup, Dict], str], PdSubject, Dict]]
	number_week: PdOptional[int]
	weekday: PdOptional[int]
	u_time: PdOptional[time] = lambda: time(00, 00)
	classroom_number: PdOptional[str]
	e_learning_url: PdOptional[Union[Dict, int, PdELearningUrl, Dict]]
	update_time: PdOptional[datetime] = lambda: datetime.now
	type: PdOptional[str]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = []
		return check_model(cls, values, WeekdayAndTimeSubject, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictWeekdayAndTimeSubject
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdELearningUrl(BaseModel):
	id: PdOptional[int]
	weekday_and_time_subject: PdOptional[Union[Dict, int, PdWeekdayAndTimeSubject, Dict]]
	url: PdOptional[str]
	login: PdOptional[str]
	password: PdOptional[str]
	additional_info: PdOptional[str]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = []
		return check_model(cls, values, ELearningUrl, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictELearningUrl
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdEvent(BaseModel):
	id: PdOptional[int]
	groups: PdOptional[List[Union[Dict, str, PdGroup, Dict, None]]] = [None]
	name: PdOptional[str]
	u_date: PdOptional[date]
	u_time: PdOptional[time]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = []
		return check_model(cls, values, Event, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictEvent
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdTeacher(BaseModel):
	id: PdOptional[int]
	subjects: PdOptional[List[Union[Dict, Tuple[Union[Dict, str, PdGroup, Dict], str], PdSubject, Dict, None]]] = [None]
	name: PdOptional[str]
	email: PdOptional[str]
	phone_number: PdOptional[str]
	vk_url: PdOptional[str]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = []
		return check_model(cls, values, Teacher, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictTeacher
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdSeniorInTheGroup(BaseModel):
	user: PdOptional[Union[Dict, int, PdUser, Dict]]
	senior_verifications: PdOptional[List[Union[Dict, Union[Dict, int, PdUser, Dict], PdSeniorVerification, Dict, None]]] = [None]
	group: PdOptional[Union[Dict, str, PdGroup, Dict]]
	is_verification: PdOptional[bool]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = [("user", "group")]
		unique_params = []
		return check_model(cls, values, SeniorInTheGroup, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictSeniorInTheGroup
		my_primaty_key_field = [("user", "group")]
		my_required_fields = []


class PdNews(BaseModel):
	id: PdOptional[int]
	group: PdOptional[Union[Dict, str, PdGroup, Dict]]
	title: PdOptional[str]
	text: PdOptional[str]
	files: PdOptional[PdJson]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = []
		return check_model(cls, values, News, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictNews
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdNoneVerification(BaseModel):
	it_is_i: PdOptional[Union[Dict, int, PdUser, Dict]]
	he_verificate_me: PdOptional[Union[Dict, int, PdUser, Dict]]
	confirmation: PdOptional[int] = 0
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = [("it_is_i", "he_verificate_me")]
		unique_params = []
		return check_model(cls, values, NoneVerification, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictNoneVerification
		my_primaty_key_field = [("it_is_i", "he_verificate_me")]
		my_required_fields = []


class PdQueue(BaseModel):
	id: PdOptional[int]
	user_has_queues: PdOptional[List[Union[Dict, int, PdUserHasQueue, Dict, None]]] = [None]
	group: PdOptional[Union[Dict, str, PdGroup, Dict]]
	name: PdOptional[str]
	subject: PdOptional[Union[Dict, Tuple[Union[Dict, str, PdGroup, Dict], str], PdSubject, Dict]]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = []
		return check_model(cls, values, Queue, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictQueue
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdUserHasQueue(BaseModel):
	user: PdOptional[Union[Dict, int, PdUser, Dict]]
	queue: PdOptional[Union[Dict, int, PdQueue, Dict]]
	number: PdOptional[int] = -1
	id: PdOptional[int]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = []
		return check_model(cls, values, UserHasQueue, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictUserHasQueue
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdReminder(BaseModel):
	id: PdOptional[int]
	title: PdOptional[str] = "Вы просили о чем-то напомнить"
	text: PdOptional[str] = " "
	reminder_time: PdOptional[datetime]
	dustbining_chat: PdOptional[Union[Dict, int, PdDustbiningChat, Dict]]
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["id"]
		unique_params = []
		return check_model(cls, values, Reminder, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictReminder
		my_primaty_key_field = ["id"]
		my_required_fields = []


class PdSeniorVerification(BaseModel):
	senior_in_the_group: PdOptional[Union[Dict, Tuple[Union[Dict, int, PdUser, Dict], Union[Dict, str, PdGroup, Dict]], PdSeniorInTheGroup, Dict]]
	user: PdOptional[Union[Dict, int, PdUser, Dict]]
	confirmation: PdOptional[int] = 0
	mode: PdOptional[Union[Literal["new"], Literal["edit"], Literal["find"], Literal["strict_find"]]] = None
	upload_orm: PdOptional[Union[bool, Literal["min"]]] = None
	primary_key: Any = None

	@root_validator
	def check_orm_correcting_model(cls, values):
		primary_keys = ["user"]
		unique_params = []
		return check_model(cls, values, SeniorVerification, pk=primary_keys, unique=unique_params)

	class Config:
		orm_mode = True
		getter_dict = MyGetterDictSeniorVerification
		my_primaty_key_field = ["user"]
		my_required_fields = []


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
