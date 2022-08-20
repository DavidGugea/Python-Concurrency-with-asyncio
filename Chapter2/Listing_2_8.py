import asyncio
from util import delay


async def main():
    sleep_for_three = asyncio.create_task(delay(3))
    print(type(sleep_for_three))
    result = await sleep_for_three
    print(result)


async def test_main():
    print("hello world")
    sleep_for_three = await delay(3)
    print(type(sleep_for_three))

asyncio.run(test_main())