import threading


def hello_from_thread():
    print("Hello from thread {0}".format(threading.current_thread()))


hello_thread = threading.Thread(target=hello_from_thread)
hello_thread.start()

total_threads = threading.active_count()
thread_name = threading.current_thread().name

print("Python is currently running {0} thread(s)".format(total_threads))
print("The current thread is {0}".format(thread_name))

hello_thread.join()