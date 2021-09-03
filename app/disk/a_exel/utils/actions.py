from abc import ABC
from typing import Union, Awaitable

from arsenic.actions import Mouse as BaseMouse, chain, Keyboard, Tick, Button
from arsenic.session import Session, Element

from app.disk.a_exel.utils.keyboard import Keys
from app.disk.a_exel.abstractions.cell import AbcCell


class Mouse(BaseMouse):
    def click(self, button: Button = Button.left) -> list:
        return [self.down(button=button), self.up(button=button)]

    def __repr__(self):
        return 'Mouse'


class ActionChain:

    def input_decorator(self, func):
        def _warp(*args, **kwargs):
            res = func(*args, **kwargs)
            self.chain += self.processing([res])
            return res

        if hasattr(func, "__annotations__") and \
                (isinstance(func.__annotations__["return"], Tick) or \
                 "Tick" in str(func.__annotations__["return"])) \
                and func.__name__ != "_tick":
            return _warp
        return func

    def input_cls_decorator(self, obj):
        [setattr(obj, key, self.input_decorator(getattr(obj, key)))
         for key in dir(obj) if not key.startswith("__")]
        return obj

    def __init__(self, *args):
        self.chain = []
        self._mouse = self.input_cls_decorator(Mouse())
        self._keyboard = self.input_cls_decorator(Keyboard())
        self.chain = self.processing(*args)

    def to_chain(self, *args) -> list:
        data = []

        for i in args:
            try:
                if isinstance(i, str) and len(i) == 1:
                    data.extend(i)
                elif _obj := list(iter(i)):
                    data.extend(self.to_chain(*_obj))

            except TypeError:
                data.append(i)

        return data

    def to_press_keys(self, data: list) -> list[Tick]:
        print(self, self.__dict__, dir(self))
        res: list[Tick] = []
        for i in data:
            if isinstance(i, str):
                self._keyboard.down(i)  # добавляются автоматически
                self._keyboard.up(i)  # добавляются автоматически
            elif isinstance(i, Tick):
                res.append(i)
            else:
                res.append(i)

        return res

    def processing(self, *args) -> list[Tick]:
        data = self.to_chain(*args)
        return self.to_press_keys(data)

    def run(self, session: Session) -> Awaitable:
        return session.perform_actions(chain(*self.chain))

    @property
    def mouse(self):
        return self._mouse

    @property
    def keyboard(self):
        return self._keyboard

    def __add__(self, other: Union["ActionChain", list]):
        if isinstance(other, ActionChain):
            self.chain += other.chain
        else:
            self.chain += self.processing(other)
        return self

    def __iadd__(self, other: Union["ActionChain", list]):
        if isinstance(other, ActionChain):
            self.chain += other.chain
        else:
            self.chain += self.processing(other)
        return self


class ActionChainsSet(ABC):

    @classmethod
    def click_to_join_element_button(cls, join_cell_button: Element, actions: ActionChain = None):
        if actions is None:
            actions = ActionChain()
        actions.mouse.move_to(join_cell_button)
        actions.mouse.click()
        return actions

    @classmethod
    def join_cell(cls, keys: Union[list[str], str], join_cell_button, actions: ActionChain = None):
        if actions is None:
            actions = ActionChain()
        actions.keyboard.down(Keys.SHIFT)
        actions += keys,
        actions.keyboard.up(Keys.SHIFT),
        actions = cls.click_to_join_element_button(join_cell_button, actions)
        return actions

    @classmethod
    def go_as_teleport(cls, cell: Union[str, AbcCell], table_name_el: Element, actions: ActionChain = None):
        if isinstance(cell, AbcCell):
            cell: str = cell.name
        if actions is None:
            actions = ActionChain()
        actions.mouse.move_to(table_name_el)
        actions.mouse.click()
        actions.mouse.click()
        actions += Keys.BACKSPACE * 10
        actions += cell
        actions += Keys.ENTER
        return actions
