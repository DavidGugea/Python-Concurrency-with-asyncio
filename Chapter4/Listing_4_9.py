import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed


async def fetch_status(session: ClientSession, url: str) -> int:
    ten_millis = aiohttp.ClientTimeout(total=1)

    async with session.get(url, timeout=ten_millis) as result:
        print(result.status)
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'

        fetchers = [
            fetch_status(session, url),
            fetch_status(session, url),
            fetch_status(session, url),
        ]

        for done_task in asyncio.as_completed(fetchers):
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print('We got a timeout error!')

        for task in asyncio.tasks.all_tasks():
            print(task)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
