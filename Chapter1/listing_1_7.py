import time
import requests


def read_example() -> None:
    response = requests.get('http://www.example.com')
    print(response.status_code)


sync_start = time.perf_counter()

read_example()
read_example()

sync_end = time.perf_counter()


print("Running synchronously took {0:.4f} seconds".format(sync_end - sync_start))