import time
from multiprocessing import Process


def count(count_to: int) -> int:
    start = time.perf_counter()

    counter = 0
    while counter < count_to:
        counter += 1

    end = time.perf_counter()

    print(f"Finished counting to {count_to} in {end - start}")
    return counter


if __name__ == '__main__':
    start_time = time.perf_counter()

    # Create a process to run the countdown function
    to_one_hundred_million = Process(target=count, args=(100000000,))
    to_two_hundred_million = Process(target=count, args=(200000000,))

    # Start the process. This method returns instantly.
    to_one_hundred_million.start()
    to_two_hundred_million.start()

    # Wait for the process to finish. This method blocks until the process is done.
    to_one_hundred_million.join()
    to_two_hundred_million.join()

    end_time = time.perf_counter()
    print(f"Completed in {end_time - start_time}")
