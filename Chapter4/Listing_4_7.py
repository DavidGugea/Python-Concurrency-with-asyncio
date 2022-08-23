import asyncio
from util import delay, async_timed


@async_timed()
async def main():
    results = await asyncio.gather(delay(3), delay(1))
    print(results)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
