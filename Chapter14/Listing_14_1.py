import asyncio


class TaskRunner:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.tasks = []

    def add_task(self, func):
        self.tasks.append(func)

    async def _run_all(self):
        awaitable_tasks = []

        for task in self.tasks:
            if asyncio.iscoroutinefunction(task):
                awaitable_tasks.append(asyncio.create_task(task()))
            elif asyncio.iscoroutine(task):
                awaitable_tasks.append(asyncio.create_task(task()))
            else:
                self.loop.call_soon(task)

    def run(self):
        self.loop.run_until_complete(self._run_all())