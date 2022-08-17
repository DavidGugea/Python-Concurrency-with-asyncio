import threading
import time


def print_fib(number: int) -> None:
    def fib(n: int) -> int:
        if n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)

    print("fib {0} is {1}".format(number, fib(number)))


def fibs_with_threads():
    thread_1 = threading.Thread(target=print_fib, args=(40, ))
    thread_2 = threading.Thread(target=print_fib, args=(41,))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()


start_threads = time.perf_counter()
fibs_with_threads()
end_threads = time.perf_counter()
print("Completed in {0:.4f} seconds".format(end_threads - start_threads))
