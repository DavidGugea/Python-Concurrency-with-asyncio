import asyncio
import functools
import time
from typing import Callable, Any


async def delay(delay_seconds: int) -> int:
    print("Sleeping for {0} second(s)".format(delay_seconds))
    await asyncio.sleep(delay_seconds)
    print("Finished sleeping for {0} second(s)".format(delay_seconds))
    return delay_seconds


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print('starting {0} with args {1} {2}'.format(func, args, kwargs))
            start = time.time()

            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print('finished {0} in {1:.4f} second(s)'.format(func, total))

        return wrapped

    return wrapper
