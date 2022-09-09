import asyncio
from asyncio import Condition


async def do_work(condition: Condition):
    while True:
        print('Waiting for condition lock...')

        # Wait to acquire the condition lock; once acquired, release the lock.
        async with condition:
            print('Acquired lock, releasing and waiting for condition...')

            # Wait for the event to fire; once it does, reacquire the condition lock.
            await condition.wait()

            print('Condition event fired, re-acquiring lock and doing work...')

            # Once we exit the async with block, release the condition lock.
            await asyncio.sleep(1)
            print('Work finished, lock released.')


async def fire_event(condition: Condition):
    while True:
        await asyncio.sleep(5)
        print('About to notify, acquiring condition lock...')
        async with condition:
            print('Lock acquired, notifying all workers.')
            # Notify all tasks that the event has happened.
            condition.notify_all()

        print('Notification finished, releasing lock.')


async def main():
    condition = Condition()

    asyncio.create_task(fire_event(condition))
    await asyncio.gather(do_work(condition), do_work(condition))


asyncio.run(main())
