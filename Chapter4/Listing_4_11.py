import asyncio
import aiohttp
import logging
from util import async_timed
from aiohttp import ClientSession


async def fetch_status(session: ClientSession, url: str) -> int:
    ten_millis = aiohttp.ClientTimeout(total=1)

    async with session.get(url, timeout=ten_millis) as result:
        print(result.status)
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session, 'https://www.example.com')
        bad_request = fetch_status(session, 'python://bad')

        fetchers = [
            asyncio.create_task(good_request),
            asyncio.create_task(bad_request)
        ]

        done, pending = await asyncio.wait(fetchers)

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("Request got an exception", exc_info=done_task.exception())
