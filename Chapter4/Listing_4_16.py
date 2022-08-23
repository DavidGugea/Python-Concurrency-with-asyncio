import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed


async def fetch_status(session: ClientSession, url: str, delay_seconds: int = 0) -> int:
    ten_millis = aiohttp.ClientTimeout(total=1)

    if delay_seconds != 0:
        await asyncio.sleep(delay_seconds)

    async with session.get(url, timeout=ten_millis) as result:
        print(result.status)
        return result.status


async def main():
    async with aiohttp.ClientSession() as session:
        api_a = fetch_status(session, 'https://www.example.com')
        api_b = fetch_status(session, 'https://www.example.com', delay_seconds=2)

        done, pending = await asyncio.wait([api_a, api_b], timeout=1)

        for task in pending:
            if task is api_b:
                print('API B too slow, cancelling')
                task.cancel()


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
