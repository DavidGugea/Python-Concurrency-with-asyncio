from concurrent.futures import ProcessPoolExecutor
import asyncio
from multiprocessing import Value

shared_counter: Value


def init(counter: Value):
    global shared_counter
    shared_counter = counter


def increment():
    with shared_counter.get_lock():
        shared_counter.value += 1


async def main():
    counter = Value('d', 0)
    # This tells the pool to execute the function init with the argument counter for each process.
    with ProcessPoolExecutor(initializer=init, initargs=(counter,)) as pool:
        await asyncio.get_running_loop().run_in_executor(pool, increment)
        print(counter.value)


if __name__ == '__main__':
    asyncio.run(main())
