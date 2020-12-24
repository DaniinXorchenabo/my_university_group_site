# -*- coding: utf-8 -*-

"""код, который собирает все зависимости, нужные для БД
Именно он применяется для импорта"""

from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *

from app.settings.config import *
from app.db.models import *
from app.db.db_addition.user_addition import *
from app.db.db_addition.Group_addition import *

from app.db.db_addition.NoneVerification_additions import *
from app.db.db_addition.Admin_additions import *
from app.db.db_addition.SeniorInTheGroup_additions import *
from app.db.tests.create_test_db import *
from app.db.db_control_func import *

if __name__ == '__main__':
    from os import chdir

    chdir(HOME_DIR)
    is_DB_created()
    create_test_db_1()
    show_all()

    # with db_session:
    #     print(User[100].check_password('1234653'))
    #     print(len(User[100]._password), User[100]._password)
    #     print(len(User[100]._get_password), User[100]._get_password)
    #     print(len(User[100]._get_salt_password + User[100]._get_key_password), User[100]._get_salt_password + User[100]._get_key_password)
    #     print(len(User[100]._get_salt_password), User[100]._get_salt_password)
    #     print(len(User[100]._get_key_password), User[100]._get_key_password)
        # print(User[100].password)
    #     print(Group['20ВП1'].users)
    #     Group['20ВП1'].users |= {User[101], User[100]}
    #     print(Group['20ВП1'].users)
    #     print(Group['20ВП1'].no_verificated_users)
    #     commit()

    import hashlib
    import os
    import binascii

    # Пример генерации
    # salt = os.urandom(32)
    # key = hashlib.pbkdf2_hmac('sha256', 'mypassw6ord'.encode('utf-8'), salt, 100000)

    # Хранение как
    # storage = salt + key
    # print(str(binascii.hexlify(storage), encoding="utf-8"))
    # Получение значений обратно
    # salt_from_storage = storage[:32]  # 32 является длиной соли
    # key_from_storage = storage[32:]
    # print(salt_from_storage, key_from_storage)
    # print(salt, key)

    # salt = salt_from_storage  # Получение соли, сохраненной для *этого* пользователя
    # key = key_from_storage  # Получение рассчитанного ключа пользователя
    #
    # password_to_check = 'mypassword'  # Пароль, предоставленный пользователем, проверяется

    # Используется та же настройка для генерации ключа, только на этот раз вставляется для проверки настоящий пароль
    # new_key = hashlib.pbkdf2_hmac(
    #     'sha256',
    #     password_to_check.encode('utf-8'),  # Конвертирование пароля в байты
    #     salt,
    #     100000
    # )

    # if new_key == key:
    #     print('Пароль правильный')
    # else:
    #     print('Пароль неправильный')