# -*- coding: utf-8 -*-

"""Дополнения к сущности старосты группы"""

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *
from app.db.db_addition.user_addition import *


if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)


@SeniorInTheGroup.only_func
def __init__(self, *args, **kwargs):
    if not (type(kwargs.get('user')) == User and kwargs.get('user').groups == kwargs['group']):
        # если польхователь не принадлежит указанной группе, то сущность старосты не создается
        del self
        return
    if not kwargs.get('user').is_verificated:
        # Если пользователь не верифициррован, то он не может быть старостой
        del self
        return
    if type(kwargs.get('user')) == User:  # на всякий случай верифицируем пользователя
        kwargs['user'].is_verification = True
    # староста не верифицирован, если явно не указано обратное
    kwargs['is_verification'] = kwargs.get('is_verification', False)
    print('^^^^^^^^^^^^^^^^^^^---------')
    super(SeniorInTheGroup, self).__init__(*args, **kwargs)
    if not kwargs['is_verification']:  # Если староста не верифицирован
        if SeniorInTheGroup.exists(**kwargs):
            print('существует')
            my_group_friends = set(kwargs['group'].users) - {kwargs.get('user')}
            print(my_group_friends)
            [SeniorVerification(senior_in_the_group=self, user=u) for u in my_group_friends
             if not SeniorVerification.exists(senior_in_the_group=self, user=u)]
            commit()  # создаем ему тех, кто будет его верифицировать
        else:
            print('не существует')
    else:
        print('староста верифицирован при инициализации')


@SeniorInTheGroup.getter_and_classmethod
def check_verificated(self):
    """если по большинству голосов за старосту он получается веривицированным, то функция верифицирует его"""
    if not self._is_verification:
        if not bool(self.senior_verifications):
            my_group_friends = set(select(i for i in self.group.users)[:]) - {self._user}
            [SeniorVerification(senior_in_the_group=self, user=u) for u in my_group_friends
             if not SeniorVerification.exists(senior_in_the_group=self, user=u)]
            commit()
            if not bool(self.senior_verifications):
                self._is_verification = True
                return True
        num, count, *_ = zip(*((i.confirmation, 1) for i in self.senior_verifications.select()))
        # print(self, num, count, sum(count) // 2 <= sum(num),  not (sum(num) == 1 and sum(count) == 0))
        if sum(count) // 2 <= sum(num) and not (sum(num) == 0 and sum(count) == 1):
            self._is_verification = True
            delete(i for i in self.senior_verifications)
            commit()
            # print('-----True')
            return True
        # print('-----False')
        return False
    # User._expanded_white_list.add('groups')
    # gr = self._groups
    # print('------', [gr])
    return True


def protect_verification(attr_name='is_verification'):
    new_attr_name = '_' + attr_name

    def decorator(cls):
        print('!!!!!!!!!!')

        @property
        def attr(self):
            return self._is_verification

        @attr.setter
        def attr(self, val):
            if val:
                delete(i for i in self.senior_verifications)
            else:
                my_group_friends = set(select(i for i in self.group.users)[:]) - {self.user}
                [SeniorVerification(senior_in_the_group=self, user=u) for u in my_group_friends
                 if not SeniorVerification.exists(senior_in_the_group=self, user=u)]
            setattr(self, new_attr_name, val)
            commit()

            return True

        last_attr = getattr(cls, attr_name)
        setattr(cls, new_attr_name, last_attr)
        setattr(cls, attr_name, attr)
        return cls

    return decorator


def protect_user(attr_name='user'):
    new_attr_name = '_' + attr_name

    def decorator(cls):
        print('!!!!!!!!!!')

        @property
        def attr(self):
            return getattr(self, new_attr_name)

        @attr.setter
        def attr(self, val):
            if not val:
                delete(i for i in self.senior_verifications)
            else:
                if type(val) == User:
                    delete(i for i in self.senior_verifications)
                    commit()
                    my_group_friends = set(select(i for i in self.group.users)[:]) - {self.user}
                    [SeniorVerification(senior_in_the_group=self, user=u) for u in my_group_friends
                     if not SeniorVerification.exists(senior_in_the_group=self, user=u)]
                else:
                    return False
            setattr(self, new_attr_name, val)
            commit()

            return True

        last_attr = getattr(cls, attr_name)
        setattr(cls, new_attr_name, last_attr)
        setattr(cls, attr_name, attr)
        return cls

    return decorator


SeniorInTheGroup = protect_verification(attr_name='is_verification')(SeniorInTheGroup)
SeniorInTheGroup = protect_user(attr_name='user')(SeniorInTheGroup)
change_field[SeniorInTheGroup] = change_field.get(User, []) + ['is_verification', 'user']