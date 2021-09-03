import asyncio
from typing import Type

from arsenic.session import Session, Element

from app.disk.a_exel.utils.keyboard import Keys
from app.disk.a_exel.abstractions.table import AbcTable
from app.disk.a_exel.yandex.table_utils import TableUtils
from app.disk.exel.cells import DataTaleType
from app.disk.a_exel.yandex.cell import Cell


__all__ = ["Table"]


class Table(AbcTable, TableUtils):

    def __init__(self, session: Session, size: tuple[int, int] = None, table: DataTaleType = None,
                 target_cell_class: Type[Cell] = Cell):
        print('-----))))))))))------------------', size, table)
        super().__init__(size=size, table=table, target_cell_class=target_cell_class)
        print('****************')
        self.session = session
        self.url = None

    async def start(self, url, *a, **k):
        self.url = url
        await self.session.get(url)
        frame = await self.session.wait_for_element(10, 'iframe[name=frameEditor]')
        data = await self.session.request(
            url='/frame',
            method='POST',
            data={'id': {"ELEMENT": frame.id, "element-6066-11e4-a52e-4f735466cecf": frame.id}}
        )
        reload = False
        for i in range(5):
            try:
                cell_name = await self.session.wait_for_element(60, 'input[id=ce-cell-name]')
                canvas = await self.session.wait_for_element(60, "canvas[id=ws-canvas-graphic-overlay]")
                print(await self.session.execute_script("return document.getElementById('ce-cell-name').value;"))

                break
            except FileNotFoundError:
                reload = True
                for i in await self.session.get_elements('button[result=ok]'):
                    try:
                        await i.click()
                    except FileNotFoundError:
                        pass
                await asyncio.sleep(2)
        if reload is True:
            # Если в процессе работы высвечиваются окна
            # о некорректном завершении работы в прошлый раз - перезагружаемся
            return self.start(url)
        await (await self.get_active_element(self.session)).send_keys(Keys.ENTER)
        return None



