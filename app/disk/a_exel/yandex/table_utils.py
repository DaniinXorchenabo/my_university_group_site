from typing import Union

from arsenic.session import Session, Element

from app.disk.a_exel.utils.keyboard import Keys
from app.disk.a_exel.yandex.base_utils import BaseUtils


__all__ = ["TableUtils"]


class TableUtils(BaseUtils):

    @classmethod
    async def send_keys_to_active_element(cls, session: Session,
                                          value: Union[str, list[str, Keys, int]]) -> Element:
        # print([cls.keys_to_typing(value), value])
        return await session.request(
            "/keys", method="POST",
            data={"value": (_list := cls._keys_to_typing(value)),
                  "text": "".join(_list)})

    @staticmethod
    def _keys_to_typing(value) -> list:
        """ Copy paste from Selenium

        Processes the values that will be typed in the element."""

        typing = []
        for val in value:
            if isinstance(val, Keys):
                typing.append(val)
            elif isinstance(val, int):
                val = str(val)
                for i in range(len(val)):
                    typing.append(val[i])
            else:
                for i in range(len(val)):
                    typing.append(val[i])
        return typing


