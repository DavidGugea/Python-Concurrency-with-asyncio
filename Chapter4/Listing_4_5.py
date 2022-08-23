import asyncio
from util import async_timed, delay


@async_timed()
async def main() -> None:
    delay_times = [3, 3, 3]
    print("hello 1")
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    print("hello 2")
    [await task for task in tasks]
    print("hello 3")


asyncio.run(main())
