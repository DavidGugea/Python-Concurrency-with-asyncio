import asyncio
import functools
from asyncio import Event


def trigger_event(event: Event):
    event.set()


async def do_work_on_event(event: Event):
    print('Waiting for event...')

    # Wait until the event occurs
    await event.wait()

    print('Performing work!')

    # Once the event occurs, wait will no longer block, and we can do work.
    await asyncio.sleep(1)

    print('Finished work!')

    # Reset the event, so future calls to wait will block.
    event.clear()


async def main():
    event = asyncio.Event()
    # Trigger the event 5 seconds in the future.
    asyncio.get_running_loop().call_later(5.0, functools.partial(trigger_event, event))
    await asyncio.gather(do_work_on_event(event), do_work_on_event(event))


asyncio.run(main())
