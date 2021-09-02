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
