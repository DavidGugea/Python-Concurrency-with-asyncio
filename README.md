# Python Concurrency with asyncio by Matthew Fowler

## 1. Getting to know asyncio
## 2. asyncio basics
## 3. A first asyncio application
## 4. Concurrent web requests
## 5. Non-blocking database drivers
## 6. Handling CPU-bound work
## 7. Handling blocking work with threads
## 8. Streams
## 9. Web applications
## 10. Microservices
## 11. Synchronization
## 12. Asynchronous queues
## 13. Managing subprocesses
## 14. Advanced asyncio

---
---

# 1. Getting to know asyncio

## What is asyncio ?

In a synchronous application, code runs sequentially. The next line of code runs as soon as the previous one has finished, and only one thing is happening at once. This model works fine for many, if not most, applications. However, what if one line of code is especially slow? In that case, all other code after our slow line will be stuck waiting for that line to complete. These potentially slow lines can block the application from running any other code. Many of us have seen this before in buggy user interfaces, where we happily click around until the application freezes, leaving us with a spinner or an unresponsive user interface. This is an example of an application being blocked leading to a poor user experience.

While any operation can block an application if it takes long enough, many applications will block waiting on I/O. I/O refers to a computer’s input and output devices such as a keyboard, hard drive, and, most commonly, a network card. These operations wait for user input or retrieve the contents from a web-based API. In a synchronous application, we’ll be stuck waiting for those operations to complete before we can run anything else. This can cause performance and responsiveness issues, as we can only have one long operation running at any given time, and that operation will stop our application from doing anything else.

One solution to this issue is to introduce concurrency. In the simplest terms, concurrency means allowing more than one task being handled at the same time. In the case of concurrent I/O, examples include allowing multiple web requests to be made at the same time or allowing simultaneous connections to a web server.

There are several ways to achieve this concurrency in Python. One of the most recent additions to the Python ecosystem is the asyncio library. asyncio is short for asynchronous I/O. It is a Python library that allows us to run code using an asynchronous programming model. This lets us handle multiple I/O operations at once, while still allowing our application to remain responsive.

So what is asynchronous programming? It means that a particular long-running task can be run in the background separate from the main application. Instead of blocking all other application code waiting for that long-running task to be completed, the system is free to do other work that is not dependent on that task. Then, once the long-running task is completed, we’ll be notified that it is done so we can process the result.

In Python version 3.4, asyncio was first introduced with decorators alongside generator yield from syntax to define coroutines. A coroutine is a method that can be paused when we have a potentially long-running task and then resumed when that task is finished. In Python version 3.5, the language implemented first-class support for coroutines and asynchronous programming when the keywords async and await were explicitly added to the language. This syntax, common in other programming languages such as C# and JavaScript, allows us to make asynchronous code look like it is run synchronously. This makes asynchronous code easy to read and understand, as it looks like the sequential flow most software engineers are familiar with. asyncio is a library to execute these coroutines in an asynchronous fashion using a concurrency model known as a single-threaded event loop.

While the name of asyncio may make us think that this library is only good for I/O operations, it has functionality to handle other types of operations as well by interoperating with multithreading and multiprocessing. With this interoperability, we can use async and await syntax with threads and processes making these workflows easier to understand. This means this library not only is good for I/O based concurrency but can also be used with code that is CPU intensive. To better understand what type of workloads asyncio can help us with and which concurrency model is best for each type of concurrency, let’s explore the differences between I/O and CPU-bound operations.

## What is I/O-bound and what is CPU-bound ?

When we refer to an operation as I/O-bound or CPU-bound we are referring to the limiting factor that prevents that operation from running faster. This means that if we increased the performance of what the operation was bound on, that operation would complete in less time.

In the case of a CPU-bound operation, it would complete faster if our CPU was more powerful, for instance by increasing its clock speed from 2 GHz to 3 GHz. In the case of an I/O-bound operation, it would get faster if our I/O devices could handle more data in less time. This could be achieved by increasing our network bandwidth through our ISP or upgrading to a faster network card.

CPU-bound operations are typically computations and processing code in the Python world. An example of this is computing the digits of pi or looping over the contents of a dictionary, applying business logic. In an I/O-bound operation we spend most of our time waiting on a network or other I/O device. An example of an I/Obound operation would be making a request to a web server or reading a file from our machine’s hard drive.

![Listing-1-1](ScreenshotsForNotes/Chapter1/Listing_1_1.PNG)

I/O-bound and CPU-bound operations usually live side by side one another. We first make an I/O-bound request to download the contents of https:/ /www.example.com. Once we have the response, we perform a CPU-bound loop to format the headers of the response and turn them into a string separated by newlines. We then open a file and write the string to that file, both I/O-bound operations.

Asynchronous I/O allows us to pause execution of a particular method when we have an I/O operation; we can run other code while waiting for our initial I/O to complete in the background. This allows us to execute many I/O operations concurrently, potentially speeding up our application.

## Understanding concurrency, parallelism, and multitasking

### Concurrency

When we say two tasks are happening concurrently, we mean those tasks are happening at the same time. Take, for instance, a baker baking two different cakes. To bake these cakes, we need to preheat our oven. Preheating can take tens of minutes depending on the oven and the baking temperature, but we don’t need to wait for our oven to preheat before starting other tasks, such as mixing the flour and sugar together with eggs. We can do other work until the oven beeps, letting us know it is preheated.

We also don’t need to limit ourselves from starting work on the second cake before finishing the first. We can start one cake batter, put it in a stand mixer, and start preparing the second batter while the first batter finishes mixing. In this model, we’re switching between different tasks concurrently. This switching between tasks (doing something else while the oven heats, switching between two different cakes) is concurrent behavior.

### Parallelism

While concurrency implies that multiple tasks are in process simultaneously, it does not imply that they are running together in parallel. When we say something is running in parallel, we mean not only are there two or more tasks happening concurrently, but they are also executing at the same time. Going back to our cake baking example, imagine we have the help of a second baker. In this scenario, we can work on the first cake while the second baker works on the second. Two people making batter at once is parallel because we have two distinct tasks running concurrently (figure 1.1).

![Figure-1-1](ScreenshotsForNotes/Chapter1/Figure_1_1.PNG)

Putting this into terms of applications run by our operating system, let’s imagine it has two applications running. In a system that is only concurrent, we can switch between running these applications, running one application for a short while before letting the other one run. If we do this fast enough, it gives the appearance of two things happening at once. In a system that is parallel, two applications are running simultaneously, and we’re actively running two things concurrently.

The concepts of concurrency and parallelism are similar (figure 1.2) and slightly confusing to differentiate, but it is important to understand what makes them distinct from one another.

![Figure-1-2](ScreenshotsForNotes/Chapter1/Figure_1_2.PNG)

### The difference between concurrency and parallelism

Concurrency is about multiple tasks that can happen independently of one another. We can have concurrency on a CPU with only one core, as the operation will employ preemptive multitasking (defined in the next section) to switch between tasks. Parallelism, however, means that we must be executing two or more tasks at the same time. On a machine with one core, this is not possible. To make this possible, we need a CPU with multiple cores that can run two tasks together.

While parallelism implies concurrency, concurrency does not always imply parallelism. A multithreaded application running on a multiple-core machine is both concurrent and parallel. In this setup, we have multiple tasks running at the same time, and there are two cores independently executing the code associated with those tasks. However, with multitasking we can have multiple tasks happening concurrently, yet only one of them is executing at a given time.

### What is multitasking?

Multitasking is everywhere in today’s world. We multitask while making breakfast by taking a call or answering a text while we wait for water to boil to make tea. We even multitask while commuting to work, by reading a book while the train takes us to our stop. Two main kinds of multitasking are discussed in this section: preemptive multitasking and cooperative multitasking.

* ***PREEMPTIVE MULTITASKING***

  * In this model, we let the operating system decide how to switch between which work is currently being executed via a process called time slicing. When the operating system switches between work, we call it preempting. How this mechanism works under the hood is up to the operating system itself. It is primarily achieved through using either multiple threads or multiple processes.

* ***COOPERATIVE MULTITASKING***

  * In this model, instead of relying on the operating system to decide when to switch between which work is currently being executed, we explicitly code points in our application where we can let other tasks run. The tasks in our application operate in a model where they cooperate, explicitly saying, “I’m pausing my task for a while; go ahead and run other tasks.”

### The benefits of cooperative multitasking

asyncio uses cooperative multitasking to achieve concurrency. When our application reaches a point where it could wait a while for a result to come back, we explicitly mark this in code. This allows other code to run while we wait for the result to come back in the background. Once the task we marked has completed, we in effect “wake up” and resume executing the task. This gives us a form of concurrency because we can have multiple tasks started at the same time but, importantly, not in parallel because they aren’t executing code simultaneously.

Cooperative multitasking has benefits over preemptive multitasking. First, cooperative multitasking is less resource intensive. When an operating system needs to switch between running a thread or process, it involves a context switch. Context switches are intensive operations because the operating system must save information about the running process or thread to be able to reload it.

A second benefit is granularity. An operating system knows that a thread or task should be paused based on whichever scheduling algorithm it uses, but that might not be the best time to pause. With cooperative multitasking, we explicitly mark the areasthat are the best for pausing our tasks. This gives us some efficiency gains in that we are only switching tasks when we explicitly know it is the right time to do so. Now that we understand concurrency, parallelism, and multitasking, we’ll use these concepts to understand how to implement them in Python with threads and processes.

## Understanding processes, threads, multithreading, and multiprocessing

### Process

A process is an application run that has a memory space that other applications cannot access. An example of creating a Python process would be running a simple “hello world” application or typing python at the command line to start up the REPL (read eval print loop).

Multiple processes can run on a single machine. If we are on a machine that has a CPU with multiple cores, we can execute multiple processes at the same time. If we are on a CPU with only one core, we can still have multiple applications running simultaneously, through time slicing. When an operating system uses time slicing, it will switch between which process is running automatically after some amount of time. The algorithms that determine when this switching occurs are different, depending on the operating system.

### Thread

 Threads can be thought of as lighter-weight processes. In addition, they are the smallest construct that can be managed by an operating system. They do not have their own memory as does a process; instead, they share the memory of the process that created them. Threads are associated with the process that created them. A process will always have at least one thread associated with it, usually known as the main thread. A process can also create other threads, which are more commonly known as worker or background threads. These threads can perform other work concurrently alongside the main thread. Threads, much like processes, can run alongside one another on a multi-core CPU, and the operating system can also switch between them via time slicing. When we run a normal Python application, we create a process as well as a main thread that will be responsible for running our Python application.

```Python3
import os
import threading

print("Python process running with process id: {0}".format(os.getpid()))

total_threads = threading.active_count()
thread_name = threading.current_thread().name

print("Python is currently running {0} thread(s)".format(total_threads))
print("The current thread is {0}".format(thread_name))
```

![Figure-1-3](ScreenshotsForNotes/Chapter1/Figure_1_3.PNG)

In figure 1.3, we sketch out the process for listing 1.2. We create a simple application to show us the basics of the main thread. We first grab the process ID (a unique identifier for a process) and print it to prove that we indeed have a dedicated process running. We then get the active count of threads running as well as the current thread’s name to show that we are running one thread—the main thread. While the process ID will be different each time this code is run, running listing 1.2 will give output similar to the following:

```
Python process running with process id: 98230
Python currently running 1 thread(s)
The current thread is MainThread
```

Processes can also create other threads that share the memory of the main process. These threads can do other work concurrently for us via what is known as multithreading.

```Python3
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
```

![Figure-1-4](ScreenshotsForNotes/Chapter1/Figure_1_4.PNG)

In figure 1.4, we sketch out the process and threads for listing 1.3. We create a method to print out the name of the current thread and then create a thread to run that method. We then call the start method of the thread to start running it. Finally, we call the join method. join will cause the program to pause until the thread we started completed. If we run the previous code, we’ll see output similar to the following:

```
Hello from thread <Thread(Thread-1, started 123145541312512)>!
Python is currently running 2 thread(s)
The current thread is MainThread
```

Note that when running this you may see the hello from thread and python is currently running 2 thread(s) messages print on the same line. This is a race condition; we’ll explore a bit about this in the next section and in chapters 6 and 7.

Multithreaded applications are a common way to achieve concurrency in many programming languages. There are a few challenges in utilizing concurrency with threads in Python, however. Multithreading is only useful for I/O-bound work because we are limited by the global interpreter lock, which is discussed in section 1.5.

Multithreading is not the only way we can achieve concurrency; we can also create multiple processes to do work concurrently for us. This is known as multiprocessing. In multiprocessing, a parent process creates one or more child processes that it manages. It can then distribute work to the child processes.

Python gives us the multiprocessing module to handle this. The API is similar to that of the threading module. We first create a process with a target function. Then, we call its start method to execute it and finally its join method to wait for it to complete running.

```Python3
import multiprocessing
import os


def hello_from_process():
  print("Hello from child process {0}".format(os.getpid()))


if __name__ == '__main__':
  hello_process = multiprocessing.Process(target=hello_from_process)
  hello_process.start()

  print("Hello from parent process {0}".format(os.getpid()))

  hello_process.join()
```

![Figure-1-5](ScreenshotsForNotes/Chapter1/Figure_1_5.PNG)

In figure 1.5, we sketch out the process and threads for listing 1.4. We create one child process that prints its process ID, and we also print out the parent process ID to prove that we are running different processes. Multiprocessing is typically best when we have CPU-intensive work.

Multithreading and multiprocessing may seem like magic bullets to enable concurrency with Python. However, the power of these concurrency models is hindered by an implementation detail of Python—the global interpreter lock.

## Understanding the global interpreter lock

The global interpreter lock, abbreviated GIL and pronounced gill, is a controversial topic in the Python community. Briefly, the GIL prevents one Python process from executing more than one Python bytecode instruction at any given time. This means that even if we have multiple threads on a machine with multiple cores, a Python process can have only one thread running Python code at a time. In a world where we have CPUs with multiple cores, this can pose a significant challenge for Python developers looking to take advantage of multithreading to improve the performance of their application.

Multiprocessing can run multiple bytecode instructions concurrently because each Python process has its own GIL.

So why does the GIL exist? The answer lies in how memory is managed in CPython. In CPython, memory is managed primarily by a process known as reference counting. Reference counting works by keeping track of who currently needs access to a particular Python object, such as an integer, dictionary, or list. A reference count is an integer keeping track of how many places reference that particular object. When someone no longer needs that referenced object, the reference count is decremented, and when someone else needs it, it is incremented. When the reference count reaches zero, no one is referencing the object, and it can be deleted from memory.

CPython is the reference implementation of Python. By reference implementation we mean it is the standard implementation of the language and is used as the reference for proper behavior of the language. There are other implementations of Python such as Jython, which is designed to run on the Java Virtual Machine, and IronPython, which is designed for the .NET framework.

The conflict with threads arises in that the implementation in CPython is not thread safe. When we say CPython is not thread safe, we mean that if two or more threads modify a shared variable, that variable may end in an unexpected state. This unexpected state depends on the order in which the threads access the variable, commonly known as a race condition. Race conditions can arise when two threads need to reference a Python object at the same time.

As shown in figure 1.6, if two threads increment the reference count at one time, we could face a situation where one thread causes the reference count to be zero when the object is still in use by the other thread. The likely result of this would be an application crash when we try to read the potentially deleted memory.

To demonstrate the effect of the GIL on multithreaded programming, let’s examine the CPU-intensive task of computing the nth number in the Fibonacci sequence. We’ll use a fairly slow implementation of the algorithm to demonstrate a time-intensive operation. A proper solution would utilize memoization or mathematical techniques to improve performance.

![Figure-1-6](ScreenshotsForNotes/Chapter1/Figure_1_6.PNG)

```Python3
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
```

This implementation uses recursion and is overall a relatively slow algorithm, requiring exponential O(2^N) time to complete. If we are in a situation where we need to print two Fibonacci numbers, it is easy enough to synchronously call them and time the result, as we have done in the preceding listing.

Depending on the speed of the CPU we run on, we will see different timings, but running the code in listing 1.5 will yield output similar to the following:

```
fib(40) is 63245986
fib(41) is 102334155
Completed in 65.1516 seconds.
```

This is a fairly long computation, but our function calls to print_fibs are independent from one another. This means that they can be put in multiple threads that our CPU can, in theory, run concurrently on multiple cores, thus, speeding up our application.

```Python3
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
```

In the preceding listing, we create two threads, one to compute fib(40) and one to compute fib(41) and start them concurrently by calling start() on each thread. Then we make a call to join(), which will cause our main program to wait until the threads finish. Given that we start our computation of fib(40) and fib(41) simultaneously and run them concurrently, you would think we could see a reasonable speedup; however, we will see an output like the following even on a multi-core machine.

```
fib(40) is 63245986
fib(41) is 102334155
Threads took 66.1059 seconds.
```

Our threaded version took almost the same amount of time. In fact, it was even a little slower! This is almost entirely due to the GIL and the overhead of creating and managing threads. While it is true the threads run concurrently, only one of them is allowed to run Python code at a time due to the lock. This leaves the other thread in a waiting state until the first one completes, which completely negates the value of multiple threads.

### Is the GIL ever released?

Based on the previous example, you may be wondering if concurrency in Python can ever happen with threads, given that the GIL prevents running two lines of Python concurrently. The GIL, however, is not held forever such that we can’t use multiple threads to our advantage.

The global interpreter lock is released when I/O operations happen. This lets us employ threads to do concurrent work when it comes to I/O, but not for CPU-bound Python code itself (there are some notable exceptions that release the GIL for CPUbound work in certain circumstances, and we’ll look at these in a later chapter). To illustrate this, let’s use an example of reading the status code of a web page.

```Python3
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
```

In the preceding listing, we retrieve the contents of example.com and print the status code twice. Depending on our network connection speed and our location, we’ll see output similar to the following when running this code:

```
200
200
Running synchronously took 0.2306 seconds.
```

Now that we have a baseline for what a synchronous version looks like, we can write a multithreaded version to compare to. In our multithreaded version, in an attempt to run them concurrently, we’ll create one thread for each request to example.com.

```Python3
import time
import threading
import requests


def read_example() -> None:
  response = requests.get("https://www.example.com")
  print(response.status_code)


thread_1 = threading.Thread(target=read_example)
thread_2 = threading.Thread(target=read_example)

thread_start = time.perf_counter()

thread_1.start()
thread_2.start()

print('All threads running!')

thread_1.join()
thread_2.join()

thread_end = time.perf_counter()

print("Running with threads took {0:.4f} seconds".format(thread_end - thread_start))
```

When we execute the preceding listing, we will see output like the following, depending  again on our network connection and location:

```
All threads running!
200
200
Running with threads took 0.0977 seconds.
```

This is roughly two times faster than our original version that did not use threads, since we’ve run the two requests at roughly the same time! Of course, depending on your internet connection and machine specs, you will see different results, but the numbers should be directionally similar.

So how is it that we can release the GIL for I/O but not for CPU-bound operations? The answer lies in the system calls that are made in the background. In the case of I/O, the low-level system calls are outside of the Python runtime. This allows the GIL to be released because it is not interacting with Python objects directly. In this case, the GIL is only reacquired when the data received is translated back into a Python object. Then, at the operating-system level, the I/O operations execute concurrently. This model gives us concurrency but not parallelism. In other languages, such as Java or C++, we would get true parallelism on multi-core machines because we don’t have the GIL and can execute simultaneously. However, in Python, because of the GIL, the best we can do is concurrency of our I/O operations, and only one piece of Python code is executing at a given time.

### asyncio and the GIL

asyncio exploits the fact that I/O operations release the GIL to give us concurrency, even with only one thread. When we utilize asyncio we create objects called coroutines. A coroutine can be thought of as executing a lightweight thread. Much like we can have multiple threads running at the same time, each with their own concurrent I/O operation, we can have many coroutines running alongside one another. While we are waiting for our I/O-bound coroutines to finish, we can still execute other Python code, thus, giving us concurrency. It is important to note that asyncio does not circumvent the GIL, and we are still subject to it. If we have a CPU-bound task, we still need to use multiple processes to execute it concurrently (which can be done with asyncio itself); otherwise, we will cause performance issues in our application. Now that we know it is possible to achieve concurrency for I/O with only a single thread, let’s dive into the specifics of how this works with non-blocking sockets.

## How single-threaded concurrency works

In the previous section, we introduced multiple threads as a mechanism for achieving concurrency for I/O operations. However, we don’t need multiple threads to achieve this kind of concurrency. We can do it all within the confines of one process and one thread. We do this by exploiting the fact that, at the system level, I/O operations can be completed concurrently. To better understand this, we’ll need to dive into how sockets work and, in particular, how non-blocking sockets work.

### What is a socket?

A socket is a low-level abstraction for sending and receiving data over a network. It is the basis for how data is transferred to and from servers. Sockets support two main operations: sending bytes and receiving bytes. We write bytes to a socket, which will then get sent to a remote address, typically some type of server. Once we’ve sent those bytes, we wait for the server to write its response back to our socket. Once these bytes have been sent back to our socket, we can then read the result.

Sockets are a low-level concept and are fairly easy to understand if you think of them as mailboxes. You can put a letter in your mailbox that your letter carrier then picks up and delivers to the recipient’s mailbox. The recipient opens their mailbox and your letter. Depending on the contents, the recipient may send you a letter back. In this analogy, you may think of the letter as the data or bytes we want to send. Consider that the act of putting a letter into the mailbox is writing the bytes to a socket, and opening the mailbox to read the letter is reading bytes from a socket. The letter carrier can be thought of as the transfer mechanism over the internet, routing the data to the correct address.

In the case of getting the contents from example.com as we saw earlier, we open a socket that connects to example.com’s server. We then write a request to get the contents to that socket and wait for the server to reply with the result: in this case, the HTML of the web page. We can visualize the flow of bytes to and from the server in figure 1.7.

![Figure-1-7](ScreenshotsForNotes/Chapter1/Figure_1_7.PNG)

Sockets are blocking by default. Simply put, this means that when we are waiting for a server to reply with data, we halt our application or block it until we get data to read. Thus, our application stops running any other tasks until we get data from the server, an error happens, or there is a timeout.

At the operating system level, we don’t need to do this blocking. Sockets can operate in non-blocking mode. In non-blocking mode, when we write bytes to a socket, we can just fire and forget the write or read, and our application can go on to perform other tasks. Later, we can have the operating system tell us that we received bytes and deal with it at that time. This lets the application do any number of things while we wait for bytes to come back to us. Instead of blocking and waiting for data to come to us, we become more reactive, letting the operating system inform us when there is data for us to act on.

In the background, this is performed by a few different event notification systems, depending on which operating system we’re running. asyncio is abstracted enough that it switches between the different notification systems, depending on which one our operating system supports. The following are the event notification systems used by specific operating systems:

* kqueue—FreeBSD and MacOS
* epoll—Linux
* IOCP (I/O completion port)—Windows

These systems keep track of our non-blocking sockets and notify us when they are ready for us to do something with them. This notification system is the basis of how asyncio can achieve concurrency. In asyncio’s model of concurrency, we have only one thread executing Python at any given time. When we hit an I/O operation, we hand it over to our operating system’s event notification system to keep track of it for us. Once we have done this handoff, our Python thread is free to keep running other Python code or add more non-blocking sockets for the OS to keep track of for us. When our I/O operation finishes, we “wake up” the task that was waiting for the result and then proceed to run any other Python code that came after that I/O operation. We can visualize this flow in figure 1.8 with a few separate operations that each rely on a socket.

![Figure-1-8](ScreenshotsForNotes/Chapter1/Figure_1_8.PNG)

But how do we keep track of which tasks are waiting for I/O as opposed to ones that can just run because they are regular Python code? The answer lies in a construct called an event loop.

## How an event loop works

An event loop is at the heart of every asyncio application. Event loops are a fairly common design pattern in many systems and have existed for quite some time. If you’ve ever used JavaScript in a browser to make an asynchronous web request, you’ve created a task on an event loop. Windows GUI applications use what are called message loops behind the scenes as a primary mechanism for handling events such as keyboard input, while still allowing the UI to draw.

The most basic event loop is extremely simple. We create a queue that holds a list of events or messages. We then loop forever, processing messages one at a time as they come into the queue. In Python, a basic event loop might look something like this:

```Python3
from collections import deque
messages = deque()

while True:
    if messages:
      message = messages.pop()
      process_message(message)
```

In asyncio, the event loop keeps a queue of tasks instead of messages. Tasks are wrappers around a coroutine. A coroutine can pause execution when it hits an I/O-bound operation and will let the event loop run other tasks that are not waiting for I/O operations to complete.

When we create an event loop, we create an empty queue of tasks. We can then add tasks into the queue to be run. Each iteration of the event loop checks for tasks that need to be run and will run them one at a time until a task hits an I/O operation. At that time the task will be “paused,” and we instruct our operating system to watch any sockets for I/O to complete. We then look for the next task to be run. On every iteration of the event loop, we’ll check to see if any of our I/O has completed; if it has, we’ll “wake up” any tasks that were paused and let them finish running. We can visualize this as follows in figure 1.9: the main thread submits tasks to the event loop, which can then run them.

To illustrate this, let’s imagine we have three tasks that each make an asynchronous web request. Imagine these tasks have a bit of code to do setup, which is CPU-bound, then they make a web request, and they follow with some CPU-bound postprocessing code. Now, let’s submit these tasks to the event loop simultaneously. In pseudocode, we would write something like this:

```Python3
def make_request():
    cpu_bound_setup()
    io_bound_web_request()
    cpu_bound_postprocess()

task_one = make_request()
task_two = make_request()
task_three = make_request()
```

![Figure-1-9](ScreenshotsForNotes/Chapter1/Figure_1_9.PNG)

All three tasks start with CPU-bound work and we are single-threaded, so only the first task starts executing code, and the other two are left waiting to run. Once the CPU-bound setup work is finished in Task 1, it hits an I/O-bound operation and will pause itself to say, “I’m waiting for I/O; any other tasks waiting to run can run.”

Once this happens, Task 2 can begin executing. Task 2 starts its CPU-bound code and then pauses, waiting for I/O. At this time both Task 1 and Task 2 are waiting concurrently for their network request to complete. Since Tasks 1 and 2 are both paused waiting for I/O, we start running Task 3.

Now imagine once Task 3 pauses to wait for its I/O to complete, the web request for Task 1 has finished. We’re now alerted by our operating system’s event notification system that this I/O has finished. We can now resume executing Task 1 while both Task 2 and Task 3 are waiting for their I/O to finish.

In figure 1.10, we show the execution flow of the pseudocode we just described. If we look at any vertical slice of this diagram, we can see that only one CPU-bound piece of work is running at any given time; however, we have up to two I/O-bound operations happening concurrently. This overlapping of waiting for I/O per each task is where the real time savings of asyncio comes in.

![Figure-1-10](ScreenshotsForNotes/Chapter1/Figure_1_10.PNG)

# 2. asyncio basics

## Introduction Coroutines

Think of a coroutine like a regular Python function but with the superpower that it can pause its execution when it encounters an operation that could take a while to complete. When that long-running operation is complete, we can “wake up” our paused coroutine and finish executing any other code in that coroutine. While a paused coroutine is waiting for the operation it paused for to finish, we can run other code. This running of other code while waiting is what gives our application concurrency. We can also run several time-consuming operations concurrently, which can give our applications big performance improvements.

To both create and pause a coroutine, we’ll need to learn to use Python’s ```async``` and ```await``` keywords. The async keyword will let us define a coroutine; the await keyword will let us pause our coroutine when we have a long-running operation.

## Creating coroutines with the ```async``` keyword

Creating a coroutine is straightforward and not much different from creating a normal Python function. The only difference is that, instead of using the def keyword, we use async def. The async keyword marks a function as a coroutine instead of a normal Python function.

```Python3
async def my_coroutine() -> None:
    print('Hello world!')
```

The coroutine in the preceding listing does nothing yet other than print “Hello world!” It’s also worth noting that this coroutine does not perform any long-running operations; it just prints our message and returns. This means that, when we put the coroutine on the event loop, it will execute immediately because we don’t have any blocking I/O, and nothing is pausing execution yet.

This syntax is simple, but we’re creating something very different from a plain Python function. To illustrate this, let’s create a function that adds one to an integer as well as a coroutine that does the same and compare the results of calling each. We’ll also use the type convenience function to look at the type returned by calling a coroutine as compared to calling our normal function.

```Python3
async def coroutine_add_one(number: int) -> int:
  return number + 1


def add_one(number: int) -> int:
  return number + 1


function_result = add_one(1)
coroutine_result = coroutine_add_one(1)

print("Function result is {0} and the type is {1}".format(function_result, type(function_result)))
print("Function result is {0} and the type is {1}".format(coroutine_result, type(coroutine_result)))
```

When we run this code, we’ll see output like the following:

```
Method result is 2 and the type is <class 'int'>
Coroutine result is <coroutine object coroutine_add_one at 0x1071d6040> and
the type is <class 'coroutine'>
```

Notice how when we call our normal add_one function it executes immediately and returns what we would expect, another integer. However, when we call coroutine_ add_one we don’t get our code in the coroutine executed at all. We get a coroutine object instead.

This is an important point, as coroutines aren’t executed when we call them directly. Instead, we create a coroutine object that can be run later. To run a coroutine, we need to explicitly run it on an event loop. So how can we create an event loop and run our coroutine?

In versions of Python older than 3.7, we had to create an event loop if one did not already exist. However, the asyncio library has added several functions that abstract the event loop management. There is a convenience function, asyncio.run, we can use to run our coroutine. This is illustrated in the following listing.

```Python3
import asyncio


async def coroutine_add_one(number: int) -> int:
  return number + 1


result = asyncio.run(coroutine_add_one(1))

print(result)
```

Running listing 2.3 will print “2,” as we would expect for returning the next integer. We’ve properly put our coroutine on the event loop, and we have executed it!

asyncio.run is doing a few important things in this scenario. First, it creates a brand-new event. Once it successfully does so, it takes whichever coroutine we pass into it and runs it until it completes, returning the result. This function will also do some cleanup of anything that might be left running after the main coroutine finishes. Once everything has finished, it shuts down and closes the event loop.

Possibly the most important thing about asyncio.run is that it is intended to be the main entry point into the asyncio application we have created. It only executes one coroutine, and that coroutine should launch all other aspects of our application. As we progress further, we will use this function as the entry point into nearly all our applications. The coroutine that asyncio.run executes will create and run other coroutines that will allow us to utilize the concurrent nature of asyncio.

## Pausing execution with the ```await``` keyword

The example we saw in listing 2.3 did not need to be a coroutine, as it executed only non-blocking Python code. The real benefit of asyncio is being able to pause execution to let the event loop run other tasks during a long-running operation. To pause execution, we use the await keyword. The await keyword is usually followed by a call to a coroutine (more specifically, an object known as an awaitable, which is not always a coroutine; we’ll learn more about awaitables later in the chapter).

Using the await keyword will cause the coroutine following it to be run, unlike calling a coroutine directly, which produces a coroutine object. The await expression will also pause the coroutine where it is contained in until the coroutine we awaited finishes and returns a result. When the coroutine we awaited finishes, we’ll have access to the result it returned, and the containing coroutine will “wake up” to handle the result.

We can use the await keyword by putting it in front of a coroutine call. Expanding on our earlier program, we can write a program where we call the add_one function inside of a “main” async function and get the result.

```Python3
import asyncio


async def add_one(number: int) -> int:
  return number + 1


async def main() -> None:
  one_plus_one = await add_one(1)
  two_plus_one = await add_one(2)
  print(one_plus_one)
  print(two_plus_one)


asyncio.run(main())
```

In listing 2.4, we pause execution twice. We first await the call to add_one(1). Once we have the result, the main function will be “unpaused,” and we will assign the return value from add_one(1) to the variable one_plus_one, which in this case will be two. We then do the same for add_one(2) and then print the results. We can visualize the execution flow of our application, as shown in figure 2.1. Each block of the figure represents what is happening at any given moment for one or more lines of code.

![Figure-2-1](ScreenshotsForNotes/Chapter2/Figure_2_1.PNG)

As it stands now, this code does not operate differently from normal, sequential code. We are, in effect, mimicking a normal call stack. Next, let’s look at a simple example of how to run other code by introducing a dummy sleep operation while we’re waiting.

## Introducing long-running coroutines with sleep

Our previous examples did not use any slow operations and were used to help us learn the basic syntax of coroutines. To fully see the benefits and show how we can run multiple events simultaneously, we’ll need to introduce some long-running operations. Instead of making web API or database queries right away, which are nondeterministic as to how much time they will take, we’ll simulate long-running operations by specifying how long we want to wait. We’ll do this with the asyncio.sleep function.

We can use asyncio.sleep to make a coroutine “sleep” for a given number of seconds. This will pause our coroutine for the time we give it, simulating what would happen if we had a long-running call to a database or web API.

```asyncio.sleep``` is itself a coroutine, so we must use it with the await keyword. If we call it just by itself, we’ll get a coroutine object. Since asyncio.sleep is a coroutine, this means that when a coroutine awaits it, other code will be able to run.

Let’s examine a simple example, shown in the following listing, that sleeps for 1 second and then prints a 'Hello World!' message.

```Python3
import asyncio


async def hello_world_message() -> str:
  await asyncio.sleep(1)
  return 'Hello World!'


async def main() -> None:
  message = await hello_world_message()
  print(message)


asyncio.run(main())
```

When we run this application, our program will wait 1 second before printing our 'Hello World!' message. Since hello_world_message is a coroutine and we pause it for 1 second with asyncio.sleep, we now have 1 second where we could be running other code concurrently.

We’ll be using sleep a lot in the next few examples, so let’s invest the time to create a reusable coroutine that sleeps for us and prints out some useful information. We’ll call this coroutine delay. This is shown in the following listing.

```Python3
import asyncio

async def delay(delay_seconds: int) -> int:
  print("Sleeping for {0} second(s)".format(delay_seconds))
  await asyncio.sleep(delay_seconds)
  print("Finished sleeping for {0} second(s)".format(delay_seconds))
  return delay_seconds
```

delay will take in an integer of the duration in seconds that we’d like the function to sleep and will return that integer to the caller once it has finished sleeping. We’ll also print when sleep begins and ends. This will help us see what other code, if any, is running concurrently while our coroutines are paused.

### Running two coroutines

```Python3
import asyncio
from util import delay


async def add_one(number: int) -> int:
  return number + 1


async def hello_word_message() -> str:
  await delay(1)
  return 'Hello World!'


async def main() -> None:
  message = await hello_word_message()
  one_plus_one = await add_one(1)
  print(one_plus_one)
  print(message)


asyncio.run(main())
```

When we run this, 1 second passes before the results of both function calls are printed. What we really want is the value of add_one(1) to be printed immediately while hello_world_message()runs concurrently. So why isn’t this happening with this code? The answer is that await pauses our current coroutine and won’t execute any other code inside that coroutine until the await expression gives us a value. Since it will take 1 second for our hello_world_message function to give us a value, the main coroutine will be paused for 1 second. Our code behaves as if it were sequential in this case. This behavior is illustrated in figure 2.2.

![Figure-2-2](ScreenshotsForNotes/Chapter2/Figure_2_2.PNG)

Both main and hello_world paused while we wait for delay(1) to finish. After it has finished, main resumes and can execute add_one.

We’d like to move away from this sequential model and run add_one concurrently with hello_world. To achieve this, we’ll need to introduce a concept called tasks.

## Running concurrently with tasks

Earlier we saw that, when we call a coroutine directly, we don’t put it on the event loop to run. Instead, we get a coroutine object that we then need to either use the await keyword on it or pass it in to asyncio.run to run and get a value. With only these tools we can write async code, but we can’t run anything concurrently. To run coroutines concurrently, we’ll need to introduce tasks.

Tasks are wrappers around a coroutine that schedule a coroutine to run on the event loop as soon as possible. This scheduling and execution happen in a non-blocking fashion, meaning that, once we create a task, we can execute other code instantly while the task is running. This contrasts with using the await keyword that acts in a blocking manner, meaning that we pause the entire coroutine until the result of the await expression comes back.

The fact that we can create tasks and schedule them to run instantly on the event loop means that we can execute multiple tasks at roughly the same time. When these tasks wrap a long-running operation, any waiting they do will happen concurrently. To illustrate this, let’s create two tasks and try to run them at the same time.

## The basics of creating tasks

Creating a task is achieved by using the asyncio.create_task function. When we call this function, we give it a coroutine to run, and it returns a task object instantly. Once we have a task object, we can put it in an await expression that will extract the return value once it is complete.

```Python3
import asyncio
from util import delay


async def main():
  sleep_for_three = asyncio.create_task(delay(3))
  print(type(sleep_for_three))
  result = await sleep_for_three
  print(result)


async def test_main():
  print("hello world")
  sleep_for_three = await delay(3)
  print(type(sleep_for_three))

asyncio.run(test_main())
```

In the preceding listing, we create a task that requires 3 seconds to complete. We also print out the type of the task, in this case, <class '_asyncio.Task'>, to show that it is different from a coroutine.

One other thing to note here is that our print statement is executed immediately after we run the task. If we had simply used await on the delay coroutine we would have waited 3 seconds before outputting the message.

Once we’ve printed our message, we apply an await expression to the task sleep_ for_three. This will suspend our main coroutine until we have a result from our task.

It is important to know that we should usually use an await keyword on our tasks at some point in our application. In listing 2.8, if we did not use await, our task would be scheduled to run, but it would almost immediately be stopped and “cleaned up” when asyncio.run shut down the event loop. Using await on our tasks in our application also has implications for how exceptions are handled, which we’ll look at in chapter 3. Now that we’ve seen how to create a task and allow other code to run concurrently, we can learn how to run multiple long-running operations at the same time.

## Running multiple tasks concurrently

Given that tasks are created instantly and are scheduled to run as soon as possible, this allows us to run many long-running tasks concurrently. We can do this by sequentially starting multiple tasks with our long-running coroutine.

```Python3
import asyncio
from util import delay


async def main():
  sleep_for_three = asyncio.create_task(delay(3))
  sleep_again = asyncio.create_task(delay(3))
  sleep_once_more = asyncio.create_task(delay(3))

  await sleep_for_three
  await sleep_again
  await sleep_once_more


asyncio.run(main())
```

In the preceding listing we start three tasks, each taking 3 seconds to complete. Each call to create_task returns instantly, so we reach the await sleep_for_three statement right away. Previously, we mentioned that tasks are scheduled to run “as soon as possible.” Generally, this means the first time we hit an await statement after creating a task, any tasks that are pending will run as await triggers an iteration of the event loop.

Since we’ve hit await sleep_for_three, all three tasks start running and will carry out any sleep operations concurrently. This means that the program in listing 2.9 will complete in about 3 seconds. We can visualize the concurrency as shown in figure 2.3, noting that all three tasks are running their sleep coroutines at the same time.

Note that in figure 2.3 the code in the tasks labeled RUN delay(3) (in this case, some print statements) does not run concurrently with other tasks; only the sleep coroutines run concurrently. If we were to run these delay operations sequentially, we’d have an application runtime of just over 9 seconds. By doing this concurrently, we’ve decreased the total runtime of this application three-fold!

![Figure-2-3](ScreenshotsForNotes/Chapter2/Figure_2_3.PNG)

This benefit compounds as we add more tasks; if we had launched 10 of these tasks, we would still take roughly 3 seconds, giving us a 10-fold speedup.

Executing these long-running operations concurrently is where asyncio really shines and delivers drastic improvements in our application’s performance, but the benefits don’t stop there. In listing 2.9, our application was actively doing nothing, while it was waiting for 3 seconds for our delay coroutines to complete. While our code is waiting, we can execute other code. As an example, let’s say we wanted to print out a status message every second while we were running some long tasks.

```Python3
import asyncio
from util import delay


async def hello_every_second() -> None:
  for _ in range(9):
    await asyncio.sleep(1)
    print("I'm running other code while I'm waiting!")


async def main() -> None:
  first_delay = asyncio.create_task(delay(3))
  second_delay = asyncio.create_task(delay(3))

  await hello_every_second()
  await first_delay
  await second_delay


asyncio.run(main())
```

In the preceding listing, we create two tasks, each of which take 3 seconds to complete. While these tasks are waiting, our application is idle, which gives us the opportunity to run other code. In this instance, we run a coroutine hello_every_second, which prints a message every second 2 times. While our two tasks are running, we’ll see messages being output, giving us the following:

```
sleeping for 3 second(s)
sleeping for 3 second(s)
I'm running other code while I'm waiting!
I'm running other code while I'm waiting!
finished sleeping for 3 second(s)
finished sleeping for 3 second(s)
```

We can imagine the execution flow as shown in figure 2.4.

![Figure-2-4](ScreenshotsForNotes/Chapter2/Figure_2_4.PNG)

First, we start two tasks that sleep for 3 seconds; then, while our two tasks are idle, we start to see I’m running other code while I’m waiting! being printed every second. This means that even when we’re running time-intensive operations, our application can still be performing other tasks.

One potential issue with tasks is that they can take an indefinite amount of time to complete. We could find ourselves wanting to stop a task if it takes too long to finish. Tasks support this use case by allowing cancellation.

## Canceling tasks and setting timeouts

Network connections can be unreliable. A user’s connection may drop because of a network slowdown, or a web server may crash and leave existing requests in limbo. When making one of these requests, we need to be especially careful that we don’t wait indefinitely. Doing so could lead to our application hanging, waiting forever for a result that may never come. It could also lead to a poor user experience; if we allow a user to make a request that takes too long, they are unlikely to wait forever for a response. Additionally, we may want to allow our users a choice if a task continues torun. A user may proactively decide things are taking too long, or they may want to stop a task they made in error.

In our previous examples, if our tasks took forever, we would be stuck waiting for the await statement to finish with no feedback. We also had no way to stop things if we wanted to. asyncio supports both these situations by allowing tasks to be canceled as well as allowing them to specify a timeout.

## Canceling tasks

Canceling a task is straightforward. Each task object has a method named cancel, which we can call whenever we’d like to stop a task. Canceling a task will cause that task to raise a CancelledError when we await it, which we can then handle as needed.

To illustrate this, let’s say we launch a long-running task that we don’t want to run for longer than 5 seconds. If the task is not completed within 5 seconds, we’d like to stop that task, reporting back to the user that it took too long and we’re stopping it. We also want a status update printed every second, to provide up-to-date information to our user, so they aren’t left without information for several seconds.

```Python3
import asyncio
from asyncio import CancelledError
from util import delay


async def main():
  long_task = asyncio.create_task(delay(10))

  seconds_elapsed = 0

  while not long_task.done():
    print("Task not finished, checking again in a second.")
    await asyncio.sleep(1)
    seconds_elapsed += 1
    if seconds_elapsed == 5:
      long_task.cancel()

  try:
    await long_task
  except CancelledError:
    print('Our task was cancelled')


asyncio.run(main())
```

In the preceding listing, we create a task that will take 10 seconds to run. We then create a while loop to check if that task is done. The done method on the task returns True if a task is finished and False otherwise. Every second, we check to see if the task has finished, keeping track of how many seconds we’ve checked so far. If our task has taken5 seconds, we cancel the task. Then, we will go on to await long_task, and we’ll see Our task was cancelled printed out, indicating we’ve caught a CancelledError.

Something important to note about cancellation is that a CancelledError can only be thrown from an await statement. This means that if we call cancel on a task when it is executing plain Python code, that code will run until completion until we hit the next await statement (if one exists) and a CancelledError can be raised. Calling cancel won’t magically stop the task in its tracks; it will only stop the task if you’re currently at an await point or its next await point.

## Setting a timeout and canceling with a ```wait_for```

Checking every second or at some other time interval, and then canceling a task, as we did in the previous example, isn’t the easiest way to handle a timeout. Ideally, we’d have a helper function that would allow us to specify this timeout and handle cancellation for us.

asyncio provides this functionality through a function called asyncio.wait_for. This function takes in a coroutine or task object, and a timeout specified in seconds. It then returns a coroutine that we can await. If the task takes more time to complete than the timeout we gave it, a TimeoutException will be raised. Once we have reached the timeout threshold, the task will automatically be canceled.

To illustrate how wait_for works, we’ll look at a case where we have a task that will take 2 seconds to complete, but we’ll only allow it 1 second to finish. When we get a TimeoutError raised, we’ll catch the exception and check to see if the task was canceled.

```Python3
import asyncio
from util import delay


async def main():
  delay_task = asyncio.create_task(delay(2))

  try:
    result = await asyncio.wait_for(delay_task, timeout=1)
    print(result)
  except asyncio.exceptions.TimeoutError:
    print("Got a timeout!")
    print('Was the task cancelled ? {0}'.format(delay_task.cancelled()))


asyncio.run(main())
```

When we run the preceding listing, our application will take roughly 1 second to complete. After 1 second our wait_for statement will raise a TimeoutError, which we then handle. We’ll then see that our original delay task was canceled, giving the following output:

```
sleeping for 2 second(s)
Got a timeout!
Was the task cancelled? True
```

Canceling tasks automatically if they take longer than expected is normally a good idea. Otherwise, we may have a coroutine waiting indefinitely, taking up resources that may never be released. However, in certain circumstances we may want to keep our coroutine running. For example, we may want to inform a user that something is taking longer than expected after a certain amount of time but not cancel the task when the timeout is exceeded.

To do this we can wrap our task with the asyncio.shield function. This function will prevent cancellation of the coroutine we pass in, giving it a “shield,” which cancellation requests then ignore.

```Python3
import asyncio
from util import delay


async def main():
  task = asyncio.create_task(delay(10))

  try:
    result = await asyncio.wait_for(asyncio.shield(task), 5)
    print(result)
  except asyncio.exceptions.TimeoutError:
    print('Task took longer than five seconds, it will finish soon!')
    result = await task
    print(result)


asyncio.run(main())
``` 

In the preceding listing, we first create a task to wrap our coroutine. This differs from our first cancellation example because we’ll need to access the task in the except block. If we had passed in a coroutine, wait_for would have wrapped it in a task, but we wouldn’t be able to reference it, as it is internal to the function.

Then, inside of a try block, we call wait_for and wrap the task in shield, which will prevent the task from being canceled. Inside our exception block, we print a useful message to the user, letting them know that the task is still running and then we await the task we initially created. This will let it finish in its entirety, and the program’s output will be as follows:

```
sleeping for 10 second(s)
Task took longer than five seconds!
finished sleeping for 10 second(s)
finished <function delay at 0x10e8cf820> in 10 second(s)
```

Cancellation and shielding are somewhat tricky subjects with several cases that are noteworthy. We introduce the basics below, but as we get into more complicated cases, we’ll explore how cancellation works in greater depth.

## Tasks, coroutines, futures, and awaitables

Coroutines and tasks can both be used in await expressions. So what is the common thread between them? To understand, we’ll need to know about both a future as well as an awaitable. You normally won’t need to use futures, but understanding them is a key to understanding the inner workings of asyncio. As some APIs return futures, we will reference them in the rest of the book.

## Introducing futures

A future is a Python object that contains a single value that you expect to get at some point in the future but may not yet have. Usually, when you create a future, it does not have any value it wraps around because it doesn’t yet exist. In this state, it is considered incomplete, unresolved, or simply not done. Then, once you get a result, you can set the value of the future. This will complete the future; at that time, we can consider it finished and extract the result from the future. To understand the basics of futures, let’s try creating one, setting its value and extracting that value back out.

```Python3
from asyncio import Future

my_future = Future()

print('Is my_future done? {0}'.format(my_future.done()))

my_future.set_result(42)

print('Is my_future done? {0}'.format(my_future.done()))
print('What is the result of my_future? {0}'.format(my_future.result()))
```

We can create a future by calling its constructor. At this time, the future will have no result set on it, so calling its done method will return False. We then set the value of the future with its set_result method, which will mark the future as done. Alternatively, if we had an exception we wanted to set on the future, we could call set_exception.

***We don’t call the result method before the result is set because the result method will throw an invalid state exception if we do so.***

Futures can also be used in await expressions. If we await a future, we’re saying “pause until the future has a value set that I can work with, and once I have a value, wake up and let me process it.”

To understand this, let’s consider an example of making a web request that returns a future. Making a request that returns a future should complete instantly, but as the request will take some time, the future will not yet be defined. Then, later, once the request has finished, the result will be set, then we can access it. If you have used JavaScript in the past, this concept is analogous to promises. In the Java world, these are known as completable futures.

```Python3
from asyncio import Future
import asyncio


def make_request() -> Future:
  future = Future()
  asyncio.create_task(set_future_value(future))
  return future


async def set_future_value(future: asyncio.Future) -> None:
  await asyncio.sleep(1)
  future.set_result(42)


async def main():
  future = make_request()
  print('Is the future done? {0}'.format(future.done()))
  value = await future
  print('Is the future done? {0}'.format(future.done()))
  print(value)


asyncio.run(main())
```

In the preceding listing, we define a function make_request. In that function we create a future and create a task that will asynchronously set the result of the future after 1 second. Then, in the main function, we call make_request. When we call this, we’ll instantly get a future with no result; it is, therefore, undone. Then, we await the future. Awaiting this future will pause main for 1 second while we wait for the value of the future to be set. Once this completes, value will be 42 and the future is done.

In the world of asyncio, you should rarely need to deal with futures. That said, you will run into some asyncio APIs which return futures, and you may need to work with callback-based code, which can require futures. You may also need to read or debug some asyncio API code yourself. The implementation of these asyncio APIs heavily rely on futures, so it is ideal to have a basic understanding of how they work.

## The relationship between futures, tasks, and coroutines

There is a strong relationship between tasks and futures. In fact, task directly inherits from future. A future can be thought as representing a value that we won’t have for a while. A task can be thought as a combination of both a coroutine and a future. When we create a task, we are creating an empty future and running the coroutine. Then, when the coroutine has completed with either an exception or a result, we set the result or exception of the future.

Given the relationship between futures and tasks, is there a similar relationship between tasks and coroutines? After all, all these types can be used in await expressions.

The common thread between these is the Awaitable abstract base class. This class defines one abstract double underscore method __await__. We won’t go into the specifics about how to create our own awaitables, but anything that implements the __await__ method can be used in an await expression. Coroutines inherit directly from Awaitable, as do futures. Tasks then extend futures, which gives us the inheritance diagram shown in figure 2.5.

![Figure-2-5](ScreenshotsForNotes/Chapter2/Figure_2_5.PNG)

Going forward, we’ll start to refer to objects that can be used in await expressions as awaitables. You’ll frequently see the term awaitable referenced in the asyncio documentation, as many API methods don’t care if you pass in coroutines, tasks, or futures.

Now that we understand the basics of coroutines, tasks, and futures, how do we assess their performance? So far, we’ve only theorized about how long they take. To make things more rigorous, let’s add some functionality to measure execution time.

## Measuring coroutine executing time with decorators

So far, we’ve talked about roughly how long our applications take to run without timing them. To really understand and profile things we’ll need to introduce some code to keep track of this for us.

As a first try we could wrap every await statement and keep track of the start and end time of the coroutine:

```Python3
import asyncio
import time

async def main():
  start = time.time()
  await asyncio.sleep(1)
  end = time.time()
  print(f'Sleeping took {end - start} seconds')
  
asyncio.run(main())
```

However, this will get messy quickly when we have multiple await statements and tasks to keep track of. A better approach is to come up with a reusable way to keep track of how long any coroutine takes to finish. We can do this by creating a decorator that will run an await statement for us (listing 2.16). We’ll call this decorator async_timed.

```Python3
import functools
import time
from typing import Callable, Any


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
```

In this decorator, we create a new coroutine called wrapped. This is a wrapper around our original coroutine that takes its arguments, *args and **kwargs, calls an await statement, and then returns the result. We surround that await statement with one message when we start running the function and another message when we end running the function, keeping track of the start and end time in much the same way that we did in our earlier start-time and end-time example. Now, as shown in listing 2.17, we can put this annotation on any coroutine, and any time we run it, we’ll see how long it took to run.

```Python3
import asyncio
from util import async_timed


@async_timed()
async def delay(delay_seconds: int) -> int:
  print('sleeping for {0} second(s)'.format(delay_seconds))
  await asyncio.sleep(delay_seconds)
  print('finished sleeping for {0} second(s)'.format(delay_seconds))
  return delay_seconds


@async_timed()
async def main():
  task_one = asyncio.create_task(delay(2))
  task_two = asyncio.create_task(delay(2))

  await task_one
  await task_two


asyncio.run(main())
```

When we run the preceding listing, we’ll see console output similar to the following:

```
starting <function main at 0x109111ee0> with args () {}
starting <function delay at 0x1090dc700> with args (2,) {}
starting <function delay at 0x1090dc700> with args (3,) {}
finished <function delay at 0x1090dc700> in 2.0032 second(s)
finished <function delay at 0x1090dc700> in 3.0003 second(s)
finished <function main at 0x109111ee0> in 3.0004 second(s)
```

We can see that our two delay calls were both started and finished in roughly 2 and 3 seconds, respectively, for a total of 5 seconds. Notice, however, that our main coroutine only took 3 seconds to complete because we were waiting concurrently.

## The pitfalls of coroutines and tasks

When seeing the performance improvements we can obtain from running some of our longer tasks concurrently, we can be tempted to start to use coroutines and tasks everywhere in our applications. While it depends on the application you’re writing, simply marking functions async and wrapping them in tasks may not help application performance. In certain cases, this may degrade performance of your applications.

Two main errors occur when trying to turn your applications asynchronous. The first is attempting to run CPU-bound code in tasks or coroutines without using multiprocessing; the second is using blocking I/O-bound APIs without using multithreading.

## Running CPU-bound code

We may have functions that perform computationally expensive calculations, such as looping over a large dictionary or doing a mathematical computation. Where we have several of these functions with the potential to run concurrently, we may get the idea to run them in separate tasks. In concept, this is a good idea, but remember that asyncio has a single-threaded concurrency model. This means we are still subject to the limitations of a single thread and the global interpreter lock.

To prove this to ourselves, let’s try to run some CPU-bound functions concurrently.

```Python3
import asyncio
from util import async_timed, delay


@async_timed()
async def cpu_bound_work() -> int:
  counter = 0

  for _ in range(100000000):
    counter += 1

  return counter


@async_timed()
async def main():
  task_one = asyncio.create_task(cpu_bound_work())
  task_two = asyncio.create_task(cpu_bound_work())

  await task_one
  await task_two


asyncio.run(main())
```

When we run the preceding listing, we’ll see that, despite creating two tasks, our code still executes sequentially. First, we run Task 1, then we run Task 2, meaning our total runtime will be the sum of the two calls to cpu_bound_work:

```
starting <function main at 0x10a8f6c10> with args () {}
starting <function cpu_bound_work at 0x10a8c0430> with args () {}
finished <function cpu_bound_work at 0x10a8c0430> in 4.6750 second(s)
starting <function cpu_bound_work at 0x10a8c0430> with args () {}
finished <function cpu_bound_work at 0x10a8c0430> in 4.6680 second(s)
finished <function main at 0x10a8f6c10> in 9.3434 second(s)
```

Looking at the output above, we may be tempted to think that there are no drawbacks to making all our code use async and await. After all, it ends up taking the same amount of time as if we had run things sequentially. However, by doing this we can run into situations where our application’s performance can degrade. This is especially true when we have other coroutines or tasks that have await expressions. Consider creating two CPU-bound tasks alongside a long-running task, such as our delay coroutine.

```Python3
import asyncio
from util import async_timed, delay


@async_timed()
async def cpu_bound_work() -> int:
  counter = 0

  for _ in range(100000000):
    counter += 1

  return counter


@async_timed()
async def main():
  task_one = asyncio.create_task(cpu_bound_work())
  task_two = asyncio.create_task(cpu_bound_work())
  delay_task = asyncio.create_task(delay(4))

  await task_one
  await task_two
  await delay_task


asyncio.run(main())
```

Running the preceding listing, we might expect to take the same amount of time as in listing 2.18. After all, won’t delay_task run concurrently alongside the CPU-bound work? In this instance it won’t because we create the two CPU-bound tasks first, which, in effect, blocks the event loop from running anything else. This means the runtime of our application will be the sum of time it took for our two cpu_bound_work tasks to finish plus the 4 seconds that our delay task took.

If we need to perform CPU-bound work and still want to use async / await syntax, we can do so. To do this we’ll still need to use multiprocessing, and we need to tell asyncio to run our tasks in a process pool. We’ll learn how to do this in chapter 6.

## Running blocking APIs

We may also be tempted to use our existing libraries for I/O-bound operations by wrapping them in coroutines. However, this will generate the same issues that we saw with CPU-bound operations. These APIs block the main thread. Therefore, when we run a blocking API call inside a coroutine, we’re blocking the event loop thread itself, meaning that we stop any other coroutines or tasks from executing. Examples of blocking API calls include libraries such as requests, or time.sleep. Generally, any function that performs I/O that is not a coroutine or performs time-consuming CPU operations can be considered blocking.

As an example, let’s try getting the status code of www.example.com three times concurrently, using the requests library. When we run this, since we’re running concurrently we’ll be expecting this application to finish in about the length of time necessary to get the status code once.

```Python3
import asyncio
import requests
from util import async_timed


@async_timed()
async def get_example_status() -> int:
  return requests.get('http://www.example.com').status_code


@async_timed()
async def main():
  task_1 = asyncio.create_task(get_example_status())
  task_2 = asyncio.create_task(get_example_status())
  task_3 = asyncio.create_task(get_example_status())

  await task_1
  await task_2
  await task_3


asyncio.run(main())
```

When running the preceding listing, we’ll see output similar to the following. Note how the total runtime of the main coroutine is roughly the sum of time for all the tasks to get the status we ran, meaning that we did not have any concurrency advantage:

```
starting <function main at 0x1102e6820> with args () {}
starting <function get_example_status at 0x1102e6700> with args () {}
finished <function get_example_status at 0x1102e6700> in 0.0839 second(s)
starting <function get_example_status at 0x1102e6700> with args () {}
finished <function get_example_status at 0x1102e6700> in 0.0441 second(s)
starting <function get_example_status at 0x1102e6700> with args () {}
finished <function get_example_status at 0x1102e6700> in 0.0419 second(s)
finished <function main at 0x1102e6820> in 0.1702 second(s)
```

This is again because the requests library is blocking, meaning it will block whichever thread it is run on. Since asyncio only has one thread, the requests library blocks the event loop from doing anything concurrently.

As a rule, most APIs you employ now are blocking and won’t work out of the box with asyncio. You need to use a library that supports coroutines and utilizes nonblocking sockets. This means that if the library you are using does not return coroutines and you aren’t using await in your own coroutines, you’re likely making a blocking call.

In the above example we can use a library such as aiohttp, which uses non-blocking sockets and returns coroutines to get proper concurrency. We’ll introduce this library later in chapter 4.

If you need to use the requests library, you can still use async syntax, but you’ll need to explicitly tell asyncio to use multithreading with a thread pool executor. We’ll see how to do this in chapter 7.

We’ve now seen a few things to look for when using asyncio and have built a few simple applications. So far, we have not created or configured the event loop ourselves but relied on convenience methods to do it for us. Next, we’ll learn to create the event loop, which will allow us to access lower-level asyncio functionality and event loop configuration properties.

## Accessing and manually managing the event loop

Until now, we have used the convenient asyncio.run to run our application and create the event loop for us behind the scenes. Given the ease of use, this is the preferred method to create the event loop. However, there may be cases in which we don’t want the functionality that asyncio.run provides. As an example, we may want to execute custom logic to stop tasks that differ from what asyncio.run does, such as letting any remaining tasks finish instead of stopping them.

In addition, we may want to access methods available on the event loop itself. These methods are typically lower level and, as such, should be used sparingly. However, if you want to perform tasks, such as working directly with sockets or scheduling a task to run at a specific time in the future, you’ll need to access the event loop. While we won’t, and shouldn’t, be managing the event loop extensively, this will be necessary from time to time.

## Creating an event loop manually

We can create an event loop by using the asyncio.new_event_loop method. This will return an event loop instance. With this, we have access to all the low-level methods that the event loop has to offer. With the event loop we have access to a method named run_until_complete, which takes a coroutine and runs it until it finishes. Once we are done with our event loop, we need to close it to free any resources it was using. This should normally be in a finally block so that any exceptions thrown don’t stop us from closing the loop. Using these concepts, we can create a loop and run an asyncio application.

```Python3
import asyncio


async def main():
  await asyncio.sleep(1)


loop = asyncio.new_event_loop()

try:
  loop.run_until_complete(main())
finally:
  loop.close()
```

The code in this listing is similar to what happens when we call asyncio.run with the difference being that this does not perform canceling any remaining tasks. If we want any special cleanup logic, we would do so in our finally clause.

## Accessing the event loop

From time to time, we may need to access the currently running event loop. asyncio exposes the asyncio.get_running_loop function that allows us to get the current event loop. As an example, let’s look at call_soon, which will schedule a function to run on the next iteration of the event loop.

```Python3
import asyncio
from util import delay


def call_later():
  print("I'm being called in the future!")


async def main():
  loop = asyncio.get_running_loop()
  loop.call_soon(call_later)
  await delay(1)


asyncio.run(main())
```

In the preceding listing, our main coroutine gets the event loop with asyncio.get _running_loop and tells it to run call_later, which takes a function and will run it on the next iteration of the event loop. In addition, there is an asyncio.get_event _loop function that lets you access the event loop.

This function can potentially create a new event loop if it is called when one is not already running, leading to strange behavior. It is recommended to use get_ running_loop, as this will throw an exception if an event loop isn’t running, avoiding any surprises.

While we shouldn’t use the event loop frequently in our applications, there are times when we will need to configure settings on the event loop or use low-level functions. We’ll see an example of configuring the event loop in the next section on debug mode.

## Using debug mode

In previous sections, we mentioned how coroutines should always be awaited at some point in the application. We also saw the drawbacks of running CPU-bound and other blocking code inside coroutines and tasks. It can, however, be hard to tell if a coroutine is taking too much time on CPU, or if we accidently forgot an await somewhere in our application. Luckily, asyncio gives us a debug mode to help us diagnose these situations.

When we run in debug mode, we’ll see a few helpful log messages when a coroutine or task takes more than 100 milliseconds to run. In addition, if we don’t await a coroutine, an exception is thrown, so we can see where to properly add an await. There are a few different ways to run in debug mode.

### Using ```asyncio.run```

The asyncio.run function we have been using to run coroutines exposes a debug parameter. By default, this is set to False, but we can set this to True to enable debug mode:

```Python3
asyncio.run(coroutine(), debug=True)
```

### Using command-line arguments

Debug mode can be enabled by passing a command-line argument when we start our Python application. To do this we apply -X dev:

```bash
$ python3 -X dev program.py
```

### Using environment-variablesWe can also use environment variables to enable debug mode by setting the PYTHONASYNCIODEBUG variable to 1:

```bash
$ PYTHONASYINCIODEBUG=1 python3 program.py
```

In versions of Python older than 3.9, there is a bug within debug mode. When using asyncio.run, only the boolean debug parameter will work. Command-line arguments and environment variables will only work when manually managing the event loop.

In debug mode, we’ll see informative messages logged when a coroutine takes too long. Let’s test this out by trying to run CPU-bound code in a task to see if we get a warning, as shown in the following listing.

```Python3
import asyncio
from util import async_timed


@async_timed()
async def cpu_bound_work() -> int:
  counter = 0
  for _ in range(100000000):
    counter += 1

  return counter


async def main() -> None:
  task_one = asyncio.create_task(cpu_bound_work())
  await task_one


asyncio.run(main(), debug=True)
```

When running this, we’ll see a helpful message that task_one was taking too long, therefore blocking the event loop from running any other tasks:

```
Executing <Task finished name='Task-2' coro=<cpu_bound_work() done, defined
at listing_2_9.py:5> result=100000000 created at tasks.py:382> took 4.829
seconds
```

This can be helpful for debugging issues where we may inadvertently be making a call that is blocking. The default settings will log a warning if a coroutine takes longer than 100 milliseconds, but this may be longer or shorter than we’d like. To change this value, we can set the slow callback duration by accessing the event loop as we do in listing 2.24 and setting slow_callback_duration. This is a floating-point value representing the seconds we want the slow callback duration to be.

```Python3
import asyncio


async def main():
  loop = asyncio.get_event_loop()
  loop.slow_callback_duration = .250


asyncio.run(main(), debug=True)
```

The preceding listing will set the slow callback duration to 250 milliseconds, meaning we’ll get a message printed out if any coroutine takes longer than 250 milliseconds of CPU time to run

# 3. A first asyncio application

## An echo server on the asyncio event loop

Working with select is a bit too low-level for most applications. We may want to have code run in the background while we’re waiting for socket data to come in, or we may want to have background tasks run on a schedule. If we were to do this with only selectors, we’d likely build our own event loop, while asyncio has a nicely implemented one ready to use. In addition, coroutines and tasks provide abstractions on top of selectors, which make our code easier to implement and maintain, as we don’t need to think about selectors at all.

Now that we have a deeper understanding on how the asyncio event loop works, let’s take the echo server that we built in the last section and build it again using coroutines and tasks. We’ll still use lower-level sockets to accomplish this, but we’ll use asyncio-based APIs that return coroutines to manage them. We’ll also add some more functionality to our echo server to demonstrate a few key concepts to illustrate how asyncio works.

## Event loop coroutines for sockets

Given that sockets are a relatively low-level concept, the methods for dealing with them are on asyncio’s event loop itself. There are three main coroutines we’ll want to work with: sock_accept, sock_recv and sock_sendall. These are analogous to the socket methods that we used earlier, except that they take in a socket as an argument and return coroutines that we can await until we have data to act on.

Let’s start with sock_accept. This coroutine is analogous to the socket.accept method that we saw in our first implementation. This method will return a tuple (a data structure that stores an ordered sequence of values) of a socket connection and a client address. We pass it in the socket we’re interested in, and we can then await the coroutine it returns. Once that coroutine completes, we’ll have our connection and address. This socket must be non-blocking and should already be bound to a port:

```Python3
connection, address = await loop.sock_accept(socket)
```

sock_recv and sock_sendall are called similarly to sock_accept. They take in a socket, and we can then await for a result. sock_recv will await until a socket has bytes we can process. sock_sendall takes in both a socket and data we want to send and will wait until all data we want to send to a socket has been sent and will return None on success:

```Python3
data = await loop.sock_recv(socket)
success = await loop.sock_sendall(socket, data)
```

With these building blocks, we’ll be able to translate our previous approaches into one using coroutines and tasks.

## Designing an asyncio echo server

In chapter 2, we introduced coroutines and tasks. So when should we use just a coroutine, and when should we wrap a coroutine in a task for our echo server? Let’s examine how we want our application to behave to make this determination.

We’ll start with how we want to listen for connections in our application. When we are listening for connections, we will only be able to process one connection at a time as socket.accept will only give us one client connection. Behind the scenes, incoming connections will be stored in a queue known as the backlog if we get multiple connections at the same time, but here, we won’t get into how this works.

Since we don’t need to process multiple connections concurrently, a single coroutine that loops forever makes sense. This will allow other code to run concurrently while we’re paused waiting for a connection. We’ll define a coroutine called listen_ for_connections that will loop forever and listen for any incoming connections:

```Python3
async def listen_for_connections(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connection from {address}")
```

Now that we have a coroutine for listening to connections, how about reading and writing data to the clients who have connected? Should that be a coroutine, or a coroutine we wrap in a task? In this case, we will have multiple connections, each of which could send data to us at any time. We don’t want to wait for data from one connection to block another, so we need to read and write data from multiple clients concurrently. Because we need to handle multiple connections at the same time, creating a task for each connection to read and write data makes sense. On every connection we get, we’ll create a task to both read data from and write data to that connection.

We’ll create a coroutine named echo that is responsible for handling data from a connection. This coroutine will loop forever listening for data from our client. Once it receives data it will then send it back to the client.

Then, in listen_for_connections we’ll create a new task that wraps our echo coroutine for each connection that we get. With these two coroutines defined, we now have all we need to build an asyncio echo server.

```Python3
import asyncio
import socket
from asyncio import AbstractEventLoop


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    # Loop forever waiting for data from a client connection
    while data := await loop.sock_recv(connection, 1024):
        # Once we have data, send it back to ALL clients.
        await loop.sock_sendall(connection, data)


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop) -> None:
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Got a connection from {address}')

        # Whenever we get a connection, create an echo task to listen for client data.
        asyncio.create_task(echo(connection, loop))


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    # Start the coroutine to listen for connections
    await listen_for_connection(server_socket, asyncio.get_event_loop())


asyncio.run(main())
```

The architecture for the preceding listing looks like figure 3.5. We have one coroutine, listen_for_connection, listening for connections. Once a client connects, our coroutine spawns an echo task for each client which then listens for data and writes it back out to the client.

![Figure-3-5](ScreenshotsForNotes/Chapter3/Figure_3_5.PNG)

When we run this application, we’ll be able to connect multiple clients concurrently and send data to them concurrently. Under the hood, this is all using selectors as we saw before, so our CPU utilization remains low.

We’ve now built a fully functioning echo server entirely using asyncio! So is our implementation error free? It turns out that the way we have designed this echo server does have an issue when our echo task fails that we’ll need to handle