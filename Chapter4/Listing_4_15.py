import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed


async def fetch_status(session: ClientSession, url: str, delay: int = 0) -> int:
    ten_millis = aiohttp.ClientTimeout(total=1)

    if delay != 0:
        asyncio.wait(delay)

    async with session.get(url, timeout=ten_millis) as result:
        print(result.status)
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'

        fetchers = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url, delay=3))
        ]

        done, pending = await asyncio.wait(fetchers, timeout=1)

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            result = await done_task
            print(result)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
