
import asyncio
import sys

from arsenic import get_session, keys, browsers, services


if sys.platform.startswith('win'):
    GECKODRIVER = 'geckodriver.exe'
else:
    GECKODRIVER = './geckodriver'


async def hello_world():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    print(service, browser)
    print(browser.__dict__)
    async with get_session(service, browser) as session:

        await session.get('https://images.google.com/')
        search_box = await session.wait_for_element(5, 'input[name=q]')
        await search_box.send_keys('Cats')
        await search_box.send_keys(keys.ENTER)
        await asyncio.sleep(10)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hello_world())


if __name__ == '__main__':
    # 'C:\\Users\\Acer\\.wdm\\drivers\\geckodriver\\win64\\v0.29.1\\geckodriver.exe'
    main()