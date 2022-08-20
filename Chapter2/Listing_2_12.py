import asyncio
from util import delay


async def main():
    delay_task = asyncio.create_task(delay(2))

    try:
        result = await asyncio.wait_for(delay_task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print("Got a timeout!")
        print('Was the task cancelled ? {0}'.format(delay_task.cancelled()))


asyncio.run(main())
