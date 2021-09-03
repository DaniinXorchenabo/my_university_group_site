from arsenic.session import Session, Element


__all__ = ["BaseUtils"]


class BaseUtils(object):

    @staticmethod
    async def get_join_button(session: Session):
        return await session.get_element("div[id=id-toolbar-rtn-merge] button")

    @staticmethod
    async def get_active_element(session: Session) -> Element:
        element_id = await session.request("/element/active", "GET")
        return session.create_element(element_id)

    @staticmethod
    async def get_current_cell_name_el(session: Session) -> Element:
        return await session.get_element("input[id=ce-cell-name]")

    @staticmethod
    async def get_current_cell_name(session: Session):
        return await session.execute_script("return document.getElementById('ce-cell-name').value;")

    @staticmethod
    async def get_current_cell_text_el(session: Session) -> Element:
        return await session.get_element("input[id=ce-cell-content]")

    @staticmethod
    def get_current_cell_text(session: Session):
        return session.execute_script('return document.getElementById("ce-cell-content").value ;')

    @classmethod
    async def set_current_text(cls, session: Session, text: str):
        el = await cls.get_active_element(session)
        await el.send_keys(text)

