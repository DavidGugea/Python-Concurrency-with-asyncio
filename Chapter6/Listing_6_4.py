import time
from concurrent.futures import ProcessPoolExecutor


def count(count_to: int) -> int:
    start = time.perf_counter()

    counter = 0
    while counter < count_to:
        counter += 1

    end = time.perf_counter()

    print(f'Finished counting to {count_to} in {end - start}')
    return counter


if __name__ == '__main__':
    with ProcessPoolExecutor() as process_pool:
        numbers = [1, 3, 5, 22, 100000000]
        for result in process_pool.map(count, numbers):
            print(result)
