from threading import Lock, Thread
import time

lock_a = Lock()
lock_b = Lock()


def a():
    # Acquire lock A.
    with lock_a:
        print('Acquired lock a from method a!')
        # Sleep for 1 seconds; this ensures we create the right conditions for deadlock
        time.sleep(1)
        with lock_b:
            print('Acquired both locks from method a!')


def b():
    # Acquire lock B.
    with lock_b:
        print('Acquired lock b from method b!')
        # Sleep for 1 seconds; this ensures we create the right conditions for deadlock
        time.sleep(1)

        # Acquire lock A.
        with lock_a:
            print('Acquired both locks from method b!')


thread1 = Thread(target=a)
thread2 = Thread(target=b)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
