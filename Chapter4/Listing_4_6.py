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
        urls = ['https://www.example.com' for _ in range(100)]

        # Generate a list of coroutines for each request we want to make.
        requests = [fetch_status(session, url) for url in urls]

        # Wait for all requests to complete.
        status_codes = await asyncio.gather(*requests)

        print(status_codes)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
