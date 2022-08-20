from asyncio import Future
import asyncio


def make_request() -> Future:
    future = Future()
    asyncio.create_task(set_future_value(future))
    return future


async def set_future_value(future: asyncio.Future) -> None:
    await asyncio.sleep(1)
    future.set_result(42)


async def main():
    future = make_request()
    print('Is the future done? {0}'.format(future.done()))
    value = await future
    print('Is the future done? {0}'.format(future.done()))
    print(value)


asyncio.run(main())
