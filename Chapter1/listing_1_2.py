import os
import threading

print("Python process running with process id: {0}".format(os.getpid()))

total_threads = threading.active_count()
thread_name = threading.current_thread().name

print("Python is currently running {0} thread(s)".format(total_threads))
print("The current thread is {0}".format(thread_name))