import asyncio
from asyncio import Lock


async def delay(delay_seconds: int) -> int:
    print("Sleeping for {0} second(s)".format(delay_seconds))
    await asyncio.sleep(delay_seconds)
    print("Finished sleeping for {0} second(s)".format(delay_seconds))
    return delay_seconds


async def a(lock: Lock):
    print('Coroutine a waiting to acquire the lock')
    async with lock:
        print('Coroutine a is in the critical section')
        await delay(2)
    print('Coroutine a released the lock')


async def b(lock: Lock):
    print('Coroutine b waiting to acquire the lock')
    async with lock:
        print('Coroutine b is in the critical section')
        await delay(2)
    print('Coroutine b released the lock')


async def main():
    lock = Lock()
    await asyncio.gather(a(lock), b(lock))


asyncio.run(main())
