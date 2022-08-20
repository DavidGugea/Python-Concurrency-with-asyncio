import asyncio
from util import delay


async def hello_every_second() -> None:
    for _ in range(9):
        await asyncio.sleep(1)
        print("I'm running other code while I'm waiting!")


async def main() -> None:
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))

    await hello_every_second()
    await first_delay
    await second_delay


asyncio.run(main())
