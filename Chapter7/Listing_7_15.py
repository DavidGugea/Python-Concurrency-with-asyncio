import asyncio
from asyncio import AbstractEventLoop
from threading import Thread
from Listing_7_14 import LoadTester


class ThreadedEventLoop(Thread):
    def __init__(self, loop: AbstractEventLoop):
        # We create a new thread class to run the asyncio event loop forever.
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        self._loop.run_forever()


loop = asyncio.new_event_loop()

asyncio_thread = ThreadedEventLoop(loop)
# STart the new thread to run the asyncio event loop in the background.
asyncio_thread.start()

# Create the load tester Tkinter application, and start its main event loop.
app = LoadTester(loop)
app.mainloop()
