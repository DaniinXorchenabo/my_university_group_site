from typing import Union, Optional

from arsenic.session import Session, Element

from app.disk.a_exel.utils.actions import ActionChainsSet
from app.disk.a_exel.utils.keyboard import Keys
from app.disk.a_exel.abstractions.cell import AbcCell
from app.disk.a_exel.yandex.cell_utils import CellUtils
from app.disk.exel.cells import BaseCell


__all__ = ["Cell"]


class Cell(AbcCell, CellUtils):
    how_to_move = ["teleport", "walk"][1]

    def __init__(self, session: Session, abc_cell: BaseCell, names: Union[tuple[int, int], str, list[str]]):
        super().__init__(abc_cell, names)
        self.session = session

    async def go_to(self, *args, where: str = None,  how_to_move: str = None, **kwargs):
        """Общий метод перемещения. Зависит от настроек класса"""
        if where is None:
            where = self.name
        if how_to_move is None:
            how_to_move = self.how_to_move
        if how_to_move == "teleport":
            return await self.go_as_teleport(where)
        else:
            return await self.go_as_walk(where) not in [False, None]

    async def go_as_teleport(self, where: str = None):
        if where is None:
            where = self.name
        table_name_el = await self.get_cell_name_el(self.session)
        actions = ActionChainsSet.go_as_teleport(where, table_name_el)
        await actions.run(self.session)
        return (await self.get_cell_name(self.session)) == where

    async def go_as_walk(self, where: str = None) -> Union[list[str], bool, None]:
        if where is None:
            where = self.name
        *where_ind, _ = self.name_to_ind(where)
        last_ind = (None, None)
        last_last_ind = (None, None)
        keys_list = []
        cells_history = []
        last_cell = None
        # reverse in [0, 2] - идем сначала вниз (или вверх),
        #                       а потом вправо (или влево)
        # reverse in [1, 3] - идем сначала влево (или вправо),
        #                       а потом вверх (или вниз)
        reverse: int = 0

        def how_key(now: str, finish: str,
                    last: Optional[str] = None,
                    last_last: Optional[str] = None) -> Optional[str]:
            nonlocal where_ind, last_ind, reverse, last_last_ind, cells_history
            *now_ind, _ = self.name_to_ind(now)

            def left_or_right():
                nonlocal where_ind, now_ind, last_ind
                return Keys.ARROW_RIGHT if now_ind[1] < where_ind[1] else Keys.ARROW_LEFT

            def up_or_down():
                nonlocal where_ind, now_ind, last_ind
                return Keys.ARROW_DOWN if now_ind[0] < where_ind[0] else Keys.ARROW_UP

            key = ""
            # если выделенная ячейка
            # находится в одной строке с целевой ячецкой
            if last_last_ind[0] == now_ind[0] and last_last_ind[1] == now_ind[1]:
                reverse -= 1
            # print([now], cells_history)
            if reverse > 20:
                return None
            elif cells_history.count(now) > 5:
                return None
            elif reverse > 3:
                if now_ind[0] == where_ind[0]:
                    key = left_or_right()
                elif now_ind[1] == where_ind[1]:
                    key = up_or_down()
                else:
                    if reverse % 2 == 0:
                        key = left_or_right()
                    else:
                        key = up_or_down()
                    reverse += 1
            elif reverse % 2 != 0:
                if now_ind[1] == where_ind[1]:
                    key = up_or_down()
                else:
                    if last_ind[0] is None or \
                            last_ind[0] <= now_ind[0] < where_ind[0] or \
                            where_ind[0] < now_ind[0] <= last_ind[0] or \
                            (last_last_ind[0] == now_ind[0] and last_last_ind[1] == now_ind[1]):

                        key = left_or_right()
                    else:
                        reverse += 1
                        return how_key(now, finish, last)
                # last_ind = now_ind
            elif reverse % 2 == 0:
                if now_ind[0] == where_ind[0]:
                    key = left_or_right()
                else:
                    if last_ind[1] is None or \
                            last_ind[1] <= now_ind[1] < where_ind[1] or \
                            where_ind[1] < now_ind[1] <= last_ind[1] or \
                            (last_last_ind[0] == now_ind[0] and last_last_ind[1] == now_ind[1]):
                        key = up_or_down()
                    else:
                        reverse += 1
                        return how_key(now, finish, last)

            if last_last_ind[0] == now_ind[0] and last_last_ind[1] == now_ind[1]:
                reverse += 1

            last_last_ind = (last_ind[0], last_ind[1])
            last_ind = (now_ind[0], now_ind[1])
            return key

        while True:
            now_cell = await self.get_cell_name(self.session)
            if now_cell == where:
                return keys_list
            elif (_key := how_key(now_cell, where, last_cell)) is not None:
                el = await self.get_active_element(self.session)
                keys_list.append(_key)
                cells_history.append(now_cell)
                await el.send_keys(_key)
                last_cell = now_cell
            else:
                return await self.go_as_teleport(where)

    # async def _get_keys_to_cell(self, join_cell_button: Element,
    #                             top_left_cell: str, bottom_right_cell: str):
    #
    #     if (await self.go_as_walk(top_left_cell)) in [False, None]:
    #         actions = ActionChainsSet.click_to_join_element_button(join_cell_button)
    #         await actions.run(self.session)
    #         await self.go_as_walk(top_left_cell)
    #     keys = await self.go_as_walk(bottom_right_cell)
    #     if keys in [False, None]:
    #         actions = ActionChainsSet.click_to_join_element_button(join_cell_button)
    #         await actions.run(self.session)
    #         await self.go_as_walk(bottom_right_cell)
    #     reverse_keys = await self.go_as_walk(top_left_cell)
    #     if keys in [False, None]:
    #         keys = await self.go_as_walk(bottom_right_cell)
    #         keys, reverse_keys = reverse_keys, keys
    #         top_left_cell, bottom_right_cell = bottom_right_cell, top_left_cell
    #     return keys, reverse_keys, top_left_cell, bottom_right_cell
    #
    # async def rejoin_cells_to_names(self, top_left_cell: str, bottom_right_cell: str):
    #     """Разъеденить указанные ячейки"""
    #     join_cell_button = await self.get_join_button(self.session)
    #     table_name_el = await self.get_cell_name_el(self.session)
    #     keys, _, top_left_cell, bottom_right_cell = await self._get_keys_to_cell(join_cell_button, top_left_cell, bottom_right_cell)
    #     actions1 = ActionChainsSet.join_cell(keys, join_cell_button)
    #     await actions1.run(self.session)
    #     [(await i.send_keys(Keys.ENTER)) for i in await self.session.get_elements("button[result=yes]")]
    #
    #     actions2 = ActionChainsSet.go_as_teleport(top_left_cell, table_name_el)
    #     actions2 = ActionChainsSet.click_to_join_element_button(join_cell_button, actions=actions2)
    #     actions2 = ActionChainsSet.go_as_teleport(top_left_cell, table_name_el, actions=actions2)
    #     actions2 += Keys.ENTER
    #     actions2 = ActionChainsSet.click_to_join_element_button(join_cell_button, actions=actions2)
    #     actions2 = ActionChainsSet.go_as_teleport(top_left_cell, table_name_el, actions=actions2)
    #     await actions2.run(self.session)
    #
    #     return join_cell_button, top_left_cell, bottom_right_cell
    #
    # async def join_cells_to_names(self, top_left_cell: str, bottom_right_cell: str):
    #     join_cell_button, top_left_cell, bottom_right_cell = await self.rejoin_cells_to_names(top_left_cell, bottom_right_cell)
    #
    #     keys, _, top_left_cell, bottom_right_cell = await self._get_keys_to_cell(join_cell_button,
    #                                                                             top_left_cell, bottom_right_cell)
    #     actions3 = ActionChainsSet.join_cell(keys, join_cell_button)
    #     await actions3.run(self.session)

    @classmethod
    async def _get_keys_to_cell(cls, session: Session, join_cell_button: Element,
                                top_left_cell: "Cell", bottom_right_cell: "Cell"):

        if (await top_left_cell.go_as_walk()) in [False, None]:
            actions = ActionChainsSet.click_to_join_element_button(join_cell_button)
            await actions.run(session)
            await top_left_cell.go_as_walk()
        keys = await bottom_right_cell.go_as_walk()
        if keys in [False, None]:
            actions = ActionChainsSet.click_to_join_element_button(join_cell_button)
            await actions.run(session)
            await bottom_right_cell.go_as_walk()
        reverse_keys = await top_left_cell.go_as_walk()
        if keys in [False, None]:
            keys = await bottom_right_cell.go_as_walk()
            keys, reverse_keys = reverse_keys, keys
            top_left_cell, bottom_right_cell = bottom_right_cell, top_left_cell
        return keys, reverse_keys, top_left_cell, bottom_right_cell

    @classmethod
    async def rejoin_cells_to_names(cls, session: Session, top_left_cell: "Cell", bottom_right_cell: "Cell"):
        """Разъеденить указанные ячейки"""

        join_cell_button = await cls.get_join_button(session)
        table_name_el = await cls.get_cell_name_el(session)
        keys, _, top_left_cell, bottom_right_cell = await cls._get_keys_to_cell(session, join_cell_button,
                                                                                top_left_cell, bottom_right_cell)
        actions1 = ActionChainsSet.join_cell(keys, join_cell_button)
        await actions1.run(session)
        [(await i.send_keys(Keys.ENTER)) for i in await session.get_elements("button[result=yes]")]

        actions2 = ActionChainsSet.go_as_teleport(top_left_cell, table_name_el)
        actions2 = ActionChainsSet.click_to_join_element_button(join_cell_button, actions=actions2)
        actions2 = ActionChainsSet.go_as_teleport(top_left_cell, table_name_el, actions=actions2)
        actions2 += Keys.ENTER
        actions2 = ActionChainsSet.click_to_join_element_button(join_cell_button, actions=actions2)
        actions2 = ActionChainsSet.go_as_teleport(top_left_cell, table_name_el, actions=actions2)
        await actions2.run(session)

        return join_cell_button, top_left_cell, bottom_right_cell

    @classmethod
    async def join_cells_to_names(cls, session: Session, top_left_cell: "Cell", bottom_right_cell: "Cell"):
        join_cell_button, top_left_cell, bottom_right_cell = await cls.rejoin_cells_to_names(session, top_left_cell,
                                                                                             bottom_right_cell)

        keys, _, top_left_cell, bottom_right_cell = await cls._get_keys_to_cell(session, join_cell_button,
                                                                                top_left_cell, bottom_right_cell)
        actions3 = ActionChainsSet.join_cell(keys, join_cell_button)
        await actions3.run(session)


