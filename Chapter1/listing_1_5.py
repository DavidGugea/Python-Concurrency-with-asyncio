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


def fibs_no_threading():
    print_fib(40)
    print_fib(41)


start = time.perf_counter()
fibs_no_threading()
end = time.perf_counter()

print("Completed in {0:.4f} seconds".format(end - start))
