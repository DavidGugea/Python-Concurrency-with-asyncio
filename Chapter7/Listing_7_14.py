from queue import Queue
from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import ttk
from typing import Optional
from Listing_7_13 import StressTest


class LoadTester(Tk):
    # In our constructor, we set up the text inputs, labels, submit button, and progress bar.
    def __init__(self, loop, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self._queue = Queue()
        self._refresh_ms = 25

        self._loop = loop
        self._load_test: Optional[StressTest] = None
        self.title('Url Requester')

        self._url_label = Label(self, text="URL:")
        self._url_label.grid(column=0, row=0)

        self._url_field = Entry(self, width=10)
        self._url_field.grid(column=1, row=0)

        self._request_label = Label(self, text="Number of requests!")
        self._request_label.grid(column=0, row=1)

        self._request_field = Entry(self, width=10)
        self._request_field.grid(column=1, row=1)

        # When clicked, our submit button will call the _start method
        self._submit = ttk.Button(self, text="Submit", command=self._start)
        self._submit.grid(column=2, row=1)

        self._pl_label = Label(self, text="Progress:")
        self._pl_label.grid(column=0, row=3)

        self._pb = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self._pb.grid(column=1, row=3, columnspan=2)

    def _update_bar(self, pct: int):
        # The update bar method will set the progress bar to a percentage complete value from 0 to 100. This method should only be called in the main thread.
        if pct == 100:
            self._load_test = None
            self._submit['text'] = 'Submit'
        else:
            self._pb['value'] = pct
            self.after(self._refresh_ms, self._poll_queue)

    def _queue_update(self, completed_requests: int, total_requests: int):
        # This method is the callback we pass to the stress test; it adds a progress update to the queue.
        self._queue.put(int(completed_requests / total_requests * 100))

    def _poll_queue(self):
        # Try to get a progress update from the queue; if we have one, update the progress bar.
        if not self._queue.empty():
            percent_complete = self._queue.get()
            self._update_bar(percent_complete)
        else:
            if self._load_test:
                self.after(self._refresh_ms, self._poll_queue)

    def _start(self):
        # Start the load test, and start polling every 25 milliseconds for queue updates.
        if self._load_test is None:
            self._submit['text'] = 'Cancel'
            test = StressTest(self._loop, self._url_field.get(), int(self._request_field.get()), self._queue_update)
            self.after(self._refresh_ms, self._poll_queue)
            test.start()
            self._load_test = test
        else:
            self._load_test.cancel()
            self._load_test = None
            self._submit['text'] = 'Submit'
